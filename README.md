# Sage Army Knife

A mutitool for cryptography CTF problems

## Install

Install `sage` (>9) from other means, then install package via git URL.

```bash
# seutp conda env?
conda install sage
pip install git+https://github.com/4yn/sage_army_knife.git@main
```

## Script Bag

```python
from sage_army_knife import *
```

Many of these functions aren't my own, credits to the original authors where due.

- Data manipulation: `ChefKnife`
- RSA: `RSAKnife`, [`boneh_durfee`](https://github.com/mimoo/RSA-and-LLL-attacks) by [@mimoo](https://github.com/mimoo)
- DH: [`b_smooth_prime`](https://github.com/mimoo/Diffie-Hellman_Backdoor) by [@mimoo](https://github.com/mimoo)
- PRNG: [`Untwister`](https://github.com/icemonster/symbolic_mersenne_cracker) by [@icemonster](https://github.com/icemonster), [`get_seed_for_random_state`](https://imp.ress.me/blog/2022-11-13/seccon-ctf-2022#janken-vs-kurenaif)
- ECC: `two_points_to_a4_a6`, `is_curve_singular`, `solve_singular_node`, `solve_singular_cusp`, [`check_ecc_curve`](https://gist.github.com/pqlx/d0bdf2d0c4a2aa400b2b52d9bd9b7b65) by [@pqlx](https://github.com/pqlx)
- Lattices: [`closest_vector`](https://github.com/hyunsikjeong/LLL) by [@rbtree](https://github.com/hyunsikjeong), [`inequality_closest_vector`](https://github.com/rkm0959/Inequality_Solving_with_CVP) by [@rkm0959](https://github.com/rkm0959)
- Polynomials: [`small_roots`](https://github.com/defund/coppersmith) by [@defund](https://github.com/defund)

Other CTF crypto code libraries worth looking at:

- [@p4-team/crypto-commons](https://github.com/p4-team/crypto-commons)
- [@ValarDragon/CTF-Crypto](https://github.com/ValarDragon/CTF-Crypto)
- [@rkm0959/Cryptography_Writeups](https://github.com/rkm0959/Cryptography_Writeups)
- [@josephsurin/lattice-based-cryptanalysis](https://github.com/josephsurin/lattice-based-cryptanalysis)

## ChefKnife

```python
from sage_army_knife import ChefKnife
from sage_army_knife import Chef
from sage_army_knife import CK
```

Polyglot data container for casting between data encodings, inspired by
[CyberChef](https://gchq.github.io/CyberChef/) and
[@securisec/chepy](https://github.com/securisec/chepy).

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

## RSAKnife

Docs WIP

## References

1. https://github.com/mimoo/RSA-and-LLL-attacks
1. https://github.com/mimoo/Diffie-Hellman_Backdoor
1. https://github.com/defund/coppersmith
1. https://gist.github.com/pqlx/d0bdf2d0c4a2aa400b2b52d9bd9b7b65
1. https://github.com/hyunsikjeong/LLL
1. https://github.com/rkm0959/Inequality_Solving_with_CVP
1. https://github.com/icemonster/symbolic_mersenne_cracker
1. https://ctftime.org/writeup/12563
1. https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp
1. https://jgeralnik.github.io/writeups/2021/08/12/Lattices/
