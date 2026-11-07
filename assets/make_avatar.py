"""Original avatar: a worm's-eye view up between night towers, a four-pointed star at the vanishing point,
retro film look (grain, lifted blacks, slight colour fringing). Pure numpy + Pillow."""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 2048  # draw at 2x, downsample to 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avatar.png")
rnd = random.Random(7)
C = np.array([S / 2, S / 2])  # vanishing point at the centre (GitHub crops avatars to a circle)
F = S * 0.62  # focal length in pixels


def proj(p):
    x, y, z = p
    return (C[0] + F * x / z, C[1] - F * y / z)


def box(cx, cy, w, d, ang, h):
    """Footprint corners (counter-clockwise) of a rotated rectangle, and the height."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x, y = sx * w / 2, sy * d / 2
        pts.append((cx + ca * x - sa * y, cy + sa * x + ca * y))
    return pts, h


# towers around the camera (metres); camera at the origin looking straight up
towers = [box(-78, 60, 70, 96, 0.12, 620), box(70, 74, 82, 66, -0.18, 700), box(84, -60, 66, 88, 0.22, 560),
          box(-66, -80, 90, 66, -0.08, 660), box(-150, -6, 56, 64, 0.35, 420), box(8, 150, 60, 50, 0.05, 470),
          box(160, 14, 50, 70, -0.3, 400), box(6, -160, 70, 50, 0.15, 440)]

img = Image.new("RGB", (S, S), (7, 9, 22))
d = ImageDraw.Draw(img, "RGBA")
# sky: subtle radial glow around the vanishing point and stars
sky = np.zeros((S, S, 3), np.float32)
yy, xx = np.mgrid[0:S, 0:S]
r = np.hypot(xx - C[0], yy - C[1]) / S
sky[..., 0] = 3 + 26 * np.exp(-(r / 0.2) ** 2)
sky[..., 1] = 4 + 30 * np.exp(-(r / 0.2) ** 2)
sky[..., 2] = 12 + 58 * np.exp(-(r / 0.24) ** 2)
img = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img, "RGBA")
for _ in range(900):
    x, y = rnd.uniform(0, S), rnd.uniform(0, S)
    b = rnd.uniform(60, 255)
    rr = rnd.choice([1, 1, 1, 2])
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(int(b), int(b), int(min(255, b + 20)), 255))

faces = []
for pts, h in towers:
    cxy = np.mean(pts, axis=0)
    for i in range(4):
        a, b = np.array(pts[i]), np.array(pts[(i + 1) % 4])
        mid = (a + b) / 2
        n = np.array([b[1] - a[1], -(b[0] - a[0])])  # outward normal for counter-clockwise corners
        if np.dot(n, mid - cxy) < 0:
            n = -n
        if np.dot(n, -mid) <= 0:  # face does not look toward the camera
            continue
        faces.append((float(np.hypot(*mid)), a, b, h, n / np.linalg.norm(n)))
faces.sort(key=lambda f_: -f_[0])  # far faces first

PALETTES = [((242, 236, 252), (255, 222, 150)), ((226, 236, 252), (255, 232, 170)), ((250, 236, 242), (255, 214, 160)),
            ((232, 244, 244), (255, 238, 190))]
light = np.array([0.6, 0.8])
for dist, a, b, h, n in faces:
    z0 = 10.0
    quad = [proj((a[0], a[1], z0)), proj((b[0], b[1], z0)), proj((b[0], b[1], h)), proj((a[0], a[1], h))]
    base, win = rnd.choice(PALETTES)
    shade = 0.62 + 0.24 * max(0.0, float(np.dot(n, light / np.linalg.norm(light))))
    zs = np.geomspace(z0, h, 40)
    for z1, z2 in zip(zs[:-1], zs[1:]):  # facade darkens and cools with height
        k = (math.log(z1) - math.log(z0)) / (math.log(h) - math.log(z0))
        f_ = shade * (1.0 - 0.42 * k)
        col = (int(base[0] * f_ * (1 - 0.18 * k)), int(base[1] * f_), int(min(255, base[2] * f_ * (1 + 0.1 * k))))
        band = [proj((a[0], a[1], z1)), proj((b[0], b[1], z1)), proj((b[0], b[1], z2 * 1.002)), proj((a[0], a[1], z2 * 1.002))]
        d.polygon(band, fill=col + (255,))
    # windows: floors every 4 m, columns every ~3 m, lit at random, projected in 3D
    width = float(np.hypot(*(b - a)))
    ncol = max(2, int(width / 3.0))
    for zf in np.arange(z0 + 2, h - 2, 3.8):
        kz = (math.log(zf) - math.log(z0)) / (math.log(h) - math.log(z0))
        for k in range(ncol):
            if rnd.random() > 0.5:
                continue
            u0, u1 = (k + 0.18) / ncol, (k + 0.82) / ncol
            p0, p1 = a + (b - a) * u0, a + (b - a) * u1
            q = [proj((p0[0], p0[1], zf)), proj((p1[0], p1[1], zf)), proj((p1[0], p1[1], zf + 2.0)), proj((p0[0], p0[1], zf + 2.0))]
            wc = win if rnd.random() < 0.95 else rnd.choice([(255, 120, 150), (150, 230, 255), (255, 250, 235)])
            k_l = rnd.uniform(0.82, 1.0) * (1.0 - 0.22 * kz)
            d.polygon(q, fill=(int(wc[0] * k_l), int(wc[1] * k_l), int(wc[2] * k_l), 255))
    d.line(quad[2:] + [quad[2]], fill=(255, 255, 255, 90), width=3)  # roof edge catching light

arr = np.asarray(img).astype(np.float32) / 255

# bloom on bright pixels
bright = np.clip(arr - 0.66, 0, 1) * 2.4
bl = np.asarray(Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255
arr = arr + 0.7 * bl

# the star at the vanishing point: core, halo, four long spikes with a slight tilt, a warm streak
r = np.hypot(xx - C[0], yy - C[1])
star = np.zeros_like(arr)
halo = np.exp(-(r / 70) ** 2)[..., None] * np.array([0.55, 0.75, 1.0]) + np.exp(-(r / 16) ** 2)[..., None] * 1.6
star += halo
for ang, length, width, colr in ((0.32, 520, 7, (0.7, 0.85, 1.0)), (0.32 + math.pi / 2, 360, 6, (0.7, 0.85, 1.0)),
                                 (0.32 - 0.5, 210, 4, (1.0, 0.6, 0.3))):
    ux, uy = math.cos(ang), math.sin(ang)
    along = (xx - C[0]) * ux + (yy - C[1]) * uy
    across = -(xx - C[0]) * uy + (yy - C[1]) * ux
    spike = np.exp(-(across / width) ** 2) * np.exp(-np.abs(along) / length * 3.2)
    star += spike[..., None] * np.array(colr) * 1.4
arr = arr + star

# film look: a pink light leak, lifted blacks, vignette, grain, colour fringing
leak = np.exp(-(((xx - 0.8 * S) / (0.2 * S)) ** 2 + ((yy - 0.92 * S) / (0.16 * S)) ** 2))
arr = arr + leak[..., None] * np.array([0.55, 0.12, 0.2]) * 0.6
arr = 0.06 + 0.94 * arr
arr[..., 2] += 0.03 * (1 - arr[..., 2])
vig = 1 - 0.35 * np.clip((r / (S * 0.72)) ** 2, 0, 1)
arr = arr * vig[..., None]
arr = np.clip(arr, 0, 1)
img = Image.fromarray((arr * 255).astype(np.uint8)).resize((1024, 1024), Image.LANCZOS)
arr = np.asarray(img).astype(np.float32) / 255
rgb = arr.copy()
rgb[..., 0] = np.roll(arr[..., 0], 1, axis=1)
rgb[..., 2] = np.roll(arr[..., 2], -1, axis=1)
noise = np.random.default_rng(3).normal(0, 0.045, rgb.shape[:2])[..., None]
rgb = np.clip(rgb + noise * (0.6 + 0.4 * (1 - rgb)), 0, 1)
Image.fromarray((rgb * 255).astype(np.uint8)).save(OUT, optimize=True)
print("avatar written", OUT, os.path.getsize(OUT) // 1000, "kB")
