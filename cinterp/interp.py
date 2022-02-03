from ctypes import CDLL, POINTER, c_double, c_size_t, c_void_p
import numpy as np



lib = CDLL("./libinterp.so")
c_double_p = POINTER(c_double)

lib.newInterp.argtypes = [c_double_p, c_size_t, c_double_p, c_size_t, c_double_p]
lib.newInterp.restype = c_void_p

lib.freeInterp.argtypes = [c_void_p]
lib.freeInterp.restype = None

lib.evalInterp.argtypes = [c_void_p, c_double, c_double]
lib.evalInterp.restype = c_double

lib.evalManyInterp.argtypes = [c_void_p, c_double_p, c_double_p, c_size_t, c_double_p]
lib.evalManyInterp.restype = None

def _as_double_p(arr):
    return arr.ctypes.data_as(c_double_p)

def _convert_arr(arr):
    return np.ascontiguousarray(arr, dtype = np.float64)

class Interp:
    def __init__(self, xs, ys, zs):
        xs, ys, zs = map(_convert_arr, (xs, ys, zs))

        if zs.size != xs.size*ys.size:
            raise ValueError("Size of z array must be product of sizes of x and y arrays")

        self.ptr = lib.newInterp(
            _as_double_p(xs), xs.size,
            _as_double_p(ys), ys.size,
            _as_double_p(zs)
        )

    def __call__(self, xs, ys):
        xs, ys = map(_convert_arr, (xs, ys))

        if xs.size != ys.size:
            raise ValueError("Interpolation x and y arrays must have same size")

        out = np.empty(xs.size, dtype = np.float64)

        lib.evalManyInterp(
            self.ptr, _as_double_p(xs), _as_double_p(ys), xs.size, _as_double_p(out)
        )

        return out

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        lib.freeInterp(self.ptr)
