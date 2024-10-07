from numpy._core.fromnumeric import matrix_transpose
from numpy._core.numeric import tensordot, vecdot

from ._linalg import (
    matrix_power,
    solve,
    tensorsolve,
    tensorinv,
    inv,
    cholesky,
    outer,
    eigvals,
    eigvalsh,
    pinv,
    slogdet,
    det,
    svd,
    svdvals,
    eig,
    eigh,
    lstsq,
    norm,
    matrix_norm,
    vector_norm,
    qr,
    cond,
    matrix_rank,
    multi_dot,
    matmul,
    trace,
    diagonal,
    cross,
)

__all__ = [
    "matrix_power",
    "solve",
    "tensorsolve",
    "tensorinv",
    "inv",
    "cholesky",
    "eigvals",
    "eigvalsh",
    "pinv",
    "slogdet",
    "det",
    "svd",
    "svdvals",
    "eig",
    "eigh",
    "lstsq",
    "norm",
    "qr",
    "cond",
    "matrix_rank",
    "LinAlgError",
    "multi_dot",
    "trace",
    "diagonal",
    "cross",
    "outer",
    "tensordot",
    "matmul",
    "matrix_transpose",
    "matrix_norm",
    "vector_norm",
    "vecdot",
]

class LinAlgError(Exception): ...
