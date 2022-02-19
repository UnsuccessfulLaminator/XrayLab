from . import load, save
from argparse import ArgumentParser
from scipy import ndimage
import numpy as np



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to scale")
parser.add_argument("angle", type = float, help = "Angle (deg) by which to rotate image")
parser.add_argument("dx", type = float, help = "Amount to shift image in x")
parser.add_argument("dy", type = float, help = "Amount to shift image in y")
parser.add_argument("-fa", "--final-angle", type = float)
parser.add_argument("-fdx", "--final-dx", type = float)
parser.add_argument("-fdy", "--final-dy", type = float)

args = parser.parse_args()
final_angle = args.final_angle if args.final_angle is not None else args.angle
final_dx = args.final_dx if args.final_dx is not None else args.dx
final_dy = args.final_dy if args.final_dy is not None else args.dy
n = len(args.file)
angles = np.linspace(args.angle, final_angle, n)
dxs = np.linspace(args.dx, final_dx, n)
dys = np.linspace(args.dy, final_dy, n)

for i, f in enumerate(args.file):
    img = load(f)

    ndimage.rotate(img, angles[i], reshape = False, output = img)
    ndimage.shift(img, (-dys[i], dxs[i]), output = img)
    
    save(f, img)
