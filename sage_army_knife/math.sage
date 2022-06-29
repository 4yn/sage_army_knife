from .stolen.boneh_durfee import boneh_durfee_attack
from .stolen.coppersmith import small_roots
from .stolen.dh_backdoor import B_smooth as b_smooth, CM_HDSS as cm_hdss, CM_HSO as cm_hso, CM_HSO_HSS as cm_hso_hss

def legendre(x, p=None):
    if x.parent() == ZZ:
        x = Zmod(p)(x)
    p = x.parent().cardinality()
    return x ^ (p // 2)