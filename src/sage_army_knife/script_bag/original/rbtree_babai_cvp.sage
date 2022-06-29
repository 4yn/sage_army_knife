# rbtree_babai_cvp.sage
# Author: Hyunsik Jeong / https://twitter.com/RBTree_ / https://github.com/hyunsikjeong
# Source: https://github.com/hyunsikjeong/LLL
# URL: https://raw.githubusercontent.com/hyunsikjeong/LLL/master/babai/BabaiCVP.sage
# md5sum: 67b28b8297343eff93360c62f4e7a8dd

from sage.modules.free_module_integer import IntegerLattice

# From https://oddcoder.com/LOL-34c3/, https://hackmd.io/@hakatashi/B1OM7HFVI
def Babai_CVP(mat, target):
    M = IntegerLattice(mat, lll_reduce=True).reduced_basis
    G = M.gram_schmidt()[0]
    diff = target
    for i in reversed(range(G.nrows())):
        diff -=  M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return target - diff
