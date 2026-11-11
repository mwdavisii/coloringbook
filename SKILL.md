---
name: crayon-coloring-book
description: Turn any document (strategy memo, policy, report, README, design doc, meeting notes, org announcement) into a hilarious crayon-drawn children's coloring book, delivered as a self-contained HTML file plus a printable PDF. Each page gets a hand-drawn SVG metaphor, rainbow crayon title, kid-voice caption, a "Color me" tip, and a deadpan "grown-up version" note. Use this skill whenever the user asks for a coloring book, a crayon or kid-drawing version of something, an "explain it like I'm five" illustrated booklet, a joke gift or offsite handout made from a document, or wants a serious document turned into a funny picture book, even if they never say "skill" or "crayon". Also supports outline-only pages for printing and real coloring, and A4 paper.
---

# Crayon Coloring Book

Turns a source document into a picture book that looks like a child drew and colored it with crayons: wobbly waxy outlines, speckled fills that drift outside the lines, rainbow letters, handwriting fonts. The comedy comes from contrast: a dense, serious document told in kid voice, with every real claim still intact.

Claude writes the creative parts (page plan, captions, one SVG drawing per page). `scripts/build_book.py` does the rendering (crayon effects, layout, HTML, PDF).

## Workflow

### 1. Check the toolchain
```bash
python3 -c "import playwright, PIL; print('ok')" && python3 -m playwright install chromium
```
If `playwright` or `pillow` is missing: `pip install playwright pillow` (add `--break-system-packages` in managed Pythons), then `playwright install chromium`. Without them the HTML still builds (`--no-pdf`).

### 2. Read the source and choose the pages
Read the whole document first. Then plan **a cover, 8 to 14 content pages, and a back page** (a crayon key or sign-off page is a good closer). One idea per page. For long documents, pick the ideas a reader would have to remember and fold or drop the rest; for short ones, 5 to 8 pages is fine.

Ask the user a question only if it changes the outcome, at most one or two: who will see it (an internal joke needs a gentler touch than a close-friends gift), and whether they want a fixed page count. Otherwise proceed with sensible defaults and say what you assumed.

If the document is internal or confidential, work only from what the user gave you. Do not web-search its names or terms.

### 3. Plan each page before drawing
For every page decide:

| Field | What good looks like |
|---|---|
| **title** | 2 to 6 words, kid-sounding, funny, still recognizable as the idea ("Standing Still Is Scarier") |
| **metaphor** | One concrete, drawable image with 3 to 8 shapes. See the metaphor menu in `references/svg_cookbook.md` |
| **labels** | Literal words inside the drawing (e.g. "moving", "standing still") so the picture carries the point even without the caption |
| **caption** | 2 to 3 sentences, plain words, keeps the document's actual argument. Names and numbers from the source stay accurate |
| **tip** | "Color me: ..." with a small joke (a color, a mood, a rule) |
| **grownup** | A deadpan pointer to the source, like "Grown-up version: Belief 3" or "Section 2.1" |

### 4. Draw the SVGs
**Read `references/svg_cookbook.md` before drawing.** It has the conventions that make the crayon effect work and ready-to-adapt snippets (stick figures, speech bubbles, seesaw, silos, door, bus, robot, piggy bank, arrows, and more). The three rules that matter most:

- Closed shapes you want colored go in `<g class="r" data-c="#hex">...</g>`. Open lines and outline-only things go in `<g class="l">...</g>`. Thick colored strokes (X marks, checks) go in `<g class="k" style="--k:#hex">`.
- Never put `fill`, `stroke`, or `transform` attributes on shapes inside a `.r` group. Wrap in a parent `<g transform="...">` instead. (The build script clones each `.r` group into an offset colored layer and an outline layer, and attributes would break that.)
- Use viewBox `0 0 600 380`, keep labels at least 19px, and keep features bigger than about 10px: the wobble filter erases tiny details.

### 5. Write the spec and build
Write a spec JSON (format in `references/spec_format.md`; a complete 14-page example is `examples/mcp-server-portals.spec.json`). Save each drawing as its own `pages/pNN.svg` file and reference it with `svg_file`, so you never have to escape quotes inside JSON. Then:
```bash
python3 scripts/build_book.py my-book.spec.json --out-dir ./out --seed 7
```
Flags: `--outline` (no fills; outlined letters; a true coloring-page version), `--paper a4` (default letter), `--seed N` (reproducible coloring), `--name`, `--no-pdf`.

The script prints lint warnings for the mistakes that silently break the effect (missing `data-c`, attributes inside `.r`, labels that probably run off the canvas). Fix every warning and rebuild.

### 6. Look at it, fix it, deliver
Open the `*-contact-sheet.png` with the image viewer and check each page: does the drawing read at thumbnail size, are labels clipped or overlapping, is anything unreadable? Fix the SVG and rebuild; expect one or two rounds. For a closer look at a page, rasterize the PDF page or screenshot the HTML.

Deliver the PDF (and the HTML, which re-colors itself on each refresh). Offer the outline-only version if the user hasn't asked. Mention the seed if they might want to reproduce it.

## Voice and humor
- Affectionate toward ideas, never toward people. Do not mock named individuals or teams; if the document names them, keep the jokes about the situation (a backlog, a gate, a pile of papers), not the person.
- Deadpan beats wacky. The funniest pages state a real, accurate claim in a kid's plain words, next to a drawing with a straight face ("The grown-ups call this a backlog. We call it Tuesday.").
- Repeating gags make a book feel authored: the gold star, "(we will not)", an unlimited crayon budget, the one sad figure who shows up on several pages.
- Keep the real point. A reader who only reads the captions should still be able to repeat the document's argument.

## Troubleshooting
- **A shape has no color:** its group is missing `data-c`, or a `fill`/`stroke` attribute inside it overrides the crayon layer.
- **A drawing looks mushy:** shapes are too small or too close; scale the drawing up or cut details.
- **Text clipped at the edge:** shorten the label, drop to `class="s"`, or move it. The lint warning names the label.
- **PDF step fails:** install playwright and chromium (step 1), or build with `--no-pdf` and print the HTML to PDF from a browser.
- **Fonts look like a default serif:** the fonts are embedded in the HTML; make sure `assets/fonts/` is intact.
