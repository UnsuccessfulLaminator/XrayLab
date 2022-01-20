import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from PIL.PngImagePlugin import PngInfo
import PIL.Image as Image
import xrayutils



# Plot a shapely Polygon with pyplot
def plot_poly(poly, *args, **kwargs):
    xs, ys = np.array(poly.exterior.coords).T
    plt.fill(xs, ys, *args, **kwargs)


# Example scene with a square and a small circle, both with density 1
objects = [
    (Polygon([(-7, -3), (-1, -3), (-1, 3), (-7, 3)]), 1),
    (Point(5, 0).buffer(0.3), 1)
]
stage_center = (0, 0)
x_range = (-10, 10)
y_range = (-10, 10)
n_rays = 256
n_angles = 180

plt.subplot(1, 2, 1)
for obj, d in objects: plot_poly(obj)
plt.title("Original scene")
plt.xlim(*x_range)
plt.ylim(*y_range)
plt.gca().set_aspect(1)

render = xrayutils.render(
    objects, x_range[0], x_range[0], n_rays, n_rays, (x_range[1]-x_range[0])/n_rays
)
plt.imsave("scene.png", render)

ray_xs = np.linspace(*x_range, n_rays)
angles = np.linspace(0, np.pi, n_angles, endpoint = False)
projection = xrayutils.gen_projections(objects, ray_xs, y_range, angles, stage_center)

plt.subplot(1, 2, 2)
plt.imshow(projection, cmap = "gray")
plt.show()

projection -= projection.min()
projection *= 255/projection.max()
img = Image.fromarray(projection.astype("uint8")).convert("L")
meta = PngInfo()
meta.add_text("ray_xs", ",".join(map(str, ray_xs)))
meta.add_text("angles", ",".join(map(str, angles)))
img.save("projection.png", pnginfo = meta)
