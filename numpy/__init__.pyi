import builtins
import sys
import os
import mmap
import ctypes as ct
import array as _array
import datetime as dt
import enum
from abc import abstractmethod
from types import EllipsisType, TracebackType, MappingProxyType, GenericAlias
from decimal import Decimal
from fractions import Fraction
from uuid import UUID

import numpy as np
from numpy._pytesttester import PytestTester
from numpy._core._internal import _ctypes

from numpy._typing import (
    # Arrays
    ArrayLike,
    NDArray,
    _SupportsArray,
    _NestedSequence,
    _FiniteNestedSequence,
    _ArrayLikeBool_co,
    _ArrayLikeUInt_co,
    _ArrayLikeInt_co,
    _ArrayLikeFloat_co,
    _ArrayLikeComplex_co,
    _ArrayLikeNumber_co,
    _ArrayLikeTD64_co,
    _ArrayLikeDT64_co,
    _ArrayLikeObject_co,
    _ArrayLikeUnknown,
    _UnknownType,

    # DTypes
    DTypeLike,
    _DTypeLike,
    _DTypeLikeVoid,
    _VoidDTypeLike,

    # Shapes
    _Shape,
    _ShapeLike,

    # Scalars
    _CharLike_co,
    _IntLike_co,
    _FloatLike_co,
    _TD64Like_co,
    _NumberLike_co,
    _ScalarLike_co,

    # `number` precision
    NBitBase,
    # NOTE: Do not remove the extended precision bit-types even if seemingly unused;
    # they're used by the mypy plugin
    _256Bit,
    _128Bit,
    _96Bit,
    _80Bit,
    _64Bit,
    _32Bit,
    _16Bit,
    _8Bit,
    _NBitByte,
    _NBitShort,
    _NBitIntC,
    _NBitIntP,
    _NBitLong,
    _NBitLongLong,
    _NBitHalf,
    _NBitSingle,
    _NBitDouble,
    _NBitLongDouble,

    # Character codes
    _BoolCodes,
    _UInt8Codes,
    _UInt16Codes,
    _UInt32Codes,
    _UInt64Codes,
    _Int8Codes,
    _Int16Codes,
    _Int32Codes,
    _Int64Codes,
    _Float16Codes,
    _Float32Codes,
    _Float64Codes,
    _Complex64Codes,
    _Complex128Codes,
    _ByteCodes,
    _ShortCodes,
    _IntCCodes,
    _IntPCodes,
    _LongCodes,
    _LongLongCodes,
    _UByteCodes,
    _UShortCodes,
    _UIntCCodes,
    _UIntPCodes,
    _ULongCodes,
    _ULongLongCodes,
    _HalfCodes,
    _SingleCodes,
    _DoubleCodes,
    _LongDoubleCodes,
    _CSingleCodes,
    _CDoubleCodes,
    _CLongDoubleCodes,
    _DT64Codes,
    _TD64Codes,
    _StrCodes,
    _BytesCodes,
    _VoidCodes,
    _ObjectCodes,
    _StringCodes,

    _UnsignedIntegerCodes,
    _SignedIntegerCodes,
    _IntegerCodes,
    _FloatingCodes,
    _ComplexFloatingCodes,
    _InexactCodes,
    _NumberCodes,
    _CharacterCodes,
    _FlexibleCodes,
    _GenericCodes,

    # Ufuncs
    _UFunc_Nin1_Nout1,
    _UFunc_Nin2_Nout1,
    _UFunc_Nin1_Nout2,
    _UFunc_Nin2_Nout2,
    _GUFunc_Nin2_Nout1,
)

from numpy._typing._callable import (
    _BoolOp,
    _BoolBitOp,
    _BoolSub,
    _BoolTrueDiv,
    _BoolMod,
    _BoolDivMod,
    _TD64Div,
    _IntTrueDiv,
    _UnsignedIntOp,
    _UnsignedIntBitOp,
    _UnsignedIntMod,
    _UnsignedIntDivMod,
    _SignedIntOp,
    _SignedIntBitOp,
    _SignedIntMod,
    _SignedIntDivMod,
    _FloatOp,
    _FloatMod,
    _FloatDivMod,
    _NumberOp,
    _ComparisonOpLT,
    _ComparisonOpLE,
    _ComparisonOpGT,
    _ComparisonOpGE,
)

# NOTE: Numpy's mypy plugin is used for removing the types unavailable
# to the specific platform
from numpy._typing._extended_precision import (
    uint128,
    uint256,
    int128,
    int256,
    float80,
    float96,
    float128,
    float256,
    complex160,
    complex192,
    complex256,
    complex512,
)

from numpy._array_api_info import __array_namespace_info__

from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
from typing import (
    Literal as L,
    Any,
    NoReturn,
    SupportsComplex,
    SupportsFloat,
    SupportsInt,
    SupportsIndex,
    Final,
    final,
    ClassVar,
    TypeAlias,
    type_check_only,
)

# NOTE: `typing_extensions` is always available in `.pyi` stubs or when
# `TYPE_CHECKING` - even if not available at runtime.
# This is because the `typeshed` stubs for the standard library include
# `typing_extensions` stubs:
# https://github.com/python/typeshed/blob/main/stdlib/typing_extensions.pyi
from typing_extensions import Generic, LiteralString, Protocol, Self, TypeVar, overload

from numpy import (
    core,
    ctypeslib,
    exceptions,
    f2py,
    fft,
    lib,
    linalg,
    ma,
    polynomial,
    random,
    testing,
    typing,
    version,
    dtypes,
    rec,
    char,
    strings,
)

from numpy._core.records import (
    record,
    recarray,
)

from numpy._core.function_base import (
    linspace,
    logspace,
    geomspace,
)

from numpy._core.fromnumeric import (
    take,
    reshape,
    choose,
    repeat,
    put,
    swapaxes,
    transpose,
    matrix_transpose,
    partition,
    argpartition,
    sort,
    argsort,
    argmax,
    argmin,
    searchsorted,
    resize,
    squeeze,
    diagonal,
    trace,
    ravel,
    nonzero,
    shape,
    compress,
    clip,
    sum,
    all,
    any,
    cumsum,
    cumulative_sum,
    ptp,
    max,
    min,
    amax,
    amin,
    prod,
    cumprod,
    cumulative_prod,
    ndim,
    size,
    around,
    round,
    mean,
    std,
    var,
)

from numpy._core._asarray import (
    require,
)

from numpy._core._type_aliases import (
    sctypeDict,
)

from numpy._core._ufunc_config import (
    seterr,
    geterr,
    setbufsize,
    getbufsize,
    seterrcall,
    geterrcall,
    _ErrKind,
    _ErrFunc,
)

from numpy._core.arrayprint import (
    set_printoptions,
    get_printoptions,
    array2string,
    format_float_scientific,
    format_float_positional,
    array_repr,
    array_str,
    printoptions,
)

from numpy._core.einsumfunc import (
    einsum,
    einsum_path,
)

from numpy._core.multiarray import (
    array,
    empty_like,
    empty,
    zeros,
    concatenate,
    inner,
    where,
    lexsort,
    can_cast,
    min_scalar_type,
    result_type,
    dot,
    vdot,
    bincount,
    copyto,
    putmask,
    packbits,
    unpackbits,
    shares_memory,
    may_share_memory,
    asarray,
    asanyarray,
    ascontiguousarray,
    asfortranarray,
    arange,
    busday_count,
    busday_offset,
    datetime_as_string,
    datetime_data,
    frombuffer,
    fromfile,
    fromiter,
    is_busday,
    promote_types,
    fromstring,
    frompyfunc,
    nested_iters,
    flagsobj,
)

from numpy._core.numeric import (
    zeros_like,
    ones,
    ones_like,
    full,
    full_like,
    count_nonzero,
    isfortran,
    argwhere,
    flatnonzero,
    correlate,
    convolve,
    outer,
    tensordot,
    roll,
    rollaxis,
    moveaxis,
    cross,
    indices,
    fromfunction,
    isscalar,
    binary_repr,
    base_repr,
    identity,
    allclose,
    isclose,
    array_equal,
    array_equiv,
    astype,
)

from numpy._core.numerictypes import (
    isdtype,
    issubdtype,
    ScalarType,
    typecodes,
)

from numpy._core.shape_base import (
    atleast_1d,
    atleast_2d,
    atleast_3d,
    block,
    hstack,
    stack,
    vstack,
    unstack,
)

from numpy.lib import (
    scimath as emath,
)

from numpy.lib._arraypad_impl import (
    pad,
)

from numpy.lib._arraysetops_impl import (
    ediff1d,
    intersect1d,
    isin,
    setdiff1d,
    setxor1d,
    union1d,
    unique,
    unique_all,
    unique_counts,
    unique_inverse,
    unique_values,
)

from numpy.lib._function_base_impl import (
    select,
    piecewise,
    trim_zeros,
    copy,
    iterable,
    percentile,
    diff,
    gradient,
    angle,
    unwrap,
    sort_complex,
    flip,
    rot90,
    extract,
    place,
    asarray_chkfinite,
    average,
    bincount,
    digitize,
    cov,
    corrcoef,
    median,
    sinc,
    hamming,
    hanning,
    bartlett,
    blackman,
    kaiser,
    i0,
    meshgrid,
    delete,
    insert,
    append,
    interp,
    quantile,
    trapezoid,
)

from numpy.lib._histograms_impl import (
    histogram_bin_edges,
    histogram,
    histogramdd,
)

from numpy.lib._index_tricks_impl import (
    ravel_multi_index,
    unravel_index,
    mgrid,
    ogrid,
    r_,
    c_,
    s_,
    index_exp,
    ix_,
    fill_diagonal,
    diag_indices,
    diag_indices_from,
)

from numpy.lib._nanfunctions_impl import (
    nansum,
    nanmax,
    nanmin,
    nanargmax,
    nanargmin,
    nanmean,
    nanmedian,
    nanpercentile,
    nanvar,
    nanstd,
    nanprod,
    nancumsum,
    nancumprod,
    nanquantile,
)

from numpy.lib._npyio_impl import (
    savetxt,
    loadtxt,
    genfromtxt,
    load,
    save,
    savez,
    savez_compressed,
    packbits,
    unpackbits,
    fromregex,
)

from numpy.lib._polynomial_impl import (
    poly,
    roots,
    polyint,
    polyder,
    polyadd,
    polysub,
    polymul,
    polydiv,
    polyval,
    polyfit,
)

from numpy.lib._shape_base_impl import (
    column_stack,
    dstack,
    array_split,
    split,
    hsplit,
    vsplit,
    dsplit,
    apply_over_axes,
    expand_dims,
    apply_along_axis,
    kron,
    tile,
    take_along_axis,
    put_along_axis,
)

from numpy.lib._stride_tricks_impl import (
    broadcast_to,
    broadcast_arrays,
    broadcast_shapes,
)

from numpy.lib._twodim_base_impl import (
    diag,
    diagflat,
    eye,
    fliplr,
    flipud,
    tri,
    triu,
    tril,
    vander,
    histogram2d,
    mask_indices,
    tril_indices,
    tril_indices_from,
    triu_indices,
    triu_indices_from,
)

from numpy.lib._type_check_impl import (
    mintypecode,
    real,
    imag,
    iscomplex,
    isreal,
    iscomplexobj,
    isrealobj,
    nan_to_num,
    real_if_close,
    typename,
    common_type,
)

from numpy.lib._ufunclike_impl import (
    fix,
    isposinf,
    isneginf,
)

from numpy.lib._utils_impl import (
    get_include,
    info,
    show_runtime,
)

from numpy.matrixlib import (
    asmatrix,
    bmat,
)

__all__ = [
    "emath", "show_config", "version", "__version__", "__array_namespace_info__",

    # __numpy_submodules__
    "linalg", "fft", "dtypes", "random", "polynomial", "ma", "exceptions", "lib",
    "ctypeslib", "testing", "test", "rec", "char", "strings",
    "core", "typing", "f2py",

    # _core.__all__
    "abs", "acos", "acosh", "asin", "asinh", "atan", "atanh", "atan2", "bitwise_invert",
    "bitwise_left_shift", "bitwise_right_shift", "concat", "pow", "permute_dims",
    "memmap", "sctypeDict", "record", "recarray",

    # _core.numeric.__all__
    "newaxis", "ndarray", "flatiter", "nditer", "nested_iters", "ufunc", "arange",
    "array", "asarray", "asanyarray", "ascontiguousarray", "asfortranarray", "zeros",
    "count_nonzero", "empty", "broadcast", "dtype", "fromstring", "fromfile",
    "frombuffer", "from_dlpack", "where", "argwhere", "copyto", "concatenate",
    "lexsort", "astype", "can_cast", "promote_types", "min_scalar_type", "result_type",
    "isfortran", "empty_like", "zeros_like", "ones_like", "correlate", "convolve",
    "inner", "dot", "outer", "vdot", "roll", "rollaxis", "moveaxis", "cross",
    "tensordot", "little_endian", "fromiter", "array_equal", "array_equiv", "indices",
    "fromfunction", "isclose", "isscalar", "binary_repr", "base_repr", "ones",
    "identity", "allclose", "putmask", "flatnonzero", "inf", "nan", "False_", "True_",
    "bitwise_not", "full", "full_like", "matmul", "vecdot", "shares_memory",
    "may_share_memory", "_get_promotion_state", "_set_promotion_state",
    "all", "amax", "amin", "any", "argmax", "argmin", "argpartition", "argsort",
    "around", "choose", "clip", "compress", "cumprod", "cumsum", "cumulative_prod",
    "cumulative_sum", "diagonal", "mean", "max", "min", "matrix_transpose", "ndim",
    "nonzero", "partition", "prod", "ptp", "put", "ravel", "repeat", "reshape",
    "resize", "round", "searchsorted", "shape", "size", "sort", "squeeze", "std", "sum",
    "swapaxes", "take", "trace", "transpose", "var",
    "absolute", "add", "arccos", "arccosh", "arcsin", "arcsinh", "arctan", "arctan2",
    "arctanh", "bitwise_and", "bitwise_or", "bitwise_xor", "cbrt", "ceil", "conj",
    "conjugate", "copysign", "cos", "cosh", "bitwise_count", "deg2rad", "degrees",
    "divide", "divmod", "e", "equal", "euler_gamma", "exp", "exp2", "expm1", "fabs",
    "floor", "floor_divide", "float_power", "fmax", "fmin", "fmod", "frexp",
    "frompyfunc", "gcd", "greater", "greater_equal", "heaviside", "hypot", "invert",
    "isfinite", "isinf", "isnan", "isnat", "lcm", "ldexp", "left_shift", "less",
    "less_equal", "log", "log10", "log1p", "log2", "logaddexp", "logaddexp2",
    "logical_and", "logical_not", "logical_or", "logical_xor", "maximum", "minimum",
    "mod", "modf", "multiply", "negative", "nextafter", "not_equal", "pi", "positive",
    "power", "rad2deg", "radians", "reciprocal", "remainder", "right_shift", "rint",
    "sign", "signbit", "sin", "sinh", "spacing", "sqrt", "square", "subtract", "tan",
    "tanh", "true_divide", "trunc", "ScalarType", "typecodes", "issubdtype",
    "datetime_data", "datetime_as_string", "busday_offset", "busday_count", "is_busday",
    "busdaycalendar", "isdtype",
    "complexfloating", "character", "unsignedinteger", "inexact", "generic", "floating",
    "integer", "signedinteger", "number", "flexible", "bool", "float16", "float32",
    "float64", "longdouble", "complex64", "complex128", "clongdouble",
    "bytes_", "str_", "void", "object_", "datetime64", "timedelta64", "int8", "byte",
    "uint8", "ubyte", "int16", "short", "uint16", "ushort", "int32", "intc", "uint32",
    "uintc", "int64", "long", "uint64", "ulong", "longlong", "ulonglong", "intp",
    "uintp", "double", "cdouble", "single", "csingle", "half", "bool_", "int_", "uint",
    "uint128", "uint256", "int128", "int256", "float80", "float96", "float128",
    "float256", "complex160", "complex192", "complex256", "complex512",
    "array2string", "array_str", "array_repr", "set_printoptions", "get_printoptions",
    "printoptions", "format_float_positional", "format_float_scientific", "require",
    "seterr", "geterr", "setbufsize", "getbufsize", "seterrcall", "geterrcall",
    "errstate", "_no_nep50_warning",
    # _core.function_base.__all__
    "logspace", "linspace", "geomspace",
    # _core.getlimits.__all__
    "finfo", "iinfo",
    # _core.shape_base.__all__
    "atleast_1d", "atleast_2d", "atleast_3d", "block", "hstack", "stack", "unstack",
    "vstack",
    # _core.einsumfunc.__all__
    "einsum", "einsum_path",

    # lib._histograms_impl.__all__
    "histogram", "histogramdd", "histogram_bin_edges",
    # lib._nanfunctions_impl.__all__
    "nansum", "nanmax", "nanmin", "nanargmax", "nanargmin", "nanmean", "nanmedian",
    "nanpercentile", "nanvar", "nanstd", "nanprod", "nancumsum", "nancumprod",
    "nanquantile",
    # lib._function_base_impl.__all__
    # NOTE: `trapz` is omitted because it is deprecated
    "select", "piecewise", "trim_zeros", "copy", "iterable", "percentile", "diff",
    "gradient", "angle", "unwrap", "sort_complex", "flip", "rot90", "extract", "place",
    "vectorize", "asarray_chkfinite", "average", "bincount", "digitize", "cov",
    "corrcoef", "median", "sinc", "hamming", "hanning", "bartlett", "blackman",
    "kaiser", "i0", "meshgrid", "delete", "insert", "append", "interp", "quantile",
    "trapezoid",
    # lib._twodim_base_impl.__all__
    "diag", "diagflat", "eye", "fliplr", "flipud", "tri", "triu", "tril", "vander",
    "histogram2d", "mask_indices", "tril_indices", "tril_indices_from", "triu_indices",
    "triu_indices_from",
    # lib._shape_base_impl.__all__
    # NOTE: `row_stack` is omitted because it is deprecated
    "column_stack", "dstack", "array_split", "split", "hsplit", "vsplit", "dsplit",
    "apply_over_axes", "expand_dims", "apply_along_axis", "kron", "tile",
    "take_along_axis", "put_along_axis",
    # lib._type_check_impl.__all__
    "iscomplexobj", "isrealobj", "imag", "iscomplex", "isreal", "nan_to_num", "real",
    "real_if_close", "typename", "mintypecode", "common_type",
    # lib._arraysetops_impl.__all__
    # NOTE: `in1d` is omitted because it is deprecated
    "ediff1d", "intersect1d", "isin", "setdiff1d", "setxor1d", "union1d", "unique",
    "unique_all", "unique_counts", "unique_inverse", "unique_values",
    # lib._ufunclike_impl.__all__
    "fix", "isneginf", "isposinf",
    # lib._arraypad_impl.__all__
    "pad",
    # lib._utils_impl.__all__
    "get_include", "info", "show_runtime",
    # lib._stride_tricks_impl.__all__
    "broadcast_to", "broadcast_arrays", "broadcast_shapes",
    # lib._polynomial_impl.__all__
    "poly", "roots", "polyint", "polyder", "polyadd", "polysub", "polymul", "polydiv",
    "polyval", "poly1d", "polyfit",
    # lib._npyio_impl.__all__
    "savetxt", "loadtxt", "genfromtxt", "load", "save", "savez", "savez_compressed",
    "packbits", "unpackbits", "fromregex",
    # lib._index_tricks_impl.__all__
    "ravel_multi_index", "unravel_index", "mgrid", "ogrid", "r_", "c_", "s_",
    "index_exp", "ix_", "ndenumerate", "ndindex", "fill_diagonal", "diag_indices",
    "diag_indices_from",

    # matrixlib.__all__
    "matrix", "bmat", "asmatrix",
]

_AnyStr_contra = TypeVar("_AnyStr_contra", LiteralString, builtins.str, bytes, contravariant=True)

# Protocol for representing file-like-objects accepted
# by `ndarray.tofile` and `fromfile`
@type_check_only
class _IOProtocol(Protocol):
    def flush(self) -> object: ...
    def fileno(self) -> int: ...
    def tell(self) -> SupportsIndex: ...
    def seek(self, offset: int, whence: int, /) -> object: ...

# NOTE: `seek`, `write` and `flush` are technically only required
# for `readwrite`/`write` modes
@type_check_only
class _MemMapIOProtocol(Protocol):
    def flush(self) -> object: ...
    def fileno(self) -> SupportsIndex: ...
    def tell(self) -> int: ...
    def seek(self, offset: int, whence: int, /) -> object: ...
    def write(self, s: bytes, /) -> object: ...
    @property
    def read(self) -> object: ...

@type_check_only
class _SupportsWrite(Protocol[_AnyStr_contra]):
    def write(self, s: _AnyStr_contra, /) -> object: ...

__version__: LiteralString
__array_api_version__: LiteralString
test: PytestTester


def show_config() -> None: ...

_NdArraySubClass = TypeVar("_NdArraySubClass", bound=NDArray[Any])
_NdArraySubClass_co = TypeVar("_NdArraySubClass_co", bound=NDArray[Any], covariant=True)
_DTypeScalar_co = TypeVar("_DTypeScalar_co", covariant=True, bound=generic)
_SCT = TypeVar("_SCT", bound=generic)

_ByteOrderChar: TypeAlias = L[
    "<",  # little-endian
    ">",  # big-endian
    "=",  # native order
    "|",  # ignore
]
# can be anything, is case-insensitive, and only the first character matters
_ByteOrder: TypeAlias = L[
    "S",                # swap the current order (default)
    "<", "L", "little", # little-endian
    ">", "B", "big",    # big endian
    "=", "N", "native", # native order
    "|", "I",           # ignore
]
_DTypeKind: TypeAlias = L[
    "b",  # boolean
    "i",  # signed integer
    "u",  # unsigned integer
    "f",  # floating-point
    "c",  # complex floating-point
    "m",  # timedelta64
    "M",  # datetime64
    "O",  # python object
    "S",  # byte-string (fixed-width)
    "U",  # unicode-string (fixed-width)
    "V",  # void
    "T",  # unicode-string (variable-width)
]
_DTypeChar: TypeAlias = L[
    "?",  # bool
    "b",  # byte
    "B",  # ubyte
    "h",  # short
    "H",  # ushort
    "i",  # intc
    "I",  # uintc
    "l",  # long
    "L",  # ulong
    "q",  # longlong
    "Q",  # ulonglong
    "e",  # half
    "f",  # single
    "d",  # double
    "g",  # longdouble
    "F",  # csingle
    "D",  # cdouble
    "G",  # clongdouble
    "O",  # object
    "S",  # bytes_ (S0)
    "a",  # bytes_ (deprecated)
    "U",  # str_
    "V",  # void
    "M",  # datetime64
    "m",  # timedelta64
    "c",  # bytes_ (S1)
    "T",  # StringDType
]
_DTypeNum: TypeAlias = L[
    0,  # bool
    1,  # byte
    2,  # ubyte
    3,  # short
    4,  # ushort
    5,  # intc
    6,  # uintc
    7,  # long
    8,  # ulong
    9,  # longlong
    10,  # ulonglong
    23,  # half
    11,  # single
    12,  # double
    13,  # longdouble
    14,  # csingle
    15,  # cdouble
    16,  # clongdouble
    17,  # object
    18,  # bytes_
    19,  # str_
    20,  # void
    21,  # datetime64
    22,  # timedelta64
    25,  # no type
    256,  # user-defined
    2056,  # StringDType
]
_DTypeBuiltinKind: TypeAlias = L[
    0,  # structured array type, with fields
    1,  # compiled into numpy
    2,  # user-defined
]

# NOTE: `type[S] | type[T]` is equivalent to `type[S | T]`
_UnsignedIntegerCType: TypeAlias = type[
    ct.c_uint8 | ct.c_uint16 | ct.c_uint32 | ct.c_uint64
    | ct.c_ubyte | ct.c_ushort | ct.c_uint | ct.c_ulong | ct.c_ulonglong
    | ct.c_size_t | ct.c_void_p
]
_SignedIntegerCType: TypeAlias = type[
    ct.c_int8 | ct.c_int16 | ct.c_int32 | ct.c_int64
    | ct.c_byte | ct.c_short | ct.c_int | ct.c_long | ct.c_longlong
    | ct.c_ssize_t
]
_FloatingCType: TypeAlias = type[ct.c_float | ct.c_double | ct.c_longdouble]
_IntegerCType: TypeAlias = _UnsignedIntegerCType | _SignedIntegerCType
_NumberCType: TypeAlias = _IntegerCType | _IntegerCType
_GenericCType: TypeAlias = _NumberCType | type[ct.c_bool | ct.c_char | ct.py_object[Any]]

# some commonly used builtin types that are known to result in a
# `dtype[object_]`, when their *type* is passed to the `dtype` constructor
# NOTE: `builtins.object` should not be included here
_BuiltinObjectLike: TypeAlias = (
    slice | Decimal | Fraction | UUID
    | dt.date | dt.time | dt.timedelta | dt.tzinfo
    | tuple[Any, ...] | list[Any] | set[Any] | frozenset[Any] | dict[Any, Any]
)  # fmt: skip

@final
class dtype(Generic[_DTypeScalar_co]):
    names: None | tuple[builtins.str, ...]
    def __hash__(self) -> int: ...

    # `None` results in the default dtype
    @overload
    def __new__(
        cls,
        dtype: None | type[float64],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...
    ) -> dtype[float64]: ...

    # Overload for `dtype` instances, scalar types, and instances that have a
    # `dtype: dtype[_SCT]` attribute
    @overload
    def __new__(
        cls,
        dtype: _DTypeLike[_SCT],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[_SCT]: ...

    # Builtin types
    #
    # NOTE: Typecheckers act as if `bool <: int <: float <: complex <: object`,
    # even though at runtime `int`, `float`, and `complex` aren't subtypes..
    # This makes it impossible to express e.g. "a float that isn't an int",
    # since type checkers treat `_: float` like `_: float | int`.
    #
    # For more details, see:
    # - https://github.com/numpy/numpy/issues/27032#issuecomment-2278958251
    # - https://typing.readthedocs.io/en/latest/spec/special-types.html#special-cases-for-float-and-complex
    @overload
    def __new__(
        cls,
        dtype: type[builtins.bool | np.bool],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[np.bool]: ...
    # NOTE: `_: type[int]` also accepts `type[int | bool]`
    @overload
    def __new__(
        cls,
        dtype: type[int | int_ | np.bool],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[int_ | np.bool]: ...
    # NOTE: `_: type[float]` also accepts `type[float | int | bool]`
    # NOTE: `float64` inherits from `float` at runtime; but this isn't
    # reflected in these stubs. So an explicit `float64` is required here.
    @overload
    def __new__(
        cls,
        dtype: None | type[float | float64 | int_ | np.bool],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[float64 | int_ | np.bool]: ...
    # NOTE: `_: type[complex]` also accepts `type[complex | float | int | bool]`
    @overload
    def __new__(
        cls,
        dtype: type[complex | complex128 | float64 | int_ | np.bool],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[complex128 | float64 | int_ | np.bool]: ...
    @overload
    def __new__(
        cls,
        dtype: type[bytes],  # also includes `type[bytes_]`
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[bytes_]: ...
    @overload
    def __new__(
        cls,
        dtype: type[str],  # also includes `type[str_]`
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[str_]: ...
    # NOTE: These `memoryview` overloads assume PEP 688, which requires mypy to
    # be run with the (undocumented) `--disable-memoryview-promotion` flag,
    # This will be the default in a future mypy release, see:
    # https://github.com/python/mypy/issues/15313
    # Pyright / Pylance requires setting `disableBytesTypePromotions=true`,
    # which is the default in strict mode
    @overload
    def __new__(
        cls,
        dtype: type[memoryview | void],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[void]: ...
    # NOTE: `_: type[object]` would also accept e.g. `type[object | complex]`,
    # and is therefore not included here
    @overload
    def __new__(
        cls,
        dtype: type[_BuiltinObjectLike | object_],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[object_]: ...

    # Unions of builtins.
    @overload
    def __new__(
        cls,
        dtype: type[bytes | str],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[character]: ...
    @overload
    def __new__(
        cls,
        dtype: type[bytes | str | memoryview],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[flexible]: ...
    @overload
    def __new__(
        cls,
        dtype: type[complex | bytes | str | memoryview | _BuiltinObjectLike],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[str, Any] = ...,
    ) -> dtype[np.bool | int_ | float64 | complex128 | flexible | object_]: ...

    # `unsignedinteger` string-based representations and ctypes
    @overload
    def __new__(cls, dtype: _UInt8Codes | type[ct.c_uint8], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uint8]: ...
    @overload
    def __new__(cls, dtype: _UInt16Codes | type[ct.c_uint16], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uint16]: ...
    @overload
    def __new__(cls, dtype: _UInt32Codes | type[ct.c_uint32], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uint32]: ...
    @overload
    def __new__(cls, dtype: _UInt64Codes | type[ct.c_uint64], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uint64]: ...
    @overload
    def __new__(cls, dtype: _UByteCodes | type[ct.c_ubyte], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[ubyte]: ...
    @overload
    def __new__(cls, dtype: _UShortCodes | type[ct.c_ushort], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[ushort]: ...
    @overload
    def __new__(cls, dtype: _UIntCCodes | type[ct.c_uint], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uintc]: ...
    # NOTE: We're assuming here that `uint_ptr_t == size_t`,
    # an assumption that does not hold in rare cases (same for `ssize_t`)
    @overload
    def __new__(cls, dtype: _UIntPCodes | type[ct.c_void_p] | type[ct.c_size_t], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[uintp]: ...
    @overload
    def __new__(cls, dtype: _ULongCodes | type[ct.c_ulong], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[ulong]: ...
    @overload
    def __new__(cls, dtype: _ULongLongCodes | type[ct.c_ulonglong], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[ulonglong]: ...

    # `signedinteger` string-based representations and ctypes
    @overload
    def __new__(cls, dtype: _Int8Codes | type[ct.c_int8], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[int8]: ...
    @overload
    def __new__(cls, dtype: _Int16Codes | type[ct.c_int16], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[int16]: ...
    @overload
    def __new__(cls, dtype: _Int32Codes | type[ct.c_int32], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[int32]: ...
    @overload
    def __new__(cls, dtype: _Int64Codes | type[ct.c_int64], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[int64]: ...
    @overload
    def __new__(cls, dtype: _ByteCodes | type[ct.c_byte], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[byte]: ...
    @overload
    def __new__(cls, dtype: _ShortCodes | type[ct.c_short], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[short]: ...
    @overload
    def __new__(cls, dtype: _IntCCodes | type[ct.c_int], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[intc]: ...
    @overload
    def __new__(cls, dtype: _IntPCodes | type[ct.c_ssize_t], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[intp]: ...
    @overload
    def __new__(cls, dtype: _LongCodes | type[ct.c_long], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[long]: ...
    @overload
    def __new__(cls, dtype: _LongLongCodes | type[ct.c_longlong], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[longlong]: ...

    # `floating` string-based representations and ctypes
    @overload
    def __new__(cls, dtype: _Float16Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[float16]: ...
    @overload
    def __new__(cls, dtype: _Float32Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[float32]: ...
    @overload
    def __new__(cls, dtype: _Float64Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[float64]: ...
    @overload
    def __new__(cls, dtype: _HalfCodes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[half]: ...
    @overload
    def __new__(cls, dtype: _SingleCodes | type[ct.c_float], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[single]: ...
    @overload
    def __new__(cls, dtype: _DoubleCodes | type[ct.c_double], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[double]: ...
    @overload
    def __new__(cls, dtype: _LongDoubleCodes | type[ct.c_longdouble], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[longdouble]: ...

    # `complexfloating` string-based representations
    @overload
    def __new__(cls, dtype: _Complex64Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[complex64]: ...
    @overload
    def __new__(cls, dtype: _Complex128Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[complex128]: ...
    @overload
    def __new__(cls, dtype: _CSingleCodes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[csingle]: ...
    @overload
    def __new__(cls, dtype: _CDoubleCodes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[cdouble]: ...
    @overload
    def __new__(cls, dtype: _CLongDoubleCodes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[clongdouble]: ...

    # Miscellaneous string-based representations and ctypes
    @overload
    def __new__(cls, dtype: _BoolCodes | type[ct.c_bool], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[np.bool]: ...
    @overload
    def __new__(cls, dtype: _TD64Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[timedelta64]: ...
    @overload
    def __new__(cls, dtype: _DT64Codes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[datetime64]: ...
    @overload
    def __new__(cls, dtype: _StrCodes, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[str_]: ...
    @overload
    def __new__(cls, dtype: _BytesCodes | type[ct.c_char], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[bytes_]: ...
    @overload
    def __new__(cls, dtype: _VoidCodes | _VoidDTypeLike, align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[void]: ...
    @overload
    def __new__(cls, dtype: _ObjectCodes | type[ct.py_object[Any]], align: builtins.bool = ..., copy: builtins.bool = ..., metadata: dict[builtins.str, Any] = ...) -> dtype[object_]: ...

    # `StringDType` requires special treatment because it has no scalar type
    @overload
    def __new__(
        cls,
        dtype: dtypes.StringDType | _StringCodes,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...
    ) -> dtypes.StringDType: ...

    # Combined char-codes and ctypes, analogous to the scalar-type hierarchy
    @overload
    def __new__(
        cls,
        dtype: _UnsignedIntegerCodes | _UnsignedIntegerCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[unsignedinteger[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _SignedIntegerCodes | _SignedIntegerCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[signedinteger[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _IntegerCodes | _IntegerCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[integer[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _FloatingCodes | _FloatingCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[floating[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _ComplexFloatingCodes,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[complexfloating[Any, Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _InexactCodes | _FloatingCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[inexact[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _NumberCodes | _NumberCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[number[Any]]: ...
    @overload
    def __new__(
        cls,
        dtype: _CharacterCodes | type[ct.c_char],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[character]: ...
    @overload
    def __new__(
        cls,
        dtype: _FlexibleCodes | type[ct.c_char],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[flexible]: ...
    @overload
    def __new__(
        cls,
        dtype: _GenericCodes | _GenericCType,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[generic]: ...

    # Handle strings that can't be expressed as literals; i.e. "S1", "S2", ...
    @overload
    def __new__(
        cls,
        dtype: builtins.str,
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[Any]: ...

    # Catch-all overload for object-likes
    # NOTE: `object_ | Any` is *not* equivalent to `Any` -- it describes some
    # (static) type `T` s.t. `object_ <: T <: builtins.object` (`<:` denotes
    # the subtyping relation, the (gradual) typing analogue of `issubclass()`).
    # https://typing.readthedocs.io/en/latest/spec/concepts.html#union-types
    @overload
    def __new__(
        cls,
        dtype: type[object],
        align: builtins.bool = ...,
        copy: builtins.bool = ...,
        metadata: dict[builtins.str, Any] = ...,
    ) -> dtype[object_ | Any]: ...

    def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

    @overload
    def __getitem__(self: dtype[void], key: list[builtins.str], /) -> dtype[void]: ...
    @overload
    def __getitem__(self: dtype[void], key: builtins.str | SupportsIndex, /) -> dtype[Any]: ...

    # NOTE: In the future 1-based multiplications will also yield `flexible` dtypes
    @overload
    def __mul__(self: _DType, value: L[1], /) -> _DType: ...
    @overload
    def __mul__(self: _FlexDType, value: SupportsIndex, /) -> _FlexDType: ...
    @overload
    def __mul__(self, value: SupportsIndex, /) -> dtype[void]: ...

    # NOTE: `__rmul__` seems to be broken when used in combination with
    # literals as of mypy 0.902. Set the return-type to `dtype[Any]` for
    # now for non-flexible dtypes.
    @overload
    def __rmul__(self: _FlexDType, value: SupportsIndex, /) -> _FlexDType: ...
    @overload
    def __rmul__(self, value: SupportsIndex, /) -> dtype[Any]: ...

    def __gt__(self, other: DTypeLike, /) -> builtins.bool: ...
    def __ge__(self, other: DTypeLike, /) -> builtins.bool: ...
    def __lt__(self, other: DTypeLike, /) -> builtins.bool: ...
    def __le__(self, other: DTypeLike, /) -> builtins.bool: ...

    # Explicitly defined `__eq__` and `__ne__` to get around mypy's
    # `strict_equality` option; even though their signatures are
    # identical to their `object`-based counterpart
    def __eq__(self, other: Any, /) -> builtins.bool: ...
    def __ne__(self, other: Any, /) -> builtins.bool: ...

    @property
    def alignment(self) -> int: ...
    @property
    def base(self) -> dtype[Any]: ...
    @property
    def byteorder(self) -> _ByteOrderChar: ...
    @property
    def char(self) -> _DTypeChar: ...
    @property
    def descr(self) -> list[tuple[LiteralString, LiteralString] | tuple[LiteralString, LiteralString, _Shape]]: ...
    @property
    def fields(self,) -> None | MappingProxyType[LiteralString, tuple[dtype[Any], int] | tuple[dtype[Any], int, Any]]: ...
    @property
    def flags(self) -> int: ...
    @property
    def hasobject(self) -> builtins.bool: ...
    @property
    def isbuiltin(self) -> _DTypeBuiltinKind: ...
    @property
    def isnative(self) -> builtins.bool: ...
    @property
    def isalignedstruct(self) -> builtins.bool: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def kind(self) -> _DTypeKind: ...
    @property
    def metadata(self) -> None | MappingProxyType[builtins.str, Any]: ...
    @property
    def name(self) -> LiteralString: ...
    @property
    def num(self) -> _DTypeNum: ...
    @property
    def shape(self) -> tuple[()] | _Shape: ...
    @property
    def ndim(self) -> int: ...
    @property
    def subdtype(self) -> None | tuple[dtype[Any], _Shape]: ...
    def newbyteorder(self, new_order: _ByteOrder = ..., /) -> Self: ...
    @property
    def str(self) -> LiteralString: ...
    @property
    def type(self) -> type[_DTypeScalar_co]: ...

_ArrayLikeInt: TypeAlias = (
    int
    | integer[Any]
    | Sequence[int | integer[Any]]
    | Sequence[Sequence[Any]]  # TODO: wait for support for recursive types
    | NDArray[Any]
)

_FlatShapeType = TypeVar("_FlatShapeType", bound=tuple[int])

@final
class flatiter(Generic[_NdArraySubClass_co]):
    __hash__: ClassVar[None]
    @property
    def base(self) -> _NdArraySubClass_co: ...
    @property
    def coords(self) -> _Shape: ...
    @property
    def index(self) -> int: ...
    def copy(self) -> _NdArraySubClass_co: ...
    def __iter__(self) -> Self: ...
    def __next__(self: flatiter[NDArray[_ScalarType]]) -> _ScalarType: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(
        self: flatiter[NDArray[_ScalarType]],
        key: int | integer[Any] | tuple[int | integer[Any]],
    ) -> _ScalarType: ...
    @overload
    def __getitem__(
        self,
        key: _ArrayLikeInt | slice | EllipsisType | tuple[_ArrayLikeInt | slice | EllipsisType],
    ) -> _NdArraySubClass_co: ...
    # TODO: `__setitem__` operates via `unsafe` casting rules, and can
    # thus accept any type accepted by the relevant underlying `np.generic`
    # constructor.
    # This means that `value` must in reality be a supertype of `npt.ArrayLike`.
    def __setitem__(
        self,
        key: _ArrayLikeInt | slice | EllipsisType | tuple[_ArrayLikeInt | slice | EllipsisType],
        value: Any,
    ) -> None: ...
    @overload
    def __array__(self: flatiter[ndarray[_FlatShapeType, _DType]], dtype: None = ..., /) -> ndarray[_FlatShapeType, _DType]: ...
    @overload
    def __array__(self: flatiter[ndarray[_FlatShapeType, Any]], dtype: _DType, /) -> ndarray[_FlatShapeType, _DType]: ...
    @overload
    def __array__(self: flatiter[ndarray[_Shape, _DType]], dtype: None = ..., /) -> ndarray[_Shape, _DType]: ...
    @overload
    def __array__(self, dtype: _DType, /) -> ndarray[_Shape, _DType]: ...

_OrderKACF: TypeAlias = L[None, "K", "A", "C", "F"]
_OrderACF: TypeAlias = L[None, "A", "C", "F"]
_OrderCF: TypeAlias = L[None, "C", "F"]

_ModeKind: TypeAlias = L["raise", "wrap", "clip"]
_PartitionKind: TypeAlias = L["introselect"]
# in practice, only the first case-insensitive character is considered (so e.g.
# "QuantumSort3000" will be interpreted as quicksort).
_SortKind: TypeAlias = L[
    "Q", "quick", "quicksort",
    "M", "merge", "mergesort",
    "H", "heap", "heapsort",
    "S", "stable", "stablesort",
]
_SortSide: TypeAlias = L["left", "right"]

@type_check_only
class _ArrayOrScalarCommon:
    @property
    def T(self) -> Self: ...
    @property
    def mT(self) -> Self: ...
    @property
    def data(self) -> memoryview: ...
    @property
    def flags(self) -> flagsobj: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def nbytes(self) -> int: ...
    @property
    def device(self) -> L["cpu"]: ...
    def __bool__(self) -> builtins.bool: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: None | dict[int, Any], /) -> Self: ...

    # TODO: How to deal with the non-commutative nature of `==` and `!=`?
    # xref numpy/numpy#17368
    def __eq__(self, other: Any, /) -> Any: ...
    def __ne__(self, other: Any, /) -> Any: ...
    def copy(self, order: _OrderKACF = ...) -> Self: ...
    def dump(self, file: str | bytes | os.PathLike[str] | os.PathLike[bytes] | _SupportsWrite[bytes]) -> None: ...
    def dumps(self) -> bytes: ...
    def tobytes(self, order: _OrderKACF = ...) -> bytes: ...
    # NOTE: `tostring()` is deprecated and therefore excluded
    # def tostring(self, order=...): ...
    def tofile(
        self,
        fid: str | bytes | os.PathLike[str] | os.PathLike[bytes] | _IOProtocol,
        sep: str = ...,
        format: str = ...,
    ) -> None: ...
    # generics and 0d arrays return builtin scalars
    def tolist(self) -> Any: ...
    def to_device(self, device: L["cpu"], /, *, stream: None | int | Any = ...) -> Self: ...

    @property
    def __array_interface__(self) -> dict[str, Any]: ...
    @property
    def __array_priority__(self) -> float: ...
    @property
    def __array_struct__(self) -> Any: ...  # builtins.PyCapsule
    def __array_namespace__(self, *, api_version: None | _ArrayAPIVersion = ...) -> Any: ...
    def __setstate__(self, state: tuple[
        SupportsIndex,  # version
        _ShapeLike,  # Shape
        _DType_co,  # DType
        np.bool,  # F-continuous
        bytes | list[Any],  # Data
    ], /) -> None: ...
    # an `np.bool` is returned when `keepdims=True` and `self` is a 0d array

    @overload
    def argmax(
        self,
        axis: None = ...,
        out: None = ...,
        *,
        keepdims: L[False] = ...,
    ) -> intp: ...
    @overload
    def argmax(
        self,
        axis: SupportsIndex = ...,
        out: None = ...,
        *,
        keepdims: builtins.bool = ...,
    ) -> Any: ...
    @overload
    def argmax(
        self,
        axis: None | SupportsIndex = ...,
        out: _NdArraySubClass = ...,
        *,
        keepdims: builtins.bool = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def argmin(
        self,
        axis: None = ...,
        out: None = ...,
        *,
        keepdims: L[False] = ...,
    ) -> intp: ...
    @overload
    def argmin(
        self,
        axis: SupportsIndex = ...,
        out: None = ...,
        *,
        keepdims: builtins.bool = ...,
    ) -> Any: ...
    @overload
    def argmin(
        self,
        axis: None | SupportsIndex = ...,
        out: _NdArraySubClass = ...,
        *,
        keepdims: builtins.bool = ...,
    ) -> _NdArraySubClass: ...

    def argsort(
        self,
        axis: None | SupportsIndex = ...,
        kind: None | _SortKind = ...,
        order: None | str | Sequence[str] = ...,
        *,
        stable: None | bool = ...,
    ) -> NDArray[Any]: ...

    @overload
    def choose(
        self,
        choices: ArrayLike,
        out: None = ...,
        mode: _ModeKind = ...,
    ) -> NDArray[Any]: ...
    @overload
    def choose(
        self,
        choices: ArrayLike,
        out: _NdArraySubClass = ...,
        mode: _ModeKind = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def clip(
        self,
        min: ArrayLike = ...,
        max: None | ArrayLike = ...,
        out: None = ...,
        **kwargs: Any,
    ) -> NDArray[Any]: ...
    @overload
    def clip(
        self,
        min: None = ...,
        max: ArrayLike = ...,
        out: None = ...,
        **kwargs: Any,
    ) -> NDArray[Any]: ...
    @overload
    def clip(
        self,
        min: ArrayLike = ...,
        max: None | ArrayLike = ...,
        out: _NdArraySubClass = ...,
        **kwargs: Any,
    ) -> _NdArraySubClass: ...
    @overload
    def clip(
        self,
        min: None = ...,
        max: ArrayLike = ...,
        out: _NdArraySubClass = ...,
        **kwargs: Any,
    ) -> _NdArraySubClass: ...

    @overload
    def compress(
        self,
        a: ArrayLike,
        axis: None | SupportsIndex = ...,
        out: None = ...,
    ) -> NDArray[Any]: ...
    @overload
    def compress(
        self,
        a: ArrayLike,
        axis: None | SupportsIndex = ...,
        out: _NdArraySubClass = ...,
    ) -> _NdArraySubClass: ...

    def conj(self) -> Self: ...
    def conjugate(self) -> Self: ...

    @overload
    def cumprod(
        self,
        axis: None | SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
    ) -> NDArray[Any]: ...
    @overload
    def cumprod(
        self,
        axis: None | SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def cumsum(
        self,
        axis: None | SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
    ) -> NDArray[Any]: ...
    @overload
    def cumsum(
        self,
        axis: None | SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def max(
        self,
        axis: None | _ShapeLike = ...,
        out: None = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def max(
        self,
        axis: None | _ShapeLike = ...,
        out: _NdArraySubClass = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def mean(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def mean(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def min(
        self,
        axis: None | _ShapeLike = ...,
        out: None = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def min(
        self,
        axis: None | _ShapeLike = ...,
        out: _NdArraySubClass = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def prod(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def prod(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def round(
        self,
        decimals: SupportsIndex = ...,
        out: None = ...,
    ) -> Self: ...
    @overload
    def round(
        self,
        decimals: SupportsIndex = ...,
        out: _NdArraySubClass = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def std(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
        ddof: float = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def std(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
        ddof: float = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def sum(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def sum(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
        keepdims: builtins.bool = ...,
        initial: _NumberLike_co = ...,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def var(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
        ddof: float = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> Any: ...
    @overload
    def var(
        self,
        axis: None | _ShapeLike = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
        ddof: float = ...,
        keepdims: builtins.bool = ...,
        *,
        where: _ArrayLikeBool_co = ...,
    ) -> _NdArraySubClass: ...

_DType = TypeVar("_DType", bound=dtype[Any])
_DType_co = TypeVar("_DType_co", covariant=True, bound=dtype[Any])
_FlexDType = TypeVar("_FlexDType", bound=dtype[flexible])

_Shape1D: TypeAlias = tuple[int]
_Shape2D: TypeAlias = tuple[int, int]

_ShapeType_co = TypeVar("_ShapeType_co", covariant=True, bound=_Shape)
_ShapeType2 = TypeVar("_ShapeType2", bound=_Shape)
_Shape2DType_co = TypeVar("_Shape2DType_co", covariant=True, bound=_Shape2D)
_NumberType = TypeVar("_NumberType", bound=number[Any])


if sys.version_info >= (3, 12):
    from collections.abc import Buffer as _SupportsBuffer
else:
    _SupportsBuffer: TypeAlias = (
        bytes
        | bytearray
        | memoryview
        | _array.array[Any]
        | mmap.mmap
        | NDArray[Any]
        | generic
    )

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_2Tuple: TypeAlias = tuple[_T, _T]
_CastingKind: TypeAlias = L["no", "equiv", "safe", "same_kind", "unsafe"]

_ArrayUInt_co: TypeAlias = NDArray[np.bool | unsignedinteger[Any]]
_ArrayInt_co: TypeAlias = NDArray[np.bool | integer[Any]]
_ArrayFloat_co: TypeAlias = NDArray[np.bool | integer[Any] | floating[Any]]
_ArrayComplex_co: TypeAlias = NDArray[np.bool | integer[Any] | floating[Any] | complexfloating[Any, Any]]
_ArrayNumber_co: TypeAlias = NDArray[np.bool | number[Any]]
_ArrayTD64_co: TypeAlias = NDArray[np.bool | integer[Any] | timedelta64]

# Introduce an alias for `dtype` to avoid naming conflicts.
_dtype: TypeAlias = dtype[_ScalarType]

if sys.version_info >= (3, 13):
    from types import CapsuleType as _PyCapsule
else:
    _PyCapsule: TypeAlias = Any

_ArrayAPIVersion: TypeAlias = L["2021.12", "2022.12", "2023.12"]

@type_check_only
class _SupportsItem(Protocol[_T_co]):
    def item(self, args: Any, /) -> _T_co: ...

@type_check_only
class _SupportsReal(Protocol[_T_co]):
    @property
    def real(self) -> _T_co: ...

@type_check_only
class _SupportsImag(Protocol[_T_co]):
    @property
    def imag(self) -> _T_co: ...

class ndarray(_ArrayOrScalarCommon, Generic[_ShapeType_co, _DType_co]):
    __hash__: ClassVar[None]
    @property
    def base(self) -> None | NDArray[Any]: ...
    @property
    def ndim(self) -> int: ...
    @property
    def size(self) -> int: ...
    @property
    def real(
        self: ndarray[_ShapeType_co, dtype[_SupportsReal[_ScalarType]]],  # type: ignore[type-var]
    ) -> ndarray[_ShapeType_co, _dtype[_ScalarType]]: ...
    @real.setter
    def real(self, value: ArrayLike) -> None: ...
    @property
    def imag(
        self: ndarray[_ShapeType_co, dtype[_SupportsImag[_ScalarType]]],  # type: ignore[type-var]
    ) -> ndarray[_ShapeType_co, _dtype[_ScalarType]]: ...
    @imag.setter
    def imag(self, value: ArrayLike) -> None: ...
    def __new__(
        cls,
        shape: _ShapeLike,
        dtype: DTypeLike = ...,
        buffer: None | _SupportsBuffer = ...,
        offset: SupportsIndex = ...,
        strides: None | _ShapeLike = ...,
        order: _OrderKACF = ...,
    ) -> Self: ...

    if sys.version_info >= (3, 12):
        def __buffer__(self, flags: int, /) -> memoryview: ...

    def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

    @overload
    def __array__(
        self, dtype: None = ..., /, *, copy: None | bool = ...
    ) -> ndarray[_ShapeType_co, _DType_co]: ...
    @overload
    def __array__(
        self, dtype: _DType, /, *, copy: None | bool = ...
    ) -> ndarray[_ShapeType_co, _DType]: ...

    def __array_ufunc__(
        self,
        ufunc: ufunc,
        method: L["__call__", "reduce", "reduceat", "accumulate", "outer", "at"],
        *inputs: Any,
        **kwargs: Any,
    ) -> Any: ...

    def __array_function__(
        self,
        func: Callable[..., Any],
        types: Iterable[type],
        args: Iterable[Any],
        kwargs: Mapping[str, Any],
    ) -> Any: ...

    # NOTE: In practice any object is accepted by `obj`, but as `__array_finalize__`
    # is a pseudo-abstract method the type has been narrowed down in order to
    # grant subclasses a bit more flexibility
    def __array_finalize__(self, obj: None | NDArray[Any], /) -> None: ...

    def __array_wrap__(
        self,
        array: ndarray[_ShapeType2, _DType],
        context: None | tuple[ufunc, tuple[Any, ...], int] = ...,
        return_scalar: builtins.bool = ...,
        /,
    ) -> ndarray[_ShapeType2, _DType]: ...

    @overload
    def __getitem__(self, key: (
        NDArray[integer[Any]]
        | NDArray[np.bool]
        | tuple[NDArray[integer[Any]] | NDArray[np.bool], ...]
    )) -> ndarray[_Shape, _DType_co]: ...
    @overload
    def __getitem__(self, key: SupportsIndex | tuple[SupportsIndex, ...]) -> Any: ...
    @overload
    def __getitem__(self, key: (
        None
        | slice
        | EllipsisType
        | SupportsIndex
        | _ArrayLikeInt_co
        | tuple[None | slice | EllipsisType | _ArrayLikeInt_co | SupportsIndex, ...]
    )) -> ndarray[_Shape, _DType_co]: ...
    @overload
    def __getitem__(self: NDArray[void], key: str) -> NDArray[Any]: ...
    @overload
    def __getitem__(self: NDArray[void], key: list[str]) -> ndarray[_ShapeType_co, _dtype[void]]: ...

    @property
    def ctypes(self) -> _ctypes[int]: ...
    @property
    def shape(self) -> _ShapeType_co: ...
    @shape.setter
    def shape(self, value: _ShapeLike) -> None: ...
    @property
    def strides(self) -> _Shape: ...
    @strides.setter
    def strides(self, value: _ShapeLike) -> None: ...
    def byteswap(self, inplace: builtins.bool = ...) -> Self: ...
    def fill(self, value: Any) -> None: ...
    @property
    def flat(self) -> flatiter[Self]: ...

    # Use the same output type as that of the underlying `generic`
    @overload
    def item(
        self: ndarray[Any, _dtype[_SupportsItem[_T]]],  # type: ignore[type-var]
        *args: SupportsIndex,
    ) -> _T: ...
    @overload
    def item(
        self: ndarray[Any, _dtype[_SupportsItem[_T]]],  # type: ignore[type-var]
        args: tuple[SupportsIndex, ...],
        /,
    ) -> _T: ...

    @overload
    def resize(self, new_shape: _ShapeLike, /, *, refcheck: builtins.bool = ...) -> None: ...
    @overload
    def resize(self, *new_shape: SupportsIndex, refcheck: builtins.bool = ...) -> None: ...

    def setflags(
        self, write: builtins.bool = ..., align: builtins.bool = ..., uic: builtins.bool = ...
    ) -> None: ...

    def squeeze(
        self,
        axis: None | SupportsIndex | tuple[SupportsIndex, ...] = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    def swapaxes(
        self,
        axis1: SupportsIndex,
        axis2: SupportsIndex,
    ) -> ndarray[_Shape, _DType_co]: ...

    @overload
    def transpose(self, axes: None | _ShapeLike, /) -> Self: ...
    @overload
    def transpose(self, *axes: SupportsIndex) -> Self: ...

    @overload
    def all(
        self,
        axis: None = None,
        out: None = None,
        keepdims: L[False, 0] = False,
        *,
        where: _ArrayLikeBool_co = True
    ) -> np.bool: ...
    @overload
    def all(
        self,
        axis: None | int | tuple[int, ...] = None,
        out: None = None,
        keepdims: SupportsIndex = False,
        *,
        where: _ArrayLikeBool_co = True,
    ) -> np.bool | NDArray[np.bool]: ...
    @overload
    def all(
        self,
        axis: None | int | tuple[int, ...],
        out: _NdArraySubClass,
        keepdims: SupportsIndex = False,
        *,
        where: _ArrayLikeBool_co = True,
    ) -> _NdArraySubClass: ...
    @overload
    def all(
        self,
        axis: None | int | tuple[int, ...] = None,
        *,
        out: _NdArraySubClass,
        keepdims: SupportsIndex = False,
        where: _ArrayLikeBool_co = True,
    ) -> _NdArraySubClass: ...

    @overload
    def any(
        self,
        axis: None = None,
        out: None = None,
        keepdims: L[False, 0] = False,
        *,
        where: _ArrayLikeBool_co = True
    ) -> np.bool: ...
    @overload
    def any(
        self,
        axis: None | int | tuple[int, ...] = None,
        out: None = None,
        keepdims: SupportsIndex = False,
        *,
        where: _ArrayLikeBool_co = True,
    ) -> np.bool | NDArray[np.bool]: ...
    @overload
    def any(
        self,
        axis: None | int | tuple[int, ...],
        out: _NdArraySubClass,
        keepdims: SupportsIndex = False,
        *,
        where: _ArrayLikeBool_co = True,
    ) -> _NdArraySubClass: ...
    @overload
    def any(
        self,
        axis: None | int | tuple[int, ...] = None,
        *,
        out: _NdArraySubClass,
        keepdims: SupportsIndex = False,
        where: _ArrayLikeBool_co = True,
    ) -> _NdArraySubClass: ...

    def argpartition(
        self,
        kth: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
        kind: _PartitionKind = ...,
        order: None | str | Sequence[str] = ...,
    ) -> NDArray[intp]: ...

    def diagonal(
        self,
        offset: SupportsIndex = ...,
        axis1: SupportsIndex = ...,
        axis2: SupportsIndex = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    # 1D + 1D returns a scalar;
    # all other with at least 1 non-0D array return an ndarray.
    @overload
    def dot(self, b: _ScalarLike_co, out: None = ...) -> NDArray[Any]: ...
    @overload
    def dot(self, b: ArrayLike, out: None = ...) -> Any: ...  # type: ignore[misc]
    @overload
    def dot(self, b: ArrayLike, out: _NdArraySubClass) -> _NdArraySubClass: ...

    # `nonzero()` is deprecated for 0d arrays/generics
    def nonzero(self) -> tuple[NDArray[intp], ...]: ...

    def partition(
        self,
        kth: _ArrayLikeInt_co,
        axis: SupportsIndex = ...,
        kind: _PartitionKind = ...,
        order: None | str | Sequence[str] = ...,
    ) -> None: ...

    # `put` is technically available to `generic`,
    # but is pointless as `generic`s are immutable
    def put(
        self,
        ind: _ArrayLikeInt_co,
        v: ArrayLike,
        mode: _ModeKind = ...,
    ) -> None: ...

    @overload
    def searchsorted(  # type: ignore[misc]
        self,  # >= 1D array
        v: _ScalarLike_co,  # 0D array-like
        side: _SortSide = ...,
        sorter: None | _ArrayLikeInt_co = ...,
    ) -> intp: ...
    @overload
    def searchsorted(
        self,  # >= 1D array
        v: ArrayLike,
        side: _SortSide = ...,
        sorter: None | _ArrayLikeInt_co = ...,
    ) -> NDArray[intp]: ...

    def setfield(
        self,
        val: ArrayLike,
        dtype: DTypeLike,
        offset: SupportsIndex = ...,
    ) -> None: ...

    def sort(
        self,
        axis: SupportsIndex = ...,
        kind: None | _SortKind = ...,
        order: None | str | Sequence[str] = ...,
        *,
        stable: None | bool = ...,
    ) -> None: ...

    @overload
    def trace(
        self,  # >= 2D array
        offset: SupportsIndex = ...,
        axis1: SupportsIndex = ...,
        axis2: SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: None = ...,
    ) -> Any: ...
    @overload
    def trace(
        self,  # >= 2D array
        offset: SupportsIndex = ...,
        axis1: SupportsIndex = ...,
        axis2: SupportsIndex = ...,
        dtype: DTypeLike = ...,
        out: _NdArraySubClass = ...,
    ) -> _NdArraySubClass: ...

    @overload
    def take(  # type: ignore[misc]
        self: NDArray[_ScalarType],
        indices: _IntLike_co,
        axis: None | SupportsIndex = ...,
        out: None = ...,
        mode: _ModeKind = ...,
    ) -> _ScalarType: ...
    @overload
    def take(  # type: ignore[misc]
        self,
        indices: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
        out: None = ...,
        mode: _ModeKind = ...,
    ) -> ndarray[_Shape, _DType_co]: ...
    @overload
    def take(
        self,
        indices: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
        out: _NdArraySubClass = ...,
        mode: _ModeKind = ...,
    ) -> _NdArraySubClass: ...

    def repeat(
        self,
        repeats: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    # TODO: use `tuple[int]` as shape type once covariant (#26081)
    def flatten(
        self,
        order: _OrderKACF = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    # TODO: use `tuple[int]` as shape type once covariant (#26081)
    def ravel(
        self,
        order: _OrderKACF = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    @overload
    def reshape(
        self,
        shape: _ShapeLike,
        /,
        *,
        order: _OrderACF = ...,
        copy: None | builtins.bool = ...,
    ) -> ndarray[_Shape, _DType_co]: ...
    @overload
    def reshape(
        self,
        *shape: SupportsIndex,
        order: _OrderACF = ...,
        copy: None | builtins.bool = ...,
    ) -> ndarray[_Shape, _DType_co]: ...

    @overload
    def astype(
        self,
        dtype: _DTypeLike[_ScalarType],
        order: _OrderKACF = ...,
        casting: _CastingKind = ...,
        subok: builtins.bool = ...,
        copy: builtins.bool | _CopyMode = ...,
    ) -> NDArray[_ScalarType]: ...
    @overload
    def astype(
        self,
        dtype: DTypeLike,
        order: _OrderKACF = ...,
        casting: _CastingKind = ...,
        subok: builtins.bool = ...,
        copy: builtins.bool | _CopyMode = ...,
    ) -> NDArray[Any]: ...

    @overload
    def view(self) -> Self: ...
    @overload
    def view(self, type: type[_NdArraySubClass]) -> _NdArraySubClass: ...
    @overload
    def view(self, dtype: _DTypeLike[_ScalarType]) -> NDArray[_ScalarType]: ...
    @overload
    def view(self, dtype: DTypeLike) -> NDArray[Any]: ...
    @overload
    def view(
        self,
        dtype: DTypeLike,
        type: type[_NdArraySubClass],
    ) -> _NdArraySubClass: ...

    @overload
    def getfield(
        self,
        dtype: _DTypeLike[_ScalarType],
        offset: SupportsIndex = ...
    ) -> NDArray[_ScalarType]: ...
    @overload
    def getfield(
        self,
        dtype: DTypeLike,
        offset: SupportsIndex = ...
    ) -> NDArray[Any]: ...

    # Dispatch to the underlying `generic` via protocols
    def __int__(
        self: NDArray[SupportsInt],  # type: ignore[type-var]
    ) -> int: ...

    def __float__(
        self: NDArray[SupportsFloat],  # type: ignore[type-var]
    ) -> float: ...

    def __complex__(
        self: NDArray[SupportsComplex],  # type: ignore[type-var]
    ) -> complex: ...

    def __index__(
        self: NDArray[SupportsIndex],  # type: ignore[type-var]
    ) -> int: ...

    def __len__(self) -> int: ...
    def __setitem__(self, key, value): ...
    def __iter__(self) -> Any: ...
    def __contains__(self, key) -> builtins.bool: ...

    # The last overload is for catching recursive objects whose
    # nesting is too deep.
    # The first overload is for catching `bytes` (as they are a subtype of
    # `Sequence[int]`) and `str`. As `str` is a recursive sequence of
    # strings, it will pass through the final overload otherwise

    @overload
    def __lt__(self: _ArrayNumber_co, other: _ArrayLikeNumber_co, /) -> NDArray[np.bool]: ...
    @overload
    def __lt__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __lt__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __lt__(self: NDArray[object_], other: Any, /) -> NDArray[np.bool]: ...
    @overload
    def __lt__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> NDArray[np.bool]: ...

    @overload
    def __le__(self: _ArrayNumber_co, other: _ArrayLikeNumber_co, /) -> NDArray[np.bool]: ...
    @overload
    def __le__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __le__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __le__(self: NDArray[object_], other: Any, /) -> NDArray[np.bool]: ...
    @overload
    def __le__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> NDArray[np.bool]: ...

    @overload
    def __gt__(self: _ArrayNumber_co, other: _ArrayLikeNumber_co, /) -> NDArray[np.bool]: ...
    @overload
    def __gt__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __gt__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __gt__(self: NDArray[object_], other: Any, /) -> NDArray[np.bool]: ...
    @overload
    def __gt__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> NDArray[np.bool]: ...

    @overload
    def __ge__(self: _ArrayNumber_co, other: _ArrayLikeNumber_co, /) -> NDArray[np.bool]: ...
    @overload
    def __ge__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __ge__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[np.bool]: ...
    @overload
    def __ge__(self: NDArray[object_], other: Any, /) -> NDArray[np.bool]: ...
    @overload
    def __ge__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> NDArray[np.bool]: ...

    # Unary ops
    @overload
    def __abs__(self: NDArray[_UnknownType]) -> NDArray[Any]: ...
    @overload
    def __abs__(self: NDArray[np.bool]) -> NDArray[np.bool]: ...
    @overload
    def __abs__(self: NDArray[complexfloating[_NBit1, _NBit1]]) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __abs__(self: NDArray[_NumberType]) -> NDArray[_NumberType]: ...
    @overload
    def __abs__(self: NDArray[timedelta64]) -> NDArray[timedelta64]: ...
    @overload
    def __abs__(self: NDArray[object_]) -> Any: ...

    @overload
    def __invert__(self: NDArray[_UnknownType]) -> NDArray[Any]: ...
    @overload
    def __invert__(self: NDArray[np.bool]) -> NDArray[np.bool]: ...
    @overload
    def __invert__(self: NDArray[_IntType]) -> NDArray[_IntType]: ...
    @overload
    def __invert__(self: NDArray[object_]) -> Any: ...

    @overload
    def __pos__(self: NDArray[_NumberType]) -> NDArray[_NumberType]: ...
    @overload
    def __pos__(self: NDArray[timedelta64]) -> NDArray[timedelta64]: ...
    @overload
    def __pos__(self: NDArray[object_]) -> Any: ...

    @overload
    def __neg__(self: NDArray[_NumberType]) -> NDArray[_NumberType]: ...
    @overload
    def __neg__(self: NDArray[timedelta64]) -> NDArray[timedelta64]: ...
    @overload
    def __neg__(self: NDArray[object_]) -> Any: ...

    # Binary ops
    @overload
    def __matmul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __matmul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __matmul__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __matmul__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __matmul__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __matmul__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...
    @overload
    def __matmul__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __matmul__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __matmul__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rmatmul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rmatmul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __rmatmul__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmatmul__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmatmul__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmatmul__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...
    @overload
    def __rmatmul__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __rmatmul__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rmatmul__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __mod__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __mod__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __mod__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __mod__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __mod__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __mod__(self: _ArrayTD64_co, other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[timedelta64]: ...
    @overload
    def __mod__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __mod__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rmod__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rmod__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rmod__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmod__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmod__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmod__(self: _ArrayTD64_co, other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[timedelta64]: ...
    @overload
    def __rmod__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rmod__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __divmod__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> _2Tuple[NDArray[Any]]: ...
    @overload
    def __divmod__(self: NDArray[np.bool], other: _ArrayLikeBool_co) -> _2Tuple[NDArray[int8]]: ...  # type: ignore[misc]
    @overload
    def __divmod__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> _2Tuple[NDArray[unsignedinteger[Any]]]: ...  # type: ignore[misc]
    @overload
    def __divmod__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> _2Tuple[NDArray[signedinteger[Any]]]: ...  # type: ignore[misc]
    @overload
    def __divmod__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> _2Tuple[NDArray[floating[Any]]]: ...  # type: ignore[misc]
    @overload
    def __divmod__(self: _ArrayTD64_co, other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> tuple[NDArray[int64], NDArray[timedelta64]]: ...

    @overload
    def __rdivmod__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> _2Tuple[NDArray[Any]]: ...
    @overload
    def __rdivmod__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> _2Tuple[NDArray[int8]]: ...  # type: ignore[misc]
    @overload
    def __rdivmod__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> _2Tuple[NDArray[unsignedinteger[Any]]]: ...  # type: ignore[misc]
    @overload
    def __rdivmod__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> _2Tuple[NDArray[signedinteger[Any]]]: ...  # type: ignore[misc]
    @overload
    def __rdivmod__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> _2Tuple[NDArray[floating[Any]]]: ...  # type: ignore[misc]
    @overload
    def __rdivmod__(self: _ArrayTD64_co, other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> tuple[NDArray[int64], NDArray[timedelta64]]: ...

    @overload
    def __add__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __add__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __add__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __add__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __add__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __add__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __add__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __add__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...  # type: ignore[misc]
    @overload
    def __add__(self: _ArrayTD64_co, other: _ArrayLikeDT64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __add__(self: NDArray[datetime64], other: _ArrayLikeTD64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __add__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __add__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __radd__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __radd__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __radd__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...  # type: ignore[misc]
    @overload
    def __radd__(self: _ArrayTD64_co, other: _ArrayLikeDT64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __radd__(self: NDArray[datetime64], other: _ArrayLikeTD64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __radd__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __radd__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __sub__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __sub__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __sub__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __sub__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __sub__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __sub__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __sub__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __sub__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...  # type: ignore[misc]
    @overload
    def __sub__(self: NDArray[datetime64], other: _ArrayLikeTD64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __sub__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __sub__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __sub__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rsub__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rsub__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __rsub__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __rsub__(self: _ArrayTD64_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: _ArrayTD64_co, other: _ArrayLikeDT64_co, /) -> NDArray[datetime64]: ...  # type: ignore[misc]
    @overload
    def __rsub__(self: NDArray[datetime64], other: _ArrayLikeDT64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __rsub__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rsub__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __mul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __mul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __mul__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __mul__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __mul__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __mul__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __mul__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __mul__(self: _ArrayTD64_co, other: _ArrayLikeFloat_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __mul__(self: _ArrayFloat_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __mul__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __mul__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rmul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rmul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __rmul__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmul__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmul__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rmul__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __rmul__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __rmul__(self: _ArrayTD64_co, other: _ArrayLikeFloat_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __rmul__(self: _ArrayFloat_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __rmul__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rmul__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __floordiv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __floordiv__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __floordiv__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __floordiv__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __floordiv__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __floordiv__(self: NDArray[timedelta64], other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[int64]: ...
    @overload
    def __floordiv__(self: NDArray[timedelta64], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __floordiv__(self: NDArray[timedelta64], other: _ArrayLikeFloat_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __floordiv__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __floordiv__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rfloordiv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rfloordiv__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self: NDArray[timedelta64], other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[int64]: ...
    @overload
    def __rfloordiv__(self: NDArray[np.bool], other: _ArrayLikeTD64_co, /) -> NoReturn: ...
    @overload
    def __rfloordiv__(self: _ArrayFloat_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __rfloordiv__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rfloordiv__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __pow__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __pow__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __pow__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __pow__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __pow__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __pow__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...
    @overload
    def __pow__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __pow__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __pow__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rpow__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rpow__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rpow__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rpow__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rpow__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rpow__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...
    @overload
    def __rpow__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __rpow__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rpow__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __truediv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __truediv__(self: _ArrayInt_co, other: _ArrayInt_co, /) -> NDArray[float64]: ...  # type: ignore[misc]
    @overload
    def __truediv__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __truediv__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __truediv__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __truediv__(self: NDArray[timedelta64], other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[float64]: ...
    @overload
    def __truediv__(self: NDArray[timedelta64], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __truediv__(self: NDArray[timedelta64], other: _ArrayLikeFloat_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __truediv__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __truediv__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rtruediv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rtruediv__(self: _ArrayInt_co, other: _ArrayInt_co, /) -> NDArray[float64]: ...  # type: ignore[misc]
    @overload
    def __rtruediv__(self: _ArrayFloat_co, other: _ArrayLikeFloat_co, /) -> NDArray[floating[Any]]: ...  # type: ignore[misc]
    @overload
    def __rtruediv__(self: _ArrayComplex_co, other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[Any, Any]]: ...  # type: ignore[misc]
    @overload
    def __rtruediv__(self: NDArray[number[Any]], other: _ArrayLikeNumber_co, /) -> NDArray[number[Any]]: ...
    @overload
    def __rtruediv__(self: NDArray[timedelta64], other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[float64]: ...
    @overload
    def __rtruediv__(self: NDArray[np.bool], other: _ArrayLikeTD64_co, /) -> NoReturn: ...
    @overload
    def __rtruediv__(self: _ArrayFloat_co, other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __rtruediv__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rtruediv__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __lshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __lshift__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __lshift__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __lshift__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __lshift__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __lshift__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rlshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rlshift__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rlshift__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rlshift__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __rlshift__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rlshift__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rshift__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rshift__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rshift__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __rshift__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rshift__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rrshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rrshift__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[int8]: ...  # type: ignore[misc]
    @overload
    def __rrshift__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rrshift__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __rrshift__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rrshift__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __and__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __and__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __and__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __and__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __and__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __and__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rand__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rand__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __rand__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rand__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __rand__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rand__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __xor__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __xor__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __xor__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __xor__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __xor__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __xor__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __rxor__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __rxor__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __rxor__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __rxor__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __rxor__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __rxor__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __or__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __or__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __or__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __or__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __or__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __or__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    @overload
    def __ror__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ror__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...  # type: ignore[misc]
    @overload
    def __ror__(self: _ArrayUInt_co, other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[Any]]: ...  # type: ignore[misc]
    @overload
    def __ror__(self: _ArrayInt_co, other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[Any]]: ...
    @overload
    def __ror__(self: NDArray[object_], other: Any, /) -> Any: ...
    @overload
    def __ror__(self: NDArray[Any], other: _ArrayLikeObject_co, /) -> Any: ...

    # `np.generic` does not support inplace operations

    # NOTE: Inplace ops generally use "same_kind" casting w.r.t. to the left
    # operand. An exception to this rule are unsigned integers though, which
    # also accepts a signed integer for the right operand as long it is a 0D
    # object and its value is >= 0
    # NOTE: Due to a mypy bug, overloading on e.g. `self: NDArray[SCT_floating]` won't
    # work, as this will lead to `false negatives` when using these inplace ops.
    @overload
    def __iadd__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __iadd__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __iadd__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __iadd__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __iadd__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __iadd__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __iadd__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __iadd__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __iadd__(self: NDArray[timedelta64], other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __iadd__(self: NDArray[datetime64], other: _ArrayLikeTD64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __iadd__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __isub__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __isub__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __isub__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __isub__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __isub__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __isub__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __isub__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __isub__(self: NDArray[timedelta64], other: _ArrayLikeTD64_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __isub__(self: NDArray[datetime64], other: _ArrayLikeTD64_co, /) -> NDArray[datetime64]: ...
    @overload
    def __isub__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __imul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __imul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __imul__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __imul__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __imul__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __imul__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __imul__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __imul__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __imul__(self: NDArray[timedelta64], other: _ArrayLikeFloat_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __imul__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __itruediv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __itruediv__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __itruediv__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __itruediv__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __itruediv__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __itruediv__(self: NDArray[timedelta64], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __itruediv__(self: NDArray[timedelta64], other: _ArrayLikeInt_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __itruediv__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __ifloordiv__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ifloordiv__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __ifloordiv__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __ifloordiv__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __ifloordiv__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __ifloordiv__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __ifloordiv__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __ifloordiv__(self: NDArray[timedelta64], other: _ArrayLikeBool_co, /) -> NoReturn: ...
    @overload
    def __ifloordiv__(self: NDArray[timedelta64], other: _ArrayLikeInt_co, /) -> NDArray[timedelta64]: ...
    @overload
    def __ifloordiv__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __ipow__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ipow__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __ipow__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __ipow__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __ipow__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __ipow__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __ipow__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __ipow__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __imod__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __imod__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __imod__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __imod__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __imod__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __imod__(self: NDArray[timedelta64], other: _SupportsArray[_dtype[timedelta64]] | _NestedSequence[_SupportsArray[_dtype[timedelta64]]], /) -> NDArray[timedelta64]: ...
    @overload
    def __imod__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __ilshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ilshift__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __ilshift__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __ilshift__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __irshift__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __irshift__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __irshift__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __irshift__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __iand__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __iand__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __iand__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __iand__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __iand__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __ixor__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ixor__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __ixor__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __ixor__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __ixor__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __ior__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __ior__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __ior__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co | _IntLike_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __ior__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __ior__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    @overload
    def __imatmul__(self: NDArray[_UnknownType], other: _ArrayLikeUnknown, /) -> NDArray[Any]: ...
    @overload
    def __imatmul__(self: NDArray[np.bool], other: _ArrayLikeBool_co, /) -> NDArray[np.bool]: ...
    @overload
    def __imatmul__(self: NDArray[unsignedinteger[_NBit1]], other: _ArrayLikeUInt_co, /) -> NDArray[unsignedinteger[_NBit1]]: ...
    @overload
    def __imatmul__(self: NDArray[signedinteger[_NBit1]], other: _ArrayLikeInt_co, /) -> NDArray[signedinteger[_NBit1]]: ...
    @overload
    def __imatmul__(self: NDArray[float64], other: _ArrayLikeFloat_co, /) -> NDArray[float64]: ...
    @overload
    def __imatmul__(self: NDArray[floating[_NBit1]], other: _ArrayLikeFloat_co, /) -> NDArray[floating[_NBit1]]: ...
    @overload
    def __imatmul__(self: NDArray[complex128], other: _ArrayLikeComplex_co, /) -> NDArray[complex128]: ...
    @overload
    def __imatmul__(self: NDArray[complexfloating[_NBit1, _NBit1]], other: _ArrayLikeComplex_co, /) -> NDArray[complexfloating[_NBit1, _NBit1]]: ...
    @overload
    def __imatmul__(self: NDArray[object_], other: Any, /) -> NDArray[object_]: ...

    def __dlpack__(
        self: NDArray[number[Any]],
        *,
        stream: int | Any | None = ...,
        max_version: tuple[int, int] | None = ...,
        dl_device: tuple[int, L[0]] | None = ...,
        copy: bool | None = ...,
    ) -> _PyCapsule: ...

    def __dlpack_device__(self) -> tuple[int, L[0]]: ...

    def bitwise_count(
        self,
        out: None | NDArray[Any] = ...,
        *,
        where: _ArrayLikeBool_co = ...,
        casting: _CastingKind = ...,
        order: _OrderKACF = ...,
        dtype: DTypeLike = ...,
        subok: builtins.bool = ...,
    ) -> NDArray[Any]: ...

    # Keep `dtype` at the bottom to avoid name conflicts with `np.dtype`
    @property
    def dtype(self) -> _DType_co: ...

# NOTE: while `np.generic` is not technically an instance of `ABCMeta`,
# the `@abstractmethod` decorator is herein used to (forcefully) deny
# the creation of `np.generic` instances.
# The `# type: ignore` comments are necessary to silence mypy errors regarding
# the missing `ABCMeta` metaclass.

# See https://github.com/numpy/numpy-stubs/pull/80 for more details.

_ScalarType = TypeVar("_ScalarType", bound=generic)
_NBit = TypeVar("_NBit", bound=NBitBase)
_NBit1 = TypeVar("_NBit1", bound=NBitBase)
_NBit2 = TypeVar("_NBit2", bound=NBitBase, default=_NBit1)

class generic(_ArrayOrScalarCommon):
    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    # TODO: use `tuple[()]` as shape type once covariant (#26081)
    @overload
    def __array__(self, dtype: None = ..., /) -> NDArray[Self]: ...
    @overload
    def __array__(self, dtype: _DType, /) -> ndarray[_Shape, _DType]: ...
    def __hash__(self) -> int: ...
    @property
    def base(self) -> None: ...
    @property
    def ndim(self) -> L[0]: ...
    @property
    def size(self) -> L[1]: ...
    @property
    def shape(self) -> tuple[()]: ...
    @property
    def strides(self) -> tuple[()]: ...
    def byteswap(self, inplace: L[False] = ...) -> Self: ...
    @property
    def flat(self) -> flatiter[NDArray[Self]]: ...

    if sys.version_info >= (3, 12):
        def __buffer__(self, flags: int, /) -> memoryview: ...

    @overload
    def astype(
        self,
        dtype: _DTypeLike[_ScalarType],
        order: _OrderKACF = ...,
        casting: _CastingKind = ...,
        subok: builtins.bool = ...,
        copy: builtins.bool | _CopyMode = ...,
    ) -> _ScalarType: ...
    @overload
    def astype(
        self,
        dtype: DTypeLike,
        order: _OrderKACF = ...,
        casting: _CastingKind = ...,
        subok: builtins.bool = ...,
        copy: builtins.bool | _CopyMode = ...,
    ) -> Any: ...

    # NOTE: `view` will perform a 0D->scalar cast,
    # thus the array `type` is irrelevant to the output type
    @overload
    def view(self, type: type[NDArray[Any]] = ...) -> Self: ...
    @overload
    def view(
        self,
        dtype: _DTypeLike[_ScalarType],
        type: type[NDArray[Any]] = ...,
    ) -> _ScalarType: ...
    @overload
    def view(
        self,
        dtype: DTypeLike,
        type: type[NDArray[Any]] = ...,
    ) -> Any: ...

    @overload
    def getfield(
        self,
        dtype: _DTypeLike[_ScalarType],
        offset: SupportsIndex = ...
    ) -> _ScalarType: ...
    @overload
    def getfield(
        self,
        dtype: DTypeLike,
        offset: SupportsIndex = ...
    ) -> Any: ...

    def item(
        self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /,
    ) -> Any: ...

    @overload
    def take(  # type: ignore[misc]
        self,
        indices: _IntLike_co,
        axis: None | SupportsIndex = ...,
        out: None = ...,
        mode: _ModeKind = ...,
    ) -> Self: ...
    @overload
    def take(  # type: ignore[misc]
        self,
        indices: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
        out: None = ...,
        mode: _ModeKind = ...,
    ) -> NDArray[Self]: ...
    @overload
    def take(
        self,
        indices: _ArrayLikeInt_co,
        axis: None | SupportsIndex = ...,
        out: _NdArraySubClass = ...,
        mode: _ModeKind = ...,
    ) -> _NdArraySubClass: ...

    def repeat(self, repeats: _ArrayLikeInt_co, axis: None | SupportsIndex = ...) -> NDArray[Self]: ...
    def flatten(self, order: _OrderKACF = ...) -> NDArray[Self]: ...
    def ravel(self, order: _OrderKACF = ...) -> NDArray[Self]: ...

    @overload
    def reshape(self, shape: _ShapeLike, /, *, order: _OrderACF = ...) -> NDArray[Self]: ...
    @overload
    def reshape(self, *shape: SupportsIndex, order: _OrderACF = ...) -> NDArray[Self]: ...

    def bitwise_count(
        self,
        out: None | NDArray[Any] = ...,
        *,
        where: _ArrayLikeBool_co = ...,
        casting: _CastingKind = ...,
        order: _OrderKACF = ...,
        dtype: DTypeLike = ...,
        subok: builtins.bool = ...,
    ) -> Any: ...

    def squeeze(self, axis: None | L[0] | tuple[()] = ...) -> Self: ...
    def transpose(self, axes: None | tuple[()] = ..., /) -> Self: ...

    @overload
    def all(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None = None,
        out: None = None,
        keepdims: SupportsIndex = False,
        *,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True
    ) -> np.bool: ...
    @overload
    def all(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None,
        out: ndarray[tuple[()], dtype[_SCT]],
        keepdims: SupportsIndex = False,
        *,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True,
    ) -> _SCT: ...
    @overload
    def all(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None = None,
        *,
        out: ndarray[tuple[()], dtype[_SCT]],
        keepdims: SupportsIndex = False,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True,
    ) -> _SCT: ...

    @overload
    def any(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None = None,
        out: None = None,
        keepdims: SupportsIndex = False,
        *,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True
    ) -> np.bool: ...
    @overload
    def any(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None,
        out: ndarray[tuple[()], dtype[_SCT]],
        keepdims: SupportsIndex = False,
        *,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True,
    ) -> _SCT: ...
    @overload
    def any(
        self,
        /,
        axis: L[0, -1] | tuple[()] | None = None,
        *,
        out: ndarray[tuple[()], dtype[_SCT]],
        keepdims: SupportsIndex = False,
        where: builtins.bool | np.bool | ndarray[tuple[()], dtype[np.bool]] = True,
    ) -> _SCT: ...

    # Keep `dtype` at the bottom to avoid name conflicts with `np.dtype`
    @property
    def dtype(self) -> _dtype[Self]: ...

class number(generic, Generic[_NBit1]):  # type: ignore
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> Self: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...
    def __neg__(self) -> Self: ...
    def __pos__(self) -> Self: ...
    def __abs__(self) -> Self: ...
    # Ensure that objects annotated as `number` support arithmetic operations
    __add__: _NumberOp
    __radd__: _NumberOp
    __sub__: _NumberOp
    __rsub__: _NumberOp
    __mul__: _NumberOp
    __rmul__: _NumberOp
    __floordiv__: _NumberOp
    __rfloordiv__: _NumberOp
    __pow__: _NumberOp
    __rpow__: _NumberOp
    __truediv__: _NumberOp
    __rtruediv__: _NumberOp
    __lt__: _ComparisonOpLT[_NumberLike_co, _ArrayLikeNumber_co]
    __le__: _ComparisonOpLE[_NumberLike_co, _ArrayLikeNumber_co]
    __gt__: _ComparisonOpGT[_NumberLike_co, _ArrayLikeNumber_co]
    __ge__: _ComparisonOpGE[_NumberLike_co, _ArrayLikeNumber_co]

class bool(generic):
    def __init__(self, value: object = ..., /) -> None: ...
    def item(
        self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /,
    ) -> builtins.bool: ...
    def tolist(self) -> builtins.bool: ...
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> Self: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...
    def __abs__(self) -> Self: ...
    __add__: _BoolOp[np.bool]
    __radd__: _BoolOp[np.bool]
    __sub__: _BoolSub
    __rsub__: _BoolSub
    __mul__: _BoolOp[np.bool]
    __rmul__: _BoolOp[np.bool]
    __floordiv__: _BoolOp[int8]
    __rfloordiv__: _BoolOp[int8]
    __pow__: _BoolOp[int8]
    __rpow__: _BoolOp[int8]
    __truediv__: _BoolTrueDiv
    __rtruediv__: _BoolTrueDiv
    def __invert__(self) -> np.bool: ...
    __lshift__: _BoolBitOp[int8]
    __rlshift__: _BoolBitOp[int8]
    __rshift__: _BoolBitOp[int8]
    __rrshift__: _BoolBitOp[int8]
    __and__: _BoolBitOp[np.bool]
    __rand__: _BoolBitOp[np.bool]
    __xor__: _BoolBitOp[np.bool]
    __rxor__: _BoolBitOp[np.bool]
    __or__: _BoolBitOp[np.bool]
    __ror__: _BoolBitOp[np.bool]
    __mod__: _BoolMod
    __rmod__: _BoolMod
    __divmod__: _BoolDivMod
    __rdivmod__: _BoolDivMod
    __lt__: _ComparisonOpLT[_NumberLike_co, _ArrayLikeNumber_co]
    __le__: _ComparisonOpLE[_NumberLike_co, _ArrayLikeNumber_co]
    __gt__: _ComparisonOpGT[_NumberLike_co, _ArrayLikeNumber_co]
    __ge__: _ComparisonOpGE[_NumberLike_co, _ArrayLikeNumber_co]

bool_: TypeAlias = bool

_StringType = TypeVar("_StringType", bound=str | bytes)
_ShapeType = TypeVar("_ShapeType", bound=_Shape)
_ObjectType = TypeVar("_ObjectType", bound=object)

# A sequence-like interface like `collections.abc.Sequence`, but without the
# irrelevant methods.
@type_check_only
class _SimpleSequence(Protocol):
    def __len__(self, /) -> int: ...
    def __getitem__(self, index: int, /) -> Any: ...

# The `object_` constructor returns the passed object, so instances with type
# `object_` cannot exists (at runtime).
@final
class object_(generic):
    @overload
    def __new__(cls, nothing_to_see_here: None = ..., /) -> None: ...
    @overload
    def __new__(cls, stringy: _StringType, /) -> _StringType: ...
    @overload
    def __new__(
        cls,
        array: ndarray[_ShapeType, Any], /,
    ) -> ndarray[_ShapeType, dtype[object_]]: ...
    @overload
    def __new__(cls, sequence: _SimpleSequence, /) -> NDArray[object_]: ...
    @overload
    def __new__(cls, value: _ObjectType, /) -> _ObjectType: ...
    # catch-all
    @overload
    def __new__(cls, value: Any = ..., /) -> object | NDArray[object_]: ...

    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> Self: ...
    # The 3 protocols below may or may not raise,
    # depending on the underlying object
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...

    if sys.version_info >= (3, 12):
        def __release_buffer__(self, buffer: memoryview, /) -> None: ...

# The `datetime64` constructors requires an object with the three attributes below,
# and thus supports datetime duck typing
@type_check_only
class _DatetimeScalar(Protocol):
    @property
    def day(self) -> int: ...
    @property
    def month(self) -> int: ...
    @property
    def year(self) -> int: ...

# TODO: `item`/`tolist` returns either `dt.date`, `dt.datetime` or `int`
# depending on the unit
class datetime64(generic):
    @overload
    def __init__(
        self,
        value: None | datetime64 | _CharLike_co | _DatetimeScalar = ...,
        format: _CharLike_co | tuple[_CharLike_co, _IntLike_co] = ...,
        /,
    ) -> None: ...
    @overload
    def __init__(
        self,
        value: int,
        format: _CharLike_co | tuple[_CharLike_co, _IntLike_co],
        /,
    ) -> None: ...
    def __add__(self, other: _TD64Like_co, /) -> datetime64: ...
    def __radd__(self, other: _TD64Like_co, /) -> datetime64: ...
    @overload
    def __sub__(self, other: datetime64, /) -> timedelta64: ...
    @overload
    def __sub__(self, other: _TD64Like_co, /) -> datetime64: ...
    def __rsub__(self, other: datetime64, /) -> timedelta64: ...
    __lt__: _ComparisonOpLT[datetime64, _ArrayLikeDT64_co]
    __le__: _ComparisonOpLE[datetime64, _ArrayLikeDT64_co]
    __gt__: _ComparisonOpGT[datetime64, _ArrayLikeDT64_co]
    __ge__: _ComparisonOpGE[datetime64, _ArrayLikeDT64_co]

_IntValue: TypeAlias = SupportsInt | _CharLike_co | SupportsIndex
_FloatValue: TypeAlias = None | _CharLike_co | SupportsFloat | SupportsIndex
_ComplexValue: TypeAlias = (
    None
    | _CharLike_co
    | SupportsFloat
    | SupportsComplex
    | SupportsIndex
    | complex  # `complex` is not a subtype of `SupportsComplex`
)

class integer(number[_NBit1]):  # type: ignore
    @property
    def numerator(self) -> Self: ...
    @property
    def denominator(self) -> L[1]: ...
    @overload
    def __round__(self, ndigits: None = ..., /) -> int: ...
    @overload
    def __round__(self, ndigits: SupportsIndex, /) -> Self: ...

    # NOTE: `__index__` is technically defined in the bottom-most
    # sub-classes (`int64`, `uint32`, etc)
    def item(
        self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /,
    ) -> int: ...
    def tolist(self) -> int: ...
    def is_integer(self) -> L[True]: ...
    def bit_count(self) -> int: ...
    def __index__(self) -> int: ...
    __truediv__: _IntTrueDiv[_NBit1]
    __rtruediv__: _IntTrueDiv[_NBit1]
    def __mod__(self, value: _IntLike_co, /) -> integer[Any]: ...
    def __rmod__(self, value: _IntLike_co, /) -> integer[Any]: ...
    def __invert__(self) -> Self: ...
    # Ensure that objects annotated as `integer` support bit-wise operations
    def __lshift__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __rlshift__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __rshift__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __rrshift__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __and__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __rand__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __or__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __ror__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __xor__(self, other: _IntLike_co, /) -> integer[Any]: ...
    def __rxor__(self, other: _IntLike_co, /) -> integer[Any]: ...

class signedinteger(integer[_NBit1]):
    def __init__(self, value: _IntValue = ..., /) -> None: ...
    __add__: _SignedIntOp[_NBit1]
    __radd__: _SignedIntOp[_NBit1]
    __sub__: _SignedIntOp[_NBit1]
    __rsub__: _SignedIntOp[_NBit1]
    __mul__: _SignedIntOp[_NBit1]
    __rmul__: _SignedIntOp[_NBit1]
    __floordiv__: _SignedIntOp[_NBit1]
    __rfloordiv__: _SignedIntOp[_NBit1]
    __pow__: _SignedIntOp[_NBit1]
    __rpow__: _SignedIntOp[_NBit1]
    __lshift__: _SignedIntBitOp[_NBit1]
    __rlshift__: _SignedIntBitOp[_NBit1]
    __rshift__: _SignedIntBitOp[_NBit1]
    __rrshift__: _SignedIntBitOp[_NBit1]
    __and__: _SignedIntBitOp[_NBit1]
    __rand__: _SignedIntBitOp[_NBit1]
    __xor__: _SignedIntBitOp[_NBit1]
    __rxor__: _SignedIntBitOp[_NBit1]
    __or__: _SignedIntBitOp[_NBit1]
    __ror__: _SignedIntBitOp[_NBit1]
    __mod__: _SignedIntMod[_NBit1]
    __rmod__: _SignedIntMod[_NBit1]
    __divmod__: _SignedIntDivMod[_NBit1]
    __rdivmod__: _SignedIntDivMod[_NBit1]

int8 = signedinteger[_8Bit]
int16 = signedinteger[_16Bit]
int32 = signedinteger[_32Bit]
int64 = signedinteger[_64Bit]

byte = signedinteger[_NBitByte]
short = signedinteger[_NBitShort]
intc = signedinteger[_NBitIntC]
intp = signedinteger[_NBitIntP]
int_ = intp
long = signedinteger[_NBitLong]
longlong = signedinteger[_NBitLongLong]

# TODO: `item`/`tolist` returns either `dt.timedelta` or `int`
# depending on the unit
class timedelta64(generic):
    def __init__(
        self,
        value: None | int | _CharLike_co | dt.timedelta | timedelta64 = ...,
        format: _CharLike_co | tuple[_CharLike_co, _IntLike_co] = ...,
        /,
    ) -> None: ...
    @property
    def numerator(self) -> Self: ...
    @property
    def denominator(self) -> L[1]: ...

    # NOTE: Only a limited number of units support conversion
    # to builtin scalar types: `Y`, `M`, `ns`, `ps`, `fs`, `as`
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...
    def __neg__(self) -> Self: ...
    def __pos__(self) -> Self: ...
    def __abs__(self) -> Self: ...
    def __add__(self, other: _TD64Like_co, /) -> timedelta64: ...
    def __radd__(self, other: _TD64Like_co, /) -> timedelta64: ...
    def __sub__(self, other: _TD64Like_co, /) -> timedelta64: ...
    def __rsub__(self, other: _TD64Like_co, /) -> timedelta64: ...
    def __mul__(self, other: _FloatLike_co, /) -> timedelta64: ...
    def __rmul__(self, other: _FloatLike_co, /) -> timedelta64: ...
    __truediv__: _TD64Div[float64]
    __floordiv__: _TD64Div[int64]
    def __rtruediv__(self, other: timedelta64, /) -> float64: ...
    def __rfloordiv__(self, other: timedelta64, /) -> int64: ...
    def __mod__(self, other: timedelta64, /) -> timedelta64: ...
    def __rmod__(self, other: timedelta64, /) -> timedelta64: ...
    def __divmod__(self, other: timedelta64, /) -> tuple[int64, timedelta64]: ...
    def __rdivmod__(self, other: timedelta64, /) -> tuple[int64, timedelta64]: ...
    __lt__: _ComparisonOpLT[_TD64Like_co, _ArrayLikeTD64_co]
    __le__: _ComparisonOpLE[_TD64Like_co, _ArrayLikeTD64_co]
    __gt__: _ComparisonOpGT[_TD64Like_co, _ArrayLikeTD64_co]
    __ge__: _ComparisonOpGE[_TD64Like_co, _ArrayLikeTD64_co]

class unsignedinteger(integer[_NBit1]):
    # NOTE: `uint64 + signedinteger -> float64`
    def __init__(self, value: _IntValue = ..., /) -> None: ...
    __add__: _UnsignedIntOp[_NBit1]
    __radd__: _UnsignedIntOp[_NBit1]
    __sub__: _UnsignedIntOp[_NBit1]
    __rsub__: _UnsignedIntOp[_NBit1]
    __mul__: _UnsignedIntOp[_NBit1]
    __rmul__: _UnsignedIntOp[_NBit1]
    __floordiv__: _UnsignedIntOp[_NBit1]
    __rfloordiv__: _UnsignedIntOp[_NBit1]
    __pow__: _UnsignedIntOp[_NBit1]
    __rpow__: _UnsignedIntOp[_NBit1]
    __lshift__: _UnsignedIntBitOp[_NBit1]
    __rlshift__: _UnsignedIntBitOp[_NBit1]
    __rshift__: _UnsignedIntBitOp[_NBit1]
    __rrshift__: _UnsignedIntBitOp[_NBit1]
    __and__: _UnsignedIntBitOp[_NBit1]
    __rand__: _UnsignedIntBitOp[_NBit1]
    __xor__: _UnsignedIntBitOp[_NBit1]
    __rxor__: _UnsignedIntBitOp[_NBit1]
    __or__: _UnsignedIntBitOp[_NBit1]
    __ror__: _UnsignedIntBitOp[_NBit1]
    __mod__: _UnsignedIntMod[_NBit1]
    __rmod__: _UnsignedIntMod[_NBit1]
    __divmod__: _UnsignedIntDivMod[_NBit1]
    __rdivmod__: _UnsignedIntDivMod[_NBit1]

uint8: TypeAlias = unsignedinteger[_8Bit]
uint16: TypeAlias = unsignedinteger[_16Bit]
uint32: TypeAlias = unsignedinteger[_32Bit]
uint64: TypeAlias = unsignedinteger[_64Bit]

ubyte: TypeAlias = unsignedinteger[_NBitByte]
ushort: TypeAlias = unsignedinteger[_NBitShort]
uintc: TypeAlias = unsignedinteger[_NBitIntC]
uintp: TypeAlias = unsignedinteger[_NBitIntP]
uint: TypeAlias = uintp
ulong: TypeAlias = unsignedinteger[_NBitLong]
ulonglong: TypeAlias = unsignedinteger[_NBitLongLong]

class inexact(number[_NBit1]): ...  # type: ignore[misc]

_IntType = TypeVar("_IntType", bound=integer[Any])

class floating(inexact[_NBit1]):
    def __init__(self, value: _FloatValue = ..., /) -> None: ...
    def item(self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /) -> float: ...
    def tolist(self) -> float: ...
    def is_integer(self) -> builtins.bool: ...
    def as_integer_ratio(self) -> tuple[int, int]: ...
    @overload
    def __round__(self, ndigits: None = ..., /) -> int: ...
    @overload
    def __round__(self, ndigits: SupportsIndex, /) -> Self: ...
    __add__: _FloatOp[_NBit1]
    __radd__: _FloatOp[_NBit1]
    __sub__: _FloatOp[_NBit1]
    __rsub__: _FloatOp[_NBit1]
    __mul__: _FloatOp[_NBit1]
    __rmul__: _FloatOp[_NBit1]
    __truediv__: _FloatOp[_NBit1]
    __rtruediv__: _FloatOp[_NBit1]
    __floordiv__: _FloatOp[_NBit1]
    __rfloordiv__: _FloatOp[_NBit1]
    __pow__: _FloatOp[_NBit1]
    __rpow__: _FloatOp[_NBit1]
    __mod__: _FloatMod[_NBit1]
    __rmod__: _FloatMod[_NBit1]
    __divmod__: _FloatDivMod[_NBit1]
    __rdivmod__: _FloatDivMod[_NBit1]

float16: TypeAlias = floating[_16Bit]
float32: TypeAlias = floating[_32Bit]

# NOTE: `_64Bit` is equivalent to `_64Bit | _32Bit | _16Bit | _8Bit`
_Float64_co: TypeAlias = float | floating[_64Bit] | integer[_64Bit] | np.bool

# either a C `double`, `float`, or `longdouble`
class float64(floating[_64Bit], float):  # type: ignore[misc]
    def __getformat__(self, typestr: L["double", "float"], /) -> str: ...
    def __getnewargs__(self, /) -> tuple[float]: ...

    # overrides for `floating` and `builtins.float` compatibility
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> Self: ...
    def conjugate(self) -> Self: ...

    # float64-specific operator overrides
    @overload
    def __add__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __add__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __add__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __add__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __radd__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __radd__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __radd__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __radd__(self, other: complex, /) -> float64 | complex128: ...

    @overload
    def __sub__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __sub__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __sub__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __sub__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __rsub__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __rsub__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __rsub__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __rsub__(self, other: complex, /) -> float64 | complex128: ...

    @overload
    def __mul__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __mul__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __mul__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __mul__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __rmul__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __rmul__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __rmul__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __rmul__(self, other: complex, /) -> float64 | complex128: ...

    @overload
    def __truediv__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __truediv__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __truediv__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __truediv__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __rtruediv__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __rtruediv__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __rtruediv__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __rtruediv__(self, other: complex, /) -> float64 | complex128: ...

    @overload
    def __floordiv__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __floordiv__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __floordiv__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __floordiv__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __rfloordiv__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __rfloordiv__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __rfloordiv__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __rfloordiv__(self, other: complex, /) -> float64 | complex128: ...

    @overload
    def __pow__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __pow__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __pow__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __pow__(self, other: complex, /) -> float64 | complex128: ...
    @overload
    def __rpow__(self, other: _Float64_co, /) -> float64: ...
    @overload
    def __rpow__(self, other: complexfloating[_64Bit, _64Bit], /) -> complex128: ...
    @overload
    def __rpow__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    @overload
    def __rpow__(self, other: complex, /) -> float64 | complex128: ...

    def __mod__(self, other: _Float64_co, /) -> float64: ...  # type: ignore[override]
    def __rmod__(self, other: _Float64_co, /) -> float64: ...  # type: ignore[override]

    def __divmod__(self, other: _Float64_co, /) -> _2Tuple[float64]: ...  # type: ignore[override]
    def __rdivmod__(self, other: _Float64_co, /) -> _2Tuple[float64]: ...  # type: ignore[override]


half: TypeAlias = floating[_NBitHalf]
single: TypeAlias = floating[_NBitSingle]
double: TypeAlias = floating[_NBitDouble]
longdouble: TypeAlias = floating[_NBitLongDouble]

_Complex64_co: TypeAlias = builtins.bool | np.bool | number[_32Bit]
_Complex128_co: TypeAlias = complex | np.bool | number[_64Bit]

# The main reason for `complexfloating` having two typevars is cosmetic.
# It is used to clarify why `complex128`s precision is `_64Bit`, the latter
# describing the two 64 bit floats representing its real and imaginary component

class complexfloating(inexact[_NBit1], Generic[_NBit1, _NBit2]):
    def __init__(self, value: _ComplexValue = ..., /) -> None: ...
    def item(self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /) -> complex: ...
    def tolist(self) -> complex: ...
    @property
    def real(self) -> floating[_NBit1]: ...  # type: ignore[override]
    @property
    def imag(self) -> floating[_NBit2]: ...  # type: ignore[override]
    def __abs__(self) -> floating[_NBit1 | _NBit2]: ...  # type: ignore[override]
    # NOTE: Deprecated
    # def __round__(self, ndigits=...): ...
    @overload
    def __add__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __add__(self, other: complex | float64 | complex128, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __add__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...
    @overload
    def __radd__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __radd__(self, other: complex, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __radd__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...

    @overload
    def __sub__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __sub__(self, other: complex | float64 | complex128, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __sub__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...
    @overload
    def __rsub__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __rsub__(self, other: complex, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __rsub__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...

    @overload
    def __mul__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __mul__(self, other: complex | float64 | complex128, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __mul__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...
    @overload
    def __rmul__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __rmul__(self, other: complex, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __rmul__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...

    @overload
    def __truediv__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __truediv__(self, other: complex | float64 | complex128, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __truediv__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...
    @overload
    def __rtruediv__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __rtruediv__(self, other: complex, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __rtruediv__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...

    @overload
    def __pow__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __pow__(self, other: complex | float64 | complex128, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __pow__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...
    @overload
    def __rpow__(self, other: _Complex64_co, /) -> complexfloating[_NBit1, _NBit2]: ...
    @overload
    def __rpow__(self, other: complex, /) -> complexfloating[_NBit1, _NBit2] | complex128: ...
    @overload
    def __rpow__(self, other: number[_NBit], /) -> complexfloating[_NBit1, _NBit2] | complexfloating[_NBit, _NBit]: ...

complex64: TypeAlias = complexfloating[_32Bit, _32Bit]

class complex128(complexfloating[_64Bit, _64Bit], complex):
    def __getnewargs__(self, /) -> tuple[float, float]: ...

    # overrides for `floating` and `builtins.float` compatibility
    @property
    def real(self) -> float64: ...
    @property
    def imag(self) -> float64: ...
    def __abs__(self) -> float64: ...
    def conjugate(self) -> Self: ...

    # complex128-specific operator overrides
    @overload
    def __add__(self, other: _Complex128_co, /) -> complex128: ...
    @overload
    def __add__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    def __radd__(self, other: _Complex128_co, /) -> complex128: ...

    @overload
    def __sub__(self, other: _Complex128_co, /) -> complex128: ...
    @overload
    def __sub__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    def __rsub__(self, other: _Complex128_co, /) -> complex128: ...

    @overload
    def __mul__(self, other: _Complex128_co, /) -> complex128: ...
    @overload
    def __mul__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    def __rmul__(self, other: _Complex128_co, /) -> complex128: ...

    @overload
    def __truediv__(self, other: _Complex128_co, /) -> complex128: ...
    @overload
    def __truediv__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    def __rtruediv__(self, other: _Complex128_co, /) -> complex128: ...

    @overload
    def __pow__(self, other: _Complex128_co, /) -> complex128: ...
    @overload
    def __pow__(self, other: complexfloating[_NBit1, _NBit2], /) -> complexfloating[_NBit1 | _64Bit, _NBit2 | _64Bit]: ...
    def __rpow__(self, other: _Complex128_co, /) -> complex128: ...


csingle: TypeAlias = complexfloating[_NBitSingle, _NBitSingle]
cdouble: TypeAlias = complexfloating[_NBitDouble, _NBitDouble]
clongdouble: TypeAlias = complexfloating[_NBitLongDouble, _NBitLongDouble]

class flexible(generic): ...  # type: ignore

# TODO: `item`/`tolist` returns either `bytes` or `tuple`
# depending on whether or not it's used as an opaque bytes sequence
# or a structure
class void(flexible):
    @overload
    def __init__(self, value: _IntLike_co | bytes, /, dtype : None = ...) -> None: ...
    @overload
    def __init__(self, value: Any, /, dtype: _DTypeLikeVoid) -> None: ...
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> Self: ...
    def setfield(
        self, val: ArrayLike, dtype: DTypeLike, offset: int = ...
    ) -> None: ...
    @overload
    def __getitem__(self, key: str | SupportsIndex, /) -> Any: ...
    @overload
    def __getitem__(self, key: list[str], /) -> void: ...
    def __setitem__(
        self,
        key: str | list[str] | SupportsIndex,
        value: ArrayLike,
        /,
    ) -> None: ...

class character(flexible):  # type: ignore
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...

# NOTE: Most `np.bytes_` / `np.str_` methods return their
# builtin `bytes` / `str` counterpart

class bytes_(character, bytes):
    @overload
    def __init__(self, value: object = ..., /) -> None: ...
    @overload
    def __init__(
        self, value: str, /, encoding: str = ..., errors: str = ...
    ) -> None: ...
    def item(
        self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /,
    ) -> bytes: ...
    def tolist(self) -> bytes: ...

class str_(character, str):
    @overload
    def __init__(self, value: object = ..., /) -> None: ...
    @overload
    def __init__(
        self, value: bytes, /, encoding: str = ..., errors: str = ...
    ) -> None: ...
    def item(
        self, args: L[0] | tuple[()] | tuple[L[0]] = ..., /,
    ) -> str: ...
    def tolist(self) -> str: ...

#
# Constants
#

e: Final[float]
euler_gamma: Final[float]
inf: Final[float]
nan: Final[float]
pi: Final[float]

little_endian: Final[builtins.bool]
True_: Final[np.bool]
False_: Final[np.bool]

newaxis: None

# See `numpy._typing._ufunc` for more concrete nin-/nout-specific stubs
@final
class ufunc:
    @property
    def __name__(self) -> LiteralString: ...
    @property
    def __doc__(self) -> str: ...
    @property
    def nin(self) -> int: ...
    @property
    def nout(self) -> int: ...
    @property
    def nargs(self) -> int: ...
    @property
    def ntypes(self) -> int: ...
    @property
    def types(self) -> list[LiteralString]: ...
    # Broad return type because it has to encompass things like
    #
    # >>> np.logical_and.identity is True
    # True
    # >>> np.add.identity is 0
    # True
    # >>> np.sin.identity is None
    # True
    #
    # and any user-defined ufuncs.
    @property
    def identity(self) -> Any: ...
    # This is None for ufuncs and a string for gufuncs.
    @property
    def signature(self) -> None | LiteralString: ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    # The next four methods will always exist, but they will just
    # raise a ValueError ufuncs with that don't accept two input
    # arguments and return one output argument. Because of that we
    # can't type them very precisely.
    def reduce(self, /, *args: Any, **kwargs: Any) -> Any: ...
    def accumulate(self, /, *args: Any, **kwargs: Any) -> NDArray[Any]: ...
    def reduceat(self, /, *args: Any, **kwargs: Any) -> NDArray[Any]: ...
    def outer(self, *args: Any, **kwargs: Any) -> Any: ...
    # Similarly at won't be defined for ufuncs that return multiple
    # outputs, so we can't type it very precisely.
    def at(self, /, *args: Any, **kwargs: Any) -> None: ...

# Parameters: `__name__`, `ntypes` and `identity`
absolute: _UFunc_Nin1_Nout1[L['absolute'], L[20], None]
add: _UFunc_Nin2_Nout1[L['add'], L[22], L[0]]
arccos: _UFunc_Nin1_Nout1[L['arccos'], L[8], None]
arccosh: _UFunc_Nin1_Nout1[L['arccosh'], L[8], None]
arcsin: _UFunc_Nin1_Nout1[L['arcsin'], L[8], None]
arcsinh: _UFunc_Nin1_Nout1[L['arcsinh'], L[8], None]
arctan2: _UFunc_Nin2_Nout1[L['arctan2'], L[5], None]
arctan: _UFunc_Nin1_Nout1[L['arctan'], L[8], None]
arctanh: _UFunc_Nin1_Nout1[L['arctanh'], L[8], None]
bitwise_and: _UFunc_Nin2_Nout1[L['bitwise_and'], L[12], L[-1]]
bitwise_count: _UFunc_Nin1_Nout1[L['bitwise_count'], L[11], None]
bitwise_not: _UFunc_Nin1_Nout1[L['invert'], L[12], None]
bitwise_or: _UFunc_Nin2_Nout1[L['bitwise_or'], L[12], L[0]]
bitwise_xor: _UFunc_Nin2_Nout1[L['bitwise_xor'], L[12], L[0]]
cbrt: _UFunc_Nin1_Nout1[L['cbrt'], L[5], None]
ceil: _UFunc_Nin1_Nout1[L['ceil'], L[7], None]
conj: _UFunc_Nin1_Nout1[L['conjugate'], L[18], None]
conjugate: _UFunc_Nin1_Nout1[L['conjugate'], L[18], None]
copysign: _UFunc_Nin2_Nout1[L['copysign'], L[4], None]
cos: _UFunc_Nin1_Nout1[L['cos'], L[9], None]
cosh: _UFunc_Nin1_Nout1[L['cosh'], L[8], None]
deg2rad: _UFunc_Nin1_Nout1[L['deg2rad'], L[5], None]
degrees: _UFunc_Nin1_Nout1[L['degrees'], L[5], None]
divide: _UFunc_Nin2_Nout1[L['true_divide'], L[11], None]
divmod: _UFunc_Nin2_Nout2[L['divmod'], L[15], None]
equal: _UFunc_Nin2_Nout1[L['equal'], L[23], None]
exp2: _UFunc_Nin1_Nout1[L['exp2'], L[8], None]
exp: _UFunc_Nin1_Nout1[L['exp'], L[10], None]
expm1: _UFunc_Nin1_Nout1[L['expm1'], L[8], None]
fabs: _UFunc_Nin1_Nout1[L['fabs'], L[5], None]
float_power: _UFunc_Nin2_Nout1[L['float_power'], L[4], None]
floor: _UFunc_Nin1_Nout1[L['floor'], L[7], None]
floor_divide: _UFunc_Nin2_Nout1[L['floor_divide'], L[21], None]
fmax: _UFunc_Nin2_Nout1[L['fmax'], L[21], None]
fmin: _UFunc_Nin2_Nout1[L['fmin'], L[21], None]
fmod: _UFunc_Nin2_Nout1[L['fmod'], L[15], None]
frexp: _UFunc_Nin1_Nout2[L['frexp'], L[4], None]
gcd: _UFunc_Nin2_Nout1[L['gcd'], L[11], L[0]]
greater: _UFunc_Nin2_Nout1[L['greater'], L[23], None]
greater_equal: _UFunc_Nin2_Nout1[L['greater_equal'], L[23], None]
heaviside: _UFunc_Nin2_Nout1[L['heaviside'], L[4], None]
hypot: _UFunc_Nin2_Nout1[L['hypot'], L[5], L[0]]
invert: _UFunc_Nin1_Nout1[L['invert'], L[12], None]
isfinite: _UFunc_Nin1_Nout1[L['isfinite'], L[20], None]
isinf: _UFunc_Nin1_Nout1[L['isinf'], L[20], None]
isnan: _UFunc_Nin1_Nout1[L['isnan'], L[20], None]
isnat: _UFunc_Nin1_Nout1[L['isnat'], L[2], None]
lcm: _UFunc_Nin2_Nout1[L['lcm'], L[11], None]
ldexp: _UFunc_Nin2_Nout1[L['ldexp'], L[8], None]
left_shift: _UFunc_Nin2_Nout1[L['left_shift'], L[11], None]
less: _UFunc_Nin2_Nout1[L['less'], L[23], None]
less_equal: _UFunc_Nin2_Nout1[L['less_equal'], L[23], None]
log10: _UFunc_Nin1_Nout1[L['log10'], L[8], None]
log1p: _UFunc_Nin1_Nout1[L['log1p'], L[8], None]
log2: _UFunc_Nin1_Nout1[L['log2'], L[8], None]
log: _UFunc_Nin1_Nout1[L['log'], L[10], None]
logaddexp2: _UFunc_Nin2_Nout1[L['logaddexp2'], L[4], float]
logaddexp: _UFunc_Nin2_Nout1[L['logaddexp'], L[4], float]
logical_and: _UFunc_Nin2_Nout1[L['logical_and'], L[20], L[True]]
logical_not: _UFunc_Nin1_Nout1[L['logical_not'], L[20], None]
logical_or: _UFunc_Nin2_Nout1[L['logical_or'], L[20], L[False]]
logical_xor: _UFunc_Nin2_Nout1[L['logical_xor'], L[19], L[False]]
matmul: _GUFunc_Nin2_Nout1[L['matmul'], L[19], None, L["(n?,k),(k,m?)->(n?,m?)"]]
maximum: _UFunc_Nin2_Nout1[L['maximum'], L[21], None]
minimum: _UFunc_Nin2_Nout1[L['minimum'], L[21], None]
mod: _UFunc_Nin2_Nout1[L['remainder'], L[16], None]
modf: _UFunc_Nin1_Nout2[L['modf'], L[4], None]
multiply: _UFunc_Nin2_Nout1[L['multiply'], L[23], L[1]]
negative: _UFunc_Nin1_Nout1[L['negative'], L[19], None]
nextafter: _UFunc_Nin2_Nout1[L['nextafter'], L[4], None]
not_equal: _UFunc_Nin2_Nout1[L['not_equal'], L[23], None]
positive: _UFunc_Nin1_Nout1[L['positive'], L[19], None]
power: _UFunc_Nin2_Nout1[L['power'], L[18], None]
rad2deg: _UFunc_Nin1_Nout1[L['rad2deg'], L[5], None]
radians: _UFunc_Nin1_Nout1[L['radians'], L[5], None]
reciprocal: _UFunc_Nin1_Nout1[L['reciprocal'], L[18], None]
remainder: _UFunc_Nin2_Nout1[L['remainder'], L[16], None]
right_shift: _UFunc_Nin2_Nout1[L['right_shift'], L[11], None]
rint: _UFunc_Nin1_Nout1[L['rint'], L[10], None]
sign: _UFunc_Nin1_Nout1[L['sign'], L[19], None]
signbit: _UFunc_Nin1_Nout1[L['signbit'], L[4], None]
sin: _UFunc_Nin1_Nout1[L['sin'], L[9], None]
sinh: _UFunc_Nin1_Nout1[L['sinh'], L[8], None]
spacing: _UFunc_Nin1_Nout1[L['spacing'], L[4], None]
sqrt: _UFunc_Nin1_Nout1[L['sqrt'], L[10], None]
square: _UFunc_Nin1_Nout1[L['square'], L[18], None]
subtract: _UFunc_Nin2_Nout1[L['subtract'], L[21], None]
tan: _UFunc_Nin1_Nout1[L['tan'], L[8], None]
tanh: _UFunc_Nin1_Nout1[L['tanh'], L[8], None]
true_divide: _UFunc_Nin2_Nout1[L['true_divide'], L[11], None]
trunc: _UFunc_Nin1_Nout1[L['trunc'], L[7], None]
vecdot: _GUFunc_Nin2_Nout1[L['vecdot'], L[19], None, L["(n),(n)->()"]]

abs = absolute
acos = arccos
acosh = arccosh
asin = arcsin
asinh = arcsinh
atan = arctan
atanh = arctanh
atan2 = arctan2
concat = concatenate
bitwise_left_shift = left_shift
bitwise_invert = invert
bitwise_right_shift = right_shift
permute_dims = transpose
pow = power

class _CopyMode(enum.Enum):
    ALWAYS: L[True]
    IF_NEEDED: L[False]
    NEVER: L[2]

_CallType = TypeVar("_CallType", bound=Callable[..., Any])

class errstate:
    def __init__(
        self,
        *,
        call: _ErrFunc | _SupportsWrite[str] = ...,
        all: None | _ErrKind = ...,
        divide: None | _ErrKind = ...,
        over: None | _ErrKind = ...,
        under: None | _ErrKind = ...,
        invalid: None | _ErrKind = ...,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: None | type[BaseException],
        exc_value: None | BaseException,
        traceback: None | TracebackType,
        /,
    ) -> None: ...
    def __call__(self, func: _CallType) -> _CallType: ...

_ScalarType_co = TypeVar("_ScalarType_co", bound=generic, covariant=True)

class ndenumerate(Generic[_ScalarType_co]):
    @property
    def iter(self) -> flatiter[NDArray[_ScalarType_co]]: ...

    @overload
    def __new__(
        cls, arr: _FiniteNestedSequence[_SupportsArray[dtype[_ScalarType]]],
    ) -> ndenumerate[_ScalarType]: ...
    @overload
    def __new__(cls, arr: str | _NestedSequence[str]) -> ndenumerate[str_]: ...
    @overload
    def __new__(cls, arr: bytes | _NestedSequence[bytes]) -> ndenumerate[bytes_]: ...
    @overload
    def __new__(cls, arr: builtins.bool | _NestedSequence[builtins.bool]) -> ndenumerate[np.bool]: ...
    @overload
    def __new__(cls, arr: int | _NestedSequence[int]) -> ndenumerate[int_]: ...
    @overload
    def __new__(cls, arr: float | _NestedSequence[float]) -> ndenumerate[float64]: ...
    @overload
    def __new__(cls, arr: complex | _NestedSequence[complex]) -> ndenumerate[complex128]: ...
    @overload
    def __new__(cls, arr: object) -> ndenumerate[object_]: ...

    # The first overload is a (semi-)workaround for a mypy bug (tested with v1.10 and v1.11)
    @overload
    def __next__(
        self: ndenumerate[np.bool | datetime64 | timedelta64 | number[Any] | flexible],
        /,
    ) -> tuple[_Shape, _ScalarType_co]: ...
    @overload
    def __next__(self: ndenumerate[object_], /) -> tuple[_Shape, Any]: ...
    @overload
    def __next__(self, /) -> tuple[_Shape, _ScalarType_co]: ...

    def __iter__(self) -> Self: ...

class ndindex:
    @overload
    def __init__(self, shape: tuple[SupportsIndex, ...], /) -> None: ...
    @overload
    def __init__(self, *shape: SupportsIndex) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> _Shape: ...

# TODO: The type of each `__next__` and `iters` return-type depends
# on the length and dtype of `args`; we can't describe this behavior yet
# as we lack variadics (PEP 646).
@final
class broadcast:
    def __new__(cls, *args: ArrayLike) -> broadcast: ...
    @property
    def index(self) -> int: ...
    @property
    def iters(self) -> tuple[flatiter[Any], ...]: ...
    @property
    def nd(self) -> int: ...
    @property
    def ndim(self) -> int: ...
    @property
    def numiter(self) -> int: ...
    @property
    def shape(self) -> _Shape: ...
    @property
    def size(self) -> int: ...
    def __next__(self) -> tuple[Any, ...]: ...
    def __iter__(self) -> Self: ...
    def reset(self) -> None: ...

@final
class busdaycalendar:
    def __new__(
        cls,
        weekmask: ArrayLike = ...,
        holidays: ArrayLike | dt.date | _NestedSequence[dt.date] = ...,
    ) -> busdaycalendar: ...
    @property
    def weekmask(self) -> NDArray[np.bool]: ...
    @property
    def holidays(self) -> NDArray[datetime64]: ...


_FloatType_co = TypeVar('_FloatType_co', bound=floating[Any], covariant=True, default=floating[NBitBase])

class finfo(Generic[_FloatType_co]):
    dtype: Final[dtype[_FloatType_co]]
    bits: Final[int]
    eps: Final[_FloatType_co]
    epsneg: Final[_FloatType_co]
    iexp: Final[int]
    machep: Final[int]
    max: Final[_FloatType_co]
    maxexp: Final[int]
    min: Final[_FloatType_co]
    minexp: Final[int]
    negep: Final[int]
    nexp: Final[int]
    nmant: Final[int]
    precision: Final[int]
    resolution: Final[_FloatType_co]
    smallest_subnormal: Final[_FloatType_co]
    @property
    def smallest_normal(self) -> _FloatType_co: ...
    @property
    def tiny(self) -> _FloatType_co: ...
    @overload
    def __new__(
        cls, dtype: inexact[_NBit1] | _DTypeLike[inexact[_NBit1]]
    ) -> finfo[floating[_NBit1]]: ...
    @overload
    def __new__(
        cls, dtype: complex | float | type[complex] | type[float]
    ) -> finfo[float64]: ...
    @overload
    def __new__(
        cls, dtype: str
    ) -> finfo[floating[Any]]: ...

_IntType_co = TypeVar("_IntType_co", bound=integer[Any], covariant=True, default=integer[NBitBase])

class iinfo(Generic[_IntType_co]):
    dtype: Final[dtype[_IntType_co]]
    kind: Final[LiteralString]
    bits: Final[int]
    key: Final[LiteralString]
    @property
    def min(self) -> int: ...
    @property
    def max(self) -> int: ...

    @overload
    def __new__(
        cls, dtype: _IntType_co | _DTypeLike[_IntType_co]
    ) -> iinfo[_IntType_co]: ...
    @overload
    def __new__(cls, dtype: int | type[int]) -> iinfo[int_]: ...
    @overload
    def __new__(cls, dtype: str) -> iinfo[Any]: ...

_NDIterFlagsKind: TypeAlias = L[
    "buffered",
    "c_index",
    "copy_if_overlap",
    "common_dtype",
    "delay_bufalloc",
    "external_loop",
    "f_index",
    "grow_inner", "growinner",
    "multi_index",
    "ranged",
    "refs_ok",
    "reduce_ok",
    "zerosize_ok",
]

_NDIterOpFlagsKind: TypeAlias = L[
    "aligned",
    "allocate",
    "arraymask",
    "copy",
    "config",
    "nbo",
    "no_subtype",
    "no_broadcast",
    "overlap_assume_elementwise",
    "readonly",
    "readwrite",
    "updateifcopy",
    "virtual",
    "writeonly",
    "writemasked"
]

@final
class nditer:
    def __new__(
        cls,
        op: ArrayLike | Sequence[ArrayLike],
        flags: None | Sequence[_NDIterFlagsKind] = ...,
        op_flags: None | Sequence[Sequence[_NDIterOpFlagsKind]] = ...,
        op_dtypes: DTypeLike | Sequence[DTypeLike] = ...,
        order: _OrderKACF = ...,
        casting: _CastingKind = ...,
        op_axes: None | Sequence[Sequence[SupportsIndex]] = ...,
        itershape: None | _ShapeLike = ...,
        buffersize: SupportsIndex = ...,
    ) -> nditer: ...
    def __enter__(self) -> nditer: ...
    def __exit__(
        self,
        exc_type: None | type[BaseException],
        exc_value: None | BaseException,
        traceback: None | TracebackType,
    ) -> None: ...
    def __iter__(self) -> nditer: ...
    def __next__(self) -> tuple[NDArray[Any], ...]: ...
    def __len__(self) -> int: ...
    def __copy__(self) -> nditer: ...
    @overload
    def __getitem__(self, index: SupportsIndex) -> NDArray[Any]: ...
    @overload
    def __getitem__(self, index: slice) -> tuple[NDArray[Any], ...]: ...
    def __setitem__(self, index: slice | SupportsIndex, value: ArrayLike) -> None: ...
    def close(self) -> None: ...
    def copy(self) -> nditer: ...
    def debug_print(self) -> None: ...
    def enable_external_loop(self) -> None: ...
    def iternext(self) -> builtins.bool: ...
    def remove_axis(self, i: SupportsIndex, /) -> None: ...
    def remove_multi_index(self) -> None: ...
    def reset(self) -> None: ...
    @property
    def dtypes(self) -> tuple[dtype[Any], ...]: ...
    @property
    def finished(self) -> builtins.bool: ...
    @property
    def has_delayed_bufalloc(self) -> builtins.bool: ...
    @property
    def has_index(self) -> builtins.bool: ...
    @property
    def has_multi_index(self) -> builtins.bool: ...
    @property
    def index(self) -> int: ...
    @property
    def iterationneedsapi(self) -> builtins.bool: ...
    @property
    def iterindex(self) -> int: ...
    @property
    def iterrange(self) -> tuple[int, ...]: ...
    @property
    def itersize(self) -> int: ...
    @property
    def itviews(self) -> tuple[NDArray[Any], ...]: ...
    @property
    def multi_index(self) -> tuple[int, ...]: ...
    @property
    def ndim(self) -> int: ...
    @property
    def nop(self) -> int: ...
    @property
    def operands(self) -> tuple[NDArray[Any], ...]: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    @property
    def value(self) -> tuple[NDArray[Any], ...]: ...

_MemMapModeKind: TypeAlias = L[
    "readonly", "r",
    "copyonwrite", "c",
    "readwrite", "r+",
    "write", "w+",
]

class memmap(ndarray[_ShapeType_co, _DType_co]):
    __array_priority__: ClassVar[float]
    filename: str | None
    offset: int
    mode: str
    @overload
    def __new__(
        subtype,
        filename: str | bytes | os.PathLike[str] | os.PathLike[bytes] | _MemMapIOProtocol,
        dtype: type[uint8] = ...,
        mode: _MemMapModeKind = ...,
        offset: int = ...,
        shape: None | int | tuple[int, ...] = ...,
        order: _OrderKACF = ...,
    ) -> memmap[Any, dtype[uint8]]: ...
    @overload
    def __new__(
        subtype,
        filename: str | bytes | os.PathLike[str] | os.PathLike[bytes] | _MemMapIOProtocol,
        dtype: _DTypeLike[_ScalarType],
        mode: _MemMapModeKind = ...,
        offset: int = ...,
        shape: None | int | tuple[int, ...] = ...,
        order: _OrderKACF = ...,
    ) -> memmap[Any, dtype[_ScalarType]]: ...
    @overload
    def __new__(
        subtype,
        filename: str | bytes | os.PathLike[str] | os.PathLike[bytes] | _MemMapIOProtocol,
        dtype: DTypeLike,
        mode: _MemMapModeKind = ...,
        offset: int = ...,
        shape: None | int | tuple[int, ...] = ...,
        order: _OrderKACF = ...,
    ) -> memmap[Any, dtype[Any]]: ...
    def __array_finalize__(self, obj: object) -> None: ...
    def __array_wrap__(
        self,
        array: memmap[_ShapeType_co, _DType_co],
        context: None | tuple[ufunc, tuple[Any, ...], int] = ...,
        return_scalar: builtins.bool = ...,
    ) -> Any: ...
    def flush(self) -> None: ...

# TODO: Add a mypy plugin for managing functions whose output type is dependent
# on the literal value of some sort of signature (e.g. `einsum` and `vectorize`)
class vectorize:
    pyfunc: Callable[..., Any]
    cache: builtins.bool
    signature: None | LiteralString
    otypes: None | LiteralString
    excluded: set[int | str]
    __doc__: None | str
    def __init__(
        self,
        pyfunc: Callable[..., Any],
        otypes: None | str | Iterable[DTypeLike] = ...,
        doc: None | str = ...,
        excluded: None | Iterable[int | str] = ...,
        cache: builtins.bool = ...,
        signature: None | str = ...,
    ) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

class poly1d:
    @property
    def variable(self) -> LiteralString: ...
    @property
    def order(self) -> int: ...
    @property
    def o(self) -> int: ...
    @property
    def roots(self) -> NDArray[Any]: ...
    @property
    def r(self) -> NDArray[Any]: ...

    @property
    def coeffs(self) -> NDArray[Any]: ...
    @coeffs.setter
    def coeffs(self, value: NDArray[Any]) -> None: ...

    @property
    def c(self) -> NDArray[Any]: ...
    @c.setter
    def c(self, value: NDArray[Any]) -> None: ...

    @property
    def coef(self) -> NDArray[Any]: ...
    @coef.setter
    def coef(self, value: NDArray[Any]) -> None: ...

    @property
    def coefficients(self) -> NDArray[Any]: ...
    @coefficients.setter
    def coefficients(self, value: NDArray[Any]) -> None: ...

    __hash__: ClassVar[None]  # type: ignore

    # TODO: use `tuple[int]` as shape type once covariant (#26081)
    @overload
    def __array__(self, t: None = ..., copy: None | bool = ...) -> NDArray[Any]: ...
    @overload
    def __array__(self, t: _DType, copy: None | bool = ...) -> ndarray[_Shape, _DType]: ...

    @overload
    def __call__(self, val: _ScalarLike_co) -> Any: ...
    @overload
    def __call__(self, val: poly1d) -> poly1d: ...
    @overload
    def __call__(self, val: ArrayLike) -> NDArray[Any]: ...

    def __init__(
        self,
        c_or_r: ArrayLike,
        r: builtins.bool = ...,
        variable: None | str = ...,
    ) -> None: ...
    def __len__(self) -> int: ...
    def __neg__(self) -> poly1d: ...
    def __pos__(self) -> poly1d: ...
    def __mul__(self, other: ArrayLike, /) -> poly1d: ...
    def __rmul__(self, other: ArrayLike, /) -> poly1d: ...
    def __add__(self, other: ArrayLike, /) -> poly1d: ...
    def __radd__(self, other: ArrayLike, /) -> poly1d: ...
    def __pow__(self, val: _FloatLike_co, /) -> poly1d: ...  # Integral floats are accepted
    def __sub__(self, other: ArrayLike, /) -> poly1d: ...
    def __rsub__(self, other: ArrayLike, /) -> poly1d: ...
    def __div__(self, other: ArrayLike, /) -> poly1d: ...
    def __truediv__(self, other: ArrayLike, /) -> poly1d: ...
    def __rdiv__(self, other: ArrayLike, /) -> poly1d: ...
    def __rtruediv__(self, other: ArrayLike, /) -> poly1d: ...
    def __getitem__(self, val: int, /) -> Any: ...
    def __setitem__(self, key: int, val: Any, /) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def deriv(self, m: SupportsInt | SupportsIndex = ...) -> poly1d: ...
    def integ(
        self,
        m: SupportsInt | SupportsIndex = ...,
        k: None | _ArrayLikeComplex_co | _ArrayLikeObject_co = ...,
    ) -> poly1d: ...


class matrix(ndarray[_Shape2DType_co, _DType_co]):
    __array_priority__: ClassVar[float]
    def __new__(
        subtype,
        data: ArrayLike,
        dtype: DTypeLike = ...,
        copy: builtins.bool = ...,
    ) -> matrix[_Shape2D, Any]: ...
    def __array_finalize__(self, obj: object) -> None: ...

    @overload
    def __getitem__(
        self,
        key: (
            SupportsIndex
            | _ArrayLikeInt_co
            | tuple[SupportsIndex | _ArrayLikeInt_co, ...]
        ),
        /,
    ) -> Any: ...
    @overload
    def __getitem__(
        self,
        key: (
            None
            | slice
            | EllipsisType
            | SupportsIndex
            | _ArrayLikeInt_co
            | tuple[None | slice | EllipsisType | _ArrayLikeInt_co | SupportsIndex, ...]
        ),
        /,
    ) -> matrix[_Shape2D, _DType_co]: ...
    @overload
    def __getitem__(self: NDArray[void], key: str, /) -> matrix[_Shape2D, dtype[Any]]: ...
    @overload
    def __getitem__(self: NDArray[void], key: list[str], /) -> matrix[_Shape2DType_co, dtype[void]]: ...

    def __mul__(self, other: ArrayLike, /) -> matrix[_Shape2D, Any]: ...
    def __rmul__(self, other: ArrayLike, /) -> matrix[_Shape2D, Any]: ...
    def __imul__(self, other: ArrayLike, /) -> matrix[_Shape2DType_co, _DType_co]: ...
    def __pow__(self, other: ArrayLike, /) -> matrix[_Shape2D, Any]: ...
    def __ipow__(self, other: ArrayLike, /) -> matrix[_Shape2DType_co, _DType_co]: ...

    @overload
    def sum(self, axis: None = ..., dtype: DTypeLike = ..., out: None = ...) -> Any: ...
    @overload
    def sum(self, axis: _ShapeLike, dtype: DTypeLike = ..., out: None = ...) -> matrix[_Shape2D, Any]: ...
    @overload
    def sum(self, axis: None | _ShapeLike = ..., dtype: DTypeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def mean(self, axis: None = ..., dtype: DTypeLike = ..., out: None = ...) -> Any: ...
    @overload
    def mean(self, axis: _ShapeLike, dtype: DTypeLike = ..., out: None = ...) -> matrix[_Shape2D, Any]: ...
    @overload
    def mean(self, axis: None | _ShapeLike = ..., dtype: DTypeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def std(self, axis: None = ..., dtype: DTypeLike = ..., out: None = ..., ddof: float = ...) -> Any: ...
    @overload
    def std(self, axis: _ShapeLike, dtype: DTypeLike = ..., out: None = ..., ddof: float = ...) -> matrix[_Shape2D, Any]: ...
    @overload
    def std(self, axis: None | _ShapeLike = ..., dtype: DTypeLike = ..., out: _NdArraySubClass = ..., ddof: float = ...) -> _NdArraySubClass: ...

    @overload
    def var(self, axis: None = ..., dtype: DTypeLike = ..., out: None = ..., ddof: float = ...) -> Any: ...
    @overload
    def var(self, axis: _ShapeLike, dtype: DTypeLike = ..., out: None = ..., ddof: float = ...) -> matrix[_Shape2D, Any]: ...
    @overload
    def var(self, axis: None | _ShapeLike = ..., dtype: DTypeLike = ..., out: _NdArraySubClass = ..., ddof: float = ...) -> _NdArraySubClass: ...

    @overload
    def prod(self, axis: None = ..., dtype: DTypeLike = ..., out: None = ...) -> Any: ...
    @overload
    def prod(self, axis: _ShapeLike, dtype: DTypeLike = ..., out: None = ...) -> matrix[_Shape2D, Any]: ...
    @overload
    def prod(self, axis: None | _ShapeLike = ..., dtype: DTypeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def any(self, axis: None = ..., out: None = ...) -> np.bool: ...
    @overload
    def any(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, dtype[np.bool]]: ...
    @overload
    def any(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def all(self, axis: None = ..., out: None = ...) -> np.bool: ...
    @overload
    def all(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, dtype[np.bool]]: ...
    @overload
    def all(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def max(self: NDArray[_ScalarType], axis: None = ..., out: None = ...) -> _ScalarType: ...
    @overload
    def max(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, _DType_co]: ...
    @overload
    def max(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def min(self: NDArray[_ScalarType], axis: None = ..., out: None = ...) -> _ScalarType: ...
    @overload
    def min(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, _DType_co]: ...
    @overload
    def min(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def argmax(self: NDArray[_ScalarType], axis: None = ..., out: None = ...) -> intp: ...
    @overload
    def argmax(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, dtype[intp]]: ...
    @overload
    def argmax(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def argmin(self: NDArray[_ScalarType], axis: None = ..., out: None = ...) -> intp: ...
    @overload
    def argmin(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, dtype[intp]]: ...
    @overload
    def argmin(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    @overload
    def ptp(self: NDArray[_ScalarType], axis: None = ..., out: None = ...) -> _ScalarType: ...
    @overload
    def ptp(self, axis: _ShapeLike, out: None = ...) -> matrix[_Shape2D, _DType_co]: ...
    @overload
    def ptp(self, axis: None | _ShapeLike = ..., out: _NdArraySubClass = ...) -> _NdArraySubClass: ...

    def squeeze(self, axis: None | _ShapeLike = ...) -> matrix[_Shape2D, _DType_co]: ...
    def tolist(self: matrix[_Shape2D, dtype[_SupportsItem[_T]]]) -> list[list[_T]]: ...  # type: ignore[typevar]
    def ravel(self, order: _OrderKACF = ...) -> matrix[_Shape2D, _DType_co]: ...
    def flatten(self, order: _OrderKACF = ...) -> matrix[_Shape2D, _DType_co]: ...

    @property
    def T(self) -> matrix[_Shape2D, _DType_co]: ...
    @property
    def I(self) -> matrix[_Shape2D, Any]: ...
    @property
    def A(self) -> ndarray[_Shape2DType_co, _DType_co]: ...
    @property
    def A1(self) -> ndarray[_Shape, _DType_co]: ...
    @property
    def H(self) -> matrix[_Shape2D, _DType_co]: ...
    def getT(self) -> matrix[_Shape2D, _DType_co]: ...
    def getI(self) -> matrix[_Shape2D, Any]: ...
    def getA(self) -> ndarray[_Shape2DType_co, _DType_co]: ...
    def getA1(self) -> ndarray[_Shape, _DType_co]: ...
    def getH(self) -> matrix[_Shape2D, _DType_co]: ...


@type_check_only
class _SupportsDLPack(Protocol[_T_contra]):
    def __dlpack__(self, *, stream: None | _T_contra = ...) -> _PyCapsule: ...

def from_dlpack(
    obj: _SupportsDLPack[None],
    /,
    *,
    device: L["cpu"] | None = ...,
    copy: bool | None = ...,
) -> NDArray[Any]: ...
