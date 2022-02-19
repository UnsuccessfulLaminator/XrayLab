import lf4
import sdl2, sdl2.ext
import numpy as np
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("file", nargs = "+", help = "LF4 file(s) to view")
parser.add_argument("-t0", type = float, help = "Lower color map threshold")
parser.add_argument("-t1", type = float, help = "Upper color map threshold")

def make_color(img, t0, t1):
    clipped = np.clip(img, t0, t1)
    xs = np.linspace(t0, t1, num = 4)
    r = np.interp(clipped, xs, (68, 49, 53, 253))
    g = np.interp(clipped, xs, (1, 104, 183, 231))
    b = np.interp(clipped, xs, (84, 142, 121, 37))
    a = np.full_like(clipped, 255)

    return np.stack((b, g, r, a), axis = 2).astype("u1")

args = parser.parse_args()
imgs = list(map(lf4.load, args.file))
win = sdl2.ext.Window("", (100, 100))

def display(win, name, img, t0 = None, t1 = None):
    win.title = name
    win.size = img.shape[::-1]
    surface = sdl2.SDL_GetWindowSurface(win.window)
    pixels = sdl2.ext.pixels3d(surface.contents)
    
    np.copyto(pixels, make_color(img.T, t0 or img.min(), t1 or img.max()))

display(win, args.file[0], imgs[0], args.t0, args.t1)
win.show()

n = 0

while True:
    for e in sdl2.ext.get_events():
        if e.type == sdl2.SDL_QUIT: exit()
        elif e.type == sdl2.SDL_KEYDOWN:
            if e.key.keysym.sym == sdl2.SDLK_RIGHT: n += 1
            elif e.key.keysym.sym == sdl2.SDLK_LEFT: n -= 1
            
            n %= len(imgs)

            display(win, args.file[n], imgs[n], args.t0, args.t1)
    
    win.refresh()
    sdl2.SDL_Delay(10)
