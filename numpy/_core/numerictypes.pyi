import sys
import types
from typing import (
    Literal as L,
    overload,
    Any,
    TypeVar,
    Protocol,
    TypedDict,
)

import numpy as np
from numpy import (
    ndarray,
    dtype,
    generic,
    ubyte,
    ushort,
    uintc,
    ulong,
    ulonglong,
    byte,
    short,
    intc,
    long,
    longlong,
    half,
    single,
    double,
    longdouble,
    csingle,
    cdouble,
    clongdouble,
    datetime64,
    timedelta64,
    object_,
    str_,
    bytes_,
    void,
)

from numpy._core._type_aliases import (
    sctypeDict as sctypeDict,
    sctypes as sctypes,
)

from numpy._typing import DTypeLike, ArrayLike, _DTypeLike

_T = TypeVar("_T")
_SCT = TypeVar("_SCT", bound=generic)

class _CastFunc(Protocol):
    def __call__(
        self, x: ArrayLike, k: DTypeLike = ...
    ) -> ndarray[Any, dtype[Any]]: ...

class _TypeCodes(TypedDict):
    Character: L['c']
    Integer: L['bhilqp']
    UnsignedInteger: L['BHILQP']
    Float: L['efdg']
    Complex: L['FDG']
    AllInteger: L['bBhHiIlLqQpP']
    AllFloat: L['efdgFDG']
    Datetime: L['Mm']
    All: L['?bhilqpBHILQPefdgFDGSUVOMm']

if sys.version_info >= (3, 10):
    _TypeTuple = (
        type[Any]
        | types.UnionType
        | tuple[type[Any] | types.UnionType | tuple[Any, ...], ...]
    )
else:
    _TypeTuple = (
        type[Any]
        | tuple[type[Any] | tuple[Any, ...], ...]
    )

__all__: list[str]

@overload
def maximum_sctype(t: _DTypeLike[_SCT]) -> type[_SCT]: ...
@overload
def maximum_sctype(t: DTypeLike) -> type[Any]: ...

@overload
def issctype(rep: dtype[Any] | type[Any]) -> bool: ...
@overload
def issctype(rep: object) -> L[False]: ...

@overload
def obj2sctype(rep: _DTypeLike[_SCT], default: None = ...) -> None | type[_SCT]: ...
@overload
def obj2sctype(rep: _DTypeLike[_SCT], default: _T) -> _T | type[_SCT]: ...
@overload
def obj2sctype(rep: DTypeLike, default: None = ...) -> None | type[Any]: ...
@overload
def obj2sctype(rep: DTypeLike, default: _T) -> _T | type[Any]: ...
@overload
def obj2sctype(rep: object, default: None = ...) -> None: ...
@overload
def obj2sctype(rep: object, default: _T) -> _T: ...

@overload
def issubclass_(arg1: type[Any], arg2: _TypeTuple) -> bool: ...
@overload
def issubclass_(arg1: object, arg2: object) -> L[False]: ...

def issubsctype(arg1: DTypeLike, arg2: DTypeLike) -> bool: ...

def isdtype(
    dtype: dtype[Any] | type[Any],
    kind: DTypeLike | tuple[DTypeLike, ...]
) -> bool: ...

def issubdtype(arg1: DTypeLike, arg2: DTypeLike) -> bool: ...

def sctype2char(sctype: DTypeLike) -> str: ...

typecodes: _TypeCodes
ScalarType: tuple[
    type[int],
    type[float],
    type[complex],
    type[bool],
    type[bytes],
    type[str],
    type[memoryview],
    type[np.bool],
    type[csingle],
    type[cdouble],
    type[clongdouble],
    type[half],
    type[single],
    type[double],
    type[longdouble],
    type[byte],
    type[short],
    type[intc],
    type[long],
    type[longlong],
    type[timedelta64],
    type[datetime64],
    type[object_],
    type[bytes_],
    type[str_],
    type[ubyte],
    type[ushort],
    type[uintc],
    type[ulong],
    type[ulonglong],
    type[void],
]
