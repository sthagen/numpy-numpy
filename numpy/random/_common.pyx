#!python
#cython: wraparound=False, nonecheck=False, boundscheck=False, cdivision=True, language_level=3
from collections import namedtuple
from cpython cimport PyFloat_AsDouble
import sys
import numpy as np
cimport numpy as np

from libc.stdint cimport uintptr_t
from libc.math cimport isnan, signbit

cdef extern from "limits.h":
    cdef long LONG_MAX  # NumPy has it, maybe `__init__.pyd` should expose it



__all__ = ['interface']

np.import_array()

interface = namedtuple('interface', ['state_address', 'state', 'next_uint64',
                                     'next_uint32', 'next_double',
                                     'bit_generator'])

cdef double LEGACY_POISSON_LAM_MAX = <double>np.iinfo('l').max - np.sqrt(np.iinfo('l').max)*10
cdef double POISSON_LAM_MAX = <double>np.iinfo('int64').max - np.sqrt(np.iinfo('int64').max)*10

cdef uint64_t MAXSIZE = <uint64_t>sys.maxsize


cdef object benchmark(bitgen_t *bitgen, object lock, Py_ssize_t cnt, object method):
    """Benchmark command used by BitGenerator"""
    cdef Py_ssize_t i
    if method=='uint64':
        with lock, nogil:
            for i in range(cnt):
                bitgen.next_uint64(bitgen.state)
    elif method=='double':
        with lock, nogil:
            for i in range(cnt):
                bitgen.next_double(bitgen.state)
    else:
        raise ValueError('Unknown method')


cdef object random_raw(bitgen_t *bitgen, object lock, object size, object output):
    """
    random_raw(self, size=None)

    Return randoms as generated by the underlying PRNG

    Parameters
    ----------
    bitgen : BitGenerator
        Address of the bit generator struct
    lock : Threading.Lock
        Lock provided by the bit generator
    size : int or tuple of ints, optional
        Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
        ``m * n * k`` samples are drawn.  Default is None, in which case a
        single value is returned.
    output : bool, optional
        Output values.  Used for performance testing since the generated
        values are not returned.

    Returns
    -------
    out : uint or ndarray
        Drawn samples.

    Notes
    -----
    This method directly exposes the raw underlying pseudo-random
    number generator. All values are returned as unsigned 64-bit
    values irrespective of the number of bits produced by the PRNG.

    See the class docstring for the number of bits returned.
    """
    cdef np.ndarray randoms
    cdef uint64_t *randoms_data
    cdef Py_ssize_t i, n

    if not output:
        if size is None:
            with lock:
                bitgen.next_raw(bitgen.state)
            return None
        n = np.asarray(size).sum()
        with lock, nogil:
            for i in range(n):
                bitgen.next_raw(bitgen.state)
        return None

    if size is None:
        with lock:
            return bitgen.next_raw(bitgen.state)

    randoms = <np.ndarray>np.empty(size, np.uint64)
    randoms_data = <uint64_t*>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    with lock, nogil:
        for i in range(n):
            randoms_data[i] = bitgen.next_raw(bitgen.state)
    return randoms

cdef object prepare_cffi(bitgen_t *bitgen):
    """
    Bundles the interfaces to interact with a BitGenerator using cffi

    Parameters
    ----------
    bitgen : pointer
        A pointer to a BitGenerator instance

    Returns
    -------
    interface : namedtuple
        The functions required to interface with the BitGenerator using cffi

        * state_address - Memory address of the state struct
        * state - pointer to the state struct
        * next_uint64 - function pointer to produce 64 bit integers
        * next_uint32 - function pointer to produce 32 bit integers
        * next_double - function pointer to produce doubles
        * bit_generator - pointer to the BitGenerator struct
    """
    try:
        import cffi
    except ImportError as e:
        raise ImportError('cffi cannot be imported.') from e

    ffi = cffi.FFI()
    _cffi = interface(<uintptr_t>bitgen.state,
                      ffi.cast('void *', <uintptr_t>bitgen.state),
                      ffi.cast('uint64_t (*)(void *)', <uintptr_t>bitgen.next_uint64),
                      ffi.cast('uint32_t (*)(void *)', <uintptr_t>bitgen.next_uint32),
                      ffi.cast('double (*)(void *)', <uintptr_t>bitgen.next_double),
                      ffi.cast('void *', <uintptr_t>bitgen))
    return _cffi

cdef object prepare_ctypes(bitgen_t *bitgen):
    """
    Bundles the interfaces to interact with a BitGenerator using ctypes

    Parameters
    ----------
    bitgen : pointer
        A pointer to a BitGenerator instance

    Returns
    -------
    interface : namedtuple
        The functions required to interface with the BitGenerator using ctypes:

        * state_address - Memory address of the state struct
        * state - pointer to the state struct
        * next_uint64 - function pointer to produce 64 bit integers
        * next_uint32 - function pointer to produce 32 bit integers
        * next_double - function pointer to produce doubles
        * bit_generator - pointer to the BitGenerator struct
    """
    import ctypes

    _ctypes = interface(<uintptr_t>bitgen.state,
                        ctypes.c_void_p(<uintptr_t>bitgen.state),
                        ctypes.cast(<uintptr_t>bitgen.next_uint64,
                                    ctypes.CFUNCTYPE(ctypes.c_uint64,
                                                     ctypes.c_void_p)),
                        ctypes.cast(<uintptr_t>bitgen.next_uint32,
                                    ctypes.CFUNCTYPE(ctypes.c_uint32,
                                                     ctypes.c_void_p)),
                        ctypes.cast(<uintptr_t>bitgen.next_double,
                                    ctypes.CFUNCTYPE(ctypes.c_double,
                                                     ctypes.c_void_p)),
                        ctypes.c_void_p(<uintptr_t>bitgen))
    return _ctypes

cdef double kahan_sum(double *darr, np.npy_intp n) noexcept:
    """
    Parameters
    ----------
    darr : reference to double array
        Address of values to sum
    n : intp
        Length of d
    
    Returns
    -------
    float
        The sum. 0.0 if n <= 0.
    """
    cdef double c, y, t, sum
    cdef np.npy_intp i
    if n <= 0:
        return 0.0
    sum = darr[0]
    c = 0.0
    for i in range(1, n):
        y = darr[i] - c
        t = sum + y
        c = (t-sum) - y
        sum = t
    return sum


cdef object wrap_int(object val, object bits):
    """Wraparound to place an integer into the interval [0, 2**bits)"""
    mask = ~(~int(0) << bits)
    return val & mask


cdef np.ndarray int_to_array(object value, object name, object bits, object uint_size):
    """Convert a large integer to an array of unsigned integers"""
    len = bits // uint_size
    value = np.asarray(value)
    if uint_size == 32:
        dtype = np.uint32
    elif uint_size == 64:
        dtype = np.uint64
    else:
        raise ValueError('Unknown uint_size')
    if value.shape == ():
        value = int(value)
        upper = int(2)**int(bits)
        if value < 0 or value >= upper:
            raise ValueError(f'{name} must be positive and less than 2**{bits}.')

        out = np.empty(len, dtype=dtype)
        for i in range(len):
            out[i] = value % 2**int(uint_size)
            value >>= int(uint_size)
    else:
        out = value.astype(dtype)
        if out.shape != (len,):
            raise ValueError(f'{name} must have {len} elements when using array form')
    return out


cdef validate_output_shape(iter_shape, np.ndarray output):
    cdef np.npy_intp *dims
    cdef np.npy_intp ndim, i
    cdef bint error
    dims = np.PyArray_DIMS(output)
    ndim = np.PyArray_NDIM(output)
    output_shape = tuple((dims[i] for i in range(ndim)))
    if iter_shape != output_shape:
        raise ValueError(
            f"Output size {output_shape} is not compatible with broadcast "
            f"dimensions of inputs {iter_shape}."
        )


cdef check_output(object out, object dtype, object size, bint require_c_array):
    """
    Check user-supplied output array properties and shape
    
    Parameters
    ----------
    out : {ndarray, None}
        The array to check.  If None, returns immediately.
    dtype : dtype
        The required dtype of out.
    size : {None, int, tuple[int]}
        The size passed.  If out is an ndarray, verifies that the shape of out
        matches size.
    require_c_array : bool
        Whether out must be a C-array.  If False, out can be either C- or F-
        ordered.  If True, must be C-ordered. In either case, must be
        contiguous, writable, aligned and in native byte-order.
    """
    if out is None:
        return
    cdef np.ndarray out_array = <np.ndarray>out
    if not (np.PyArray_ISCARRAY(out_array) or
            (np.PyArray_ISFARRAY(out_array) and not require_c_array)):
        req = "C-" if require_c_array else ""
        raise ValueError(
            f'Supplied output array must be {req}contiguous, writable, '
            f'aligned, and in machine byte-order.'
        )
    if out_array.dtype != dtype:
        raise TypeError('Supplied output array has the wrong type. '
                        f'Expected {np.dtype(dtype)}, got {out_array.dtype}')
    if size is not None:
        try:
            tup_size = tuple(size)
        except TypeError:
            tup_size = tuple([size])
        if tup_size != out.shape:
            raise ValueError('size must match out.shape when used together')


cdef object double_fill(void *func, bitgen_t *state, object size, object lock, object out):
    cdef random_double_fill random_func = (<random_double_fill>func)
    cdef double out_val
    cdef double *out_array_data
    cdef np.ndarray out_array
    cdef np.npy_intp i, n

    if size is None and out is None:
        with lock:
            random_func(state, 1, &out_val)
            return out_val

    if out is not None:
        check_output(out, np.float64, size, False)
        out_array = <np.ndarray>out
    else:
        out_array = <np.ndarray>np.empty(size, np.double)

    n = np.PyArray_SIZE(out_array)
    out_array_data = <double *>np.PyArray_DATA(out_array)
    with lock, nogil:
        random_func(state, n, out_array_data)
    return out_array

cdef object float_fill(void *func, bitgen_t *state, object size, object lock, object out):
    cdef random_float_fill random_func = (<random_float_fill>func)
    cdef float out_val
    cdef float *out_array_data
    cdef np.ndarray out_array
    cdef np.npy_intp i, n

    if size is None and out is None:
        with lock:
            random_func(state, 1, &out_val)
            return out_val

    if out is not None:
        check_output(out, np.float32, size, False)
        out_array = <np.ndarray>out
    else:
        out_array = <np.ndarray>np.empty(size, np.float32)

    n = np.PyArray_SIZE(out_array)
    out_array_data = <float *>np.PyArray_DATA(out_array)
    with lock, nogil:
        random_func(state, n, out_array_data)
    return out_array

cdef object float_fill_from_double(void *func, bitgen_t *state, object size, object lock, object out):
    cdef random_double_0 random_func = (<random_double_0>func)
    cdef float *out_array_data
    cdef np.ndarray out_array
    cdef np.npy_intp i, n

    if size is None and out is None:
        with lock:
            return <float>random_func(state)

    if out is not None:
        check_output(out, np.float32, size, False)
        out_array = <np.ndarray>out
    else:
        out_array = <np.ndarray>np.empty(size, np.float32)

    n = np.PyArray_SIZE(out_array)
    out_array_data = <float *>np.PyArray_DATA(out_array)
    with lock, nogil:
        for i in range(n):
            out_array_data[i] = <float>random_func(state)
    return out_array

cdef int _check_array_cons_bounded_0_1(np.ndarray val, object name) except -1:
    cdef double *val_data
    cdef np.npy_intp i
    cdef bint err = 0

    if not np.PyArray_ISONESEGMENT(val) or np.PyArray_TYPE(val) != np.NPY_DOUBLE:
        # slow path for non-contiguous arrays or any non-double dtypes
        err = not np.all(np.greater_equal(val, 0)) or not np.all(np.less_equal(val, 1))
    else:
        val_data = <double *>np.PyArray_DATA(val)
        for i in range(np.PyArray_SIZE(val)):
            err = (not (val_data[i] >= 0)) or (not val_data[i] <= 1)
            if err:
                break
    if err:
        raise ValueError(f"{name} < 0, {name} > 1 or {name} contains NaNs")

    return 0

cdef int check_array_constraint(np.ndarray val, object name, constraint_type cons) except -1:
    if cons == CONS_NON_NEGATIVE:
        if np.any(np.logical_and(np.logical_not(np.isnan(val)), np.signbit(val))):
            raise ValueError(f"{name} < 0")
    elif cons == CONS_POSITIVE or cons == CONS_POSITIVE_NOT_NAN:
        if cons == CONS_POSITIVE_NOT_NAN and np.any(np.isnan(val)):
            raise ValueError(f"{name} must not be NaN")
        elif np.any(np.less_equal(val, 0)):
            raise ValueError(f"{name} <= 0")
    elif cons == CONS_BOUNDED_0_1:
        return _check_array_cons_bounded_0_1(val, name)
    elif cons == CONS_BOUNDED_GT_0_1:
        if not np.all(np.greater(val, 0)) or not np.all(np.less_equal(val, 1)):
            raise ValueError(f"{name} <= 0, {name} > 1 or {name} contains NaNs")
    elif cons == CONS_BOUNDED_LT_0_1:
        if not np.all(np.greater_equal(val, 0)) or not np.all(np.less(val, 1)):
            raise ValueError(f"{name} < 0, {name} >= 1 or {name} contains NaNs")
    elif cons == CONS_GT_1:
        if not np.all(np.greater(val, 1)):
            raise ValueError(f"{name} <= 1 or {name} contains NaNs")
    elif cons == CONS_GTE_1:
        if not np.all(np.greater_equal(val, 1)):
            raise ValueError(f"{name} < 1 or {name} contains NaNs")
    elif cons == CONS_POISSON:
        if not np.all(np.less_equal(val, POISSON_LAM_MAX)):
            raise ValueError(f"{name} value too large")
        elif not np.all(np.greater_equal(val, 0.0)):
            raise ValueError(f"{name} < 0 or {name} contains NaNs")
    elif cons == LEGACY_CONS_POISSON:
        if not np.all(np.less_equal(val, LEGACY_POISSON_LAM_MAX)):
            raise ValueError(f"{name} value too large")
        elif not np.all(np.greater_equal(val, 0.0)):
            raise ValueError(f"{name} < 0 or {name} contains NaNs")
    elif cons == LEGACY_CONS_NON_NEGATIVE_INBOUNDS_LONG:
        # Note, we assume that array is integral:
        if not np.all(val >= 0):
            raise ValueError(f"{name} < 0")
        elif not np.all(val <= int(LONG_MAX)):
            raise ValueError(
                    f"{name} is out of bounds for long, consider using "
                    "the new generator API for 64bit integers.")

    return 0


cdef int check_constraint(double val, object name, constraint_type cons) except -1:
    cdef bint is_nan
    if cons == CONS_NON_NEGATIVE:
        if not isnan(val) and signbit(val):
            raise ValueError(f"{name} < 0")
    elif cons == CONS_POSITIVE or cons == CONS_POSITIVE_NOT_NAN:
        if cons == CONS_POSITIVE_NOT_NAN and isnan(val):
            raise ValueError(f"{name} must not be NaN")
        elif val <= 0:
            raise ValueError(f"{name} <= 0")
    elif cons == CONS_BOUNDED_0_1:
        if not (val >= 0) or not (val <= 1):
            raise ValueError(f"{name} < 0, {name} > 1 or {name} is NaN")
    elif cons == CONS_BOUNDED_GT_0_1:
        if not val >0 or not val <= 1:
            raise ValueError(f"{name} <= 0, {name} > 1 or {name} contains NaNs")
    elif cons == CONS_BOUNDED_LT_0_1:
        if not (val >= 0) or not (val < 1):
            raise ValueError(f"{name} < 0, {name} >= 1 or {name} is NaN")
    elif cons == CONS_GT_1:
        if not (val > 1):
            raise ValueError(f"{name} <= 1 or {name} is NaN")
    elif cons == CONS_GTE_1:
        if not (val >= 1):
            raise ValueError(f"{name} < 1 or {name} is NaN")
    elif cons == CONS_POISSON:
        if not (val >= 0):
            raise ValueError(f"{name} < 0 or {name} is NaN")
        elif not (val <= POISSON_LAM_MAX):
            raise ValueError(f"{name} value too large")
    elif cons == LEGACY_CONS_POISSON:
        if not (val >= 0):
            raise ValueError(f"{name} < 0 or {name} is NaN")
        elif not (val <= LEGACY_POISSON_LAM_MAX):
            raise ValueError(f"{name} value too large")
    elif cons == LEGACY_CONS_NON_NEGATIVE_INBOUNDS_LONG:
        # Note: Assume value is integral (double of LONG_MAX should work out)
        if val < 0:
            raise ValueError(f"{name} < 0")
        elif val > <double> LONG_MAX:
            raise ValueError(
                    f"{name} is out of bounds for long, consider using "
                    "the new generator API for 64bit integers.")

    return 0

cdef object cont_broadcast_1(void *func, void *state, object size, object lock,
                             np.ndarray a_arr, object a_name, constraint_type a_constraint,
                             object out):

    cdef np.ndarray randoms
    cdef double a_val
    cdef double *randoms_data
    cdef np.broadcast it
    cdef random_double_1 f = (<random_double_1>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if size is not None and out is None:
        randoms = <np.ndarray>np.empty(size, np.double)
    elif out is None:
        randoms = np.PyArray_SimpleNew(np.PyArray_NDIM(a_arr), np.PyArray_DIMS(a_arr), np.NPY_DOUBLE)
    else:
        randoms = <np.ndarray>out

    randoms_data = <double *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)
    it = np.PyArray_MultiIterNew2(randoms, a_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            randoms_data[i] = f(state, a_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object cont_broadcast_2(void *func, void *state, object size, object lock,
                 np.ndarray a_arr, object a_name, constraint_type a_constraint,
                 np.ndarray b_arr, object b_name, constraint_type b_constraint):
    cdef np.ndarray randoms
    cdef double a_val, b_val
    cdef double *randoms_data
    cdef np.broadcast it
    cdef random_double_2 f = (<random_double_2>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if b_constraint != CONS_NONE:
        check_array_constraint(b_arr, b_name, b_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.double)
    else:
        it = np.PyArray_MultiIterNew2(a_arr, b_arr)
        randoms = <np.ndarray>np.empty(it.shape, np.double)
        # randoms = np.PyArray_SimpleNew(it.nd, np.PyArray_DIMS(it), np.NPY_DOUBLE)

    randoms_data = <double *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew3(randoms, a_arr, b_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            b_val = (<double*>np.PyArray_MultiIter_DATA(it, 2))[0]
            randoms_data[i] = f(state, a_val, b_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object cont_broadcast_3(void *func, void *state, object size, object lock,
                             np.ndarray a_arr, object a_name, constraint_type a_constraint,
                             np.ndarray b_arr, object b_name, constraint_type b_constraint,
                             np.ndarray c_arr, object c_name, constraint_type c_constraint):
    cdef np.ndarray randoms
    cdef double a_val, b_val, c_val
    cdef double *randoms_data
    cdef np.broadcast it
    cdef random_double_3 f = (<random_double_3>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if b_constraint != CONS_NONE:
        check_array_constraint(b_arr, b_name, b_constraint)

    if c_constraint != CONS_NONE:
        check_array_constraint(c_arr, c_name, c_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.double)
    else:
        it = np.PyArray_MultiIterNew3(a_arr, b_arr, c_arr)
        # randoms = np.PyArray_SimpleNew(it.nd, np.PyArray_DIMS(it), np.NPY_DOUBLE)
        randoms = <np.ndarray>np.empty(it.shape, np.double)

    randoms_data = <double *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew4(randoms, a_arr, b_arr, c_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            b_val = (<double*>np.PyArray_MultiIter_DATA(it, 2))[0]
            c_val = (<double*>np.PyArray_MultiIter_DATA(it, 3))[0]
            randoms_data[i] = f(state, a_val, b_val, c_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object cont(void *func, void *state, object size, object lock, int narg,
                 object a, object a_name, constraint_type a_constraint,
                 object b, object b_name, constraint_type b_constraint,
                 object c, object c_name, constraint_type c_constraint,
                 object out):

    cdef np.ndarray a_arr, b_arr, c_arr
    cdef double _a = 0.0, _b = 0.0, _c = 0.0
    cdef bint is_scalar = True
    check_output(out, np.float64, size, narg > 0)
    if narg > 0:
        a_arr = <np.ndarray>np.PyArray_FROM_OTF(a, np.NPY_DOUBLE, np.NPY_ARRAY_ALIGNED)
        is_scalar = is_scalar and np.PyArray_NDIM(a_arr) == 0
    if narg > 1:
        b_arr = <np.ndarray>np.PyArray_FROM_OTF(b, np.NPY_DOUBLE, np.NPY_ARRAY_ALIGNED)
        is_scalar = is_scalar and np.PyArray_NDIM(b_arr) == 0
    if narg == 3:
        c_arr = <np.ndarray>np.PyArray_FROM_OTF(c, np.NPY_DOUBLE, np.NPY_ARRAY_ALIGNED)
        is_scalar = is_scalar and np.PyArray_NDIM(c_arr) == 0

    if not is_scalar:
        if narg == 1:
            return cont_broadcast_1(func, state, size, lock,
                                    a_arr, a_name, a_constraint,
                                    out)
        elif narg == 2:
            return cont_broadcast_2(func, state, size, lock,
                                    a_arr, a_name, a_constraint,
                                    b_arr, b_name, b_constraint)
        else:
            return cont_broadcast_3(func, state, size, lock,
                                    a_arr, a_name, a_constraint,
                                    b_arr, b_name, b_constraint,
                                    c_arr, c_name, c_constraint)

    if narg > 0:
        _a = PyFloat_AsDouble(a)
        if a_constraint != CONS_NONE and is_scalar:
            check_constraint(_a, a_name, a_constraint)
    if narg > 1:
        _b = PyFloat_AsDouble(b)
        if b_constraint != CONS_NONE:
            check_constraint(_b, b_name, b_constraint)
    if narg == 3:
        _c = PyFloat_AsDouble(c)
        if c_constraint != CONS_NONE and is_scalar:
            check_constraint(_c, c_name, c_constraint)

    if size is None and out is None:
        with lock:
            if narg == 0:
                return (<random_double_0>func)(state)
            elif narg == 1:
                return (<random_double_1>func)(state, _a)
            elif narg == 2:
                return (<random_double_2>func)(state, _a, _b)
            elif narg == 3:
                return (<random_double_3>func)(state, _a, _b, _c)

    cdef np.npy_intp i, n
    cdef np.ndarray randoms
    if out is None:
        randoms = <np.ndarray>np.empty(size)
    else:
        randoms = <np.ndarray>out
    n = np.PyArray_SIZE(randoms)

    cdef double *randoms_data = <double *>np.PyArray_DATA(randoms)
    cdef random_double_0 f0
    cdef random_double_1 f1
    cdef random_double_2 f2
    cdef random_double_3 f3

    with lock, nogil:
        if narg == 0:
            f0 = (<random_double_0>func)
            for i in range(n):
                randoms_data[i] = f0(state)
        elif narg == 1:
            f1 = (<random_double_1>func)
            for i in range(n):
                randoms_data[i] = f1(state, _a)
        elif narg == 2:
            f2 = (<random_double_2>func)
            for i in range(n):
                randoms_data[i] = f2(state, _a, _b)
        elif narg == 3:
            f3 = (<random_double_3>func)
            for i in range(n):
                randoms_data[i] = f3(state, _a, _b, _c)

    if out is None:
        return randoms
    else:
        return out

cdef object discrete_broadcast_d(void *func, void *state, object size, object lock,
                                 np.ndarray a_arr, object a_name, constraint_type a_constraint):

    cdef np.ndarray randoms
    cdef int64_t *randoms_data
    cdef np.broadcast it
    cdef random_uint_d f = (<random_uint_d>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if size is not None:
        randoms = np.empty(size, np.int64)
    else:
        # randoms = np.empty(np.shape(a_arr), np.double)
        randoms = np.PyArray_SimpleNew(np.PyArray_NDIM(a_arr), np.PyArray_DIMS(a_arr), np.NPY_INT64)

    randoms_data = <int64_t *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew2(randoms, a_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            randoms_data[i] = f(state, a_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object discrete_broadcast_dd(void *func, void *state, object size, object lock,
                                  np.ndarray a_arr, object a_name, constraint_type a_constraint,
                                  np.ndarray b_arr, object b_name, constraint_type b_constraint):
    cdef np.ndarray randoms
    cdef int64_t *randoms_data
    cdef np.broadcast it
    cdef random_uint_dd f = (<random_uint_dd>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)
    if b_constraint != CONS_NONE:
        check_array_constraint(b_arr, b_name, b_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.int64)
    else:
        it = np.PyArray_MultiIterNew2(a_arr, b_arr)
        randoms = <np.ndarray>np.empty(it.shape, np.int64)
        # randoms = np.PyArray_SimpleNew(it.nd, np.PyArray_DIMS(it), np.NPY_INT64)

    randoms_data = <int64_t *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew3(randoms, a_arr, b_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            b_val = (<double*>np.PyArray_MultiIter_DATA(it, 2))[0]
            randoms_data[i] = f(state, a_val, b_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object discrete_broadcast_di(void *func, void *state, object size, object lock,
                                  np.ndarray a_arr, object a_name, constraint_type a_constraint,
                                  np.ndarray b_arr, object b_name, constraint_type b_constraint):
    cdef np.ndarray randoms
    cdef int64_t *randoms_data
    cdef np.broadcast it
    cdef random_uint_di f = (<random_uint_di>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if b_constraint != CONS_NONE:
        check_array_constraint(b_arr, b_name, b_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.int64)
    else:
        it = np.PyArray_MultiIterNew2(a_arr, b_arr)
        randoms = <np.ndarray>np.empty(it.shape, np.int64)

    randoms_data = <int64_t *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew3(randoms, a_arr, b_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<double*>np.PyArray_MultiIter_DATA(it, 1))[0]
            b_val = (<int64_t*>np.PyArray_MultiIter_DATA(it, 2))[0]
            (<int64_t*>np.PyArray_MultiIter_DATA(it, 0))[0] = f(state, a_val, b_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object discrete_broadcast_iii(void *func, void *state, object size, object lock,
                                   np.ndarray a_arr, object a_name, constraint_type a_constraint,
                                   np.ndarray b_arr, object b_name, constraint_type b_constraint,
                                   np.ndarray c_arr, object c_name, constraint_type c_constraint):
    cdef np.ndarray randoms
    cdef int64_t *randoms_data
    cdef np.broadcast it
    cdef random_uint_iii f = (<random_uint_iii>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if b_constraint != CONS_NONE:
        check_array_constraint(b_arr, b_name, b_constraint)

    if c_constraint != CONS_NONE:
        check_array_constraint(c_arr, c_name, c_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.int64)
    else:
        it = np.PyArray_MultiIterNew3(a_arr, b_arr, c_arr)
        randoms = <np.ndarray>np.empty(it.shape, np.int64)

    randoms_data = <int64_t *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew4(randoms, a_arr, b_arr, c_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<int64_t*>np.PyArray_MultiIter_DATA(it, 1))[0]
            b_val = (<int64_t*>np.PyArray_MultiIter_DATA(it, 2))[0]
            c_val = (<int64_t*>np.PyArray_MultiIter_DATA(it, 3))[0]
            randoms_data[i] = f(state, a_val, b_val, c_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object discrete_broadcast_i(void *func, void *state, object size, object lock,
                                 np.ndarray a_arr, object a_name, constraint_type a_constraint):
    cdef np.ndarray randoms
    cdef int64_t *randoms_data
    cdef np.broadcast it
    cdef random_uint_i f = (<random_uint_i>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if size is not None:
        randoms = <np.ndarray>np.empty(size, np.int64)
    else:
        randoms = np.PyArray_SimpleNew(np.PyArray_NDIM(a_arr), np.PyArray_DIMS(a_arr), np.NPY_INT64)

    randoms_data = <int64_t *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)

    it = np.PyArray_MultiIterNew2(randoms, a_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<int64_t*>np.PyArray_MultiIter_DATA(it, 1))[0]
            randoms_data[i] = f(state, a_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

# Needs double <vec>, double-double <vec>, double-int64_t<vec>, int64_t <vec>, int64_t-int64_t-int64_t
cdef object disc(void *func, void *state, object size, object lock,
                 int narg_double, int narg_int64,
                 object a, object a_name, constraint_type a_constraint,
                 object b, object b_name, constraint_type b_constraint,
                 object c, object c_name, constraint_type c_constraint):

    cdef double _da = 0, _db = 0
    cdef int64_t _ia = 0, _ib = 0, _ic = 0
    cdef bint is_scalar = True
    if narg_double > 0:
        a_arr = <np.ndarray>np.PyArray_FROM_OTF(a, np.NPY_DOUBLE, np.NPY_ARRAY_ALIGNED)
        is_scalar = is_scalar and np.PyArray_NDIM(a_arr) == 0
        if narg_double > 1:
            b_arr = <np.ndarray>np.PyArray_FROM_OTF(b, np.NPY_DOUBLE, np.NPY_ARRAY_ALIGNED)
            is_scalar = is_scalar and np.PyArray_NDIM(b_arr) == 0
        elif narg_int64 == 1:
            b_arr = <np.ndarray>np.PyArray_FROM_OTF(b, np.NPY_INT64, np.NPY_ARRAY_ALIGNED)
            is_scalar = is_scalar and np.PyArray_NDIM(b_arr) == 0
    else:
        if narg_int64 > 0:
            a_arr = <np.ndarray>np.PyArray_FROM_OTF(a, np.NPY_INT64, np.NPY_ARRAY_ALIGNED)
            is_scalar = is_scalar and np.PyArray_NDIM(a_arr) == 0
        if narg_int64 > 1:
            b_arr = <np.ndarray>np.PyArray_FROM_OTF(b, np.NPY_INT64, np.NPY_ARRAY_ALIGNED)
            is_scalar = is_scalar and np.PyArray_NDIM(b_arr) == 0
        if narg_int64 > 2:
            c_arr = <np.ndarray>np.PyArray_FROM_OTF(c, np.NPY_INT64, np.NPY_ARRAY_ALIGNED)
            is_scalar = is_scalar and np.PyArray_NDIM(c_arr) == 0

    if not is_scalar:
        if narg_int64 == 0:
            if narg_double == 1:
                return discrete_broadcast_d(func, state, size, lock,
                                            a_arr, a_name, a_constraint)
            elif narg_double == 2:
                return discrete_broadcast_dd(func, state, size, lock,
                                             a_arr, a_name, a_constraint,
                                             b_arr, b_name, b_constraint)
        elif narg_int64 == 1:
            if narg_double == 0:
                return discrete_broadcast_i(func, state, size, lock,
                                            a_arr, a_name, a_constraint)
            elif narg_double == 1:
                return discrete_broadcast_di(func, state, size, lock,
                                             a_arr, a_name, a_constraint,
                                             b_arr, b_name, b_constraint)
        else:
            raise NotImplementedError("No vector path available")

    # At this point, we know is_scalar is True.

    if narg_double > 0:
        _da = PyFloat_AsDouble(a)
        if a_constraint != CONS_NONE:
            check_constraint(_da, a_name, a_constraint)

        if narg_double > 1:
            _db = PyFloat_AsDouble(b)
            if b_constraint != CONS_NONE:
                check_constraint(_db, b_name, b_constraint)
        elif narg_int64 == 1:
            _ib = <int64_t>b
            if b_constraint != CONS_NONE:
                check_constraint(<double>_ib, b_name, b_constraint)
    else:
        if narg_int64 > 0:
            _ia = <int64_t>a
            if a_constraint != CONS_NONE:
                check_constraint(<double>_ia, a_name, a_constraint)
        if narg_int64 > 1:
            _ib = <int64_t>b
            if b_constraint != CONS_NONE:
                check_constraint(<double>_ib, b_name, b_constraint)
        if narg_int64 > 2:
            _ic = <int64_t>c
            if c_constraint != CONS_NONE:
                check_constraint(<double>_ic, c_name, c_constraint)

    if size is None:
        with lock:
            if narg_int64 == 0:
                if narg_double == 0:
                    return (<random_uint_0>func)(state)
                elif narg_double == 1:
                    return (<random_uint_d>func)(state, _da)
                elif narg_double == 2:
                    return (<random_uint_dd>func)(state, _da, _db)
            elif narg_int64 == 1:
                if narg_double == 0:
                    return (<random_uint_i>func)(state, _ia)
                if narg_double == 1:
                    return (<random_uint_di>func)(state, _da, _ib)
            else:
                return (<random_uint_iii>func)(state, _ia, _ib, _ic)

    cdef np.npy_intp i, n
    cdef np.ndarray randoms = <np.ndarray>np.empty(size, np.int64)
    cdef np.int64_t *randoms_data
    cdef random_uint_0 f0
    cdef random_uint_d fd
    cdef random_uint_dd fdd
    cdef random_uint_di fdi
    cdef random_uint_i fi
    cdef random_uint_iii fiii

    n = np.PyArray_SIZE(randoms)
    randoms_data = <np.int64_t *>np.PyArray_DATA(randoms)

    with lock, nogil:
        if narg_int64 == 0:
            if narg_double == 0:
                f0 = (<random_uint_0>func)
                for i in range(n):
                    randoms_data[i] = f0(state)
            elif narg_double == 1:
                fd = (<random_uint_d>func)
                for i in range(n):
                    randoms_data[i] = fd(state, _da)
            elif narg_double == 2:
                fdd = (<random_uint_dd>func)
                for i in range(n):
                    randoms_data[i] = fdd(state, _da, _db)
        elif narg_int64 == 1:
            if narg_double == 0:
                fi = (<random_uint_i>func)
                for i in range(n):
                    randoms_data[i] = fi(state, _ia)
            if narg_double == 1:
                fdi = (<random_uint_di>func)
                for i in range(n):
                    randoms_data[i] = fdi(state, _da, _ib)
        else:
            fiii = (<random_uint_iii>func)
            for i in range(n):
                randoms_data[i] = fiii(state, _ia, _ib, _ic)

    return randoms


cdef object cont_broadcast_1_f(void *func, bitgen_t *state, object size, object lock,
                               np.ndarray a_arr, object a_name, constraint_type a_constraint,
                               object out):

    cdef np.ndarray randoms
    cdef float a_val
    cdef float *randoms_data
    cdef np.broadcast it
    cdef random_float_1 f = (<random_float_1>func)
    cdef np.npy_intp i, n

    if a_constraint != CONS_NONE:
        check_array_constraint(a_arr, a_name, a_constraint)

    if size is not None and out is None:
        randoms = <np.ndarray>np.empty(size, np.float32)
    elif out is None:
        randoms = np.PyArray_SimpleNew(np.PyArray_NDIM(a_arr),
                                       np.PyArray_DIMS(a_arr),
                                       np.NPY_FLOAT32)
    else:
        randoms = <np.ndarray>out

    randoms_data = <float *>np.PyArray_DATA(randoms)
    n = np.PyArray_SIZE(randoms)
    it = np.PyArray_MultiIterNew2(randoms, a_arr)
    validate_output_shape(it.shape, randoms)

    with lock, nogil:
        for i in range(n):
            a_val = (<float*>np.PyArray_MultiIter_DATA(it, 1))[0]
            randoms_data[i] = f(state, a_val)

            np.PyArray_MultiIter_NEXT(it)

    return randoms

cdef object cont_f(void *func, bitgen_t *state, object size, object lock,
                   object a, object a_name, constraint_type a_constraint,
                   object out):

    cdef np.ndarray a_arr, b_arr, c_arr
    cdef float _a
    cdef bint is_scalar = True
    cdef int requirements = np.NPY_ARRAY_ALIGNED | np.NPY_ARRAY_FORCECAST
    check_output(out, np.float32, size, True)
    a_arr = <np.ndarray>np.PyArray_FROMANY(a, np.NPY_FLOAT32, 0, 0, requirements)
    is_scalar = np.PyArray_NDIM(a_arr) == 0

    if not is_scalar:
        return cont_broadcast_1_f(func, state, size, lock, a_arr, a_name, a_constraint, out)

    _a = <float>PyFloat_AsDouble(a)
    if a_constraint != CONS_NONE:
        check_constraint(_a, a_name, a_constraint)

    if size is None and out is None:
        with lock:
            return (<random_float_1>func)(state, _a)

    cdef np.npy_intp i, n
    cdef np.ndarray randoms
    if out is None:
        randoms = <np.ndarray>np.empty(size, np.float32)
    else:
        randoms = <np.ndarray>out
    n = np.PyArray_SIZE(randoms)

    cdef float *randoms_data = <float *>np.PyArray_DATA(randoms)
    cdef random_float_1 f1 = <random_float_1>func

    with lock, nogil:
        for i in range(n):
            randoms_data[i] = f1(state, _a)

    if out is None:
        return randoms
    else:
        return out
