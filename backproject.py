import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import xrayutils
import os
from PIL import Image
import re
from itertools import count



parser = ArgumentParser()
parser.add_argument("-t0", type = float, help = "Lower threshold for saved image values")
parser.add_argument("-t1", type = float, help = "Upper threshold for saved image values")
parser.add_argument("-p", "--plot", action = "store_true")
parser.add_argument("projection", help = "Image file/dir containing xray projection data")
parser.add_argument("out_file", help = "Destination/base name for backprojected image(s)")

args = parser.parse_args()
ray_xs = np.linspace(-127.5, 127.5, 256)
angles = np.linspace(0, np.pi*2, 360, endpoint = False)
proj_files = []
out_files = []

if os.path.isdir(args.projection):
    def alpha_num_key(s):
        return [ int(w) if w.isdigit() else w for w in re.split(r"(\d+)", s) ]

    for filename in sorted(os.listdir(args.projection), key = alpha_num_key):
        full_name = os.path.join(args.projection, filename)
        if os.path.isfile(full_name): proj_files.append(full_name)
    
    for i in range(len(proj_files)):
        out_files.append(args.out_file+f"{i}.png")
elif os.path.isfile(args.projection):
    proj_files.append(args.projection)
    out_files.append(args.out_file)
else:
    print("Projection file/dir is invalid!")
    exit(1)

def filter_func(w):
    return np.abs(w)*np.hanning(w.size*2)[w.size:]

for i, in_file, out_file in zip(count(), proj_files, out_files):
    img = Image.open(in_file)
    proj = np.asarray(img.convert("I")).astype(np.float64)
    proj = xrayutils.filter_projection(proj, filter_func)
    backproj = xrayutils.backproject(proj, ray_xs, angles, 256)
    
    if args.plot:
        plt.imshow(backproj, vmin = args.t0, vmax = args.t1, cmap = "gray")
        plt.show()

    plt.imsave(out_file, backproj, vmin = args.t0, vmax = args.t1, cmap = "gray")

    print(f"{i+1}/{len(proj_files)} files completed")
