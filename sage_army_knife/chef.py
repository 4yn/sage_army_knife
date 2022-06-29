import base64
import json
import itertools
import hashlib
from Crypto.Cipher import AES

class ChefKnife:
    """
    Data loading and config setting
    """

    def __init__(self, data=None, inplace=False):
        if isinstance(data, Chef):
            data = data.data
        self.data = data
        self.inplace = inplace
        return
    
    def update(self, data):
        if self.inplace:
            self.data = data
            return self
        else:
            return Chef(data)

    def get(self):
        return self.data

    def __repr__(self):
        data_repr = repr(self.data)
        if len(data_repr) > 100:
            data_repr = data_repr[:100] + f"[... {len(data_repr) - 100} more]"
        return f"ChefKnife({data_repr})"

    """
    indexing
    """

    def __getitem__(self, key):
        return Chef(self.data[key])

    """
    File IO
    """

    @staticmethod
    def read_file(filename):
        with open(filename, "rb") as f:
            return Chef(f.read())

    def write_file(self, filename):
        with open(filename, "wb") as f:
            return f.write(self.bytes())

    """
    List-like operations
    """
    
    def reverse(self):
        data = self.data
        if not isinstance(data, (bytes, str, list)):
            raise TypeError(f"Cannot reverse {type(data)}")
        data = data[::-1]
        return self.update(data)

    def chunked(self, block_size, raw=False):
        data = self.data
        if not isinstance(data, (bytes, str, list)):
            raise TypeError(f"Cannot chunk {type(data)}")
        data = [
            Chef(data[i:i+block_size]) if not raw
            else data[i:i+block_size]
            for i in range(0, len(data), block_size)
        ]
        return data # no update used

    """
    Hard casting
    """

    def to_bytes(self):
        data = self.data
        if isinstance(data, bytes):
            pass
        elif isinstance(data, str):
            data = data.encode()
        else:
            raise TypeError(f"Cannot convert {type(self.data)} to bytes")
        return self.update(data)

    def bytes(self):
        return self.to_bytes().data

    def to_str(self):
        data = self.data
        if isinstance(data, str):
            pass
        elif isinstance(data, bytes):
            data = data.decode()
        else:
            raise TypeError(f"Cannot convert {type(self.data)} to str")
        return self.update(data)

    def str(self):
        return self.to_str().data

    def __str__(self):
        return self.to_str().data

    """
    Encodings
    """
    
    def to_b64(self):
        data = self.to_bytes().data
        data = base64.b64encode(data)
        return self.update(data)
    
    def from_b64(self):
        data = self.to_str().data
        data = base64.b64decode(data)
        return self.update(data)

    def b64(self):
        return self.to_b64().data

    def to_json_str(self):
        data = self.data
        data = json.dumps(data)
        return self.update(data)

    def from_json_str(self):
        data = self.to_str().data
        data = json.loads(data)
        return self.update(data)

    def json_str(self):
        return self.to_json_str().data

    def to_hex(self, head=False):
        data = self.to_bytes().data
        data = data.hex()
        if head:
            data = "0x" + data
        return self.update(data)

    def from_hex(self):
        data = self.to_str().data
        if data[:2] == "0x":
            data = data[2:]
        res = []
        for i in range(0, len(data), 2):
            c = data[i:i+2]
            if len(c) != 2:
                raise ValueError(f"Odd number of hex digits with trailing {c}")
            res.append(int(c, 16))
        res = bytes(res)
        return self.update(res)

    def hex(self):
        return self.to_hex().data

    def to_int(self):
        data = self.to_bytes().data
        data = int(data.hex(), 16)
        return self.update(data)

    def from_int(self):
        try:
            data = int(self.data)
        except TypeError:
            raise TypeError(f"Cannot convert {type(self.data)} to int")
        data = hex(data)[2:]
        return self.update(data).from_hex()

    def int(self):
        return self.to_int().data

    """
    Bytes manipulation
    """

    def nullbytes(self, length):
        return self.update(b"\x00" * length)
    
    def pcks7(self, block_size=16):
        data = self.to_bytes().data
        pad_len = 16 - (len(data) % block_size)
        data = data + bytes([pad_len] * pad_len)
        return self.update(data)

    def cast_bytes_stream(self, key):
        if isinstance(key, Chef):
            key = key.to_bytes().data
        elif isinstance(key, bytes):
            pass
        elif isinstance(key, int) and key < 256:
            key = bytes([key])
        else:
            raise TypeError(f"Cannot cast {type(key)} to bytes stream")
        return key

    def bxor(self, key):
        key = self.cast_bytes_stream(key)
        data = self.bytes()
        data = bytes([
            i ^ j
            for i, j in zip(data, itertools.cycle(key))
        ])
        return self.update(data)

    def badd(self, key):
        key = self.cast_bytes_stream(key)
        data = self.to_bytes().data
        data = bytes([
            (i + j + 256) % 256
            for i, j in zip(data, itertools.cycle(key))
        ])
        return self.update(data)

    def bsub(self, key):
        key = self.cast_bytes_stream(key)
        key = [
            (256 - i) % 256
            for i in key
        ]
        return self.badd(key)

    """
    Hashing
    """
    
    def digest(self, hash_type):
        data = self.to_bytes().data
        data = getattr(hashlib, hash_type)(data).digest()
        return self.update(data)

    def digest_hex(self, hash_type):
        return self.digest(hash_type).to_hex()
    
    def digest_int(self, hash_type):
        return self.digest(hash_type).to_int()

    """
    Cipher
    """

    def aes(self, key, iv=None, mode=None, encrypt=False, **kwargs):
        aes_mode = getattr(AES, f"MODE_{mode.upper()}", None)
        if aes_mode is None:
            raise ValueError(f"Unknown AES mode {mode}")

        key = Chef(key).bytes()
        iv = Chef(iv).bytes() if iv is not None else None

        data = self.bytes()
        cipher = AES.new(key, aes_mode, iv=iv, **kwargs)

        if not encrypt:
            data = cipher.decrypt(data)
        else:
            data = cipher.encrypt(data)
        return self.update(data)

    def aes_encrypt(self, key, iv=None, mode=None, **kwargs):
        return self.aes(key, iv=iv, mode=mode, encrypt=True)

    def aes_decrypt(self, key, iv=None, mode=None, **kwargs):
        return self.aes(key, iv=iv, mode=mode, encrypt=False)

Chef = ChefKnife
CK = ChefKnife