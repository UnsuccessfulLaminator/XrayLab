#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "numpy/arrayobject.h"

#include "point.hpp"
#include "line.hpp"



static PyObject *Py_grid_coeffs(PyObject *self, PyObject *args);

// Defines all the methods that will be in the module
static PyMethodDef gridcoeffsMethods[] = {
    {"grid_coeffs", Py_grid_coeffs, METH_VARARGS, nullptr},
    {nullptr, nullptr, 0, nullptr}
};

// Defines the module itself
static PyModuleDef gridcoeffsModule{
    PyModuleDef_HEAD_INIT,
    "gridcoeffs", nullptr, -1, gridcoeffsMethods
};

// Pull numpy in, and create a new module from the descriptor above
PyMODINIT_FUNC PyInit_gridcoeffs() {
    import_array();

    if(PyErr_Occurred()) return nullptr;
    else return PyModule_Create(&gridcoeffsModule);
}



// This is a template function so unfortunately it can't have a prototype higher up.
// Parameters:
//     coeffs           - Iterator over coefficient destination (container of numbers)
//     step             - Size of the grid step
//     p0               - Center of the grid square with lowest x and y
//     nx, ny           - Dimensions of the grid
//     rayBegin, rayEnd - Iterators over the range of rays (container of Line)
// Returns nothing.
// This is essentially a take on Bresenham's line algorithm.
template<typename InputIt, typename OutputIt>
void gridCoeffs(
    OutputIt coeffs,
    double step, const Point &p0, int nx, int ny, InputIt rayBegin, InputIt rayEnd
) {
    unsigned int rayIdx = 0;

    for(InputIt it = rayBegin; it != rayEnd; it++) {
        const Line &ray = *it;
        double m = -1/tan(ray.t);
        
        if(abs(m) <= 1) {
            double x = p0.x;
            double y = ray.getY(p0.x), dy = m*step;

            for(int i = 0; i < nx; i++) {
                int j0 = round((y-p0.y)/step)-1;
                double ySnap = p0.y+step*j0;

                for(int j = j0; j <= j0+2; j++) {
                    if(j >= 0 && j < ny) {
                        coeffs[nx*ny*rayIdx + nx*j + i] += ray.lengthInsideBounds(
                            Point{x-step/2, ySnap-step/2}, Point{x+step/2, ySnap+step/2}
                        );
                    }

                    ySnap += step;
                }

                x += step;
                y += dy;
            }
        }
        else {
            double x = ray.getX(p0.y), dx = step/m;
            double y = p0.y;

            for(int j = 0; j < ny; j++) {
                int i0 = round((x-p0.x)/step)-1;
                double xSnap = p0.x+step*i0;

                for(int i = i0; i <= i0+2; i++) {
                    if(i >= 0 && i < nx) {
                        coeffs[nx*ny*rayIdx + nx*j + i] += ray.lengthInsideBounds(
                            Point{xSnap-step/2, y-step/2}, Point{xSnap+step/2, y+step/2}
                        );
                    }

                    xSnap += step;
                }

                x += dx;
                y += step;
            }
        }

        rayIdx++;
    }
}

// Python+numpy wrapper around the function above.
static PyObject *Py_grid_coeffs(PyObject *self, PyObject *args) {
    double step;
    Point p0;
    unsigned int nx, ny;
    PyObject *pyRays_;
    PyArrayObject *out = nullptr;
    
    // Parse the input arguments. This doesn't increment any refcounts
    if(!PyArg_ParseTuple(
        args, "dddkkO|O!",
        &step, &p0.x, &p0.y, &nx, &ny, &pyRays_, &PyArray_Type, &out
    )) return nullptr;
    
    // Convert the rays argument into a C-contiguous numpy array of doubles, if needed
    if(!(pyRays_ = PyArray_FROM_OTF(pyRays_, PyArray_DOUBLE, NPY_ARRAY_CARRAY_RO))) {
        return nullptr;
    }
    
    // Done purely for type conversion
    PyArrayObject *pyRays = (PyArrayObject*) pyRays_;
    
    // Check the array of rays actually has the right shape, and complain if it doesn't.
    if(pyRays->nd != 2 || pyRays->dimensions[1] != 2) {
        PyErr_SetString(PyExc_ValueError, "rays must have shape (*, 2)");
        Py_DECREF(pyRays_);

        return nullptr;
    }

    npy_intp n = pyRays->dimensions[0];
    
    // If a destination array wasn't given, make a new one full of zeros. Otherwise, make
    // sure the array given has the right shape.
    if(!out) {
        npy_intp dims[] = {n, nx*ny};
        out = (PyArrayObject*) PyArray_ZEROS(2, dims, PyArray_DOUBLE, 0);
    }
    else if(out->nd != 2 || out->dimensions[0] != n || out->dimensions[1] != nx*ny) {
        PyErr_SetString(PyExc_ValueError, "out must have shape (rays.size, nx*ny)");
        Py_DECREF(pyRays_);

        return nullptr;
    }
    else if(out->descr->type_num != PyArray_FLOAT64) {
        PyErr_SetString(PyExc_ValueError, "out must have dtype float64");
        Py_DECREF(pyRays_);

        return nullptr;
    }
    
    // Calculate
    double *coeffs = (double*) ((PyArrayObject*) out)->data;
    Line *rayBegin = (Line*) pyRays->data;
    gridCoeffs(coeffs, step, p0, nx, ny, rayBegin, rayBegin+n);
    
    Py_DECREF(pyRays_);
    Py_INCREF(out);

    return (PyObject*) out;
}
