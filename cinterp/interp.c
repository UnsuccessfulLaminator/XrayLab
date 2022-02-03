#include <gsl/gsl_interp2d.h>
#include <gsl/gsl_spline2d.h>
#include <stdio.h>



void interp(
    const double *xs, size_t nx, const double *ys, size_t ny, const double *zs,
    const double *ixs, const double *iys, size_t n, double *is
) {
    gsl_spline2d *spl = gsl_spline2d_alloc(gsl_interp2d_bilinear, nx, ny);
    gsl_interp_accel *xacc = gsl_interp_accel_alloc();
    gsl_interp_accel *yacc = gsl_interp_accel_alloc();

    gsl_spline2d_init(spl, xs, ys, zs, nx, ny);

    printf("x range is [%lf, %lf], y range is [%lf, %lf]\n", xs[0], xs[nx-1], ys[0], ys[ny-1]);

    for(size_t i = 0; i < n; i++) {
        printf("Evaluating at (%lf, %lf)\n", ixs[i], iys[i]);
        is[i] = gsl_spline2d_eval(spl, ixs[i], iys[i], xacc, yacc);
    }

    gsl_spline2d_free(spl);
    gsl_interp_accel_free(xacc);
    gsl_interp_accel_free(yacc);
}
