

# This file was *autogenerated* from the file /home/sy/ctf2/sage_army_knife/src/sage_army_knife/dot_sage/matrix.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0)
def get_2d_dims(x):
    if isinstance(x, list):
        assert len(x) >= _sage_const_1 
        r = len(x)
        assert len(set([len(i) for i in x])) == _sage_const_1 
        c = len(x[_sage_const_0 ])
        return r, c
    elif isinstance(x, sage.matrix.matrix0.Matrix):
        return x.nrows(), x.ncols()
    return None, None

def aggreate_dims(x):
    dims = [
        i
        for i in x
        if i is not None
    ]
    dims = list(set(dims))

    if len(dims) != _sage_const_1 :
        raise ValueError(f"Inconsistent dimensions {dims}")
    return dims[_sage_const_0 ]

def expand_cell(x, r, c):
    if isinstance(x, (list, sage.matrix.matrix0.Matrix)):
        return x
    else:
        if x is None:
            x = _sage_const_0 

        return [
            [
                x
                for _ in range(c)
            ]
            for _ in range(r)
        ]
    
def expand_matrix(raw_matrix, base_ring=None):
    compress_r, compress_c = get_2d_dims(raw_matrix)
    sub_dims = [
        [
            get_2d_dims(cell)
            for cell in row
        ]
        for row in raw_matrix
    ]

    row_dims = [
        aggreate_dims([sub_dims[row_i][col_i][_sage_const_0 ] for col_i in range(compress_c)])
        for row_i in range(compress_r)
    ]
    col_dims = [
        aggreate_dims([sub_dims[row_i][col_i][_sage_const_1 ] for row_i in range(compress_r)])
        for col_i in range(compress_c)
    ]

    uncompress_r = sum(row_dims)
    uncompress_c = sum(col_dims)

    expand_matrix = [
        [
            _sage_const_0 
            for _ in range(uncompress_c)
        ]
        for _ in range(uncompress_r)
    ]
    
    for row_i in range(compress_r):
        for col_i in range(compress_c):
            cell = expand_cell(
                raw_matrix[row_i][col_i],
                row_dims[row_i],
                col_dims[col_i]
            )

            if isinstance(cell, sage.matrix.matrix0.Matrix):
                cell_base_ring = cell.base_ring()
                if base_ring is None:
                    base_ring = cell_base_ring
                else:
                    if base_ring != cell_base_ring:
                        raise ValueError(f"Inconsistent base ring {cell_base_ring} and {base_ring}")

            base_row_i = sum(row_dims[:row_i])
            base_col_i = sum(col_dims[:col_i])
            for sub_row_i in range(row_dims[row_i]):
                for sub_col_i in range(col_dims[col_i]):
                    expand_matrix[base_row_i + sub_row_i][base_col_i + sub_col_i] = cell[sub_row_i][sub_col_i]

    if base_ring is None:
        base_ring = ZZ

    return Matrix(base_ring, expand_matrix)


class SparseMatrixRow:
    def __init__(self, y, parent):
        self.y = y
        self.parent = parent

    def __getitem__(self, x):
        return self.parent.getitem_2d(self.y, x)

    def __setitem__(self, x, val):
        return self.parent.setitem_2d(self.y, x, val)

class SparseMatrix:
    def __init__(self, fill=_sage_const_0 ):
        self.rows = {}
        self.data = {}
        self.fill = fill

    def __getitem__(self, y):
        if y not in self.data:
            self.rows[y] = SparseMatrixRow(y, self)
        return self.rows[y]

    def getitem_2d(self, y, x):
        return self.data.get((y, x), self.fill)

    def setitem_2d(self, y, x, val):
        self.data[(y, x)] = val
        return val

    def build(self, base_ring=None):
        r = max([y for y, _ in self.data.keys()]) + _sage_const_1 
        c = max([x for _, x in self.data.keys()]) + _sage_const_1 
        
        data = [
            [
                self.data.get((y, x), self.fill)
                for x in range(c)
            ]
            for y in range(r)
        ]
        if base_ring is None:
            return Matrix(data)
        else:
            return Matrix(base_ring, data)
