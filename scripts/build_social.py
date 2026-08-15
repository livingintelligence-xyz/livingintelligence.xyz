#!/usr/bin/env python3
"""
Generate the Living Intelligence social asset kit as SVG + PNG.

Same approach as build_og.py: tokens copied from index.html, text converted
to outlines so nothing depends on a webfont at render time.

Outputs
-------
    company-cover-1128x191.{svg,png}    LinkedIn company cover
    company-cover-4200x700.{svg,png}    LinkedIn company cover, hi-res
    link-preview-1200x627.{svg,png}     og:image / link card
    post-square-1080.{svg,png}          square post
    li-lockup-caps-1600.png             bare lockup, transparent
    li-lockup-caps.svg                  bare lockup, for dark backgrounds
    li-lockup-caps-white.svg            monochrome warm white
    li-lockup-caps-white-pure.svg       monochrome pure white
    li-lockup-caps-black.svg            monochrome near-black
    li-lockup-caps-light.svg            heat mark, dark text, for light backgrounds

Setup
-----
    pip install fonttools cairosvg brotli
    npm pack @ibm/plex-sans && tar xzf ibm-plex-sans-*.tgz

Run
---
    python3 build_social.py [outdir]
"""

import math
import pathlib
import sys

import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FONT_DIR = pathlib.Path('package/fonts/complete/woff')

# --------------------------------------------------------------------------
# design tokens -- keep in sync with :root in index.html
# --------------------------------------------------------------------------

BG = '#0D0B09'
FG = '#F5F0E8'          # --fg
FG_SOFT = '#E8DDD0'     # --fg-soft
MUTED = '#A8977F'       # --muted
INK = '#16130F'         # near-black, for light backgrounds
INK_SOFT = '#6E6252'
G1, G2, G3 = '#A93415', '#E4572E', '#F5A623'

FIELD_ANGLE = 158
FIELD_STOPS = [(0.00, '#42362A'), (0.26, '#2B231B'), (0.58, '#191410'),
               (0.82, '#0B0908'), (1.00, '#030202')]
GLOW_OPACITY = 0.16

WORDMARK = 'LIVING INTELLIGENCE'
TAGLINE = 'Intelligence for living, that lives.'

# lockup proportions, expressed against the mark box (from build_og.py)
GAP_R = 42 / 196
WM_R = 54 / 196
MO_R = 32 / 196
NAME_GAP_R = 9 / 196
WM_TRACK = 0.15
MO_TRACK = 0.005

# mark geometry, verbatim from index.html
VB_X, VB_Y, VB_W, VB_H = -80.6, -49.1, 351.3, 350.3
MARK_STROKE = 25
MARK_PATH = ("M -54.13 274.63 L -31.50 252.00 L 190.00 252.00 "
             "A 31.5 31.5 0 0 0 190.00 189.00 L 0.00 189.00 "
             "A 31.5 31.5 0 0 1 0.00 126.00 L 190.00 126.00 "
             "A 31.5 31.5 0 0 0 190.00 63.00 L 0.00 63.00 "
             "A 31.5 31.5 0 0 1 0.00 0.00 L 190.00 0.00 "
             "L 221.50 0.00 L 244.13 -22.63")

CONTENT_BOX = 1.30      # IBM Plex Sans hhea box, in em
ASCENT = 1.025


# --------------------------------------------------------------------------
# text -> outlines
# --------------------------------------------------------------------------

class Face:
    def __init__(self, path):
        self.font = TTFont(path)
        self.upm = self.font['head'].unitsPerEm
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font['hmtx']

    def text(self, s, size, tracking_em=0.0, x=0.0, baseline=0.0):
        scale = size / self.upm
        track = tracking_em * size
        pen_x, parts = x, []
        for ch in s:
            name = self.cmap[ord(ch)]
            pen = SVGPathPen(self.glyphs, ntos=lambda v: f'{v:.2f}')
            self.glyphs[name].draw(pen)
            d = pen.getCommands()
            if d:
                parts.append(
                    f'<path transform="translate({pen_x:.2f},{baseline:.2f}) '
                    f'scale({scale:.6f},{-scale:.6f})" d="{d}"/>'
                )
            pen_x += self.hmtx[name][0] * scale + track
        return ''.join(parts), pen_x - x - track


MEDIUM = Face(FONT_DIR / 'IBMPlexSans-Medium.woff')
REGULAR = Face(FONT_DIR / 'IBMPlexSans-Regular.woff')


def baseline_offset(size, line_height_mult):
    lh = size * line_height_mult
    return (lh - CONTENT_BOX * size) / 2 + ASCENT * size, lh


def css_linear_gradient(angle_deg, w, h):
    a = math.radians(angle_deg)
    dx, dy = math.sin(a), -math.cos(a)
    length = abs(w * math.sin(a)) + abs(h * math.cos(a))
    return (w / 2 - dx * length / 2, h / 2 - dy * length / 2,
            w / 2 + dx * length / 2, h / 2 + dy * length / 2)


# --------------------------------------------------------------------------
# lockup
# --------------------------------------------------------------------------

def lockup_width(mark):
    _, wm_w = MEDIUM.text(WORDMARK, mark * WM_R, WM_TRACK)
    _, mo_w = REGULAR.text(TAGLINE, mark * MO_R, MO_TRACK)
    return mark + mark * GAP_R + max(wm_w, mo_w)


def lockup(mark, x, cy, uid, mark_paint=None, wm_fill=FG,
           mo_fill=FG_SOFT, mo_opacity=0.92):
    """Emit the lockup with its mark box left edge at x, centred on cy.

    mark_paint=None uses the heat gradient; a colour string goes monochrome.
    Returns (defs, body).
    """
    wm_size, mo_size = mark * WM_R, mark * MO_R
    gap, name_gap = mark * GAP_R, mark * NAME_GAP_R
    names_x = x + mark + gap

    wm_bl, wm_lh = baseline_offset(wm_size, 1.02)
    mo_bl, mo_lh = baseline_offset(mo_size, 1.30)
    names_top = cy - (wm_lh + name_gap + mo_lh) / 2

    wm_d, _ = MEDIUM.text(WORDMARK, wm_size, WM_TRACK,
                          x=names_x, baseline=names_top + wm_bl)
    mo_d, _ = REGULAR.text(TAGLINE, mo_size, MO_TRACK,
                           x=names_x, baseline=names_top + wm_lh + name_gap + mo_bl)

    scale = min(mark / VB_W, mark / VB_H)
    tx = x - VB_X * scale
    ty = (cy - mark / 2) + (mark - VB_H * scale) / 2 - VB_Y * scale

    if mark_paint is None:
        stroke = f'url(#heat-{uid})'
        # userSpaceOnUse resolves in the referencing element's space, i.e.
        # inside the mark's <g> transform -- so these stay in mark coordinates.
        defs = (f'<linearGradient id="heat-{uid}" gradientUnits="userSpaceOnUse"'
                f' x1="{VB_X}" y1="301.2" x2="270.7" y2="{VB_Y}">'
                f'<stop offset="0" stop-color="{G1}"/>'
                f'<stop offset="0.5" stop-color="{G2}"/>'
                f'<stop offset="1" stop-color="{G3}"/></linearGradient>')
    else:
        stroke, defs = mark_paint, ''

    body = (f'<g transform="translate({tx:.3f},{ty:.3f}) scale({scale:.6f})">'
            f'<path d="{MARK_PATH}" fill="none" stroke="{stroke}" '
            f'stroke-width="{MARK_STROKE}" stroke-linecap="round"/></g>'
            f'<g fill="{wm_fill}">{wm_d}</g>'
            f'<g fill="{mo_fill}" opacity="{mo_opacity}">{mo_d}</g>')
    return defs, body


def scene(w, h, mark, uid, x=None, cy=None):
    """A full-bleed card: field gradient, glow, centred lockup."""
    lw = lockup_width(mark)
    x = (w - lw) / 2 if x is None else x
    cy = h / 2 if cy is None else cy

    x1, y1, x2, y2 = css_linear_gradient(FIELD_ANGLE, w, h)
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in FIELD_STOPS)
    ldefs, body = lockup(mark, x, cy, uid)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}" role="img"
     aria-label="Living Intelligence — {TAGLINE}">
  <title>Living Intelligence — {TAGLINE}</title>
  <defs>
    <linearGradient id="field-{uid}" gradientUnits="userSpaceOnUse"
      x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}">{stops}</linearGradient>
    <radialGradient id="glow-{uid}" gradientUnits="userSpaceOnUse"
      cx="{w/2:.1f}" cy="{h*0.239:.1f}" r="{max(w, h)*0.517:.1f}">
      <stop offset="0" stop-color="{G2}" stop-opacity="{GLOW_OPACITY}"/>
      <stop offset="0.72" stop-color="{G2}" stop-opacity="0"/>
    </radialGradient>
    {ldefs}
  </defs>
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#field-{uid})"/>
  <rect width="{w}" height="{h}" fill="url(#glow-{uid})"/>
  {body}
</svg>
'''


def bare(mark, uid, pad=None, **paint):
    """Transparent, tightly cropped lockup."""
    pad = mark * 0.06 if pad is None else pad
    lw = lockup_width(mark)
    w, h = lw + 2 * pad, mark + 2 * pad
    ldefs, body = lockup(mark, pad, h / 2, uid, **paint)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}" height="{h:.1f}"
     viewBox="0 0 {w:.1f} {h:.1f}" role="img"
     aria-label="Living Intelligence — {TAGLINE}">
  <title>Living Intelligence — {TAGLINE}</title>
  <defs>{ldefs}</defs>
  {body}
</svg>
'''


# --------------------------------------------------------------------------

def render_png(svg, path, w, h, ss=2):
    """Render at ss x and downsample -- dithers the dark background ramps,
    which otherwise band visibly in 8-bit."""
    import io
    from PIL import Image
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=w * ss, output_height=h * ss)
    buf.seek(0)
    Image.open(buf).resize((w, h), Image.LANCZOS).save(path)


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    out.mkdir(parents=True, exist_ok=True)

    def write(name, svg, png_w=None, png_h=None):
        (out / f'{name}.svg').write_text(svg)
        if png_w:
            render_png(svg, out / f'{name}.png', png_w, png_h)
        print(f'  {name}')

    print('cards')
    # LinkedIn covers: mark is 62.8% of canvas height, lockup nudged right so
    # the profile avatar (lower left) does not crowd it.
    for w, h in ((1128, 191), (4200, 700)):
        mark = h * 0.628
        x = (w - lockup_width(mark)) / 2 + w * 0.053
        write(f'company-cover-{w}x{h}', scene(w, h, mark, f'c{w}', x=x), w, h)

    write('link-preview-1200x627', scene(1200, 627, 196, 'lp', cy=313), 1200, 627)
    write('post-square-1080', scene(1080, 1080, 184.4, 'sq'), 1080, 1080)

    print('lockups')
    variants = {
        'li-lockup-caps': dict(),
        'li-lockup-caps-white': dict(mark_paint=FG, wm_fill=FG, mo_fill=FG, mo_opacity=1),
        'li-lockup-caps-white-pure': dict(mark_paint='#FFFFFF', wm_fill='#FFFFFF',
                                          mo_fill='#FFFFFF', mo_opacity=1),
        'li-lockup-caps-black': dict(mark_paint=INK, wm_fill=INK, mo_fill=INK, mo_opacity=1),
        'li-lockup-caps-light': dict(wm_fill=INK, mo_fill=INK_SOFT, mo_opacity=1),
    }
    for i, (name, paint) in enumerate(variants.items()):
        write(name, bare(196, f'b{i}', **paint))

    # transparent raster of the default lockup, 1600px wide
    svg = bare(196, 'r')
    lw = lockup_width(196) + 2 * 196 * 0.06
    h = round(1600 * (196 + 2 * 196 * 0.06) / lw)
    render_png(svg, out / 'li-lockup-caps-1600.png', 1600, h)
    print(f'  li-lockup-caps-1600  (1600x{h}, transparent)')


if __name__ == '__main__':
    main()
