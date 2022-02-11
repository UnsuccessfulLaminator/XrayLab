import mpxread
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
import cv2



parser = ArgumentParser()
parser.add_argument("mpx_file", help = "MPX containing the 2D projections")
parser.add_argument("-s", "--start", type = int, default = 0)
parser.add_argument("-n", "--number", type = int, default = -1)
parser.add_argument("-b", "--bias-img", help = "Image to subtract off each 2D projection")
parser.add_argument("-d", "--dead-map", help = "Image file with dead pixels as non-zero")
parser.add_argument("-t", "--translate", type = float, help = "Apply horizontal translation to outputs")
parser.add_argument("-dt", type = float)
parser.add_argument("-dtype", help = "Numpy string dtype of the mpx data", default = "u2")
parser.add_argument("-g", "--gaussian", type = float, default = 0, help = "Gaussian blur")
parser.add_argument("out_base_name", help = "Base name of output projection files")

args = parser.parse_args()
start, num = args.start, args.number
imgs = mpxread.load_mpx_imgs(args.mpx_file, dtype = args.dtype)
n_angles, n_rays, n_slices = imgs.shape

if args.dead_map:
    dead = Image.open(args.dead_map).convert("I")
    dead = np.asarray(dead, dtype = np.uint8)
    
    for i, img in enumerate(imgs):
        imgs[i] = cv2.inpaint(img, dead, inpaintRadius = 3, flags = cv2.INPAINT_TELEA)

if args.gaussian > 0:
    for img in imgs:
        ndimage.gaussian_filter(img, args.gaussian, output = img)

imgs = imgs.astype(np.int16)

if args.bias_img:
    bias = Image.open(args.bias_img).convert("I;16")
    bias = np.asarray(bias)

    for img in imgs: img -= bias

imgs = np.clip(-imgs, 0, None)
imgs = imgs.astype(np.uint16)

if num < 0: end = n_slices
else: end = start+num

for i in range(start, end):
    proj = imgs[:, :, i]

    if args.translate:
        shift = int(round(args.translate+(i-start)*args.dt))
        proj = np.roll(proj, shift, axis = 1)
        
        if shift < 0: proj[:, shift:] = 0
        else: proj[:, :shift] = 0

    filename = args.out_base_name+f"{i}.png"
    Image.fromarray(proj).save(filename)

    print(f"\r{i-start+1}/{end-start} files completed", end = "")

print()
