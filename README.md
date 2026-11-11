# Crayon Coloring Book

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that turns any serious document (a strategy memo, policy, report, README, design doc, meeting notes, org announcement) into a children's coloring book that looks drawn in crayon. You get a self-contained HTML file and a printable PDF.

Each page has:

- a hand-drawn SVG metaphor with wobbly, waxy outlines and speckled fills that drift outside the lines
- a rainbow crayon title
- a kid-voice caption that still makes the document's real argument
- a "Color me: ..." tip
- a deadpan "Grown-up version" pointer back to the source

The joke is the contrast between a dense, serious document and a kid's plain words. The facts stay accurate.

## How it works

Claude writes the creative parts: the page plan, the captions, and one SVG drawing per page. `scripts/build_book.py` does the rendering: crayon filters, layout, embedded fonts, HTML, PDF, and a contact sheet for checking the result.

```
SKILL.md                  Instructions Claude follows when the skill triggers
scripts/build_book.py     Spec JSON -> HTML + PDF + contact sheet
references/
  spec_format.md          The spec JSON format
  svg_cookbook.md         Drawing conventions and reusable SVG snippets
assets/                   CSS, crayon JS, SVG filters, embedded fonts
examples/                 A complete 14-page example spec (Cloudflare MCP server portals)
```

## Installation

### Claude Code

Clone into your personal skills directory:

```bash
git clone https://github.com/mwdavisii/coloringbook ~/.claude/skills/crayon-coloring-book
```

Or into a project, so everyone working in that repo gets it:

```bash
git clone https://github.com/mwdavisii/coloringbook .claude/skills/crayon-coloring-book
```

### Claude.ai / Claude Desktop

Zip the repository folder and upload it under **Settings → Capabilities → Skills**.

### Requirements for PDF output

```bash
pip install playwright pillow
python3 -m playwright install chromium
```

Without these, the HTML still builds. Use `--no-pdf` and print to PDF from a browser.

## Usage

Ask Claude for a coloring book version of a document:

> Turn this quarterly planning doc into a crayon coloring book.

> Make an "explain it like I'm five" picture book of our incident postmortem for the team offsite.

> Coloring book of this README, outline-only, A4.

Claude reads the document, plans a cover, 8 to 14 content pages, and a back page, draws each page, builds the book, checks the contact sheet, and fixes problems before handing it over.

### Running the build script directly

```bash
python3 scripts/build_book.py examples/mcp-server-portals.spec.json --out-dir ./out --seed 7
```

| Flag | Effect |
|---|---|
| `--out-dir DIR` | Where to write output (default: current directory) |
| `--name NAME` | Output file base name (default: spec file name) |
| `--outline` | Outline-only pages with no fills, for printing and coloring by hand |
| `--paper letter\|a4` | Paper size (default: `letter`) |
| `--seed N` | Fixes the random "kid coloring" so output is reproducible |
| `--no-pdf` | Build only the HTML |

Outputs in `--out-dir`:

- `<name>.html`: self-contained book. It re-colors itself on each refresh.
- `<name>.pdf`: printable book
- `<name>-contact-sheet.png`: thumbnails of every page for a quick visual check

The script also prints lint warnings for mistakes that quietly break the crayon effect, such as a missing `data-c` color, attributes inside a `.r` group, or labels that probably run off the canvas.

## Writing your own spec

See [`references/spec_format.md`](references/spec_format.md) for the JSON format and [`references/svg_cookbook.md`](references/svg_cookbook.md) for the drawing conventions. The short version:

- Closed shapes to color go in `<g class="r" data-c="#hex">`. Open lines go in `<g class="l">`. Thick colored strokes go in `<g class="k" style="--k:#hex">`.
- Don't put `fill`, `stroke`, or `transform` on shapes inside a `.r` group. Wrap them in a parent `<g transform="...">` instead.
- Use viewBox `0 0 600 380`, labels of at least 19px, and features bigger than about 10px.

## Fonts

The bundled fonts in `assets/fonts/`, [Patrick Hand](https://fonts.google.com/specimen/Patrick+Hand) and [Schoolbell](https://fonts.google.com/specimen/Schoolbell), are licensed under the [SIL Open Font License 1.1](https://openfontlicense.org/).

## License

The example in `examples/mcp-server-portals.spec.json` is adapted from Cloudflare's public [MCP server portals documentation](https://developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/mcp-portals/) and [launch blog post](https://blog.cloudflare.com/zero-trust-mcp-server-portals/), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). It is not made or endorsed by Cloudflare.

The skill itself is [MIT](LICENSE), except the bundled fonts, which remain under the SIL Open Font License 1.1.
