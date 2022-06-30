from __future__ import annotations

import base64
import json
import itertools
import hashlib
from Crypto.Cipher import AES
from typing import Union

class ChefKnife:
    """
    Polyglot data container for casting between data encodings
    """

    """
    Data loading and config setting
    """

    def __init__(self, data:Union[None, str, bytes, int]=None, inplace=False):
        """
        Create a new ChefKnife to process data

        Arguments:
            data: Data to be processed
            inplace(bool): Make all transformations inplace
        """
        if isinstance(data, Chef):
            data = data.data
        self.data = data
        self.inplace = inplace
        return
    
    def update(self, data:Union[None, str, bytes, int]):
        """
        Overwrite data inside ChefKnife

        Arguments:
            data: Data to be processed
        """
        if self.inplace:
            self.data = data
            return self
        else:
            return Chef(data)

    def get(self) -> Union[None, str, bytes, int]:
        """
        Retrieve data inside ChefKnife
        """
        return self.data

    def __repr__(self) -> str:
        data_repr = repr(self.data)
        if len(data_repr) > 100:
            data_repr = data_repr[:100] + f"[... {len(data_repr) - 100} more]"
        return f"ChefKnife({data_repr})"

    """
    indexing
    """

    def __getitem__(self, key: Union[None, int, slice]) -> Union[int, bytes, str]:
        return Chef(self.data[key])

    """
    File IO
    """

    @staticmethod
    def read_file(filename: str):
        """
        Read file contents as bytes into ChefKnife

        Arguments:
            filename(str): Path to file to read data from
        """
        with open(filename, "rb") as f:
            return Chef(f.read())

    def write_file(self, filename: str):
        """
        Write ChefKnife bytes contents into file

        Arguments:
            filename(str): Path to file to write data to
        """
        with open(filename, "wb") as f:
            f.write(self.bytes())
        return None

    """
    List-like operations
    """
    
    def reverse(self):
        """
        Reverse data inside ChefKnife
        """
        data = self.data
        if not isinstance(data, (bytes, str, list)):
            raise TypeError(f"Cannot reverse {type(data)}")
        data = data[::-1]
        return self.update(data)

    def chunked(self, block_size: int, raw=False):
        """
        Make a list of `block_size` long chunks, each wrapped inside ChefKnife

        Arguments:
            block_size(int): Number of elements per chunk
            raw(bool): Set to `True` to return a list of raw data
        """
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
        """
        ? => bytes
        """
        data = self.data
        if isinstance(data, bytes):
            pass
        elif isinstance(data, str):
            data = data.encode()
        else:
            raise TypeError(f"Cannot convert {type(self.data)} to bytes")
        return self.update(data)

    def bytes(self) -> bytes:
        """
        ? => bytes, returns bytes
        """
        return self.to_bytes().data

    def to_str(self):
        """
        ? => str
        """
        data = self.data
        if isinstance(data, str):
            pass
        elif isinstance(data, bytes):
            data = data.decode()
        else:
            raise TypeError(f"Cannot convert {type(self.data)} to str")
        return self.update(data)

    def str(self) -> str:
        """
        ? => str, returns str
        """
        return self.to_str().data

    def __str__(self) -> str:
        return self.to_str().data

    """
    Encodings
    """
    
    def to_b64(self):
        """
        ? => b64 bytes
        """
        data = self.to_bytes().data
        data = base64.b64encode(data)
        return self.update(data)
    
    def from_b64(self):
        """
        b64 => bytes
        """
        data = self.to_str().data
        data = base64.b64decode(data)
        return self.update(data)

    def b64(self) -> bytes:
        """
        ? => b64 bytes, returns bytes
        """
        return self.to_b64().data

    def to_json_str(self):
        """
        ? => json str
        """
        data = self.data
        data = json.dumps(data)
        return self.update(data)

    def from_json_str(self):
        """
        json str => object
        """
        data = self.to_str().data
        data = json.loads(data)
        return self.update(data)

    def json_str(self) -> str:
        """
        ? => json str, returns str
        """
        return self.to_json_str().data

    def to_hex(self, head=False):
        """
        ? => hex str
        """
        data = self.to_bytes().data
        data = data.hex()
        if head:
            data = "0x" + data
        return self.update(data)

    def from_hex(self):
        """
        hex str => bytes
        """
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
        """
        ? => hex str, retuurns str
        """
        return self.to_hex().data

    def to_int(self):
        """
        ? => int
        """
        data = self.to_bytes().data
        data = int(data.hex(), 16)
        return self.update(data)

    def from_int(self):
        """
        int => bytes
        """
        try:
            data = int(self.data)
        except TypeError:
            raise TypeError(f"Cannot convert {type(self.data)} to int")
        data = hex(data)[2:]
        return self.update(data).from_hex()

    def int(self):
        """
        ? => int, returns int
        """
        return self.to_int().data

    """
    Bytes manipulation
    """

    def nullbytes(self, length: int):
        """
        Overwrite inner data with null bytes

        Arguments:
            length(int): Numer of null bytes
        """
        return self.update(b"\x00" * length)
    
    def pcks7(self, block_size=16):
        """
        Add pcks7 padding to data

        Arguments:
            block_size(int): Block size to pad to
        """
        data = self.to_bytes().data
        pad_len = 16 - (len(data) % block_size)
        data = data + bytes([pad_len] * pad_len)
        return self.update(data)

    @staticmethod
    def cast_bytes_stream(key: Union[ChefKnife, bytes, int]):
        """
        Massage data into bytes object for binary operations
        """
        if isinstance(key, ChefKnife):
            key = key.to_bytes().data
        elif isinstance(key, bytes):
            pass
        elif isinstance(key, int) and key < 256:
            key = bytes([key])
        else:
            raise TypeError(f"Cannot cast {type(key)} to bytes stream")
        return key

    def bxor(self, key):
        """
        Cyclic binary xor
        """
        key = self.cast_bytes_stream(key)
        data = self.bytes()
        data = bytes([
            i ^ j
            for i, j in zip(data, itertools.cycle(key))
        ])
        return self.update(data)

    def badd(self, key):
        """
        Cyclic binary add
        """
        key = self.cast_bytes_stream(key)
        data = self.to_bytes().data
        data = bytes([
            (i + j + 256) % 256
            for i, j in zip(data, itertools.cycle(key))
        ])
        return self.update(data)

    def bsub(self, key):
        """
        Cyclic binary subtract
        """
        key = self.cast_bytes_stream(key)
        key = [
            (256 - i) % 256
            for i in key
        ]
        return self.badd(key)

    """
    Hashing
    """
    
    def digest(self, hash_type: str):
        """
        Take hash digest of inner data
        """
        data = self.to_bytes().data
        data = getattr(hashlib, hash_type)(data).digest()
        return self.update(data)

    def digest_hex(self, hash_type):
        """
        Take hash digest of inner data as hex str
        """
        data = self.to_bytes().data
        return self.digest(hash_type).to_hex()
    
    def digest_int(self, hash_type):
        """
        Take hash digest of inner data as int
        """
        data = self.to_bytes().data
        return self.digest(hash_type).to_int()

    """
    Cipher
    """

    def aes(self, mode, key:Union[ChefKnife, bytes], iv:Union[None, ChefKnife, bytes]=None, encrypt=False, **kwargs):
        """
        Take AES decryption / encryption of inner data
        """
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
        """
        Take AES encryption of inner data
        """
        return self.aes(key, iv=iv, mode=mode, encrypt=True, **kwargs)

    def aes_decrypt(self, key, iv=None, mode=None, **kwargs):
        """
        Take AES decryption of inner data
        """
        return self.aes(key, iv=iv, mode=mode, encrypt=False, **kwargs)

Chef = ChefKnife
CK = ChefKnife