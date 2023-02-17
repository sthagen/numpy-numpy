#ifndef NUMPY_SRC_COMMON_NPYSORT_SIMD_QSORT_HPP
#define NUMPY_SRC_COMMON_NPYSORT_SIMD_QSORT_HPP

#include "common.hpp"

namespace np { namespace qsort_simd {

#ifndef NPY_DISABLE_OPTIMIZATION
    #include "simd_qsort.dispatch.h"
#endif
NPY_CPU_DISPATCH_DECLARE(template <typename T> void QSort, (T *arr, intptr_t size))

#ifndef NPY_DISABLE_OPTIMIZATION
    #include "simd_qsort_16bit.dispatch.h"
#endif
NPY_CPU_DISPATCH_DECLARE(template <typename T> void QSort, (T *arr, intptr_t size))

} } // np::qsort_simd
#endif // NUMPY_SRC_COMMON_NPYSORT_SIMD_QSORT_HPP
