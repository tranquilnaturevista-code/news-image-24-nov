#!/usr/bin/env python3
"""Paint the front page for Tuesday 24 November 2026 and save entry.png.

The page is a one-day newspaper front page drawn from scratch with
Pillow drawing calls: a masthead, a dateline, one lead story, six story
cards in a two-column grid, a ticker of shorter items and a footer with
sources. There is no network access, no randomness and no clock in here,
so running the script twice gives the same bytes twice.

Every story below was reported on Tuesday 24 November 2026 (or, for
the overnight US stories, first published in Asian time zones on
24 November) by the outlets named in the footer. Where outlets
disagreed about a casualty figure, the page prints no figure at all
instead of guessing one.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024

# --- palette ------------------------------------------------------------
PAPER = (251, 246, 236)
INK = (25, 23, 19)
BODY = (64, 60, 52)
MUTED = (92, 86, 76)
NAVY = (20, 54, 93)
NAVY_DEEP = (13, 38, 66)
SCARLET = (179, 38, 30)
GOLD = (201, 154, 43)
CARD = (255, 255, 255)
CARD_EDGE = (205, 198, 182)
LEAD_WASH = (232, 240, 247)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _load(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def serif(size, bold=False):
    return _load("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return _load("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


# --- text helpers -------------------------------------------------------

def wrap_text(draw, text, fnt, width):
    """Split text into lines no wider than width, breaking on spaces."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_lines(draw, lines, x, y, fnt, fill, step):
    """Draw lines top to bottom, returning the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="mm")


# --- shapes -------------------------------------------------------------

def star_points(cx, cy, outer, inner, count):
    """Vertices of a star, alternating outer and inner radius."""
    verts = []
    for i in range(count * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.pi * i / count - math.pi / 2
        verts.append((cx + radius * math.cos(angle),
                      cy + radius * math.sin(angle)))
    return verts


def paint_globe(draw, cx, cy, r, fg, ring):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=ring, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=ring, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             0, 360, fill=ring, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy - r * 0.25],
             180, 360, fill=ring, width=3)


def paint_burst(draw, cx, cy, r, fg):
    draw.polygon(star_points(cx, cy, r, r * 0.45, 8), fill=fg)
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
                 fill=WHITE)


def paint_ship(draw, cx, cy, r, fg):
    draw.polygon([(cx - r, cy - r * 0.1), (cx + r, cy - r * 0.1),
                  (cx + r * 0.7, cy + r * 0.55),
                  (cx - r * 0.7, cy + r * 0.55)], fill=fg)
    draw.rectangle([cx - r * 0.7, cy - r * 0.75, cx - r * 0.1, cy - r * 0.15],
                   fill=fg)
    draw.rectangle([cx + r * 0.05, cy - r * 0.6, cx + r * 0.65, cy - r * 0.15],
                   fill=fg)
    for k, yy in enumerate((cy + r * 0.75, cy + r * 0.9)):
        draw.arc([cx - r - 6 + k * 4, yy - 6, cx - r * 0.2 + k * 4, yy + 6],
                 180, 360, fill=fg, width=3)
        draw.arc([cx + r * 0.2 - k * 4, yy - 6, cx + r + 6 - k * 4, yy + 6],
                 180, 360, fill=fg, width=3)


def paint_drone(draw, cx, cy, r, fg):
    draw.ellipse([cx - r * 0.3, cy - r * 0.25, cx + r * 0.3, cy + r * 0.25],
                 fill=fg)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, py = cx + sx * r * 0.62, cy + sy * r * 0.55
        draw.line([px - r * 0.3, py, px + r * 0.3, py], fill=fg, width=4)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=fg)
    draw.line([cx - r * 0.3, cy, cx + r * 0.3, cy], fill=fg, width=3)


def paint_star(draw, cx, cy, r, fg):
    draw.polygon(star_points(cx, cy, r, r * 0.42, 5), fill=fg)
    draw.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18],
                 fill=WHITE)


def paint_chart(draw, cx, cy, r, fg):
    draw.line([cx - r * 0.8, cy + r * 0.7, cx + r * 0.8, cy + r * 0.7],
              fill=fg, width=4)
    draw.line([cx - r * 0.8, cy + r * 0.7, cx - r * 0.8, cy - r * 0.7],
              fill=fg, width=4)
    trace = [(cx - r * 0.65, cy + r * 0.35), (cx - r * 0.2, cy - r * 0.1),
             (cx + r * 0.15, cy + r * 0.1), (cx + r * 0.7, cy - r * 0.55)]
    draw.line(trace, fill=fg, width=5, joint="curve")
    draw.polygon([(cx + r * 0.7, cy - r * 0.55), (cx + r * 0.45, cy - r * 0.5),
                  (cx + r * 0.55, cy - r * 0.28)], fill=fg)


def paint_ballot(draw, cx, cy, r, fg):
    draw.rectangle([cx - r * 0.32, cy - r * 0.9, cx + r * 0.32, cy - r * 0.05],
                   fill=fg)
    draw.rectangle([cx - r * 0.75, cy - r * 0.05, cx + r * 0.75, cy + r * 0.75],
                   fill=fg)
    draw.line([cx - r * 0.45, cy + r * 0.32, cx - r * 0.12, cy + r * 0.58,
               cx + r * 0.5, cy + r * 0.02], fill=WHITE,
              width=5, joint="curve")


def paint_rocket(draw, cx, cy, r, fg):
    draw.polygon([(cx, cy - r), (cx + r * 0.45, cy - r * 0.1),
                  (cx + r * 0.45, cy + r * 0.45),
                  (cx - r * 0.45, cy + r * 0.45),
                  (cx - r * 0.45, cy - r * 0.1)], fill=fg)
    draw.ellipse([cx - r * 0.18, cy - r * 0.45, cx + r * 0.18, cy - r * 0.05],
                 fill=WHITE)
    draw.polygon([(cx - r * 0.45, cy + r * 0.25), (cx - r * 0.85, cy + r * 0.7),
                  (cx - r * 0.45, cy + r * 0.55)], fill=fg)
    draw.polygon([(cx + r * 0.45, cy + r * 0.25), (cx + r * 0.85, cy + r * 0.7),
                  (cx + r * 0.45, cy + r * 0.55)], fill=fg)
    draw.polygon([(cx - r * 0.25, cy + r * 0.55), (cx + r * 0.25, cy + r * 0.55),
                  (cx, cy + r)], fill=fg)


def paint_shield(draw, cx, cy, r, fg):
    draw.polygon([(cx - r * 0.8, cy - r * 0.7), (cx + r * 0.8, cy - r * 0.7),
                  (cx + r * 0.8, cy + r * 0.1), (cx, cy + r * 0.9),
                  (cx - r * 0.8, cy + r * 0.1)], fill=fg)
    draw.line([cx - r * 0.4, cy + r * 0.05, cx - r * 0.1, cy + r * 0.35,
               cx + r * 0.45, cy - r * 0.35], fill=WHITE,
              width=5, joint="curve")


PAINTERS = {
    "globe": paint_globe,
    "burst": paint_burst,
    "ship": paint_ship,
    "drone": paint_drone,
    "star": paint_star,
    "chart": paint_chart,
    "ballot": paint_ballot,
    "rocket": paint_rocket,
    "shield": paint_shield,
}


def badge(draw, cx, cy, r, color, kind):
    """A coloured disc with one of the pictograms inside it."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    painter = PAINTERS[kind]
    if kind == "globe":
        painter(draw, cx, cy, r * 0.72, WHITE, NAVY)
    else:
        painter(draw, cx, cy, r * 0.62, WHITE)


# --- the day's stories --------------------------------------------------

LEAD = {
    "tag": "MARKETS  •  WALL STREET",
    "headline": "Huang is back — Nvidia soars",
    "deck": ("Reinstated as chief executive, Jensen Huang watches "
             "Nvidia jump 31% in a day — about $950bn of value."),
}

ITEMS = [
    {
        "tag": "USA",
        "color": (169, 50, 38),
        "icon": "ballot",
        "headline": "Court revives Trump's bid to erase conviction",
        "deck": ("The 2nd Circuit revives his bid to move the hush-money "
                 "case to federal court."),
    },
    {
        "tag": "INDONESIA",
        "color": (180, 83, 9),
        "icon": "burst",
        "headline": "Factory fire toll at 24; dozens missing",
        "deck": ("Rescuers search the burned candy factory in Banten; "
                 "the toll is confirmed at 24."),
    },
    {
        "tag": "CLIMATE",
        "color": (15, 118, 110),
        "icon": "globe",
        "headline": "COP31 ends with no deal",
        "deck": ("The Antalya summit collapses over fossil fuels; talks "
                 "may resume next year."),
    },
    {
        "tag": "DENMARK",
        "color": (53, 80, 122),
        "icon": "shield",
        "headline": "Top court backs 'ghetto law' evictions",
        "deck": ("Denmark's Supreme Court rules ending 91 leases was "
                 "not ethnic discrimination."),
    },
    {
        "tag": "CHESS",
        "color": (107, 78, 155),
        "icon": "star",
        "headline": "World chess title match begins",
        "deck": ("Gukesh defends his crown against Sindarov in Geneva — "
                 "the youngest final ever."),
    },
    {
        "tag": "ASIA",
        "color": (47, 107, 51),
        "icon": "chart",
        "headline": "India, China hold military talks",
        "deck": ("The neighbours hold military-level talks in Arunachal "
                 "Pradesh to ease tensions."),
    },
]

TICKER = ("ALSO TODAY:  Alcaraz wins a first ATP Finals title  •  "
          "India–New Zealand Test ends in a draw  •  Waymo pulls "
          "driverless taxis from US freeways")

SOURCE_LINE = ("All stories as reported on Tuesday 24 November 2026  •  "
               "Sources: Reuters, BBC, AP, The Hindu, Chess.com")


# --- layout -------------------------------------------------------------

def compose():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: scarlet strip, navy band with the title, gold rule.
    d.rectangle([0, 0, PAGE_W, 10], fill=SCARLET)
    d.rectangle([0, 10, PAGE_W, 112], fill=NAVY)
    centred(d, PAGE_W // 2, 58, "THE WORLD IN ONE DAY", serif(62, bold=True),
            WHITE)
    d.rectangle([0, 112, PAGE_W, 116], fill=GOLD)

    # Dateline and standfirst, closed by a double rule.
    centred(d, PAGE_W // 2, 150, "TUESDAY 24 NOVEMBER 2026",
            serif(48, bold=True), NAVY_DEEP)
    centred(d, PAGE_W // 2, 192,
            "One day's world news — seven stories from every corner of the globe",
            serif(21), MUTED)
    d.line([36, 212, PAGE_W - 36, 212], fill=INK, width=3)
    d.line([36, 218, PAGE_W - 36, 218], fill=INK, width=1)

    # Lead story: a wide card with a scarlet spine and a globe badge.
    lx, ly, lw, lh = 36, 230, PAGE_W - 72, 138
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_WASH)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=NAVY, width=2)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=SCARLET)
    tx = lx + 28
    d.text((tx, ly + 14), LEAD["tag"], font=sans(18, bold=True), fill=SCARLET)
    head = wrap_text(d, LEAD["headline"], sans(38, bold=True), lw - 220)
    y = put_lines(d, head, tx, ly + 38, sans(38, bold=True), NAVY_DEEP, 44)
    deck = wrap_text(d, LEAD["deck"], sans(20), lw - 220)
    put_lines(d, deck, tx, y + 2, sans(20), INK, 25)
    badge(d, lx + lw - 82, ly + lh // 2, 56, NAVY, "globe")

    # Story grid: two columns, three rows of cards.
    gx, gy = 36, 382
    cw, ch, gap = (PAGE_W - 72 - 12) // 2, 170, 12
    for i, item in enumerate(ITEMS):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD)
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=CARD_EDGE, width=1)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=item["color"])
        pad = 16
        badge(d, cx + cw - 42, cy + 42, 28, item["color"], item["icon"])
        d.text((cx + pad, cy + 20), item["tag"],
               font=sans(17, bold=True), fill=item["color"])
        hl = wrap_text(d, item["headline"], sans(27, bold=True),
                       cw - pad * 2 - 70)
        y = put_lines(d, hl, cx + pad, cy + 48, sans(27, bold=True), INK, 31)
        dl = wrap_text(d, item["deck"], sans(19), cw - pad * 2)
        put_lines(d, dl, cx + pad, y + 4, sans(19), BODY, 23)

    # Ticker: a navy band with the shorter items of the day.
    ty = 382 + 3 * ch + 2 * gap + 8
    d.rectangle([36, ty, PAGE_W - 36, ty + 56], fill=NAVY)
    lines = wrap_text(d, TICKER, sans(19, bold=True), PAGE_W - 72 - 28)
    yy = ty + 28 - (len(lines) * 24) // 2
    for line in lines:
        centred(d, PAGE_W // 2, yy + 12, line, sans(19, bold=True), WHITE)
        yy += 24

    # Footer: a hairline and the sources line.
    fy = ty + 56 + 12
    d.line([36, fy, PAGE_W - 36, fy], fill=CARD_EDGE, width=1)
    d.text((PAGE_W // 2, fy + 6), SOURCE_LINE, font=sans(14),
           fill=MUTED, anchor="ma")

    return img


def main():
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("RENDER_OUTPUT_DIR", str(here)))
    out_dir.mkdir(parents=True, exist_ok=True)
    img = compose()
    target = out_dir / "entry.png"
    img.save(target, format="PNG")
    print(f"wrote {target} {img.size[0]}x{img.size[1]} "
          f"{target.stat().st_size} bytes")


if __name__ == "__main__":
    main()
