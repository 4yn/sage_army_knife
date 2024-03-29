

# This file was *autogenerated* from the file /home/sy/dev/sage_army_knife/tests/dot_sage/test_cvp.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_256 = Integer(256); _sage_const_5 = Integer(5); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
from sage_army_knife import CVPKnife

def test_sss():
    p = random_prime(_sage_const_2 **_sage_const_256 )
    deg = _sage_const_5 
    coeffs = [randrange(_sage_const_0 , p) for _ in range(deg + _sage_const_1 )]

    shares = []
    for _ in range(deg + _sage_const_1 ):
        x = randrange(_sage_const_0 , p)
        y = ZZ(sum([c * x**d for d, c in enumerate(coeffs)]) % p)
        shares.append((x, y))

    cvpknife = CVPKnife()
    sym_coeffs = var("c0 c1 c2 c3 c4 c5")

    for sym_coeff in sym_coeffs:
        cvpknife.add_expr(sym_coeff, bounds=(_sage_const_0 , p))

    for x, y in shares:
        expr = sum([c * x**d for d, c in enumerate(sym_coeffs)])
        cvpknife.add_expr(expr, mod=p, bounds=(y, y), trace=False)

    cvpknife.compile()
    assert cvpknife.solve() == coeffs

