import pytest

from sage_army_knife.chef import ChefKnife

def test_ck_casting():
    bytes_ck = ChefKnife(b"abcd")
    str_ck = ChefKnife("abcd")

    assert bytes_ck.get() == b"abcd"
    assert bytes_ck.to_str().get() == "abcd"
    assert bytes_ck.into_bytes() == b"abcd"
    assert bytes_ck.into_str() == "abcd"

    assert str_ck.get() == "abcd"
    assert str_ck.to_bytes().get() == b"abcd"
    assert str_ck.into_bytes() == b"abcd"
    assert str_ck.into_str() == "abcd"

def test_ck_encoding():
    b64_ck = ChefKnife("YWJjZA==")
    assert b64_ck.from_b64().into_bytes() == b"abcd"
    assert b64_ck.to_b64().into_bytes() == b"WVdKalpBPT0="
    assert b64_ck.into_b64() == b"WVdKalpBPT0="

    json_str_ck = ChefKnife('{"a": 1}')
    assert json_str_ck.from_json_str().get() == {"a":1}
    json_ck = ChefKnife({"a":1})
    assert json_ck.to_json_str().get() == '{"a": 1}'
    assert json_ck.into_json_str() == '{"a": 1}'

    hex_ck = ChefKnife("61626364")
    assert hex_ck.from_hex().get() == b"abcd"
    assert hex_ck.to_hex().get() == "3631363236333634"
    assert hex_ck.into_hex() == "3631363236333634"

    assert ChefKnife.init_int(1633837924).get() == b"abcd"
    assert ChefKnife("abcd").into_int() == 1633837924

def test_ck_file_io():
    import pathlib
    test_dir = pathlib.Path(__file__).parent.resolve()

    assert ChefKnife.init_file(test_dir / "dummy_file.txt").get() == b"abcd"
    assert ChefKnife.init_file(test_dir / "dummy_file.txt", as_str=True).get() == "abcd"
    assert ChefKnife("abcd").into_io().read() == "abcd"
    assert ChefKnife(b"abcd").into_io().read() == b"abcd"

def test_ck_list():
    bytes_ck = ChefKnife(b"abcd")

    assert bytes_ck[1] == b"b"[0]
    assert bytes_ck[1:3].get() == b"bc"
    assert bytes_ck[::2].get() == b"ac"
    assert bytes_ck.reverse().get() == b"dcba"
    assert bytes_ck.chunked(2)[1].get() == b"cd"
    assert bytes_ck.chunked(2, raw=True)[1] == b"cd"

def test_ck_bytes_manip():
    assert ChefKnife.init_nullbytes(4).get() == b"\x00" * 4
    
    bytes_ck = ChefKnife(b"abcd")
    assert bytes_ck.pad_pcks7().get() == b"abcd" + bytes([12] * 12)
    assert bytes_ck.pad_pcks7().unpad_pcks7().get() == b"abcd"
    with pytest.raises(ValueError) as e:
        ChefKnife(b"abcd").unpad_pcks7()

    # TODO: add, xor, add, sub

def test_ck_hashing():
    bytes_ck = ChefKnife(b"abcd")

    assert bytes_ck.to_digest("md5").get() == bytes.fromhex("e2fc714c4727ee9395f324cd2e7f331f")
    assert bytes_ck.to_hexdigest("md5").get() == "e2fc714c4727ee9395f324cd2e7f331f"
    assert bytes_ck.into_digest_int("md5") == 0xe2fc714c4727ee9395f324cd2e7f331f
    assert bytes_ck.to_digest("sha512").get() == bytes.fromhex("d8022f2060ad6efd297ab73dcc5355c9b214054b0d1776a136a669d26a7d3b14f73aa0d0ebff19ee333368f0164b6419a96da49e3e481753e7e96b716bdccb6f")
    assert bytes_ck.to_hexdigest("sha512").get() == "d8022f2060ad6efd297ab73dcc5355c9b214054b0d1776a136a669d26a7d3b14f73aa0d0ebff19ee333368f0164b6419a96da49e3e481753e7e96b716bdccb6f"
    assert bytes_ck.into_digest_int("sha512") == 0xd8022f2060ad6efd297ab73dcc5355c9b214054b0d1776a136a669d26a7d3b14f73aa0d0ebff19ee333368f0164b6419a96da49e3e481753e7e96b716bdccb6f

def test_ck_cipher():
    bytes_ck = ChefKnife(b"abcd")

    aes_key = ChefKnife(b"this_is_key").pad_pcks7()
    aes_iv = ChefKnife(b"this_is_iv").pad_pcks7()
    aes_ctr_nonce = ChefKnife(b"this_is_nonce")
    
    ecb_enc_ck = bytes_ck.pad_pcks7().aes_encrypt(aes_key)
    assert ecb_enc_ck.into_int() == 0xb855c6f237354331180e1f7a14d44567
    assert ecb_enc_ck.aes_decrypt(aes_key).unpad_pcks7().get() == b"abcd"
    
    ecb_enc_ck = bytes_ck.pad_pcks7().aes_encrypt(aes_key, "CBC", iv=aes_iv)
    assert ecb_enc_ck.into_int() == 0xa51a4b28af7518554dc1d1026ca774c0
    assert ecb_enc_ck.aes_decrypt(aes_key, "CBC", iv=aes_iv).unpad_pcks7().get() == b"abcd"
    
    ctr_enc_ck = bytes_ck.aes_encrypt(aes_key, "CTR", nonce=aes_ctr_nonce)
    assert ctr_enc_ck.into_int() == 0x2ba54251
    assert ctr_enc_ck.aes_decrypt(aes_key, "CTR", nonce=aes_ctr_nonce).get() == b"abcd"