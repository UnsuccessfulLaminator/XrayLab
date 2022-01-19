#pragma once

#include <cmath>



struct Point{
    double x, y;

    Point(double x_, double y_) : x(x_), y(y_) {}
    Point() : x(0), y(0) {}

    double dist(const Point &other) const;
};
