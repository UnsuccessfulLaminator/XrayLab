#include "point.hpp"



double Point::dist(const Point &other) const {
    return hypot(x-other.x, y-other.y);
}
