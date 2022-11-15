from sagemath.check_version import check_version

try:
    check_version(">9")
except ValueError as e:
    import_error_message = str(e)
    if "Sage does not seem to be installed" in import_error_message:
        raise ImportError("Sage not installed. Please `conda install sage`.")
    elif "is older than the required one" in import_error_message:
        raise ImportError("Sage is too old. Please update.")

from .chef import ChefKnife, Chef, CK
from .untwister import Untwister, get_seed_for_random_state

from .dot_sage.rsa import RSAKnife
from .dot_sage.curve import two_points_to_a4_a6, is_curve_singular, solve_singular_node, solve_singular_cusp

from .script_bag.mimoo_boneh_durfee import boneh_durfee
from .script_bag.mimoo_dh_backdoor import B_smooth as b_smooth_prime
from .script_bag.defund_coppersmith import small_roots
from .script_bag.pqlx_ec_check_param import check as check_ecc_curve
from .script_bag.rbtree_babai_cvp import Babai_CVP as closest_vector
from .script_bag.rkm_inequality_cvp import solve as inequality_closest_vector