from distutils.core import setup, Extension
import os
from glob import glob
import numpy as np



module = Extension(
    "gridcoeffs",
    sources = ["gridcoeffs.cpp", "point.cpp", "line.cpp"],
    include_dirs = [np.get_include()],
    extra_compile_args = ["-O3"]
)

setup(
    name = "gridcoeffs",
    ext_modules = [module]
)

lib_file = glob(os.sep.join(["build", "lib*", "gridcoeffs*"]))[0]
dest = "."+lib_file[lib_file.rfind(os.sep):]

os.rename(lib_file, dest)
