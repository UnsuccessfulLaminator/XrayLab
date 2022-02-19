import lf4
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to inpaint")
parser.add_argument("map", help = "LF4 file where pixels to inpaint are non-zero")

args = parser.parse_args()
paint_map = lf4.load(args.map)

def inpaint(img, where):
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            if where[r, c]:
                img[r, c] = (img[r-1, c]+img[r, c-1])/2

for f in args.file:
    img = lf4.load(f)
    inpaint(img, paint_map)
    lf4.save(f, img)
