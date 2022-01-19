#pragma once

#include "point.hpp"



struct Line{
    double r, t;

    Line(double r_, double t_) : r(r_), t(t_) {}
    
    double getY(double x) const;
    double getX(double y) const;
    Line translate(double dx, double dy) const;
    Line rotate(const Point &center, double angle) const;
    double lengthInsideBounds(const Point &min, const Point &max) const;
};
