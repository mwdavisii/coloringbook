#!/usr/bin/env python3
"""Build a crayon coloring book (HTML + PDF) from a JSON spec.

Usage:
  python build_book.py spec.json --out-dir ./out [--name my-book] [--outline]
                       [--seed 42] [--paper letter|a4] [--no-pdf]

Spec format: see references/spec_format.md (and examples/*.spec.json).

Outputs (in --out-dir):
  <name>.html            self-contained, fonts embedded, re-colors on refresh
  <name>.pdf             one sheet per page (flattened images; ~2 MB for 14 pages)
  <name>-contact-sheet.png   thumbnails of every page, for a quick visual check

PDF rendering needs: pip install playwright pillow && playwright install chromium
"""
import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"

PAPER_PX = {"letter": (816, 1056), "a4": (794, 1123)}
DEFAULT_VIEWBOX = "0 0 600 380"


def esc(s):
    return html.escape(s or "", quote=False)


def font_face_css():
    out = []
    for family, fname in (
        ("Schoolbell", "schoolbell-latin-400-normal.woff2"),
        ("Patrick Hand", "patrick-hand-latin-400-normal.woff2"),
    ):
        data = base64.b64encode((ASSETS / "fonts" / fname).read_bytes()).decode()
        out.append(
            f'@font-face{{font-family:"{family}";'
            f"src:url(data:font/woff2;base64,{data}) format(\"woff2\");font-weight:400}}"
        )
    return "\n".join(out)


# ---------------------------------------------------------------- linting
def lint_page(idx, page):
    """Catch the mistakes that silently break the crayon effect. Returns warnings."""
    warns = []
    svg = page.get("svg", "")
    label = f"page {idx + 1} ({page.get('title', '?')[:30]})"
    if not svg.strip():
        warns.append(f"{label}: no svg")
        return warns

    for m in re.finditer(r'<g\s+class="r"([^>]*)>', svg):
        attrs = m.group(1)
        if "data-c=" not in attrs:
            warns.append(f'{label}: <g class="r"> without data-c (it will not be colored)')
        if "transform=" in attrs:
            warns.append(f'{label}: <g class="r"> has a transform; wrap it in a parent <g transform> instead')
    # Fill/stroke attributes on shapes inside .r groups override the crayon layer
    for m in re.finditer(r'<g\s+class="r"[^>]*>(.*?)</g>', svg, re.S):
        if re.search(r'\s(fill|stroke)="', m.group(1)):
            warns.append(f'{label}: fill/stroke attribute inside a .r group (remove it; color comes from data-c)')
            break

    vb = [float(v) for v in (page.get("viewbox") or DEFAULT_VIEWBOX).split()]
    vw, vh = vb[2], vb[3]
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", svg, re.S):
        attrs, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        x = re.search(r'\sx="([\d.]+)"', attrs)
        y = re.search(r'\sy="([\d.]+)"', attrs)
        if not (x and y):
            continue
        x, y = float(x.group(1)), float(y.group(1))
        cls = re.search(r'class="([^"]*)"', attrs)
        size = 19 if cls and "s" in cls.group(1).split() else 34 if cls and "b" in cls.group(1).split() else 25
        width = 0.40 * size * len(body)  # rough handwriting-font estimate
        anchor = re.search(r'text-anchor="(\w+)"', attrs)
        if anchor and anchor.group(1) == "middle":
            left, right = x - width / 2, x + width / 2
        else:
            left, right = x, x + width
        if left < -4 or right > vw + 4:
            warns.append(f'{label}: text "{body[:28]}" probably runs off the canvas (~{left:.0f}..{right:.0f} of {vw:.0f})')
        if y > vh + 2 or y < 0:
            warns.append(f'{label}: text "{body[:28]}" is outside the canvas vertically (y={y:.0f})')
    return warns


# ---------------------------------------------------------------- html
def section(idx, page, page_no):
    t = page.get("type", "page")
    vb = page.get("viewbox", DEFAULT_VIEWBOX)
    alt = esc(page.get("alt", ""))
    svg = (f'<svg class="art" viewBox="{vb}" role="img" aria-label="{alt}">\n'
           f'{page.get("svg", "")}\n</svg>')
    title = esc(page.get("title", ""))
    parts = ['<section class="paper">']
    if t == "cover":
        parts.append(f'<h1 class="rb">{title}</h1>')
        if page.get("subtitle"):
            parts.append(f'<p class="sub">{esc(page["subtitle"])}</p>')
        parts.append(svg)
        parts.append(f'<p class="say">{esc(page.get("caption"))}</p>')
        parts.append('<div class="foot">'
                     f'<span class="tip">{esc(page.get("tip"))}</span>'
                     f'<span class="gu">{esc(page.get("footer"))}</span></div>')
    elif t == "back":
        parts.append(f'<p class="pg">{esc(page.get("pg", "last page"))}</p>')
        parts.append(f'<h2 class="rb">{title}</h2>')
        parts.append(svg)
        parts.append(page.get("extra_html", ""))  # trusted, authored by Claude
    else:
        parts.append(f'<p class="pg">{esc(page.get("pg", f"page {page_no}"))}</p>')
        parts.append(f'<h2 class="rb">{title}</h2>')
        parts.append(svg)
        parts.append(f'<p class="say">{esc(page.get("caption"))}</p>')
        parts.append('<div class="foot">'
                     f'<span class="tip">{esc(page.get("tip"))}</span>'
                     f'<span class="gu">{esc(page.get("grownup"))}</span></div>')
    parts.append("</section>")
    return "\n".join(parts)


def build_html(spec, outline, seed):
    pages = spec["pages"]
    body, n = [], 0
    for i, p in enumerate(pages):
        if p.get("type", "page") == "page":
            n += 1
        body.append(section(i, p, n))
    intro = esc(spec.get("intro", "Best enjoyed with crayons. Scroll to turn the page. "
                                   "Refresh to re-color it (we went outside the lines on purpose)."))
    seed_js = f"window.CRAYON_SEED={int(seed)};" if seed is not None else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec.get("book_title", "Coloring Book"))}</title>
<style>
{font_face_css()}
{(ASSETS / "style.css").read_text()}
</style>
</head>
<body{' class="outline"' if outline else ''}>
{(ASSETS / "filters.svg").read_text()}
<p class="intro">{intro}</p>
{chr(10).join(body)}
<script>
{seed_js}
{(ASSETS / "crayon.js").read_text()}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- pdf
def render_pdf(html_path, pdf_path, sheet_path, paper, scale=2):
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError:
        sys.exit("PDF needs playwright + pillow:  pip install playwright pillow && playwright install chromium\n"
                 "(The HTML was still written; use --no-pdf to skip this step.)")
    import io

    pw, ph = PAPER_PX[paper]
    css = f":root{{--pw:{pw}px;--ph:{ph}px}}\n" + (ASSETS / "print.css").read_text()
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": pw, "height": ph}, device_scale_factor=scale)
        page.goto(html_path.resolve().as_uri())
        page.add_style_tag(content=css)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1000)
        for el in page.locator("section.paper").all():
            shots.append(Image.open(io.BytesIO(el.screenshot(type="jpeg", quality=85))).convert("RGB"))
        browser.close()
    dpi = 96 * scale
    shots[0].save(pdf_path, save_all=True, append_images=shots[1:], resolution=dpi)

    # contact sheet for a quick visual check
    tw, th = 340, int(340 * ph / pw)
    cols = 5
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), "white")
    for k, im in enumerate(shots):
        sheet.paste(im.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
    sheet.save(sheet_path)
    return len(shots)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--name", help="output file base name (default: spec file name)")
    ap.add_argument("--outline", action="store_true", help="outline-only pages, no fills, for printing and real coloring")
    ap.add_argument("--seed", type=int, help="fix the random 'kid coloring' so output is reproducible")
    ap.add_argument("--paper", choices=sorted(PAPER_PX), default="letter")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    # Let pages point at separate files so SVG/HTML needn't be escaped inside JSON
    for page in spec["pages"]:
        for key, fkey in (("svg", "svg_file"), ("extra_html", "extra_html_file")):
            if fkey in page:
                page[key] = (spec_path.parent / page[fkey]).read_text()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    name = args.name or spec_path.name.replace(".spec.json", "").replace(".json", "")

    warnings = [w for i, p in enumerate(spec["pages"]) for w in lint_page(i, p)]
    for w in warnings:
        print("WARN", w)

    html_path = out / f"{name}.html"
    html_path.write_text(build_html(spec, args.outline, args.seed))
    print("wrote", html_path)

    if not args.no_pdf:
        n = render_pdf(html_path, out / f"{name}.pdf", out / f"{name}-contact-sheet.png", args.paper)
        print(f"wrote {out / (name + '.pdf')} ({n} pages) and {name}-contact-sheet.png")
    if warnings:
        print(f"{len(warnings)} lint warning(s) above: fix them, then rebuild.")


if __name__ == "__main__":
    main()
