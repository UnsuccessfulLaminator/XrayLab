#include <gsl/gsl_interp2d.h>
#include <gsl/gsl_spline2d.h>
#include <stdlib.h>
#include <stdio.h>



typedef struct {
    gsl_spline2d *spline;
    gsl_interp_accel *xAccel, *yAccel;
} Interp;

Interp *newInterp(
    const double *xs, size_t nx, const double *ys, size_t ny, const double *zs
) {
    Interp *i = malloc(sizeof(Interp));
    i->spline = gsl_spline2d_alloc(gsl_interp2d_bilinear, nx, ny);
    i->xAccel = gsl_interp_accel_alloc();
    i->yAccel = gsl_interp_accel_alloc();

    gsl_spline2d_init(i->spline, xs, ys, zs, nx, ny);

    return i;
}

void freeInterp(Interp *i) {
    gsl_spline2d_free(i->spline);
    gsl_interp_accel_free(i->xAccel);
    gsl_interp_accel_free(i->yAccel);

    free(i);
}

double evalInterp(Interp *i, double x, double y) {
    gsl_interp2d *iObj = &(i->spline->interp_object);

    if(x >= iObj->xmin && x <= iObj->xmax && y >= iObj->ymin && y <= iObj->ymax) {
        return gsl_spline2d_eval(i->spline, x, y, i->xAccel, i->yAccel);
    }
    else return 0;
}

void evalManyInterp(Interp *i, const double *xs, const double *ys, size_t n, double *out) {
    for(size_t idx = 0; idx < n; idx++) {
        out[idx] = evalInterp(i, xs[idx], ys[idx]);
    }
}
