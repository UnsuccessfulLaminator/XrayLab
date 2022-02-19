import matplotlib.pyplot as plt
from argparse import ArgumentParser
from . import load



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 file(s) to view")
parser.add_argument("-t0", type = float, help = "Lower color map threshold")
parser.add_argument("-t1", type = float, help = "Upper color map threshold")
parser.add_argument("-c", help = "Matplotlib color map", default = "viridis")

args = parser.parse_args()
img_num = 0
imgs = list(map(load, args.file))

def on_press(e):
    global img_num

    if e.key == "right": img_num += 1
    elif e.key == "left": img_num -= 1

    img_num %= len(imgs)

    plt.imshow(imgs[img_num], cmap = args.c, vmin = args.t0, vmax = args.t1)
    plt.title(args.file[img_num])
    plt.gcf().canvas.draw()

plt.imshow(imgs[0], cmap = args.c, vmin = args.t0, vmax = args.t1)
plt.title(args.file[0])
plt.gcf().canvas.mpl_connect("key_press_event", on_press)
plt.show()
