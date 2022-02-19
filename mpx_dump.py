# Dumps all images from an MPX file into my lf4 format.

import mpxread
import lf4
from argparse import ArgumentParser
from itertools import chain
from functools import partial



parser = ArgumentParser()
parser.add_argument("mpx", nargs = "*", help = "MPX file(s) to dump")
parser.add_argument("out", help = "Out file path. Should include {} where number will be")
parser.add_argument("-dtype", help = "MPX data type, as a numpy dtype string.", default = "<u2")

args = parser.parse_args()
load = partial(mpxread.load, dtype = args.dtype)

for i, img in enumerate(chain.from_iterable(map(load, args.mpx))):
    lf4.save(args.out.format(i), img)
