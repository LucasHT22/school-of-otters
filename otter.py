import numpy as np
import matplotlib.pyplot as plt
import colorsys

C_BODY = '#5c3010'
C_FUR = '#7a4520'
C_FACE = '#f2e2b8'
C_BELLY = '#e8d4a0'
C_NOSE = '#110500'
C_EYE = '#110500'
C_WHITE = '#ffffff'
C_PAW = '#6b3a18'

def ell(cx, cy, rx, ry, tilt=0, n=200):
    t = np.linspace(0, 2*np.pi, n)
    x = cx + rx*np.cos(t)*np.cos(tilt) - ry*np.sin(t)*np.sin(tilt)
    y = cy + rx*np.cos(t)*np.sin(tilt) - ry*np.sin(t)*np.cos(tilt)
    return x, y

def draw_otter(ax, cx, cy, sc, ang_deg, rng, z0=10):
    ang = np.radians(ang_deg)
    ca, sa = np.cos(ang), np.sin(ang)

    def T(xs, ys):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        return sc*(ca*xs - sa*ys)+cx, sc*(sa*xs + ca*ys)+cy
    
    def fe(ex, ey, rx, ry, col, tilt=0, a=1.0, z=0):
        xs, ys = ell(ex, ey, rx, ry, tilt)
        xr, yr = T(xs, ys)
        ax.fill(xr, yr, color=col, linewidth=0, alpha=a, zorder=z0+z)
    
    def fp(xs, ys, col, a=1.0, z=0):
        xr, yr = T(xs, ys)
        ax.fill(xr, yr, color=col, linewidth=0, alpha=a, zorder=z0+z)
    
    def pt(x, y, col, ms, z=0):
        xr, yr = T(x, y)
        ax.plot(xr, yr, color=col, markersize=ms*sc, markeredgewidth=0, zorder=z0+z)
    
    def ln(xs, ys, col, lw, a=1.0, z=0):
        xr, yr = T(xs, ys)
        ax.plot(xr, yr, color=col, linewidth=lw*sc, alpha=a, zorder=z0+z, solid_capstyle='round')
    
    hj = rng.uniform(-0.008, 0.008)
    def jc(hx, dl=0):
        r,g,b = [int(hx.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4)]
        h,l,s = colorsys.rgb_to_hls(r,g,b)
        r2,g2,b2 = colorsys.hls_to_rgb(np.clip(h+hj,0,1), np.clip(l+dl, 0.05, 0.95), s)
        return (r2,g2,b2)
    
    body = jc(C_BODY)
    fur = jc(C_FUR, +0.04)
    face = jc(C_FACE, +0.01)
    belly = jc(C_BELLY, +0.01)
    paw = jc(C_PAW, +0.02)

    # tail
    fe(0.0, -0.80, 0.38, 0.14, body, z=0)
    fe(0.0, -0.80, 0.22, 0.07, fur, z=1)

    # body
    fe(0.0, 0.0, 0.46, 0.72, body, z=2)

    # belly
    fe(0.0, 0.05, 0.28, 0.55, belly, z=3)

    # feet
    fe(-0.30, -0.68, 0.18, 0.10, paw, tilt=0.6, z=3)
    fe(0.30, -0.68, 0.18, 0.10, paw, tilt=-0.6, z=3)

    # arms
    fe(-0.50, 0.28, 0.14, 0.24, fur, tilt=0.15, z=3)
    fe(0.50, 0.28, 0.14, 0.24, fur, tilt=-0.15, z=3)

    # paws
    fe(-0.46, 0.54, 0.16, 0.12, paw, tilt=0.4, z=4)
    fe(0.46, 0.54, 0.16, 0.12, paw, tilt=-0.4, z=4)

    # head
    fe(0.0, 0.82, 0.36, 0.34, fur, z=5)

    # ears
    fe(-0.28, 1.12, 0.12, 0.12, fur, z=5)
    fe(-0.28, 1.12, 0.07, 0.07, fur, z=6)
    fe(0.28, 1.12, 0.12, 0.12, fur, z=5)
    fe(0.28, 1.12, 0.07, 0.07, fur, z=6)

    # face
    fe(0.0, 0.80, 0.28, 0.27, face, z=6)

    # muzzle
    fe(0.0, 0.68, 0.16, 0.12, face, z=7)
    fe(0.0, 0.68, 0.11, 0.08, jc(C_FACE, +0.04), z=8)

    # eyes
    pt(-0.13, 0.88, C_EYE, 5.2, z=9)
    pt(-0.10, 0.91, C_WHITE, 2.0, z=10)
    pt(0.13, 0.88, C_EYE, 5.2, z=9)
    pt(0.16, 0.91, C_WHITE, 2.0, z=10)

    # nose
    fp([-0.07, 0.07, 0.0], [0.72, 0.72, 0.65], C_NOSE, z=9)

    # mouth
    ln([-0.08, 0.0, 0.08], [0.64, 0.60, 0.64], C_NOSE, 0.9, a=0.95, z=9)

    for dy in [0.05, 0.0, -0.05]:
        ln([-0.06, -0.34], [0.68+dy, 0.69+dy], face, 0.85, a=0.85, z=9)
        ln([0.06, 0.34], [0.68+dy, 0.69+dy], face, 0.85, a=0.85, z=9)

rng = np.random.default_rng(1)
fig, ax = plt.subplots(figsize=(5,9), facecolor='#0d2b35')
ax.set_facecolor('#0d2b35')
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-1.1, 1.4)

draw_otter(ax, 0, 0, 1.0, 0, rng, z0=10)

plt.tight_layout(pad=0.2)
plt.savefig('otter_v2.png', dpi=150, bbox_inches='tight', facecolor='#0d2b35')