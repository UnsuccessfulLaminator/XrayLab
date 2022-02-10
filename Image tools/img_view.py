#!/bin/python3

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("-c", "--color-map", default = "gray")
parser.add_argument("-o", "--output")

args = parser.parse_args()
img = Image.open(args.file)
data = np.asarray(img)

plt.imshow(data, cmap = args.color_map)
plt.show()

if args.output:
    plt.imsave(args.output, data, cmap = args.color_map)
