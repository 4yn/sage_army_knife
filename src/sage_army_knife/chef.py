from __future__ import annotations

from typing import Union
from typing_extensions import Self

import base64
import json
import itertools
import hashlib
import io

try:
    from Crypto.Cipher import AES
except ImportError:
    AES = None

class ChefKnife:
    """
    Polyglot data container for casting between data encodings

    Has functions for casting to and from `str`, `bytes`, `b64`, `json`, `hex`,
    `int`, `io.BytesIO` and `io.StringIO`. Can also calculate hashes, xor and
    basic AES calculations.

    The aliases `CK` or `Chef` can also be used.

    The conversion functions try to follow this naming convention:

    - `to_*` encodes a `ChefKnife(data)` to `ChefKnife(encoded data)`
    - `from_*` parses a `ChefKnife(encoded data)` to `ChefKnife(data)`
    - `init_*` takes in a non-`ChefKnife` object, decodes the data and
        returns a `ChefKnife(data)`
    - `into_*` turns a `ChefKnife(data)` into a non-`ChefKnife` object

    The conversion functions can also be chained together.

    Example usage:
    ```python
    >>> from sage_army_knife import ChefKnife
    >>> # from sage_army_knife import CK, Chef
    >>> ChefKnife("abcd").to_b64()
    ChefKnife(b'YWJjZA==')
    >>> ChefKnife("abcd").to_b64().to_hex()
    ChefKnife('59574a6a5a413d3d')
    >>> ChefKnife("abcd").to_b64().to_hex().to_hexdigest("md5")
    ChefKnife('58a15dd16f7d263689469ea66b4e57d9')
    >>> ChefKnife("abcd").to_b64().to_hex().to_hexdigest("md5").into_str()
    '58a15dd16f7d263689469ea66b4e57d9'
    >>> ChefKnife("abcd") ^ "bcde"
    ChefKnife(b'\x03\x01\x07\x01')
    >>> ck = ChefKnife("abcd")
    >>> ck
    ChefKnife('abcd')
    >>> ck += "efg"
    >>> ck
    ChefKnife('abcdefg')
    >>> ck += b"hij"
    >>> ck
    ChefKnife(b'abcdefghij')
    >>> ck += ChefKnife("bG1u").from_b64()
    >>> ck
    ChefKnife(b'abcdefghijlmn')
    >>> ck[1::2]
    Chef(b'bdfhjm')
    >>> ck.pad_pcks7()
    ChefKnife(b'abcdefghijlmn\x03\x03\x03')
    ```
    """

    """
    Data loading and config setting
    """

    def __init__(self, data:Union[None, str, bytes]=None, inplace=False):
        """
        Create a new ChefKnife to process data

        Arguments:
            data: Data to be stored
            inplace(bool): Set to `True` to make all transformations inplace
        """
        if isinstance(data, ChefKnife):
            data = data.get()
        self.data = data
        self.inplace = inplace

    def get(self) -> Union[None, str, bytes]:
        """
        Retrieve data inside ChefKnife
        """
        return self.data

    def update(self, data:Union[None, str, bytes]) -> Self:
        """
        Overwrite data inside ChefKnife

        Arguments:
            data: Data to be stored
        """
        if self.inplace:
            self.data = data
            return self
        else:
            return self.__class__(data)

    def __repr__(self) -> str:
        data_repr = repr(self.data)
        if len(data_repr) > 110:
            data_repr = data_repr[:100] + f"[... {len(data_repr) - 100} more]"
        return f"{self.__class__.__name__}({data_repr})"

    def __str__(self) -> str:
        return str(self.data)

    """
    Data casting
    """

    def to_bytes(self) -> Self:
        """
        ChefKnife(?) => ChefKnife(bytes)
        """
        data = self.get()
        if isinstance(data, bytes):
            pass
        elif isinstance(data, str):
            data = data.encode()
        else:
            raise TypeError(f"Cannot convert {type(data)} to bytes")
        return self.update(data)

    def into_bytes(self) -> bytes:
        """
        ChefKnife(?) => bytes
        """
        return self.to_bytes().get()

    def __bytes__(self) -> bytes:
        return self.into_bytes()

    def to_str(self) -> Self:
        """
        ChefKnife(?) => ChefKnife(str)
        """
        data = self.get()
        if isinstance(data, str):
            pass
        elif isinstance(data, bytes):
            data = data.decode()
        else:
            raise TypeError(f"Cannot convert {type(data)} to str")
        return self.update(data)

    def into_str(self) -> str:
        """
        ChefKnife(?) => str
        """
        return self.to_str().get()

    def __str__(self) -> str:
        return self.into_str()

    def __add__(self, other) -> Self:
        data = self.get()
        if isinstance(data, str) and isinstance(other, str):
            data = data + other
        elif isinstance(other, (str, bytes, ChefKnife)):
            data = self.into_bytes()
            data = data + self.__class__(other).into_bytes()
        else:
            raise TypeError(f"Cannot add {type(other)} to ChefKnife({type(data)})")
        return self.update(data)

    def __radd__(self, other) -> Self:
        data = self.get()
        if isinstance(data, str) and isinstance(other, str):
            data = other + data
        elif isinstance(other, (str, bytes, ChefKnife)):
            data = self.into_bytes()
            data = self.__class__(other).into_bytes() + data
        else:
            raise TypeError(f"Cannot add ChefKnife({type(data)}) to {type(other)}")
        return self.update(data)

    """
    Encodings
    """
    
    def from_b64(self) -> Self:
        """
        ChefKnife(? in b64 str) => ChefKnife(bytes)
        """
        data = self.into_bytes()
        data = base64.b64decode(data)
        return self.update(data)
    
    def to_b64(self) -> Self:
        """
        ChefKnife(?) => ChefKnife(bytes in b64 str)
        """
        data = self.into_bytes()
        data = base64.b64encode(data)
        return self.update(data)
    
    def into_b64(self) -> bytes:
        """
        ? => b64 bytes, returns bytes
        """
        return self.to_b64().get()

    def from_json_str(self) -> Self:
        """
        ChefKnife(? in json str) => ChefKnife(json object)
        """
        data = self.into_str()
        data = json.loads(data)
        return self.update(data)

    def to_json_str(self) -> Self:
        """
        ChefKnife(?) => ChefKnife(json str)
        """
        data = self.get()
        data = json.dumps(data)
        return self.update(data)

    def into_json_str(self) -> str:
        """
        ChefKnife(?) => json str
        """
        return self.to_json_str().get()

    def from_hex(self) -> Self:
        """
        ChefKnife(hex str) => ChefKnife(bytes)
        """
        data = self.into_str()
        if data[:2] == "0x":
            data = data[2:]

        if len(data) % 2 == 1:
            # TODO: warn odd digits
            data = "0" + data

        res = []
        for i in range(0, len(data), 2):
            try:
                res.append(int(data[i:i+2], 16))
            except ValueError:
                raise ValueError(f"Found non-hex character {data[i-4:i+6]}")
        res = bytes(res)
        return self.update(res)

    def to_hex(self, head=False) -> Self:
        """
        ChefKnife(?) => ChefKnife(hex str)
        
        Arguments:
            head(bool): Set to `True` to add leading "0x"
        """
        data = self.into_bytes()
        data = data.hex()
        if head:
            data = "0x" + data
        return self.update(data)

    def into_hex(self) -> str:
        """
        ChefKnife(?) => hex str
        """
        return self.to_hex().get()

    @classmethod
    def init_int(cls, data) -> Self:
        """
        int => ChefKnife(bytes)
        """
        data = hex(data)[2:]
        if len(data) % 2 == 1:
            # TODO: warn odd digits
            data = "0" + data
        data = bytes.fromhex(data)
        return cls(data)

    def into_int(self) -> int:
        """
        ChefKnife(?) => int
        """
        return int(self.into_hex(), 16)

    def __int__(self) -> int:
        return self.into_int()

    """
    File IO
    """

    @classmethod
    def init_file(cls, filename: str, as_str:bool=False) -> Self:
        """
        Read file contents as bytes/str into ChefKnife

        Arguments:
            filename(str): Path to file to read data from
            as_str(bool): Set to `True` to read file as str
        """
        if as_str:
            with open(filename, "r") as f:
                return cls(f.read())

        with open(filename, "rb") as f:
            return cls(f.read())

    def write_file(self, filename: str) -> None:
        """
        Write ChefKnife bytes contents into file

        Arguments:
            filename(str): Path to file to write data to
        """
        with open(filename, "wb") as f:
            f.write(self.bytes())

    def into_io(self) -> Union[io.BytesIO, io.StringIO]:
        """
        Wrap data in a io.BytesIO / io.StringIO file handle
        """
        data = self.get()
        if isinstance(data, bytes):
            return io.BytesIO(data)
        elif isinstance(data, str):
            return io.StringIO(data)
        else:
            raise TypeError(f"Cannot create file handle from {type(data)}")

    """
    List-like operations
    """
    
    def __getitem__(self, key: Union[None, int, slice]) -> Self:
        data = self.get()[key]
        if isinstance(data, (int, list)):
            return data
        return Chef(data)
    
    def reverse(self) -> Self:
        """
        Reverse data inside ChefKnife
        """
        data = self.get()
        if not isinstance(data, (bytes, str)):
            raise TypeError(f"Cannot reverse {type(data)}")
        data = data[::-1]
        return self.update(data)

    def chunked(self, block_size: int, raw=False) -> list[Self]:
        """
        Make a list of `block_size` long chunks, each wrapped inside ChefKnife

        Arguments:
            block_size(int): Number of elements per chunk
            raw(bool): Set to `True` to return a list of raw data
        """
        data = self.get()
        if not isinstance(data, (bytes, str)):
            raise TypeError(f"Cannot chunk {type(data)}")

        data = [
            data[i:i+block_size]
            for i in range(0, len(data), block_size)
        ]

        if not raw:
            data = [self.__class__(i) for i in data]

        return data

    """
    Bytes manipulation
    """

    @classmethod
    def init_nullbytes(cls, length: int) -> Self:
        """
        Overwrite inner data with null bytes

        Arguments:
            length(int): Numer of null bytes
        """
        return cls(b"\x00" * length)

    def pad_pcks7(self, block_size=16) -> Self:
        """
        Add pcks7 padding to data

        Arguments:
            block_size(int): Block size to pad to
        """
        data = self.into_bytes()
        pad_len = 16 - (len(data) % block_size)
        data = data + bytes([pad_len] * pad_len)
        return self.update(data)

    def unpad_pcks7(self, block_size=16) -> Self:
        """
        Removes pcks7 padding to data

        Arguments:
            block_size(int): Block size to pad to
        """
        data = self.into_bytes()
        data_len = len(data)
        if data_len == 0:
            raise ValueError("Invalid padding: data has 0 length")
        if data_len % block_size != 0:
            raise ValueError(f"Invalid padding: data length {data_len} is not multiple of block size {block_size}")

        pad_len = data[-1]
        if pad_len > block_size:
            raise ValueError(f"Invalid padding: padding length {pad_len} is longer than block size {block_size}")

        data, padding = data[:-pad_len], data[-pad_len:]
        if padding != bytes([pad_len] * pad_len):
            raise ValueError(f"Invalid padding: padding {pad_len.hex()} is invalid")
            
        return self.update(data)

    def bxor(self, *keys, cycle=False) -> Self:
        """
        Binary xor
        """
        data = self.into_bytes()

        for key in keys:
            key = self.__class__(key).into_bytes()
            if cycle:
                key = itertools.cycle(key)

            data = bytes([
                i ^ j
                for i, j in zip(data, key)
            ])
        
        return self.update(data)

    def __xor__(self, other):
        return self.bxor(other)
    
    def __rxor__(self, other):
        return self.bxor(other)

    def badd(self, *keys, cycle=False) -> Self:
        """
        Cyclic binary add
        """
        data = self.into_bytes()

        for key in keys:
            key = self.__class__(key).into_bytes()
            if cycle:
                key = itertools.cycle(key)

            data = bytes([
                (i + j) % 256
                for i, j in zip(data, key)
            ])
        
        return self.update(data)

    def bsub(self, *keys, cycle=False):
        """
        Cyclic binary subtract
        """
        data = self.into_bytes()

        for key in keys:
            key = self.__class__(key).into_bytes()
            if cycle:
                key = itertools.cycle(key)

            data = bytes([
                (i - j + 256) % 256
                for i, j in zip(data, key)
            ])
        
        return self.update(data)

    """
    Hashing
    """
    
    def to_digest(self, hash_type: str):
        """
        ChefKnife(?) => ChefKnife(hash bytes)
        """
        data = self.into_bytes()
        data = getattr(hashlib, hash_type)(data).digest()
        return self.update(data)

    def to_hexdigest(self, hash_type):
        """
        ChefKnife(?) => ChefKnife(hash hex str)
        """
        data = self.into_bytes()
        data = getattr(hashlib, hash_type)(data).hexdigest()
        return self.update(data)
    
    def into_digest_int(self, hash_type):
        """
        ChefKnife(?) => int
        """
        data = self.into_bytes()
        data = getattr(hashlib, hash_type)(data).hexdigest()
        return int(data, 16)

    """
    AES Cipher
    """

    def aes(self, key:Union[ChefKnife, bytes], mode="ECB", encrypt=False, **kwargs) -> Self:
        """
        Take AES decryption / encryption of inner data
        """

        if AES is None:
            raise ImportError("AES module not found, please `pip install pycryptodome`")

        aes_mode = getattr(AES, f"MODE_{mode.upper()}", None)
        if aes_mode is None:
            raise ValueError(f"Unknown AES mode {mode}")

        data = self.into_bytes()
        key = self.__class__(key).into_bytes()

        for k in list(kwargs.keys()):
            if isinstance(kwargs[k], ChefKnife):
                kwargs[k] = kwargs[k].into_bytes()

        cipher = AES.new(key, aes_mode, **kwargs)

        if not encrypt:
            data = cipher.decrypt(data)
        else:
            data = cipher.encrypt(data)
        return self.update(data)

    def aes_encrypt(self, key, mode="ECB", **kwargs) -> Self:
        """
        Take AES encryption of inner data
        """
        return self.aes(key, mode, encrypt=True, **kwargs)

    def aes_decrypt(self, key, mode="ECB", **kwargs) -> Self:
        """
        Take AES decryption of inner data
        """
        return self.aes(key, mode, encrypt=False, **kwargs)

class Chef(ChefKnife):
    pass

class CK(ChefKnife):
    pass