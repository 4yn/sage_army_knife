

# This file was *autogenerated* from the file /home/sy/ctf2/sage_army_knife/tests/dot_sage/test_rsa.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_128 = Integer(128); _sage_const_0x10001 = Integer(0x10001); _sage_const_16 = Integer(16)
from sage_army_knife import RSAKnife

def test_npq():
    p = random_prime(_sage_const_2 **_sage_const_128 )
    q = random_prime(_sage_const_2 **_sage_const_128 )
    n = p * q

    assert RSAKnife(auto=False, n=n, p=p).npq().q == q
    assert RSAKnife(auto=False, n=n, q=q).npq().p == p
    assert RSAKnife(auto=False, p=p, q=q).npq().n == n

def test_enc_dec_sign_verify():
    e = _sage_const_0x10001 
    p = random_prime(_sage_const_2 **_sage_const_128 )
    q = random_prime(_sage_const_2 **_sage_const_128 )
    n = p * q

    pt_bytes = b"hello_potato"
    pt = int(b"hello_potato".hex(), _sage_const_16 )
    ct = ZZ(Zmod(n)(pt) ** e)

    knife = RSAKnife(auto=False, p=p, q=q, e=e).npq().pqphi().ed_from_phi()

    assert knife.encrypt(pt) == ct
    assert knife.decrypt(ct) == pt
    assert knife.decrypt_bytes(ct) == pt_bytes
    assert knife.sign(ct) == pt
    assert knife.verify(ct, pt)

def test_pq_from_ed():
    e = _sage_const_0x10001 
    p = random_prime(_sage_const_2 **_sage_const_128 )
    q = random_prime(_sage_const_2 **_sage_const_128 )
    n = p * q
    d = RSAKnife(auto=False, p=p, q=q, e=e).npq().pqphi().ed_from_phi().d

    knife = RSAKnife(auto=False, n=n, e=e, d=d).pq_from_ed()
    assert set([knife.p, knife.q]) == set([p, q])

def test_auto():
    e = _sage_const_0x10001 
    p = random_prime(_sage_const_2 **_sage_const_128 )
    q = random_prime(_sage_const_2 **_sage_const_128 )
    n = p * q

    d = RSAKnife(auto=False, p=p, q=q, e=e).npq().pqphi().ed_from_phi().d

    autoknife = RSAKnife(p=p, q=q, e=e)
    assert autoknife.n == n
    assert autoknife.d == d

    autoknife = RSAKnife(n=n, p=p, e=e)
    assert autoknife.q == q
    assert autoknife.d == d

