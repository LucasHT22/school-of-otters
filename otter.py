import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import PathPatch
from matplotlib.path import Path

t = np.linspace(0, 2 * np.pi, 400)

def body(t):
    x = np.cos(t) + 0.15*np.cos(2*t) - 0.04*np.cos(3*t)
    y = 0.38*np.sin(t) + 0.06*np.sin(2*t) - 0.02*np.sin(3*t)
    return x, y

def head(t):
    x = 0.30*np.cos(t) + 0.04*np.cos(2*t) - 1.08
    y = 0.28*np.sin(t) + 0.03*np.sin(2*t) + 0.06
    return x, y

def muzzle(t):
    x = 0.14*np.cos(t) - 1.30
    y = 0.09*np.sin(t) - 0.02
    return x, y

# https://en.wikipedia.org/wiki/Lemniscate_of_Bernoulli
def tail(t):
    t2 = np.linspace(0, np.pi, 200)
    x = 0.45*np.cos(t2) + 0.18*np.cos(2*t2) + 0.14*np.cos(3*t2) + 1.12
    y = 0.14*np.sin(t2) + 0.07*np.sin(2*t2) - 0.03*np.sin(3*t2)
    return x, y

def ear(t, side=1):
    x = 0.08*np.cos(t) - 1.08 + side*0.18
    y = 0.12*np.sin(t) + 0.28
    return x, y

def paw(t, ox, oy):
    x = 0.13*np.cos(t) + 0.03*np.cos(2*t) + ox
    y = 0.07*np.sin(t) + oy
    return x, y

def transform(x, y, scale, angle_deg, tx, ty):
    angle = np.radians(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    xr = scale * (c*x - s*y) + tx
    yr = scale * (s*x + c*y) + ty
    return xr, yr

def otter_palette(hue):
    # https://en.wikipedia.org/wiki/HSL_and_HSV
    def hsl(h, s, l):
        return mcolors.hsv_to_rgb([h, s, l])
    
    import colorsys
    def hsl_c(h, s, l):
        return colorsys.hls_to_rgb(h, l, s)
    
    return {
        'body': hsl_c(hue, 0.65, 0.38),
        'head': hsl_c(hue, 0.60, 0.44),
        'muzzle': hsl_c(hue + 0.05, 0.30, 0.72),
        'tail': hsl_c(hue - 0.03, 0.70, 0.30),
        'ear': hsl_c(hue, 0.55, 0.50),
        'paw': hsl_c(hue + 0.02, 0.45, 0.58),
        'nose': hsl_c(hue + 0.08, 0.20, 0.85),
    }

