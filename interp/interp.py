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

    def __call__(self, xs, ys):
        if xs.shape != ys.shape:
            raise ValueError("x and y arrays must have the same shape")
        
        data = np.empty((xs.size, 2), dtype = "<f4")
        data[:, 0] = xs.ravel()
        data[:, 0] /= self.dx*self.size[0]
        data[:, 0] += 1/(2*self.size[0])
        data[:, 1] = ys.ravel()
        data[:, 1] /= self.dy*self.size[1]
        data[:, 1] += 1/(2*self.size[1])
        data = data.tobytes()

        GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, self.buf)
        GL.glBufferData(GL.GL_SHADER_STORAGE_BUFFER, len(data), data, GL.GL_DYNAMIC_DRAW)

        GL.glUseProgram(program)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glBindBufferBase(GL.GL_SHADER_STORAGE_BUFFER, 2, self.buf)
        GL.glDispatchCompute(xs.size, 1, 1)

        GL.glMemoryBarrier(GL.GL_SHADER_STORAGE_BARRIER_BIT)
        GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, self.buf)
        
        res = GL.glGetBufferSubData(GL.GL_SHADER_STORAGE_BUFFER, 0, len(data)).view("<f4")
        
        return res[::2]
