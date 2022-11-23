from .chef import ChefKnife, Chef, CK
from .untwister import Untwister, get_seed_for_random_state

_sage_found = False
try:
    from sage.all import version as sage_version_function
    _sage_found = True
except ModuleNotFoundError:
    pass
except ImportError:
    pass

if _sage_found:
    from .dot_sage.rsa import RSAKnife
    from .dot_sage.curve import two_points_to_a4_a6, is_curve_singular, solve_singular_node, solve_singular_cusp
    from .dot_sage.matrix import expand_matrix

    from .script_bag.mimoo_boneh_durfee import boneh_durfee
    from .script_bag.mimoo_dh_backdoor import B_smooth as b_smooth_prime
    from .script_bag.defund_coppersmith import small_roots
    from .script_bag.pqlx_ec_check_param import check as check_ecc_curve
    from .script_bag.rbtree_babai_cvp import Babai_CVP as closest_vector
    from .script_bag.rkm_inequality_cvp import solve as inequality_closest_vector