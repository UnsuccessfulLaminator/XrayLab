from distutils.core import setup, Extension
import os



module = Extension(
    "gridcoeffs",
    sources = ["gridcoeffs.cpp", "point.cpp", "line.cpp"],
    include_dirs = ["/usr/local/lib/python3.8/dist-packages/numpy/core/include"],
    extra_compile_args = ["-O3"]
)

setup(
    name = "gridcoeffs",
    ext_modules = [module]
)

os.system("mv build/lib*/gridcoeffs* .")
