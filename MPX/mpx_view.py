import mpxread
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from PIL import Image


parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("-i", "--image-num", type = int, default = 0)
parser.add_argument("-o", "--output", help = "If given, save image instead of displaying")
parser.add_argument("-d", "--data-type", help = "Numpy string representation of data type", default = "u2")

args = parser.parse_args()
imgs = mpxread.load_mpx_imgs(args.file, n = args.image_num+1, dtype = args.data_type)

if args.output:
    Image.fromarray(imgs[-1]).save(args.output)
else:
    plt.imshow(imgs[-1])
    plt.show()
