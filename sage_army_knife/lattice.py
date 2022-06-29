

# This file was *autogenerated* from the file sage_army_knife/lattice.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1)# by jgeralnik from https://jgeralnik.github.io/writeups/2021/08/12/Lattices/

# def Babai_closest_vector(B, target):
def closest_vector(B, target):
    # Babai's Nearest Plane algorithm
    M = B.LLL()
    G = M.gram_schmidt()[_sage_const_0 ]
    small = target
    for _ in range(_sage_const_1 ):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small
