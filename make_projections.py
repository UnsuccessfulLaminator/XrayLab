import lf4
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to reshape")
parser.add_argument("-s", "--start", type = int, default = 0)
parser.add_argument("-n", "--number", type = int, default = -1)
parser.add_argument("out_base_name", help = "Base name of output projection files")

args = parser.parse_args()
start, num = args.start, args.number
imgs = np.array(list(map(lf4.load, args.file)))
n_angles, n_rays, n_slices = imgs.shape

if num < 0: end = n_slices
else: end = start+num

for i in range(start, end):
    proj = imgs[:, :, i]
    filename = args.out_base_name+f"{i}.f4"

    lf4.save(filename, proj)

    print(f"\r{i-start+1}/{end-start} files completed", end = "")

print()
