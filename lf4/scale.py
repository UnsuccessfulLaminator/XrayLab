from . import load, save
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to scale")
parser.add_argument("value", type = float, help = "Value by which to scale")

args = parser.parse_args()

for f in args.file: save(f, load(f)*args.value)
