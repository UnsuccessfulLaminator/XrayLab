import lf4
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to flat-field correct")
parser.add_argument("bias", help = "Bias image, i.e. image taken with no object")

args = parser.parse_args()
bias = lf4.load(args.bias)

for f in args.file:
    img = lf4.load(f)
    img /= bias
    zeros = img == 0
    img[zeros] = img[~zeros].min()
    np.log(img, out = img)
    img *= -1
    np.clip(img, 0, None, out = img)
    
    lf4.save(f, img)
