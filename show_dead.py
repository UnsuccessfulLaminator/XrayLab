import lf4
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np



parser = ArgumentParser()
parser.add_argument("file", help = "LF4 file to display")

args = parser.parse_args()
img = lf4.load(args.file)
s = img.std()
m = img.mean()
zeros = np.argwhere(img < m-4*s)

print(m-4*s)

plt.imshow(img)
plt.plot(zeros[:, 1], zeros[:, 0], "ro")
plt.show()
