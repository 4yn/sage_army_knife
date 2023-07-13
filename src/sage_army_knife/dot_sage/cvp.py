

# This file was *autogenerated* from the file cvp.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1000 = Integer(1000); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3)
from ..script_bag.rbtree_babai_cvp import Babai_CVP

class CVPKnife:
    def __init__(self, show=True, preview_mod=_sage_const_1000 ):
        self.raw_exprs = []

        self.expr_count = _sage_const_0 
        self.row_count = _sage_const_0 
        self.var_to_row = {}
        self.row_labels = {}
        self.magnitude = _sage_const_0 

        self.wip_matrix = {}
        self.wip_vector = []
        self.trace = []

        self.show = show
        self.preview_mod = _sage_const_1000 

        self.status = "input"

    def register_variable(self, var_name):
        if var_name not in self.var_to_row:
            self.var_to_row[var_name] = self.row_count
            self.row_labels[self.row_count] = str(var_name)
            self.row_count += _sage_const_1 
        return self.var_to_row[var_name]

    def add_expr(self, expr: sage.symbolic.expression.Expression, mod=None, bounds=(_sage_const_0 , _sage_const_0 ), trace=None):
        if self.status != "input":
            raise ValueError("CVP already compiled, cannot add new expressions")
        
        if not isinstance(expr.base_ring(), sage.symbolic.ring.SymbolicRing):
            raise ValueError("Expression is not symbolic")
        
        orig_expr = expr
        expr = expr.expand()
        if expr.is_relational():
            if not expr.operator() == operator.eq:
                raise ValueError("Relational expressions should have equality (=) or supply bounds in kwargs")
            expr = expr.lhs() - expr.rhs()
        
        poly = expr.polynomial(expr.base_ring())
        poly_vars = poly.variables()
        poly_parts = list(poly)
        if len(poly_vars) == _sage_const_0 :
            raise ValueError("Expression is constant")
        elif len(poly_vars) == _sage_const_1 :
            poly_parts = [
                (coefficient, poly_vars[_sage_const_0 ] ** idx)
                for idx, coefficient in enumerate(poly_parts)
            ]

        for coefficient, variable in poly_parts:
            if coefficient == _sage_const_0 :
                continue
            if variable.degree() >= _sage_const_2 :
                print(f"Warning: expression has component {variable} with degree >= 2")
            if mod is not None:
                coefficient = ZZ(ZZ(coefficient) % mod)
            self.wip_matrix[(self.register_variable(variable), self.expr_count)] = coefficient
            self.magnitude = max(self.magnitude, coefficient)

        if mod is not None:
            self.wip_matrix[(self.row_count, self.expr_count)] = mod
            self.row_labels[self.row_count] = f"% col {self.expr_count}"
            self.row_count += _sage_const_1 

        if not isinstance(bounds, tuple) or len(bounds) != _sage_const_2 :
            raise ValueError("Bounds are invalid, expecting length-2 tuple of (lb, ub)")
        if bounds[_sage_const_1 ] < bounds[_sage_const_0 ]:
            raise ValueError("Bounds are invalid, lb > ub")
        self.wip_vector.append(bounds)

        if trace is None:
            if bounds == (_sage_const_0 , _sage_const_0 ):
                trace = False
            else:
                trace = True
        self.trace.append(trace)

        self.raw_exprs.append(orig_expr)

        self.expr_count += _sage_const_1 

    def compile(self):
        if self.status != "input":
            raise ValueError("CVP already compiled, cannot re-compile")
        
        # calculate expected vector error and large constants
        self.expected_error = lcm([_sage_const_1 ] + [(ub - lb) * _sage_const_2  for lb, ub in self.wip_vector if lb != ub])
        self.magnitude = max(self.magnitude, self.expected_error)
        self.large = _sage_const_2  ** (self.magnitude.nbits() * _sage_const_2 )
        self.huge = _sage_const_2  ** (self.magnitude.nbits() * _sage_const_3 )

        # calculate scale for each column
        self.scale = {}
        for col, (lb, ub) in enumerate(self.wip_vector):
            scale = self.large
            if (ub - lb) != _sage_const_0 :
                scale = self.expected_error // (ub - lb)
            self.scale[col] = scale

        # add large constant to x^0 row
        if _sage_const_1  in self.var_to_row:
            self.wip_matrix[(self.register_variable(_sage_const_1 ), self.expr_count)] = _sage_const_1 
            self.wip_vector.append((_sage_const_1 , _sage_const_1 ))
            self.scale[self.expr_count] = self.huge
            self.expr_count += _sage_const_1 

        # apply scale to vector
        scaled_vector = []
        for col, (lb, ub) in enumerate(self.wip_vector):
            midpoint = self.scale[col] * (ub + lb) // _sage_const_2 
            scaled_vector.append(midpoint)
        
        # compile vector
        self.vector = vector(ZZ, scaled_vector)

        # apply scale to matrix
        scaled_matrix = {
            (row, col): v * self.scale[col]
            for (row, col), v in self.wip_matrix.items()
        }

        # compile matrix
        self.matrix = Matrix(ZZ, scaled_matrix, sparse=False)

        if self.show:
            matrix_str = (self.matrix % self.preview_mod).str()
            matrix_str_with_vars = [
                f"{row_str} <- {self.row_labels[row]}"
                for row, row_str
                in enumerate(matrix_str.strip().split("\n"))
            ]
            print("Lattice:")
            print("\n".join(matrix_str_with_vars))
            print("Goal vector:")
            print((self.vector % self.preview_mod))

        self.status = "compiled"

    def solve(self, fmt="list"):
        if self.status != "compiled":
            raise ValueError("CVP not yet compiled")
        
        # run cvp
        self.raw_cv = Babai_CVP(self.matrix, self.vector)

        if self.show:
            print("Closest vector:")
            print((self.raw_cv % self.preview_mod))

        # unscale
        self.cv = []
        for col, raw_cv_i in enumerate(self.raw_cv):
            scale = self.scale[col]
            if raw_cv_i % scale != _sage_const_0 :
                raise ValueError("Solution out of scale")
            self.cv.append(raw_cv_i // scale)
        
        # bounds check
        if self.show:
            for idx, (cv_i, (lb, ub)) in enumerate(zip(self.cv, self.wip_vector)):
                if not (lb <= cv_i <= ub):
                    print(f"Warning: expression {idx} solution was out of bounds")
        
        # return traced
        if fmt == "list":
            return [
                res
                for res, to_trace
                in zip(self.cv, self.trace)
                if to_trace
            ]
        
        elif fmt == "dict":
            return {
                expr: res
                for expr, res, to_trace
                in zip(self.raw_exprs, self.cv, self.trace)
                if to_trace
            }
    
    def __repr__(self):
        return f"CVPKnife({len(self.raw_exprs)} expressions with {sum(self.trace)} traced across {len(self.var_to_row)} variables)"

