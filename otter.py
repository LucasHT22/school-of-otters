import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import PathPatch
from matplotlib.path import Path

t = np.linspace(0, 2 * np.pi, 400)

def body(t):
    x = -(np.cos(t) + 0.15*np.cos(2*t) - 0.04*np.cos(3*t))
    y = -(0.38*np.sin(t) + 0.06*np.sin(2*t) - 0.02*np.sin(3*t))
    return x, y

def head(t):
    x = -(0.30*np.cos(t) + 0.04*np.cos(2*t) - 1.08)
    y = 0.28*np.sin(t) + 0.03*np.sin(2*t) + 0.06
    return x, y

def muzzle(t):
    x = -(0.14*np.cos(t) - 1.30)
    y = 0.09*np.sin(t) - 0.02
    return x, y

# https://en.wikipedia.org/wiki/Lemniscate_of_Bernoulli
def tail(t):
    t2 = np.linspace(0, np.pi, 200)
    x = -(0.45*np.cos(t2) + 0.18*np.cos(2*t2) + 0.03*np.cos(3*t2) + 1.12)
    y = 0.16*np.sin(t2) + 0.05*np.sin(2*t2)
    return x, y

def ear(t, side=1):
    x = -(0.08*np.cos(t) - 1.08 + side*0.18)
    y = 0.10*np.sin(t) + 0.22
    return x, y

def paw(t, ox, oy):
    x = -(0.13*np.cos(t) + 0.03*np.cos(2*t) + ox)
    y = 0.07*np.sin(t) + oy
    return x, y

def transform(x, y, scale, angle_deg, tx, ty):
    angle = np.radians(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    xr = scale * (c*x - s*y) + tx
    yr = scale * (s*x + c*y) + ty
    return xr, yr

def otter_palette(rng):
    base_hue = rng.uniform(0.055, 0.085)
    
    # https://en.wikipedia.org/wiki/HSL_and_HSV
    import colorsys
    def c(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r, g, b)
    
    jitter = rng.uniform(-0.01, 0.01)
    
    return {
        'body': c(base_hue + jitter, 0.7, 0.28),
        'head': c(base_hue + jitter, 0.65, 0.35),
        'muzzle': c(base_hue + 0.02 + jitter, 0.40, 0.68),
        'tail': c(base_hue - 0.01 + jitter, 0.75, 0.22),
        'ear': c(base_hue + jitter, 0.60, 0.32),
        'paw': c(base_hue + 0.01 + jitter, 0.50, 0.42),
        'nose': c(base_hue - 0.01, 0.20, 0.12),
        'belly': c(base_hue + 0.03 + jitter, 0.35, 0.62)
    }

def draw_otter(ax, scale, angle, tx, ty, rng, alpha=0.88):
    pal = otter_palette(rng)
    lw = 0

    def fill(xy_fn, color, t_=t):
        x, y = xy_fn(t_)
        xr, yr = transform(x, y, scale, angle, tx, ty)
        ax.fill(xr, yr, color=color, linewidth=lw, alpha=alpha, zorder=ty)
    
    fill(body, pal['body'])
    fill(lambda t_: tail(None), pal['tail'])
    fill(head, pal['head'])
    fill(muzzle, pal['muzzle'])
    fill(lambda t: ear(t, -1), pal['ear'])
    fill(lambda t: ear(t, 1), pal['ear'])
    fill(lambda t: paw(t, -0.45, -0.38), pal['paw'])
    fill(lambda t: paw(t, 0.15, -0.39), pal['paw'])

    nx, ny = transform(np.array([1.40]), np.array([0.0]), scale, angle, tx, ty)
    ax.plot(nx, ny, 'o', color=pal['nose'], markersize=scale*3.5, zorder=ty+1)

    for dy in [-0.035, 0.0, 0.035]:
        for sign in [-1, 1]:
            wx = np.array([1.32, 1.32 + sign*0.20])
            wy = np.array([dy, dy + sign*0.01])
            xr, yr = transform(wx, wy, scale, angle, tx, ty)
            ax.plot(xr, yr, color=pal['nose'], linewidth=0.6, alpha=0.6, zorder=ty+1)

rng = np.random.default_rng(7)
N = 80

fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0d2b35')
ax.set_aspect('equal')
ax.axis('off')

fig.patch.set_facecolor('#0d2b35')
ax.set_facecolor('#0d2b35')

ax.fill_between([-10, 10], -5.5, 5.5, color='#0d2b35', zorder=0)

water_colors = ['#1a6b7a', '#2a4a6b', '#1e3d4f', '#16505f', '#0f3d4a']
for _ in range(200):
    wx = rng.uniform(-11, 11)
    wy = rng.uniform(-6, 6)
    wl = rng.uniform(0.4, 3.0)
    col = rng.choice(water_colors)
    alp = rng.uniform(0.06, 0.20)
    lw = rng.uniform(0.4, 1.8)
    dx = wl * np.cos(np.radians(35))
    dy = wl * np.sin(np.radians(35))
    ax.plot([wx, wx + dx], [wy, wy + dy], color=col, alpha=alp, linewidth=lw, zorder=1)

for _ in range(80):
    gx = rng.uniform(-9, 9)
    gy = rng.uniform(-5, 5)
    gl = rng.uniform(0.1, 0.6)
    ax.plot([gx, gx + gl], [gy, gy], color='#a8d8e8', alpha=rng.uniform(0.04, 0.12), linewidth=0.6, zorder=1)

ax.set_xlim(-10, 10)
ax.set_ylim(-5.5, 5.5)

cols, rows = 12, 10

for row in range(rows):
    for col in range(cols):
        phi = col / (cols - 1)
        band = (row / (rows - 1)) - 0.5

        cx = -7 + phi * 14 + band * 2.5 + rng.normal(0, 0.4)
        cy = -3 + phi * 6 + band * 1.2 + rng.normal(0, 0.3)

        scale = rng.uniform(0.65, 1.0) * (0.80 + 0.20 * phi)
        angle = 35 + rng.normal(0, 18)
        alpha = rng.uniform(0.80, 0.95)

        draw_otter(ax, scale=scale, angle=angle, tx=cx, ty=cy, rng=rng, alpha=alpha)

plt.tight_layout(pad=0)
plt.savefig('otter_v1.png', dpi=200, bbox_inches='tight', facecolor='#0d2b35')
plt.show()