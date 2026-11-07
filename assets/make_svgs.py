"""Animated SVGs for the GitHub profile README: a dusk skyline where San Francisco meets Tokyo (original art),
with a typing intro, and a human hand and a robot hand reaching for each other."""
import math
import os
import random

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
rnd = random.Random(15)
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Consolas, 'SFMono-Regular', Menlo, 'DejaVu Sans Mono', monospace"


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


# ----------------------------------------------------------------------------------------------- banner
W, H, HZ = 1200, 340, 268  # width, height, horizon (water line)


def typing_block(lines, x0, y, size, color):
    """One text line at a time types in, holds, erases. SMIL with discrete steps; monospace advance = 0.6 em."""
    cw = 0.6 * size
    t_char, hold, t_erase, gap = 0.075, 1.8, 0.025, 0.35
    slots, t = [], 0.0
    for s in lines:
        n = len(s)
        slots.append((t, n))
        t += n * t_char + hold + n * t_erase + gap
    total = t
    parts = [f'<text x="{f(x0)}" y="{f(y)}" font-family="{MONO}" font-size="{size}" fill="#8b93b8">&gt;</text>']
    tx = x0 + 1.6 * cw
    cur_times, cur_vals = [0.0], [tx]
    for i, (s, (start, n)) in enumerate(zip(lines, slots)):
        times, vals = [0.0], [0.0]
        for k in range(1, n + 1):
            times.append(start + k * t_char); vals.append(k * cw)
        t_hold_end = start + n * t_char + hold
        for k in range(n - 1, -1, -1):
            times.append(t_hold_end + (n - k) * t_erase); vals.append(k * cw)
        cur_times += times[1:]
        cur_vals += [tx + v for v in vals[1:]]
        if start > 0:
            times.insert(1, start); vals.insert(1, 0.0)
        kt = ";".join(f"{min(tt / total, 1):.4f}" for tt in times)
        vv = ";".join(f(v) for v in vals)
        esc = s.replace("&", "&amp;")
        parts.append(
            f'<clipPath id="type{i}"><rect x="{f(tx)}" y="{f(y - size)}" height="{f(size * 1.4)}" width="0">'
            f'<animate attributeName="width" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
            f'keyTimes="{kt}" values="{vv}"/></rect></clipPath>'
            f'<text x="{f(tx)}" y="{f(y)}" font-family="{MONO}" font-size="{size}" fill="{color}" '
            f'textLength="{f(n * cw)}" lengthAdjust="spacing" clip-path="url(#type{i})">{esc}</text>')
    order = sorted(zip(cur_times, cur_vals))
    kt = ";".join(f"{min(tt / total, 1):.4f}" for tt, _ in order)
    vv = ";".join(f(v) for _, v in order)
    parts.append(
        f'<rect y="{f(y - size * 0.82)}" width="{f(cw * 0.9)}" height="{f(size * 1.0)}" fill="{color}" x="{f(tx)}">'
        f'<animate attributeName="x" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" keyTimes="{kt}" values="{vv}"/>'
        f'<animate attributeName="opacity" calcMode="discrete" values="1;0" dur="1.05s" repeatCount="indefinite"/></rect>')
    return "".join(parts)


def bridge():
    """A suspension bridge in international orange, cars crossing."""
    g = []
    deck_y, x_a, x_b, top, low = 247, 128, 372, 138, 236
    left, right = 10, 520
    c = 2 * low - top  # control y of the main-span parabola
    col = "#c8432f"

    def main_y(x):  # main span quadratic between the towers
        s = (x - x_a) / (x_b - x_a)
        return (1 - s) ** 2 * top + 2 * s * (1 - s) * c + s ** 2 * top

    def side_y(x, x0, x1):  # side spans: straight-ish sag from the anchorage to the tower top
        s = (x - x0) / (x1 - x0)
        return (1 - s) * 212 + s * top - 18 * math.sin(math.pi * s)

    hangers = []
    for x in range(x_a + 10, x_b - 5, 10):
        hangers.append(f'M{x},{f(main_y(x))}V{deck_y}')
    for x in range(left + 12, x_a - 4, 10):
        hangers.append(f'M{x},{f(side_y(x, left, x_a))}V{deck_y}')
    for x in range(x_b + 8, right - 6, 10):
        hangers.append(f'M{x},{f(side_y(right - (x - x_b), right, x_b))}V{deck_y}')
    g.append(f'<path d="{"".join(hangers)}" stroke="{col}" stroke-width="0.8" opacity="0.55"/>')
    side_l = " ".join(f"{x},{f(side_y(x, left, x_a))}" for x in range(left, x_a + 1, 4))
    side_r = " ".join(f"{x},{f(side_y(right - (x - x_b), right, x_b))}" for x in range(x_b, right + 1, 4))
    g.append(f'<polyline points="{side_l}" fill="none" stroke="{col}" stroke-width="2"/>')
    g.append(f'<polyline points="{side_r}" fill="none" stroke="{col}" stroke-width="2"/>')
    g.append(f'<path d="M{x_a},{top} Q{(x_a + x_b) / 2},{c} {x_b},{top}" fill="none" stroke="{col}" stroke-width="2.2"/>')
    for x in (x_a, x_b):  # towers with portal bracing
        g.append(f'<rect x="{x - 9}" y="{top - 10}" width="5" height="{HZ - top + 10}" fill="{col}"/>'
                 f'<rect x="{x + 4}" y="{top - 10}" width="5" height="{HZ - top + 10}" fill="{col}"/>')
        for yy in (top - 4, top + 26, top + 56, top + 86):
            g.append(f'<rect x="{x - 9}" y="{yy}" width="18" height="4" fill="{col}"/>')
        g.append(f'<circle cx="{x}" cy="{top - 12}" r="1.8" fill="#ff5a4e">'
                 f'<animate attributeName="opacity" values="1;0.15;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    g.append(f'<rect x="{left - 10}" y="{deck_y}" width="{right - left + 20}" height="5" fill="{col}"/>')
    g.append(f'<rect x="{left - 10}" y="{deck_y + 5}" width="{right - left + 20}" height="2" fill="#5a1d1a"/>')
    for i, (dur, beg, colr, rev) in enumerate([(11, 0, "#fff6d6", False), (11, 5.5, "#fff6d6", False),
                                                (13, 2, "#ff4d4d", True), (13, 8.5, "#ff4d4d", True)]):
        a, b = (right + 10, left - 10) if rev else (left - 10, right + 10)
        g.append(f'<circle cy="{deck_y - 1.5}" r="1.6" fill="{colr}" cx="{a}">'
                 f'<animate attributeName="cx" values="{a};{b}" dur="{dur}s" begin="-{beg}s" repeatCount="indefinite"/></circle>')
    return "".join(g)


def lattice_tower(cx, base_y, top_y, base_w):
    """A Tokyo-style lattice tower: tapered legs, observation decks, red and white bands, beacon."""
    g = []
    h = base_y - top_y

    def half_w(y):
        s = (base_y - y) / h
        return base_w / 2 * (1 - s) ** 1.6 + 2.5

    pts_l = [(cx - half_w(y), y) for y in range(base_y, top_y - 1, -6)]
    pts_r = [(cx + half_w(y), y) for y in range(top_y, base_y + 1, 6)]
    poly = " ".join(f"{f(x)},{f(y)}" for x, y in pts_l + pts_r)
    g.append(f'<polygon points="{poly}" fill="url(#towerGrad)"/>')
    lat = []
    for y in range(base_y - 6, top_y + 20, -12):  # lattice crosses
        wa, wb = half_w(y), half_w(y - 12)
        lat.append(f"M{f(cx - wa)},{y}L{f(cx + wb)},{y - 12}M{f(cx + wa)},{y}L{f(cx - wb)},{y - 12}")
    g.append(f'<path d="{"".join(lat)}" stroke="#2b1530" stroke-width="0.9" opacity="0.55"/>')
    for y in (base_y - 62, base_y - 118):  # observation decks
        w = half_w(y) + 7
        g.append(f'<rect x="{f(cx - w)}" y="{y - 5}" width="{f(2 * w)}" height="9" rx="2" fill="#f2e6dc" opacity="0.92"/>'
                 f'<rect x="{f(cx - w + 3)}" y="{y - 2}" width="{f(2 * w - 6)}" height="3" fill="#ffd27a">'
                 f'<animate attributeName="opacity" values="0.7;1;0.7" dur="3.2s" repeatCount="indefinite"/></rect>')
    g.append(f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{top_y - 22}" stroke="#f2e6dc" stroke-width="1.6"/>'
             f'<circle cx="{cx}" cy="{top_y - 23}" r="2.4" fill="#ff4d4d">'
             f'<animate attributeName="opacity" values="1;0.1;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    return "".join(g)


def pagoda(cx, base_y, tiers=5, w0=70):
    g = []
    y = base_y
    w = w0
    for i in range(tiers):
        body_h = 16 - i
        g.append(f'<rect x="{f(cx - w * 0.32)}" y="{f(y - body_h)}" width="{f(w * 0.64)}" height="{body_h}" fill="#1c1431"/>')
        for k in range(3):
            if rnd.random() < 0.8:
                g.append(f'<rect x="{f(cx - w * 0.22 + k * w * 0.18)}" y="{f(y - body_h + 5)}" width="3" height="5" fill="#ffc46b" opacity="0.85"/>')
        y -= body_h
        roof = (f"M{f(cx - w / 2 - 6)},{f(y - 1)} Q{f(cx - w / 2)},{f(y + 2)} {f(cx - w * 0.36)},{f(y - 2)} "
                f"L{f(cx)},{f(y - 9)} L{f(cx + w * 0.36)},{f(y - 2)} Q{f(cx + w / 2)},{f(y + 2)} {f(cx + w / 2 + 6)},{f(y - 1)} "
                f"L{f(cx + w * 0.3)},{f(y - 7)} L{f(cx - w * 0.3)},{f(y - 7)} Z")
        g.append(f'<path d="{roof}" fill="#140f26"/>')
        y -= 7
        w *= 0.82
    g.append(f'<rect x="{f(cx - 1.2)}" y="{f(y - 24)}" width="2.4" height="24" fill="#140f26"/>')
    for k in range(4):
        g.append(f'<rect x="{f(cx - 4)}" y="{f(y - 20 + k * 5)}" width="8" height="1.6" fill="#140f26"/>')
    return "".join(g)


def buildings():
    """Two rows of towers with windows; a few windows and neon signs are animated."""
    g = []
    anim_left = 70
    for row, (color, y_off, n, hmin, hmax) in enumerate([("#1a1433", 0, 26, 50, 120), ("#120e25", 0, 30, 24, 80)]):
        x = 470 + rnd.uniform(-20, 10)
        while x < W + 10:
            bw = rnd.uniform(18, 44)
            bh = rnd.uniform(hmin, hmax)
            if 585 < x < 640 or 935 < x < 1030:  # leave the pyramid and the tower clear in the back row
                if row == 0:
                    x += bw * 0.6
                    continue
            top = HZ - bh
            g.append(f'<rect x="{f(x)}" y="{f(top)}" width="{f(bw)}" height="{f(bh)}" fill="{color}"/>')
            if rnd.random() < 0.25:
                g.append(f'<rect x="{f(x + bw / 2 - 0.6)}" y="{f(top - 9)}" width="1.2" height="9" fill="{color}"/>')
            for wy in range(int(top) + 6, HZ - 6, 7):
                for wx in range(int(x) + 4, int(x + bw) - 4, 6):
                    p = rnd.random()
                    if p < 0.30:
                        colw = "#ffd27a" if rnd.random() < 0.75 else "#9fd8ff"
                        if anim_left > 0 and rnd.random() < 0.08:
                            anim_left -= 1
                            d = rnd.uniform(3, 9)
                            g.append(f'<rect x="{wx}" y="{wy}" width="2.4" height="3.2" fill="{colw}">'
                                     f'<animate attributeName="opacity" calcMode="discrete" values="0.9;0.05;0.9" '
                                     f'keyTimes="0;{rnd.uniform(0.2, 0.7):.2f};1" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></rect>')
                        else:
                            g.append(f'<rect x="{wx}" y="{wy}" width="2.4" height="3.2" fill="{colw}" opacity="{rnd.uniform(0.45, 0.95):.2f}"/>')
            x += bw + rnd.uniform(-6, 4)
    for x, y, h, colr in [(700, 205, 26, "#ff4fa3"), (858, 214, 22, "#3ef0ff"), (1062, 200, 30, "#ff4fa3"),
                          (1160, 216, 20, "#3ef0ff"), (560, 222, 18, "#3ef0ff")]:
        g.append(f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="1.5" fill="{colr}" filter="url(#glow)">'
                 f'<animate attributeName="opacity" values="1;0.55;1;0.9;1" dur="{rnd.uniform(2.5, 4.5):.1f}s" repeatCount="indefinite"/></rect>')
    return "".join(g)


def torii(x, base_y, s=1.0, color="#d2402f"):
    return (f'<g transform="translate({x},{base_y}) scale({s})" fill="{color}">'
            f'<rect x="-15" y="-34" width="3.4" height="34"/><rect x="11.6" y="-34" width="3.4" height="34"/>'
            f'<rect x="-18" y="-29" width="36" height="3"/>'
            f'<path d="M-24,-38 Q0,-33 24,-38 L22,-34 Q0,-31 -22,-34 Z"/></g>')


def drone(path, dur, begin, scale=1.0):
    return (f'<g><g transform="scale({scale})">'
            f'<rect x="-6" y="-1.5" width="12" height="3" rx="1.5" fill="#d6dcf0"/>'
            f'<path d="M-9,-3.5h6M3,-3.5h6" stroke="#d6dcf0" stroke-width="1.2"/>'
            f'<circle cx="-7" cy="1.5" r="1.1" fill="#ff4d4d"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></circle>'
            f'<circle cx="7" cy="1.5" r="1.1" fill="#4dff88"><animate attributeName="opacity" values="0;1;0" dur="0.9s" repeatCount="indefinite"/></circle>'
            f'</g><animateMotion path="{path}" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/></g>')


def banner():
    stars = []
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(6, 175)
        r = rnd.uniform(0.5, 1.5)
        d = rnd.uniform(2.5, 6.5)
        lo = rnd.uniform(0.1, 0.4)
        stars.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r:.2f}" fill="#ffffff">'
                     f'<animate attributeName="opacity" values="{lo:.2f};1;{lo:.2f}" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
    hills = (f"M0,{HZ} L0,232 C60,222 110,214 170,226 C230,238 280,224 340,230 C420,238 470,228 540,236 "
             f"C640,246 760,240 860,244 C980,248 1090,238 1200,244 L1200,{HZ} Z")
    shimmer = []
    for i in range(14):
        y = HZ + 6 + i * 4.6
        w = 70 - i * 3.4 + rnd.uniform(-6, 6)
        shimmer.append(f'<rect x="{f(838 - w / 2)}" y="{f(y)}" width="{f(w)}" height="1.6" rx="0.8" fill="#ffb878">'
                       f'<animate attributeName="opacity" values="0.15;0.75;0.15" dur="{rnd.uniform(1.8, 3.4):.1f}s" begin="-{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="width" values="{f(w)};{f(w * 0.7)};{f(w)}" dur="{rnd.uniform(2.5, 4):.1f}s" repeatCount="indefinite"/></rect>')
    waves = []
    for i in range(18):
        x, y = rnd.uniform(0, W), rnd.uniform(HZ + 8, H - 6)
        ln = rnd.uniform(14, 40)
        d = rnd.uniform(9, 18)
        waves.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(ln)}" height="1" fill="#8f7bd6" opacity="0.25">'
                     f'<animate attributeName="x" values="{f(x)};{f(x - 60)};{f(x)}" dur="{d:.1f}s" repeatCount="indefinite"/></rect>')
    pyramid = ('<polygon points="586,268 610,92 634,268" fill="#1d1636"/>'
               '<polygon points="578,268 586,214 594,268" fill="#1a1432"/><polygon points="626,268 634,214 642,268" fill="#1a1432"/>'
               '<circle cx="610" cy="91" r="2" fill="#ff4d4d"><animate attributeName="opacity" values="1;0.1;1" dur="2s" repeatCount="indefinite"/></circle>')
    roles = ["founder @ Athena Labs", "building physical AI", "first exit at 15", "math olympiad",
             "AI · robotics · startups · venture"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Anuar Zhambakin. Founder of Athena Labs, building physical AI. A dusk skyline where San Francisco meets Tokyo.">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="{HZ}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#060a1c"/><stop offset="0.42" stop-color="#191541"/><stop offset="0.7" stop-color="#55285c"/>
<stop offset="0.88" stop-color="#c94f5d"/><stop offset="1" stop-color="#f6a05c"/></linearGradient>
<linearGradient id="water" x1="0" y1="{HZ}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#3b1f4a"/><stop offset="1" stop-color="#090b1d"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffe2a6"/><stop offset="0.7" stop-color="#ff9a62"/><stop offset="1" stop-color="#ff7a5a"/></radialGradient>
<radialGradient id="sunGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ff9e6b" stop-opacity="0.55"/><stop offset="1" stop-color="#ff9e6b" stop-opacity="0"/></radialGradient>
<linearGradient id="towerGrad" x1="0" y1="70" x2="0" y2="{HZ}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#f2e6dc"/><stop offset="0.12" stop-color="#e0533d"/><stop offset="0.24" stop-color="#f2e6dc"/><stop offset="0.36" stop-color="#d94a37"/>
<stop offset="0.6" stop-color="#b53a2e"/><stop offset="1" stop-color="#5a1f2a"/></linearGradient>
<filter id="glow" x="-200%" y="-50%" width="500%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{HZ}" fill="url(#sky)"/>
{"".join(stars)}
<circle cx="840" cy="226" r="150" fill="url(#sunGlow)"><animate attributeName="r" values="140;158;140" dur="7s" repeatCount="indefinite"/></circle>
<circle cx="840" cy="226" r="60" fill="url(#sun)"/>
<path d="{hills}" fill="#2f1a45"/>
{bridge()}
{pyramid}
{lattice_tower(980, HZ, 72, 96)}
{buildings()}
{pagoda(1118, HZ, 5, 74)}
{torii(735, HZ, 0.9)}
<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#water)"/>
{"".join(shimmer)}
{"".join(waves)}
{drone("M-40,150 C200,110 420,160 640,120 S1000,90 1260,130", 34, 0, 1.0)}
{drone("M1260,70 C1000,100 760,60 520,92 S160,70 -40,96", 41, 12, 0.85)}
{drone("M-40,190 C300,170 700,200 1260,165", 27, 20, 0.7)}
<text x="48" y="80" font-family="{SANS}" font-size="46" font-weight="700" fill="#ffffff" letter-spacing="0.5">Anuar Zhambakin</text>
{typing_block(roles, 50, 122, 22, "#7ee0ff")}
</g>
</svg>
'''
    return svg


# ----------------------------------------------------------------------------------------------- hands
HW, HH = 1200, 230
CY = 112


def human_hand():
    """Outline of a relaxed hand reaching right, index fingertip at the origin (y down)."""
    arm = ("M-640,-30 C-480,-31 -330,-27 -206,-20 C-186,-19 -168,-25 -148,-27 C-126,-29 -110,-24 -99,-17 "
           "C-74,-12 -40,-9 -11,-7 C-3,-6.6 2.6,-3.4 2,0.6 C1.4,4 -3.6,5.6 -10,5.2 C-36,4.4 -62,5.2 -84,7 "
           "C-91,8.4 -93,13.6 -89,18.6 C-85,24.6 -91,30.4 -101,30 C-112,29.6 -118,25.6 -118.6,21.6 "
           "C-114,33 -122,40 -134,38.4 C-144,37 -149,32 -146.6,26.8 C-150.6,37.6 -160.6,42 -170.4,38.2 "
           "C-178.4,35 -180.4,28.6 -176.8,23 C-186,24.4 -196,22.6 -207,20.4 C-330,27 -480,35 -640,37 Z")
    thumb = "M-160,3 C-142,-1.5 -121,2 -108,8 C-101,11.5 -103.5,18.4 -111.5,17.6 C-126,16 -143,15 -160,15 Z"
    creases = "M-62,-8.6 C-61,-4 -61,0 -62,5.4 M-35,-8.2 C-34.4,-4 -34.4,0.5 -35,4.6 M-150,-26 C-160,-14 -158,-2 -150,8"
    thumb_edge = "M-158,15 C-143,15 -126,16 -111.5,17.6 C-103.5,18.4 -101,11.5 -108,8"
    return (f'<path d="{arm}" fill="url(#skin)" stroke="#7a4b38" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="{thumb}" fill="url(#skin)"/>'
            f'<path d="{thumb_edge}" fill="none" stroke="#7a4b38" stroke-width="1.4" stroke-linecap="round" opacity="0.8"/>'
            f'<path d="{creases}" fill="none" stroke="#7a4b38" stroke-width="1" opacity="0.45" stroke-linecap="round"/>')


def robot_hand():
    """A segmented robot hand reaching left, index fingertip at the origin (y down)."""
    g = []
    g.append('<rect x="198" y="-27" width="460" height="54" rx="20" fill="url(#metal)" stroke="#2f3a4c" stroke-width="1.6"/>'
             '<rect x="230" y="-4" width="400" height="7" rx="3.5" fill="#22d3ee" filter="url(#glowH)">'
             '<animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" repeatCount="indefinite"/></rect>'
             '<path d="M260,-27V-12M320,-27V-12M380,-27V-12M260,27V12M320,27V12M380,27V12" stroke="#2f3a4c" stroke-width="1.2" opacity="0.6"/>')
    g.append('<circle cx="190" cy="0" r="22" fill="url(#metal)" stroke="#2f3a4c" stroke-width="1.6"/>'
             '<circle cx="190" cy="0" r="9" fill="#0b1220" stroke="#22d3ee" stroke-width="2"/>'
             '<circle cx="190" cy="0" r="3.2" fill="#22d3ee"><animate attributeName="opacity" values="1;0.35;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    g.append('<path d="M172,-24 L118,-26 C106,-26 100,-20 99,-12 L98,14 C99,24 108,30 120,30 L172,26 Z" fill="url(#metal)" stroke="#2f3a4c" stroke-width="1.6"/>'
             '<path d="M150,-20 L150,22" stroke="#2f3a4c" stroke-width="1" opacity="0.5"/>')
    for x0, x1 in ((66, 96), (35, 62), (5, 31)):  # index finger phalanges
        g.append(f'<rect x="{x0}" y="-7.5" width="{x1 - x0}" height="15" rx="6.5" fill="url(#metal)" stroke="#2f3a4c" stroke-width="1.4"/>')
    for x in (64, 33):
        g.append(f'<circle cx="{x}" cy="0" r="5" fill="#0b1220" stroke="#22d3ee" stroke-width="1.6"/>')
    g.append('<circle cx="98" cy="-1" r="6" fill="#0b1220" stroke="#22d3ee" stroke-width="1.6"/>')
    g.append('<circle cx="6.5" cy="0" r="2.4" fill="#22d3ee" filter="url(#glowH)"/>')
    for k in range(3):  # folded fingers, a robot fist under the pointing finger
        y = 9 + k * 10.5
        g.append(f'<rect x="{74 + k * 2}" y="{y}" width="{44 - k * 2}" height="12.5" rx="6" fill="url(#metal)" stroke="#2f3a4c" stroke-width="1.3"/>'
                 f'<circle cx="{81 + k * 2}" cy="{y + 6.2}" r="3.4" fill="#0b1220" stroke="#22d3ee" stroke-width="1.2"/>')
    return "".join(g)


def hands():
    dur = 6.5
    kt, ks = "0;0.42;0.6;1", "0.45 0 0.3 1;0 0 1 1;0.6 0 0.55 1"
    gap0, gap1 = 95, 5
    dots = []
    for _ in range(70):
        x, y = rnd.uniform(0, HW), rnd.uniform(0, HH)
        d = rnd.uniform(3, 7)
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rnd.uniform(0.5, 1.3):.2f}" fill="#9fb3ff">'
                    f'<animate attributeName="opacity" values="0.05;0.6;0.05" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
    rays = []
    for k in range(10):
        a = 2 * math.pi * k / 10 + 0.2
        r0, r1 = 8, 22 + 8 * (k % 2)
        rays.append(f"M{f(600 + r0 * math.cos(a))},{f(CY + r0 * math.sin(a))}L{f(600 + r1 * math.cos(a))},{f(CY + r1 * math.sin(a))}")
    flash_kt = "0;0.40;0.43;0.57;0.62;1"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {HW} {HH}" width="{HW}" height="{HH}" role="img" aria-label="A human hand and a robot hand reach for each other; a spark jumps between their fingertips.">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b1f"/><stop offset="0.55" stop-color="#14123a"/><stop offset="1" stop-color="#2a1640"/></linearGradient>
<linearGradient id="skin" x1="0" y1="-30" x2="0" y2="40" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f6cfae"/><stop offset="1" stop-color="#d79a74"/></linearGradient>
<linearGradient id="metal" x1="0" y1="-30" x2="0" y2="40" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#eef3f9"/><stop offset="0.5" stop-color="#aeb9c8"/><stop offset="1" stop-color="#6f7c8f"/></linearGradient>
<radialGradient id="spark" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff"/><stop offset="0.35" stop-color="#bff3ff"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
<filter id="glowH" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="card2"><rect width="{HW}" height="{HH}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card2)">
<rect width="{HW}" height="{HH}" fill="url(#bg)"/>
{"".join(dots)}
<g transform="translate(600,{CY})"><g>
<animateTransform attributeName="transform" type="translate" calcMode="spline" keyTimes="{kt}" keySplines="{ks}" values="-{gap0} 6;-{gap1} 1;-{gap1} 1;-{gap0} 6" dur="{dur}s" repeatCount="indefinite"/>
{human_hand()}
</g></g>
<g transform="translate(600,{CY})"><g>
<animateTransform attributeName="transform" type="translate" calcMode="spline" keyTimes="{kt}" keySplines="{ks}" values="{gap0} -4;{gap1} 0;{gap1} 0;{gap0} -4" dur="{dur}s" repeatCount="indefinite"/>
{robot_hand()}
</g></g>
<circle cx="600" cy="{CY}" r="34" fill="url(#spark)" opacity="0">
<animate attributeName="opacity" values="0;0;1;0.85;0;0" keyTimes="{flash_kt}" dur="{dur}s" repeatCount="indefinite"/>
<animate attributeName="r" values="10;10;34;28;12;10" keyTimes="{flash_kt}" dur="{dur}s" repeatCount="indefinite"/></circle>
<path d="{"".join(rays)}" stroke="#bff3ff" stroke-width="1.6" stroke-linecap="round" opacity="0">
<animate attributeName="opacity" values="0;0;1;0.3;0;0" keyTimes="{flash_kt}" dur="{dur}s" repeatCount="indefinite"/></path>
<circle cx="600" cy="{CY}" r="6" fill="none" stroke="#7ee0ff" stroke-width="1.5" opacity="0">
<animate attributeName="r" values="6;6;6;70;70" keyTimes="0;0.42;0.43;0.75;1" dur="{dur}s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;0;0.9;0;0" keyTimes="0;0.42;0.43;0.75;1" dur="{dur}s" repeatCount="indefinite"/></circle>
</g>
</svg>
'''
    return svg


open(os.path.join(OUT, "banner.svg"), "w", encoding="utf-8").write(banner())
open(os.path.join(OUT, "hands.svg"), "w", encoding="utf-8").write(hands())
for n in ("banner.svg", "hands.svg"):
    print(n, os.path.getsize(os.path.join(OUT, n)) // 1000, "kB")
