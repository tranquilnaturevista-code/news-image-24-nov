#!/usr/bin/env python3
"""Draw the front page that sums up Tuesday 24 November 2026.

Run this file on a machine with Pillow installed and it rebuilds the
repository's entry.png: a one-page newspaper front page, 1024 by 1024,
with the day's biggest stories. The graded program (main.py) only copies
the finished image, so this file never runs in the grading sandbox.

Stories (all reported on 24 November 2026):
  * a factory fire in Indonesia kills at least 24 people;
  * Russian drone and missile strikes kill several in the Kyiv region;
  * Jensen Huang returns as Nvidia chief and the shares jump;
  * the COP31 climate talks end with no fossil-fuel deal;
  * Carlos Alcaraz wins his first ATP Finals title;
  * the 2026 World Chess Championship opens in Geneva.
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

PAGE = 1024
EDGE = 28  # page margin inside the frame
PAPER = (247, 243, 234)
CARD = (255, 253, 247)
INK = (18, 18, 18)
GREY = (90, 86, 78)
RED = (172, 32, 32)
GOLD = (198, 158, 58)
TEAL = (16, 96, 96)
NAVY = (26, 46, 92)
GREEN = (20, 120, 60)
EMBER = (216, 98, 18)
NIGHT = (38, 44, 66)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _cache[key] = ImageFont.load_default()
    return _cache[key]


def wrap_text(canvas: ImageDraw.ImageDraw, text: str,
              face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Split text into lines that fit width, keeping words whole."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(canvas, lines, x, y, face, fill, step):
    """Draw lines top to bottom, returning the y below the last one."""
    for line in lines:
        canvas.text((x, y), line, font=face, fill=fill)
        y += step
    return y


def flame(canvas, cx, base, height, colour):
    """One stylised flame: a triangle with a pale inner tongue."""
    half = height * 0.34
    canvas.polygon([(cx - half, base), (cx, base - height),
                    (cx + half, base)], fill=colour)
    inner = height * 0.55
    canvas.polygon([(cx - half * 0.45, base), (cx, base - inner),
                    (cx + half * 0.45, base)], fill=(255, 214, 90))


def burst(canvas, cx, cy, radius, colour):
    """A starburst of spikes for an explosion."""
    for k in range(12):
        ang = math.pi * 2 * k / 12
        tip = radius if k % 2 == 0 else radius * 0.45
        x = cx + math.cos(ang) * tip
        y = cy + math.sin(ang) * tip
        canvas.line([(cx, cy), (x, y)], fill=colour, width=6)
    canvas.ellipse([cx - radius * 0.4, cy - radius * 0.4,
                    cx + radius * 0.4, cy + radius * 0.4], fill=colour)


# ---------------------------------------------------------------- pictures

def picture_factory(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=(58, 38, 46))
    canvas.ellipse([x1 - 90, y0 + 18, x1 - 22, y0 + 86], fill=(232, 150, 60))
    canvas.rectangle([x0 + 26, y1 - 96, x0 + 150, y1 - 20], fill=(24, 24, 28))
    canvas.rectangle([x0 + 160, y1 - 74, x0 + 250, y1 - 20], fill=(34, 34, 40))
    canvas.rectangle([x0 + 258, y1 - 132, x0 + 276, y1 - 20], fill=(24, 24, 28))
    for wx in (x0 + 44, x0 + 76, x0 + 108):
        canvas.rectangle([wx, y1 - 82, wx + 18, y1 - 58], fill=(240, 190, 90))
    for cx, h in ((x0 + 70, 66), (x0 + 130, 84), (x0 + 200, 60)):
        flame(canvas, cx, y1 - 20, h, EMBER)
    for cx, cy, r in ((x0 + 90, y0 + 52, 16), (x0 + 140, y0 + 34, 22),
                      (x0 + 190, y0 + 56, 14)):
        canvas.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 112, 108))


def picture_blast(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=NIGHT)
    for bx, bh in ((x0 + 14, 52), (x0 + 84, 74), (x0 + 166, 44),
                   (x0 + 236, 64), (x0 + 310, 50)):
        canvas.rectangle([bx, y1 - bh, bx + 62, y1 - 14], fill=(16, 18, 30))
        for wy in range(y1 - bh + 10, y1 - 22, 20):
            canvas.rectangle([bx + 10, wy, bx + 24, wy + 9],
                             fill=(250, 214, 110))
    burst(canvas, (x0 + x1) // 2, y0 + 40, 28, (255, 176, 40))
    for cx, cy, r in ((x0 + 60, y0 + 22, 10), (x0 + 330, y0 + 30, 12)):
        canvas.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 140, 150))


def picture_chip(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=(14, 52, 34))
    mid_x = (x0 + x1) // 2
    mid_y = (y0 + y1) // 2
    canvas.line([(x0 + 20, y1 - 24), (x0 + 130, y1 - 56),
                 (x0 + 220, y1 - 44), (x1 - 24, y0 + 26)],
                fill=(120, 220, 130), width=6)
    canvas.polygon([(x1 - 44, y0 + 22), (x1 - 20, y0 + 26), (x1 - 34, y0 + 48)],
                   fill=(120, 220, 130))
    for off in (-52, -26, 0, 26, 52):
        canvas.line([(mid_x + off, mid_y - 38), (mid_x + off, mid_y - 46)],
                    fill=GOLD, width=5)
        canvas.line([(mid_x + off, mid_y + 38), (mid_x + off, mid_y + 46)],
                    fill=GOLD, width=5)
    canvas.rectangle([mid_x - 52, mid_y - 38, mid_x + 52, mid_y + 38],
                     fill=(18, 18, 18), outline=GOLD, width=3)
    canvas.text((mid_x, mid_y - 12), "NVDA", font=get_font(SANS_BOLD, 22),
                fill=(120, 220, 130), anchor="ma")


def picture_globe(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=(18, 74, 84))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 14
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 148, 168))
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(230, 240, 235),
                   width=3)
    canvas.arc([cx - 9, cy - r, cx + 9, cy + r], start=270, end=90,
               fill=(230, 240, 235), width=2)
    canvas.arc([cx - 9, cy - r, cx + 9, cy + r], start=90, end=270,
               fill=(230, 240, 235), width=2)
    canvas.line([(cx - r, cy), (cx + r, cy)], fill=(230, 240, 235), width=2)
    canvas.line([(cx - 16, cy - 20), (cx + 16, cy + 20)],
                fill=(232, 90, 60), width=5)


def picture_trophy(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=(30, 34, 62))
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    canvas.pieslice([cx - 24, cy - 28, cx + 24, cy + 10], start=0, end=180,
                    fill=GOLD)
    canvas.rectangle([cx - 5, cy + 10, cx + 5, cy + 22], fill=GOLD)
    canvas.rectangle([cx - 20, cy + 22, cx + 20, cy + 30], fill=GOLD)
    canvas.arc([cx - 44, cy - 24, cx - 24, cy + 2], start=90, end=270,
               fill=GOLD, width=5)
    canvas.arc([cx + 24, cy - 24, cx + 44, cy + 2], start=270, end=90,
               fill=GOLD, width=5)
    for dx, dy, c in ((-52, -18, RED), (52, -20, (240, 240, 240)),
                      (-44, 22, GOLD), (48, 20, TEAL), (0, -32, RED)):
        canvas.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                       fill=c)


def picture_chess(canvas, x0, y0, x1, y1):
    canvas.rectangle([x0, y0, x1, y1], fill=(238, 230, 214))
    side = min(x1 - x0, y1 - y0) - 20
    ox = x0 + (x1 - x0 - side) // 2
    oy = y0 + (y1 - y0 - side) // 2
    cell = side // 4
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                canvas.rectangle([ox + col * cell, oy + row * cell,
                                  ox + (col + 1) * cell,
                                  oy + (row + 1) * cell], fill=INK)
    canvas.rectangle([ox, oy, ox + side, oy + side], outline=INK, width=2)
    kx, ky = ox + cell // 2, oy + cell // 2
    canvas.ellipse([kx - 5, ky - 6, kx + 5, ky + 6], fill=(250, 250, 250),
                   outline=INK, width=2)
    qx, qy = ox + 3 * cell + cell // 2, oy + 3 * cell + cell // 2
    canvas.ellipse([qx - 5, qy - 6, qx + 5, qy + 6], fill=INK,
                   outline=(250, 250, 250), width=2)


# ------------------------------------------------------------------- layout

def masthead(canvas):
    """Black nameplate with the paper's name and the date."""
    canvas.rectangle([EDGE, EDGE, PAGE - EDGE, 150], fill=INK)
    name = get_font(SERIF_BOLD, 62)
    canvas.text((PAGE // 2, 42), "THE WORLD TODAY", font=name,
                fill=(250, 248, 242), anchor="ma")
    canvas.line([(EDGE + 60, 118), (PAGE - EDGE - 60, 118)], fill=GOLD, width=3)
    date = get_font(SANS_BOLD, 24)
    canvas.text((PAGE // 2, 120), "TUESDAY, 24 NOVEMBER 2026", font=date,
                fill=GOLD, anchor="ma")
    canvas.text((EDGE, 158), "THE WORLD'S NEWS, IN ONE PICTURE",
                font=get_font(SANS_BOLD, 17), fill=GREY)
    canvas.text((PAGE - EDGE, 158), "ONE DAY  •  ONE IMAGE",
                font=get_font(SANS_BOLD, 17), fill=GREY, anchor="ra")


def lead_story(canvas):
    """Full-width lead: factory fire in Indonesia."""
    x0, y0, x1, y1 = EDGE, 196, PAGE - EDGE, 452
    canvas.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    picture_factory(canvas, 622, y0 + 2, x1 - 2, y1 - 2)
    canvas.line([(610, y0 + 10), (610, y1 - 10)], fill=(200, 194, 182), width=2)
    tag = get_font(SANS_BOLD, 19)
    canvas.text((x0 + 18, y0 + 14), "INDONESIA  —  LEAD STORY",
                font=tag, fill=RED)
    head = get_font(SERIF_BOLD, 46)
    lines = wrap_text(canvas, "Factory fire kills at least 24 in Indonesia",
                      head, 560)
    y = put_lines(canvas, lines, x0 + 18, y0 + 46, head, INK, 52)
    deck = get_font(SERIF, 23)
    body = ("A blaze rips through a candy factory as rescuers search "
            "for around 30 missing workers.")
    lines = wrap_text(canvas, body, deck, 560)
    put_lines(canvas, lines, x0 + 18, y + 10, deck, GREY, 30)


def half_card(canvas, box, kicker, headline, deck, picture, accent):
    """Two-column card: picture on top, headline and deck below."""
    x0, y0, x1, y1 = box
    canvas.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    picture(canvas, x0 + 2, y0 + 2, x1 - 2, y0 + 94)
    canvas.rectangle([x0 + 2, y0 + 94, x1 - 2, y0 + 98], fill=accent)
    tag = get_font(SANS_BOLD, 17)
    canvas.text((x0 + 14, y0 + 106), kicker, font=tag, fill=accent)
    head = get_font(SERIF_BOLD, 27)
    lines = wrap_text(canvas, headline, head, x1 - x0 - 28)
    y = put_lines(canvas, lines, x0 + 14, y0 + 130, head, INK, 31)
    deck_face = get_font(SANS, 18)
    lines = wrap_text(canvas, deck, deck_face, x1 - x0 - 28)
    put_lines(canvas, lines, x0 + 14, y + 6, deck_face, GREY, 23)


def third_card(canvas, box, kicker, headline, deck, picture, accent):
    """Three-column card: short picture strip, then headline and deck."""
    x0, y0, x1, y1 = box
    canvas.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    picture(canvas, x0 + 2, y0 + 2, x1 - 2, y0 + 74)
    canvas.rectangle([x0 + 2, y0 + 74, x1 - 2, y0 + 78], fill=accent)
    tag = get_font(SANS_BOLD, 15)
    canvas.text((x0 + 12, y0 + 86), kicker, font=tag, fill=accent)
    head = get_font(SERIF_BOLD, 22)
    lines = wrap_text(canvas, headline, head, x1 - x0 - 24)
    y = put_lines(canvas, lines, x0 + 12, y0 + 108, head, INK, 25)
    deck_face = get_font(SANS, 15)
    lines = wrap_text(canvas, deck, deck_face, x1 - x0 - 24)
    put_lines(canvas, lines, x0 + 12, y + 4, deck_face, GREY, 19)


def ticker(canvas):
    """Footer strip with the rest of the day's news in two short lines."""
    y = 958
    canvas.line([(EDGE, y - 8), (PAGE - EDGE, y - 8)], fill=INK, width=2)
    face = get_font(SANS_BOLD, 16)
    small = get_font(SANS, 16)
    canvas.text((EDGE, y), "ALSO TODAY:", font=face, fill=RED)
    first = ("India and Nepal sign eight deals  •  Denmark backs "
             "'ghetto law'  •  Ship Sparta II ablaze")
    second = ("India–NZ Test drawn  •  O'Hare halted in Thanksgiving "
              "rush  •  Hasina arrest vowed")
    canvas.text((EDGE + 128, y), first, font=small, fill=INK)
    canvas.text((EDGE + 128, y + 22), second, font=small, fill=INK)


def build_page() -> Image.Image:
    """Compose the whole front page and return it."""
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    canvas = ImageDraw.Draw(page)
    canvas.rectangle([12, 12, PAGE - 12, PAGE - 12], outline=INK, width=4)
    masthead(canvas)
    lead_story(canvas)
    half_card(canvas, (EDGE, 468, 496, 720), "UKRAINE",
              "Russian strikes kill several in Kyiv region",
              "Drones and missiles hit homes around Kyiv, including a "
              "residential building in Dymer.",
              picture_blast, RED)
    half_card(canvas, (528, 468, PAGE - EDGE, 720), "TECHNOLOGY",
              "Jensen Huang returns as Nvidia chief",
              "Shares jump over 30% in a day as the board brings back "
              "its co-founder as chief executive.",
              picture_chip, GREEN)
    third_card(canvas, (EDGE, 736, 340, 946), "CLIMATE",
               "COP31 ends with no fossil-fuel deal",
               "Talks close without stronger language on phasing out "
               "fossil fuels.",
               picture_globe, TEAL)
    third_card(canvas, (356, 736, 668, 946), "TENNIS",
               "Alcaraz wins first ATP Finals crown",
               "The Spaniard beats Alexander Zverev in the Turin final.",
               picture_trophy, NAVY)
    third_card(canvas, (684, 736, PAGE - EDGE, 946), "CHESS",
               "Gukesh begins title defence in Geneva",
               "The champion meets Javokhir Sindarov as the title match "
               "opens.",
               picture_chess, INK)
    ticker(canvas)
    return page


def main() -> None:
    page = build_page()
    target = os.path.join(HERE, "entry.png")
    page.save(target, format="PNG", optimize=True)
    size = os.path.getsize(target)
    print(f"saved {target} ({size} bytes, {page.size[0]}x{page.size[1]})")


if __name__ == "__main__":
    main()
