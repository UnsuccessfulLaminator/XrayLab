import numpy as np
from scipy import interpolate, fft
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from PIL.PngImagePlugin import PngImageFile



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


parser = ArgumentParser()
parser.add_argument("projection", help = "Image file containing the xray projection data")

args = parser.parse_args()
img = PngImageFile(args.projection)
ray_xs = np.fromiter(map(float, img.text["ray_xs"].split(",")), dtype = np.float64)
angles = np.fromiter(map(float, img.text["angles"].split(",")), dtype = np.float64)

proj = np.asarray(img, dtype = np.uint8)

# If the image has multiple color components, average them into one
if len(proj.shape) == 3: proj = proj[:, :, :3].mean(axis = 2)

proj = filter_projection(proj, lambda w: np.abs(w))
backproj = gen_backprojection(proj, ray_xs, angles, 256)

plt.imshow(backproj)
plt.show()

plt.imsave("backproj.png", backproj)
