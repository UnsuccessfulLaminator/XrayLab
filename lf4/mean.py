from . import load, save
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 files to take the mean of")
parser.add_argument("out_file", help = "Destination file")

args = parser.parse_args()
mean = sum(map(load, args.file))/len(args.file)

save(args.out_file, mean)
