import numpy as np
import matplotlib.pyplot as plt
from PIL.PngImagePlugin import PngInfo
import PIL.Image as Image
from gridcoeffs import grid_coeffs



def translate_line(r, t, dx, dy):
    return r+np.cos(t)*dx+np.sin(t)*dy, t

def rotate_line(r, t, cx, cy, angle):
    r, t = translate_line(r, t, -cx, -cy)
    t = (t+angle)%(np.pi*2)
    
    return translate_line(r, t, cx, cy)


step = 1
nx, ny = 256, 256
p0 = (0.5-nx/2, 0.5-ny/2)
ray_xs = p0[0]+np.arange(nx)*step
rays = [ (x, 0) for x in ray_xs ]
n_angles = 180
angles = np.linspace(0, np.pi, n_angles, endpoint = False)

img = plt.imread("../backproj.png")
img = img[:, :, 0]
img.shape = (img.size,)

proj = np.empty((n_angles, len(rays)))

for i, angle in enumerate(angles):
    coeffs = grid_coeffs(step, *p0, nx, ny, rays)
    coeffs.shape = (len(rays), nx*ny)

    proj[i] = np.matmul(coeffs, img)

    for j, ray in enumerate(rays): rays[j] = rotate_line(*ray, 0, 0, np.pi/n_angles)

plt.imshow(proj, cmap = "gray")
plt.show()

proj *= 255/proj.max()
img = Image.fromarray(proj.astype("uint8")).convert("L")
meta = PngInfo()
meta.add_text("ray_xs", ",".join(map(str, ray_xs)))
meta.add_text("angles", ",".join(map(str, angles)))
img.save("projection.png", pnginfo = meta)
