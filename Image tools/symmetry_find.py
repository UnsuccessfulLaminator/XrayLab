from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from argparse import ArgumentParser



def trans_matrix(dx, dy):
    return np.array(((1, 0, dx), (0, 1, dy), (0, 0, 1)))

def rot_matrix(t):
    s, c = np.sin(t), np.cos(t)
    return np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))

def mirror(img, r, t):
    center = (np.array(img.size)-1)/2
    rot = rot_matrix(-t)
    np.matmul(rot, trans_matrix(*(-center)), out = rot)
    np.matmul(trans_matrix(*center), rot, out = rot)
    derot = np.linalg.inv(rot)

    x_mirror = np.array(((-1, 0, 2*(center[0]+r)), (0, 1, 0), (0, 0, 1)))

    total = np.matmul(x_mirror, rot)
    np.matmul(derot, total, out = total)

    return img.transform(
        img.size, Image.AFFINE, data = total.ravel()[:6], resample = Image.BILINEAR,
        fillcolor = 0
    )

def draw_line(img, r, t):
    center = (np.array(img.size)-1)/2
    m = np.tan(t+np.pi/2)
    p = (r*np.cos(t), r*np.sin(t))
    c = p[1]-m*p[0]
    left = (0, m*(-center[0])+c+center[1])
    right = (img.size[0]-1, m*center[0]+c+center[1])

    print(left[1], right[1])

    draw = ImageDraw.Draw(img)
    draw.line(left+right, fill = 128)

def image_mse(img1, img2):
    a1, a2 = map(np.asarray, (img1, img2))
    return ((a1-a2)**2).mean()

def click(e):
    x, y = e.xdata, e.ydata
    
    print("r =", rs[int(round(y))])
    print("t =", ts[int(round(x))])


parser = ArgumentParser()
parser.add_argument("img1")
parser.add_argument("img2", nargs = "?")

args = parser.parse_args()
img1 = Image.open(args.img1).convert("L")
img2 = Image.open(args.img2).convert("L") if args.img2 else img1
rs = np.linspace(-10, 10, 50)
ts = np.linspace(1, 2, 50, endpoint = False)
mse = np.empty((rs.size, ts.size))

for i, r in enumerate(rs):
    for j, t in enumerate(ts):
        mse[i, j] = image_mse(img1, mirror(img2, r, t))

    print("{:.1f}%".format(i*100/len(rs)), end = "\r")

print()

mse = ndimage.gaussian_filter(mse, 2)
argmin = np.unravel_index(mse.argmin(), mse.shape)
r, t = rs[argmin[0]], ts[argmin[1]]

print(f"Global minimum: r, t = {r}, {t}")

plt.subplot(1, 3, 1)
plt.imshow(img1)
plt.subplot(1, 3, 2)
plt.imshow(mirror(img2, r, t))
plt.subplot(1, 3, 3)
plt.imshow(mse)
plt.plot(*np.unravel_index(mse.argmin(), mse.shape)[::-1], "ro")
plt.gcf().canvas.mpl_connect("button_press_event", click)
plt.show()
