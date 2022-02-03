import ctypes
from ctypes import c_size_t as size_t
import numpy as np



_lib = ctypes.CDLL("./libinterp.so")

double_ptr_t = ctypes.POINTER(ctypes.c_double)

_interp = _lib.interp
_interp.argtypes = [
    double_ptr_t, size_t, double_ptr_t, size_t, double_ptr_t,
    double_ptr_t, double_ptr_t, size_t, double_ptr_t
]

def _as_double_ptr(arr):
    return arr.ctypes.data_as(double_ptr_t)

def interp(xs, ys, zs, ixs, iys):
    def convert(arr):
        return np.ascontiguousarray(arr, dtype = np.float64)
    
    xs, ys, zs, ixs, iys = map(convert, (xs, ys, zs, ixs, iys))
    
    if zs.size != xs.size*ys.size:
        raise ValueError("Size of z array must be product of sizes of x and y arrays")
    if ixs.size != iys.size:
        raise ValueError("Interpolation x and y arrays must have same size")

    out = np.empty(ixs.size, dtype = np.float64)

    _interp(
        _as_double_ptr(xs), xs.size,
        _as_double_ptr(ys), ys.size,
        _as_double_ptr(zs),
        _as_double_ptr(ixs), _as_double_ptr(iys), ixs.size,
        _as_double_ptr(out)
    )

    return out
