import random
from z3 import *
from .script_bag.icemonster_untwister import Untwister as _Untwister

# https://imp.ress.me/blog/2022-11-13/seccon-ctf-2022/#janken-vs-kurenaif

class Untwister(_Untwister):
    def __init__(self):
        super().__init__()
        self.first_MT = self.MT

        # https://github.com/python/cpython/blob/main/Modules/_randommodule.c#L201
        # Index is 624 after seeding
        self.index = 624

    def get_random_after_seed(self):
        # https://github.com/python/cpython/blob/main/Modules/_randommodule.c#L232
        # First MT state is set to 0x80000000 after seeding
        self.solver.add(self.first_MT[0] == 0x80000000)

        print(self.solver.check())
        model = self.solver.model()
        state = [
            model[x].as_long() if model[x] is not None else 0
            for x in self.first_MT
        ]

        result_state = (3, tuple(state+[624]), None)
        rand = random.Random()
        rand.setstate(result_state)
        return rand

prng_N = 624

def u32(x):
    return x & 0xffffffff

# Note that LShR is used instead of ">>" operator
# unsigned 32 bit integers use logical bitshift, not arithmetic bitshift.

# https://github.com/python/cpython/blob/main/Modules/_randommodule.c#L186
def init_genrand(s):
    mt = [0 for _ in range(prng_N)]

    mt[0] = BitVecVal(s, 32)
    mti = 1
    while mti < prng_N:
        mt[mti] = u32(
            1812433253 * (mt[mti-1] ^ LShR(mt[mti-1], 30)) + mti
            # 1812433253 * (mt[mti-1] ^ (mt[mti-1] >> 30)) + mti
        )
        mti += 1
    return mt, mti

# https://github.com/python/cpython/blob/main/Modules/_randommodule.c#L209
def init_by_array(init_key):
    key_length = len(init_key)
    mt, mti = init_genrand(19650218)

    i, j = 1, 0
    k = prng_N if prng_N > key_length else key_length
    while k:
        mt[i] = u32(
            (mt[i] ^ ((mt[i-1] ^ LShR(mt[i-1], 30)) * 1664525)) + init_key[j] + j
        )
        i, j = i + 1, j + 1
        if i >= prng_N:
            mt[0] = mt[prng_N-1]
            i = 1
        if j >= key_length:
            j = 0
        k -= 1

    k = prng_N - 1
    while k:
        mt[i] = u32(
            (mt[i] ^ ((mt[i-1] ^ LShR(mt[i-1], 30)) * 1566083941)) - i
        )
        i += 1
        if i >= prng_N:
            mt[0] = mt[prng_N-1]
            i = 1
        k -= 1

    mt[0] = 0x80000000;

    return mt

def get_seed_for_random_state(ut_rand_state, seed_length=624, return_init_key=False):
    seed_vars = [
        BitVec(f"seed_{i}", 32) for i in range(seed_length)
    ]
    seed_rand_state = init_by_array(seed_vars)

    s = Solver()
    for a, b in zip(seed_rand_state, ut_rand_state):
        s.add(a == b)
    print(s.check())

    model = s.model()
    seed_init_key = [
        model[x].as_long() if model[x] is not None else 0
        for x in seed_vars
    ]

    seed_rand_seed = sum([x * (2 ** (idx * 32))for idx, x in enumerate(seed_init_key)])

    verify_rand = random.Random()
    verify_rand.seed(seed_rand_seed)
    assert list(verify_rand.getstate()[1][:-1]) == list(ut_rand_state)

    if return_init_key:
        return seed_init_key

    return seed_rand_seed
