import interp
import numpy as np



data = np.zeros((8, 8))
data[1, 1] = 10

p = interp.Interp2D()
p.set_data(1, 1, data)

xs = np.random.random(256)*7
ys = np.random.random(256)*7

print(p(xs, ys))
