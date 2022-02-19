from . import load
from argparse import ArgumentParser
from os import path
import matplotlib.pyplot as plt



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to convert to images")
parser.add_argument("out_dir", help = "Output directory to place images in")
parser.add_argument("-f", "--format", help = "Image format, e.g. 'png', 'jpg', etc", default = "png")
parser.add_argument("-c", "--color-map", help = "Matplotlib color map", default = "viridis")
parser.add_argument("-t0", type = float, help = "Lower color map threshold")
parser.add_argument("-t1", type = float, help = "Upper color map threshold")

args = parser.parse_args()

if not path.isdir(args.out_dir):
    print("Argument out_dir must specify a directory")
    exit(1)

for f in args.file:
    img = load(f)
    name = path.basename(f)
    name = name[:name.rfind(".")+1]+args.format
    out_path = path.join(args.out_dir, name)

    plt.imsave(out_path, img, cmap = args.color_map, vmin = args.t0, vmax = args.t1)
