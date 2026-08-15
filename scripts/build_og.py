#!/usr/bin/env python3
"""
Generate the Living Intelligence OG card (1200x627) as SVG + PNG.

Text is converted to outlines, so the SVG renders identically anywhere
without loading a webfont. Design tokens are copied from index.html --
if you change them there, change them here.

Setup
-----
    pip install fonttools cairosvg brotli
    npm pack @ibm/plex-sans && tar xzf ibm-plex-sans-*.tgz
    # fonts land in package/fonts/complete/woff/

Run
---
    python3 build_og.py            # writes og-1200x627.svg and .png
"""

import math
import pathlib

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------

FONT_DIR = pathlib.Path('package/fonts/complete/woff')
OUT_SVG = pathlib.Path('og-1200x627.svg')
OUT_PNG = pathlib.Path('og-1200x627.png')

# --------------------------------------------------------------------------
# design tokens -- keep in sync with :root in index.html
# --------------------------------------------------------------------------

W, H = 1200, 627

BG = '#0D0B09'
FG = '#F5F0E8'          # --fg, wordmark
FG_SOFT = '#E8DDD0'     # --fg-soft, tagline
G1, G2, G3 = '#A93415', '#E4572E', '#F5A623'   # heat gradient

FIELD_ANGLE = 158       # CSS deg
FIELD_STOPS = [(0.00, '#42362A'), (0.26, '#2B231B'), (0.58, '#191410'),
               (0.82, '#0B0908'), (1.00, '#030202')]

GLOW_CX, GLOW_CY, GLOW_R = 600, 150, 620
GLOW_OPACITY = 0.16     # rgba(228,87,46,.16)

WORDMARK = 'LIVING INTELLIGENCE'
TAGLINE = 'Intelligence for living, that lives.'

# lockup -- scaled up from the on-page sizes so the card reads at feed scale
MARK = 196.0            # mark box, px
GAP = 42.0              # mark -> names gap
WM_SIZE = 54.0
WM_TRACK = 0.15         # em, matches h1 letter-spacing
MO_SIZE = 32.0
MO_TRACK = 0.005
NAME_GAP = 9.0          # wordmark -> tagline
LOCKUP_CY = 313.0       # vertical centre of the lockup

# mark geometry, verbatim from index.html
VB_X, VB_Y, VB_W, VB_H = -80.6, -49.1, 351.3, 350.3
MARK_STROKE = 25
MARK_PATH = ("M -54.13 274.63 L -31.50 252.00 L 190.00 252.00 "
             "A 31.5 31.5 0 0 0 190.00 189.00 L 0.00 189.00 "
             "A 31.5 31.5 0 0 1 0.00 126.00 L 190.00 126.00 "
             "A 31.5 31.5 0 0 0 190.00 63.00 L 0.00 63.00 "
             "A 31.5 31.5 0 0 1 0.00 0.00 L 190.00 0.00 "
             "L 221.50 0.00 L 244.13 -22.63")

# IBM Plex Sans hhea metrics per 1000 upm -> browsers use a 1.30em content box
CONTENT_BOX = 1.30
ASCENT = 1.025


# --------------------------------------------------------------------------
# text -> outlines
# --------------------------------------------------------------------------

class Face:
    """Renders a string as SVG <path> outlines at a given size and tracking."""

    def __init__(self, path):
        self.font = TTFont(path)
        self.upm = self.font['head'].unitsPerEm
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font['hmtx']

    def text(self, s, size, tracking_em=0.0, x=0.0, baseline=0.0):
        """Return (svg_fragment, advance_width). Trailing tracking is dropped."""
        scale = size / self.upm
        track = tracking_em * size
        pen_x = x
        parts = []
        for ch in s:
            name = self.cmap[ord(ch)]
            pen = SVGPathPen(self.glyphs, ntos=lambda v: f'{v:.2f}')
            self.glyphs[name].draw(pen)
            d = pen.getCommands()
            if d:  # skip whitespace
                parts.append(
                    f'<path transform="translate({pen_x:.2f},{baseline:.2f}) '
                    f'scale({scale:.6f},{-scale:.6f})" d="{d}"/>'
                )
            pen_x += self.hmtx[name][0] * scale + track
        return ''.join(parts), pen_x - x - track


def baseline_offset(size, line_height_mult):
    """Baseline distance from the top of a CSS line box, and the box height."""
    line_height = size * line_height_mult
    half_leading = (line_height - CONTENT_BOX * size) / 2
    return half_leading + ASCENT * size, line_height


def css_linear_gradient(angle_deg, w, h):
    """CSS <angle> -> SVG userSpaceOnUse x1,y1,x2,y2 across a w*h box."""
    a = math.radians(angle_deg)
    dx, dy = math.sin(a), -math.cos(a)          # SVG y grows downward
    length = abs(w * math.sin(a)) + abs(h * math.cos(a))
    cx, cy = w / 2, h / 2
    return (cx - dx * length / 2, cy - dy * length / 2,
            cx + dx * length / 2, cy + dy * length / 2)


# --------------------------------------------------------------------------
# layout
# --------------------------------------------------------------------------

def build():
    medium = Face(FONT_DIR / 'IBMPlexSans-Medium.woff')    # 500, wordmark
    regular = Face(FONT_DIR / 'IBMPlexSans-Regular.woff')  # 400, tagline

    _, wm_w = medium.text(WORDMARK, WM_SIZE, WM_TRACK)
    _, mo_w = regular.text(TAGLINE, MO_SIZE, MO_TRACK)

    # horizontal: centre the whole lockup
    lockup_w = MARK + GAP + max(wm_w, mo_w)
    lockup_x = (W - lockup_w) / 2
    names_x = lockup_x + MARK + GAP

    # vertical: names block centred against the mark (flex align-items:center)
    wm_bl, wm_lh = baseline_offset(WM_SIZE, 1.02)
    mo_bl, mo_lh = baseline_offset(MO_SIZE, 1.30)
    names_h = wm_lh + NAME_GAP + mo_lh
    names_top = LOCKUP_CY - names_h / 2

    wm_d, _ = medium.text(WORDMARK, WM_SIZE, WM_TRACK,
                          x=names_x, baseline=names_top + wm_bl)
    mo_d, _ = regular.text(TAGLINE, MO_SIZE, MO_TRACK,
                           x=names_x, baseline=names_top + wm_lh + NAME_GAP + mo_bl)

    # mark: emulate preserveAspectRatio="xMidYMid meet" into a MARK-square box
    scale = min(MARK / VB_W, MARK / VB_H)
    tx = lockup_x - VB_X * scale
    ty = (LOCKUP_CY - MARK / 2) + (MARK - VB_H * scale) / 2 - VB_Y * scale

    x1, y1, x2, y2 = css_linear_gradient(FIELD_ANGLE, W, H)
    stops = '\n      '.join(
        f'<stop offset="{o}" stop-color="{c}"/>' for o, c in FIELD_STOPS)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img"
     aria-label="Living Intelligence — {TAGLINE}">
  <title>Living Intelligence — {TAGLINE}</title>
  <defs>
    <linearGradient id="field" gradientUnits="userSpaceOnUse"
      x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}">
      {stops}
    </linearGradient>
    <radialGradient id="glow" gradientUnits="userSpaceOnUse"
      cx="{GLOW_CX}" cy="{GLOW_CY}" r="{GLOW_R}">
      <stop offset="0" stop-color="{G2}" stop-opacity="{GLOW_OPACITY}"/>
      <stop offset="0.72" stop-color="{G2}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="liHeat" gradientUnits="userSpaceOnUse"
      x1="{VB_X}" y1="301.2" x2="270.7" y2="{VB_Y}">
      <stop offset="0" stop-color="{G1}"/>
      <stop offset="0.5" stop-color="{G2}"/>
      <stop offset="1" stop-color="{G3}"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#field)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>

  <g transform="translate({tx:.3f},{ty:.3f}) scale({scale:.6f})">
    <path d="{MARK_PATH}" fill="none" stroke="url(#liHeat)"
          stroke-width="{MARK_STROKE}" stroke-linecap="round"/>
  </g>

  <g fill="{FG}">{wm_d}</g>
  <g fill="{FG_SOFT}" opacity="0.92">{mo_d}</g>
</svg>
'''


if __name__ == '__main__':
    svg = build()
    OUT_SVG.write_text(svg)

    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT_PNG),
                     output_width=W, output_height=H)

    print(f'wrote {OUT_SVG} and {OUT_PNG}')
