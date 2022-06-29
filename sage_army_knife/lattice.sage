# by jgeralnik from https://jgeralnik.github.io/writeups/2021/08/12/Lattices/

# def Babai_closest_vector(B, target):
def closest_vector(B, target):
    # Babai's Nearest Plane algorithm
    M = B.LLL()
    G = M.gram_schmidt()[0]
    small = target
    for _ in range(1):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small