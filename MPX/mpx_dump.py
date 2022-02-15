import mpxread
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from PIL import Image
import numpy as np



parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("out")
parser.add_argument("-d", "--data-type", help = "Numpy string representation of data type", default = "u2")
parser.add_argument("-c", "--color-map", help = "Pyplot color map", default = "gray")
parser.add_argument("-b", "--bias", help = "Bias image to subtract")

args = parser.parse_args()
imgs = mpxread.load_mpx_imgs(args.file, dtype = args.data_type)

if args.bias:
    with Image.open(args.bias) as bias:
        imgs = imgs.astype("i2")
        for img in imgs: img -= bias
        imgs = np.clip(-imgs, 0, None)

for i, img in enumerate(imgs):
    plt.imsave(args.out+f"{i}.png", img, cmap = args.color_map)
