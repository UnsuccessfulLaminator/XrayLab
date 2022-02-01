from OpenGL import GL, GLU
import glfw
import sys
import numpy as np



# --------------------------
# OpenGL initialisation code
# --------------------------

if not glfw.init():
    print("Failed to initialise.", file = sys.stderr)
    exit(1)

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

win = glfw.create_window(640, 480, "Main", None, None)

if not win:
    print("Failed to create window.", file = sys.stderr)
    exit(1)

glfw.make_context_current(win)

shader = GL.glCreateShader(GL.GL_COMPUTE_SHADER)
GL.glShaderSource(shader, open("interp.glsl").read())
GL.glCompileShader(shader)

if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
    print("Shader compilation error:\n", GL.glGetShaderInfoLog(shader), file = sys.stderr)
    exit(1)

program = GL.glCreateProgram()
GL.glAttachShader(program, shader)
GL.glLinkProgram(program)

if GL.glGetProgramiv(program, GL.GL_LINK_STATUS) != GL.GL_TRUE:
    print("Shader linking error:\n", GL.glGetProgramInfoLog(program), file = sys.stderr)
    exit(1)



# ------------------------------
# Interpolation class definition
# ------------------------------

class Interp2D:
    def __init__(self):
        self.tex = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)

        self.buf = GL.glGenBuffers(1)

    def set_data(self, dx, dy, zs):
        self.dx = dx
        self.dy = dy
        self.size = (zs.shape[1], zs.shape[0])
        data = zs.astype("<f4")

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_R32F, *self.size, 0, GL.GL_RED, GL.GL_FLOAT, data)

    def _upload(self, b):
        GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, self.buf)
        GL.glBufferData(GL.GL_SHADER_STORAGE_BUFFER, len(b), b, GL.GL_DYNAMIC_DRAW)

    def _compute(self, invocs):
        GL.glUseProgram(program)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glBindBufferBase(GL.GL_SHADER_STORAGE_BUFFER, 2, self.buf)
        GL.glDispatchCompute(invocs, 1, 1)
        GL.glMemoryBarrier(GL.GL_SHADER_STORAGE_BARRIER_BIT)

    def _download(self, size):
        GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, self.buf)
        
        return GL.glGetBufferSubData(GL.GL_SHADER_STORAGE_BUFFER, 0, size).view("<f4")[::2]

    def __call__(self, xs, ys):
        if xs.shape != ys.shape:
            raise ValueError("Not implemented for x and y having different shape")
        elif xs.size > 65536:
            raise ValueError("Not implemented for more than 65536 points at a time")
        
        n = xs.size
        data = np.empty((n, 2), dtype = "<f4")
        data[:, 0] = xs.ravel()
        data[:, 0] /= self.dx*self.size[0]
        data[:, 0] += 1/(2*self.size[0])
        data[:, 1] = ys.ravel()
        data[:, 1] /= self.dy*self.size[1]
        data[:, 1] += 1/(2*self.size[1])
        b = data.tobytes()
        
        self._upload(b)
        self._compute(int(np.ceil(len(b)/64)))
        res = self._download(len(b))
        res.shape = xs.shape

        return res
