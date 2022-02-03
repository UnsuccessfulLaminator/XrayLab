from interp import Interp
import numpy as np



xs = np.linspace(0, 1, 10)
ys = xs
zs = np.random.random((10, 10))*100
ixs = np.random.random(65536)
iys = np.random.random(65536)

with Interp(xs, ys, zs) as i:
    print(i(ixs, iys))
