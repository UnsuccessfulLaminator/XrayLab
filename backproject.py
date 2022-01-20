import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from PIL.PngImagePlugin import PngImageFile
import xrayutils



parser = ArgumentParser()
parser.add_argument("projection", help = "Image file containing the xray projection data")

args = parser.parse_args()
img = PngImageFile(args.projection)
ray_xs = np.fromiter(map(float, img.text["ray_xs"].split(",")), dtype = np.float64)
angles = np.fromiter(map(float, img.text["angles"].split(",")), dtype = np.float64)

proj = np.asarray(img, dtype = np.uint8)

# If the image has multiple color components, average them into one
if len(proj.shape) == 3: proj = proj[:, :, :3].mean(axis = 2)

proj = xrayutils.filter_projection(proj, lambda w: np.abs(w))
backproj = xrayutils.gen_backprojection(proj, ray_xs, angles, 256)

plt.imshow(backproj)
plt.show()

plt.imsave("backproj.png", backproj)
