#include "line.hpp"



double Line::getY(double x) const {
    double c = cos(t), s = sin(t);
    return r*s-c*(x-r*c)/s;
};

double Line::getX(double y) const {
    double c = cos(t), s = sin(t);
    return (r*s-y)*(s/c)+r*c;
}

Line Line::translate(double dx, double dy) const {
    double c = cos(t), s = sin(t);
    return Line{r+c*dx+s*dy, t};
};

Line Line::rotate(const Point &center, double angle) const {
    Line l1 = translate(-center.x, -center.y);
    l1.t = fmod(l1.t+angle, M_PI*2);

    return l1.translate(center.x, center.y);
}

double Line::lengthInsideBounds(const Point &min, const Point &max) const {
    // std::cerr << "Call to lengthInsideRect with params:\n";
    // std::cerr << "\tp0 = (" << min.x << ", " << min.y << ")\n";
    // std::cerr << "\tp1 = (" << max.x << ", " << max.y << ")\n";
    // std::cerr << "\tray = (r = " << line.r << ", t = " << line.t << ")\n";

    Point inter0{min.x, getY(min.x)};
    Point inter1{max.x, getY(max.x)};
    Point inter2{getX(min.y), min.y};
    Point inter3{getX(max.y), max.y};

    Point *inter;
    bool found = false;

    if(inter0.y >= min.y && inter0.y <= max.y) {
        inter = &inter0;
        found = true;
    }

    if(inter1.y >= min.y && inter1.y <= max.y) {
        if(found) return inter->dist(inter1);
        else {
            inter = &inter1;
            found = true;
        }
    }

    if(inter2.x >= min.x && inter2.x <= max.x) {
        if(found) return inter->dist(inter2);
        else {
            inter = &inter2;
            found = true;
        }
    }

    if(inter3.x >= min.x && inter3.x <= max.x && found) {
        return inter->dist(inter3);
    }

    return 0;
}
