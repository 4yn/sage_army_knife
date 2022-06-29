def two_points_to_a4_a6(p, x1, y1, x2, y2):
    F = Zmod(p)
    x1, y1, x2, y2 = [
        F(ZZ(i))
        for i in [x1, y1, x2, y2]
    ]

    a4, a6 = Matrix(F, [
        [x1, 1],
        [x2, 1]
    ]).solve_right(vector(F, [
        y1 ^ 2 - x1 ^ 3, y2 ^ 2 - x2 ^ 3
    ]))

    assert y1 ^ 2 == x1 ^ 3 + x1 * a4 + a6
    assert y2 ^ 2 == x2 ^ 3 + x2 * a4 + a6

    return ZZ(a4), ZZ(a6)

def is_curve_singular(*args, **kwargs):
    try:
        EllipticCurve(*args, **kwargs)
    except ArithmeticError as e:
        return "singular" in str(e)
    return False

def solve_singular_node(p, a, b, gx, gy, px, py):
    # https://ctftime.org/writeup/12563
    # https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp
    
    F.<x> = Zmod(p)[]
    rhs = x ^ 3 + a * x + b
    rhs_factor = rhs.factor()
    assert len(rhs_factor) == 2

    linear_shift = [
        poly
        for poly, exp in rhs_factor
        if exp == 2
    ][0].coefficients()[0]

    rhs_shift_factor = rhs.subs(x=x-linear_shift).factor()
    scale_shift = F([
        poly
        for poly, exp in rhs_shift_factor
        if exp == 1
    ][0].coefficients()[0]).sqrt()

    gx_, px_ = [
        i + linear_shift
        for i in [gx, px]
    ]

    gz, pz = [
        (y + scale_shift * x) / (y - scale_shift * x)
        for x, y in [(gx_, gy), (px_, py)]
    ]

    sk = discrete_log(pz, gz)
    return ZZ(sk)

def solve_singular_cusp(p, gx, gy, px, py):
    F.<x> = Zmod(p)[]
    gx, gy, px, py = [
        F(ZZ(i))
        for i in [gx, gy, px, py]
    ]
    gz = gx / gy
    pz = px / py
    return ZZ(pz / gz)