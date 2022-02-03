import interp
import numpy as np



xs = np.linspace(0, 1, 10)
ys = xs
zs = np.random.random((10, 10))*100
ixs = np.random.random(65536)
iys = np.random.random(65536)

print(interp.interp(xs, ys, zs, ixs, iys))
