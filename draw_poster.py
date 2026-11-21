"""Render entry.png: a vintage travel poster for VELMORA.

VELMORA is an invented place: a lagoon where lantern-lit islands float
above a mirror sea at golden dusk. One landmark: a slender lighthouse
tower with a glowing orb, on the largest floating island.

Run locally with Pillow installed:  python3 draw_poster.py
Everything is drawn with plain PIL shapes and DejaVu fonts; no network.
Output is deterministic: 1024x1024 PNG.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"

# Palette: deep teal sea/sky -> amber/gold sun -> warm cream type.
TEAL_TOP = (13, 46, 56)
TEAL_MID = (24, 84, 92)
TEAL_DEEP = (10, 38, 48)
GOLD = (246, 196, 83)
GOLD_DEEP = (232, 163, 76)
AMBER = (238, 178, 96)
CREAM = (247, 232, 200)
CREAM_DIM = (228, 205, 164)
ISLAND = (18, 52, 58)
ISLAND_LIT = (46, 96, 92)
TOWER = (244, 228, 188)
TOWER_BAND = (30, 74, 80)
SEA_TOP = (23, 74, 84)
SEA_BOT = (8, 30, 40)
HORIZON = 640


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, x0, y0, x1, y1, c0, c1):
    """Vertical gradient band."""
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(c0, c1, (y - y0) / h))


def glow_circle(base, cx, cy, r, color, steps=24):
    """Soft radial glow: concentric translucent circles on `base`."""
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(70 * (1 - i / steps) ** 2) + 6
        od.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                   fill=color + (a,))
    base.alpha_composite(ov)


def tracked_text(d, cx, y, text, font, fill, tracking=18, shadow=None):
    """Draw centred text with letter tracking; returns (top, bottom)."""
    widths = []
    total = 0
    for ch in text:
        w = d.textbbox((0, 0), ch, font=font)[2]
        widths.append(w)
        total += w
    total += tracking * (len(text) - 1)
    x = cx - total // 2
    top = y
    bottom = y
    for ch, w in zip(text, widths):
        bbox = d.textbbox((x, y), ch, font=font)
        bottom = max(bottom, bbox[3])
        if shadow:
            d.text((x + 4, y + 5), ch, font=font, fill=shadow)
        d.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return top, bottom


def island_shape(d, cx, top, width, depth, fill, rim=None):
    """A floating island: domed top, gently rounded underside."""
    x0, x1 = cx - width // 2, cx + width // 2
    pts_top = []
    for i in range(33):
        t = i / 32
        x = x0 + t * width
        y = top - int(math.sin(t * math.pi) * depth * 0.35)
        pts_top.append((x, y))
    # rounded keel: trace the underside right -> left so the polygon
    # never self-intersects (a bowtie would leave the middle unfilled)
    keel_pts = [(cx + width * 0.22, top + depth * 0.78),
                (cx, top + depth),
                (cx - width * 0.22, top + depth * 0.78)]
    d.polygon(pts_top + keel_pts, fill=fill)
    if rim:
        d.line(pts_top, fill=rim, width=3)


def main():
    img = Image.new("RGB", (W, H), TEAL_TOP)
    d = ImageDraw.Draw(img)

    # --- sky: deep teal down to warm amber at the horizon ---
    vgrad(d, 0, 0, W, HORIZON, TEAL_TOP, TEAL_MID)
    vgrad(d, 0, 470, W, HORIZON, TEAL_MID, GOLD_DEEP)

    # --- sun: big golden disc low over the horizon, with halo ---
    sun_cx, sun_cy, sun_r = 512, 468, 108
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_circle(img.convert("RGBA"), sun_cx, sun_cy, 260, GOLD)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r,
               sun_cx + sun_r, sun_cy + sun_r], fill=GOLD)
    d.ellipse([sun_cx - sun_r + 14, sun_cy - sun_r + 14,
               sun_cx + sun_r - 14, sun_cy + sun_r - 14], fill=(250, 214, 120))

    # --- thin warm cloud bands, kept clear of the centre column ---
    for (x0, cy, cw, ch, col) in [
            (90, 312, 280, 11, (247, 214, 150)),
            (660, 330, 270, 10, (240, 196, 130)),
            (120, 408, 220, 9, (244, 205, 140)),
            (700, 412, 230, 8, (238, 190, 120))]:
        d.rounded_rectangle([x0, cy, x0 + cw, cy + ch], radius=ch // 2,
                            fill=col)

    # --- birds ---
    for (bx, by, s) in [(240, 300, 15), (790, 288, 13), (180, 372, 12),
                        (838, 372, 11)]:
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340,
              fill=(16, 44, 50), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340,
              fill=(16, 44, 50), width=3)

    # --- sea: mirror water below the horizon ---
    vgrad(d, 0, HORIZON, W, H, SEA_TOP, SEA_BOT)

    # sun reflection: a glittering column under the sun, fading with depth
    rng = random.Random(7)
    for i in range(52):
        y = HORIZON + 14 + i * 7
        t = i / 52
        wdt = int(46 + 110 * (1 - t) + rng.randint(-12, 12))
        x0 = 512 - wdt // 2
        col = lerp(GOLD, SEA_BOT, t * 0.85)
        d.line([(x0, y), (x0 + wdt, y)], fill=col, width=2)
    # faint horizontal ripples
    for y in (700, 760, 830, 905, 970):
        d.line([(90, y), (934, y)], fill=(60, 120, 124), width=2)

    # tower reflection in the water, under the central island
    for i in range(16):
        y = HORIZON + 26 + i * 7
        wdt = max(6, 40 - i * 2)
        col = lerp(TOWER, SEA_BOT, i / 16)
        d.line([(512 - wdt // 2, y), (512 + wdt // 2, y)], fill=col, width=2)

    # --- floating islands ---
    # small left island
    island_shape(d, 185, 596, 190, 34, ISLAND, rim=ISLAND_LIT)
    # small right island
    island_shape(d, 845, 606, 160, 30, ISLAND, rim=ISLAND_LIT)
    # big central island (the landmark's island)
    island_shape(d, 512, 556, 560, 62, ISLAND, rim=ISLAND_LIT)

    # lantern dots along the islands
    for (lx, ly) in [(120, 590), (185, 584), (250, 590), (790, 600),
                     (845, 596), (900, 600), (300, 566), (724, 566)]:
        d.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], fill=GOLD)
    # soft glow under the floating islands
    glow_img = img.convert("RGBA")
    glow_circle(glow_img, 512, 660, 200, (60, 140, 140))
    glow_circle(glow_img, 185, 656, 80, (60, 140, 140))
    glow_circle(glow_img, 845, 660, 70, (60, 140, 140))
    img = glow_img.convert("RGB")
    d = ImageDraw.Draw(img)

    # --- THE LANDMARK: slender lighthouse tower with a glowing orb ---
    tx0, tx1 = 489, 535  # tower base width
    top_y, base_y = 330, 556
    d.polygon([(tx0, base_y), (tx1, base_y), (527, top_y), (497, top_y)],
              fill=TOWER)
    # dark bands on the tower
    for (by0, by1) in [(392, 414), (452, 474)]:
        t0 = (by0 - top_y) / (base_y - top_y)
        t1 = (by1 - top_y) / (base_y - top_y)
        xa0 = tx0 + (497 - tx0) * t0
        xa1 = tx1 + (527 - tx1) * t0
        xb0 = tx0 + (497 - tx0) * t1
        xb1 = tx1 + (527 - tx1) * t1
        d.polygon([(xa0, by0), (xa1, by0), (xb1, by1), (xb0, by1)],
                  fill=TOWER_BAND)
    # gallery + orb
    d.rectangle([488, 318, 536, 332], fill=TOWER_BAND)
    glow2 = img.convert("RGBA")
    glow_circle(glow2, 512, 296, 90, GOLD)
    img = glow2.convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse([512 - 24, 296 - 24, 512 + 24, 296 + 24], fill=(252, 224, 140))
    d.ellipse([512 - 15, 296 - 15, 512 + 15, 296 + 15], fill=(255, 240, 190))
    # tower windows, warm lit
    for wy in (352, 432, 508):
        d.ellipse([508, wy, 516, wy + 12], fill=GOLD_DEEP)

    # --- name: VELMORA, big cream serif across the upper third ---
    # auto-fit: shrink until the tracked name fits inside the frame
    size = 148
    while size > 60:
        name_font = ImageFont.truetype(SERIF_B, size)
        widths = [d.textbbox((0, 0), ch, font=name_font)[2] for ch in "VELMORA"]
        if sum(widths) + 22 * 6 <= 920:
            break
        size -= 4
    top, bottom = tracked_text(d, 512, 92, "VELMORA", name_font, CREAM,
                               tracking=22, shadow=(10, 34, 42))
    # thin gold rules flanking a small diamond under the name
    d.line([(212, 268), (452, 268)], fill=GOLD, width=3)
    d.line([(572, 268), (812, 268)], fill=GOLD, width=3)
    d.polygon([(512, 258), (522, 268), (512, 278), (502, 268)], fill=GOLD)

    # --- classic poster frame ---
    d.rectangle([28, 28, W - 28, H - 28], outline=CREAM, width=4)
    d.rectangle([38, 38, W - 38, H - 38], outline=(247, 232, 200), width=1)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
