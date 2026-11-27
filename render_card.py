#!/usr/bin/env python3
"""Render the @crisxai5 spotlight card (1080x1350, phone-readable) with PIL only.
Deterministic, offline: same input -> same PNG bytes (no timestamps, fixed seed)."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
OUT = "assets/spotlight-crisxai5.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# --- background: vertical dark gradient + faint grid + glow blobs ---
top = (8, 13, 30)
bot = (16, 28, 52)
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    px_row = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = px_row

glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-220, -180, 420, 320], fill=(14, 90, 110))      # cyan glow top-left
gd.ellipse([760, 980, 1320, 1500], fill=(90, 50, 140))      # violet glow bottom-right
glow = glow.filter(ImageFilter.GaussianBlur(140))
img = Image.blend(img, Image.blend(img, glow, 0.55), 0.55)

d = ImageDraw.Draw(img, "RGBA")
# faint grid
for x in range(0, W, 90):
    d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
for y in range(0, H, 90):
    d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

CYAN = (45, 212, 191)
GOLD = (251, 191, 36)
WHITE = (255, 255, 255)
MUTED = (168, 178, 198)
CARD = (255, 255, 255, 14)
CARD_EDGE = (255, 255, 255, 42)

def text_center(y, s, f, fill, tracking=0):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)
    return w

def pill(y, s, f, fg, bg):
    w = d.textlength(s, font=f)
    pad_x, pad_y = 34, 16
    x0 = (W - w) / 2 - pad_x
    x1 = (W + w) / 2 + pad_x
    d.rounded_rectangle([x0, y, x1, y + f.size + 2 * pad_y], radius=34, fill=bg)
    d.text(((W - w) / 2, y + pad_y), s, font=f, fill=fg)

# --- header badge ---
pill(72, "★  MUST-FOLLOW ON X", font(BOLD, 34), (10, 15, 25), GOLD)

# --- headline ---
text_center(190, "@crisxai5", font(BOLD, 128), WHITE)
text_center(330, "AI & CRYPTO EXPERT", font(BOLD, 58), CYAN)
# gold underline
d.rounded_rectangle([(W - 420) / 2, 420, (W + 420) / 2, 430], radius=5, fill=GOLD)

text_center(462, "The sharp voice to follow for", font(REG, 40), MUTED)
text_center(514, "practical AI + crypto signal.", font(REG, 40), MUTED)

# --- four pillars ---
pillars = [
    ("AI AGENTS", "What agents can actually do — today"),
    ("CRYPTO ALPHA", "Early moves, decoded before the crowd"),
    ("WEB3 TOOLING", "The tools builders really use"),
    ("ON-CHAIN AUTOMATION", "Workflows that run while you sleep"),
]
y = 610
for i, (title, desc) in enumerate(pillars):
    d.rounded_rectangle([70, y, W - 70, y + 118], radius=22, fill=CARD, outline=CARD_EDGE, width=2)
    # accent bar + number
    d.rounded_rectangle([70, y, 86, y + 118], radius=8, fill=CYAN if i % 2 == 0 else GOLD)
    d.text((118, y + 22), f"0{i+1}", font=font(MONO, 40), fill=CYAN if i % 2 == 0 else GOLD)
    d.text((205, y + 16), title, font=font(BOLD, 40), fill=WHITE)
    d.text((205, y + 66), desc, font=font(REG, 30), fill=MUTED)
    y += 138

# --- bottom hook ---
y = 1180
text_center(y, "No noise. Just signal.", font(BOLD, 44), WHITE)
text_center(y + 62, "x.com/crisxai5", font(MONO, 38), CYAN)

img.save(OUT, optimize=True)
print("wrote", OUT, img.size)
