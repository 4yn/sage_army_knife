from sage_army_knife import CVPKnife

def test_sss():
    p = random_prime(2^256)
    deg = 5
    coeffs = [randrange(0, p) for _ in range(deg + 1)]

    shares = []
    for _ in range(deg + 1):
        x = randrange(0, p)
        y = ZZ(sum([c * x^d for d, c in enumerate(coeffs)]) % p)
        shares.append((x, y))

    cvpknife = CVPKnife()
    sym_coeffs = var("c0 c1 c2 c3 c4 c5")

    for sym_coeff in sym_coeffs:
        cvpknife.add_expr(sym_coeff, bounds=(0, p))

    for x, y in shares:
        expr = sum([c * x^d for d, c in enumerate(sym_coeffs)])
        cvpknife.add_expr(expr, mod=p, bounds=(y, y), trace=False)

    cvpknife.compile()
    assert cvpknife.solve() == coeffs