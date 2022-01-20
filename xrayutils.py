from shapely.geometry import Point, LineString
from shapely import affinity
import numpy as np
from scipy import interpolate, fft



# Parameters:
#     ray     - LineString with 2 points, representing a single ray
#     poly    - Polygon representing an object which the ray may pass through
#     density - the object's density
# Returns the line integral of the ray through the object.
def find_ray_integral(ray, poly, density):
    ints = list(map(Point, poly.intersection(ray).coords))
    
    if len(ints) == 0: return 0
    elif len(ints) == 2: return ints[0].distance(ints[1])*density
    elif len(ints) > 2: raise ValueError("Non-convex polygon")


# Parameters:
#     objects - list of (object, density) where object is a Polygon and density is a number
#     ray_xs  - x-coordinates of the rays to simulate passing through the objects
#     y_range - tuple of the form (start, end) giving the extent of the rays
#     angles  - angles at which to take projections
#     center  - center around which to rotate
# Returns a 2D array of projections, where each row corresponds to an angle, each column to
# a ray.
def gen_projections(objects, ray_xs, y_range, angles, center):
    projection = np.zeros((len(angles), len(ray_xs)), dtype = np.float64)
    rays = [ LineString(((x, y_range[0]), (x, y_range[1]))) for x in ray_xs ]

    for i, angle in enumerate(angles):
        for poly, density in objects:
            poly = affinity.rotate(poly, angle, center, use_radians = True)
            
            for j, ray in enumerate(rays):
                projection[i, j] += find_ray_integral(ray, poly, density)

    return projection


# Parameters:
#     objects - list of (object, density) where object is a Polygon and density is a number
#     x0, y0  - coordinate of center of pixel with lowest x and y values
#     nx, ny  - dimensions of the pixel grid
#     step    - step size of the pixel grid
# Returns a 2D array of pixels whose values are densities.
def render(objects, x0, y0, nx, ny, step):
    pixels = np.zeros((nx, ny))
    
    for i, x in enumerate(x0+np.arange(nx)*step):
        for j, y in enumerate(y0+np.arange(ny)*step):
            for poly, density in objects:
                if poly.contains(Point(x, y)): pixels[j, i] += density

    return pixels


# Parameters:
#     projection  - 2D array of projection data, each row corresponding to an angle
#     filter_func - function in angular frequency space with which the projections will be
#                   filtered. Default value is f(w) = |w|
# Returns a 2D array of filtered projection data, the same shape as the input data
def filter_projection(projection, filter_func = lambda w: np.abs(w)):
    proj_ft = fft.rfft(projection, axis = 1)
    filt = filter_func(fft.rfftfreq(projection.shape[1])*2*np.pi)
    proj_ft[:] *= filt
    
    return fft.irfft(proj_ft, axis = 1)


# Parameters:
#     projection    - 2D array of projection data, each row corresponding to an angle
#     ray_xs        - x-coordinates of the rays which passed through the scene
#     angles        - angles at which projections were taken
#     backproj_size - pixel width of the backprojected image
# Returns a 2D array containing the backprojected image.
def gen_backprojection(projection, ray_xs, angles, backproj_size):
    print(len(angles), len(ray_xs), projection.shape)

    xs = np.linspace(ray_xs.min(), ray_xs.max(), backproj_size)
    backproj = np.zeros((backproj_size,)*2)
    p = interpolate.RectBivariateSpline(angles, ray_xs, projection, kx = 1, ky = 1)
    ss = np.empty_like(backproj)

    for angle in angles:
        cos = np.cos(angle)
        sin = np.sin(angle)
        ss[:] = xs*cos
        ss.T[:] += xs*sin

        backproj += p(angle, ss, grid = False)
    
    return backproj
