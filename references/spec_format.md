# Spec format

One JSON file describes the whole book. `scripts/build_book.py` turns it into HTML and PDF.

```json
{
  "book_title": "The Big Book of Quarterly Planning",
  "intro": "Optional line shown above the first page in the HTML (hidden in the PDF).",
  "pages": [ { ...cover... }, { ...page... }, { ...page... }, { ...back... } ]
}
```

## Page types

### `cover` (first page)
| Field | Notes |
|---|---|
| `type` | `"cover"` |
| `title` | Big rainbow title. Keep under about 40 characters so it fits on two lines |
| `subtitle` | Purple line under the title, e.g. "A coloring book about our roadmap" |
| `svg` | Inner SVG markup (see svg_cookbook.md) |
| `alt` | One-sentence description of the drawing for accessibility |
| `caption` | Navy kid-voice paragraph under the drawing |
| `tip` | Dashed red box, "Color me: ..." |
| `footer` | Small grey line at the bottom right, e.g. "Property of Finance. Ages 18+." |

### `page` (content pages; numbered automatically as "page 1", "page 2", ...)
| Field | Notes |
|---|---|
| `type` | `"page"` (default if omitted) |
| `title` | 2 to 6 words, rainbow crayon |
| `svg`, `alt` | As above |
| `caption` | 2 to 3 sentences |
| `tip` | "Color me: ..." |
| `grownup` | Small grey pointer to the source, e.g. "Grown-up version: Belief 3" |
| `pg` | Optional override for the small page label |
| `viewbox` | Optional, default `"0 0 600 380"`. Change only for unusual drawings |

### `back` (last page)
| Field | Notes |
|---|---|
| `type` | `"back"` |
| `title`, `svg`, `alt` | As above. A crayon key (color swatches with labels) works well |
| `extra_html` | Raw HTML below the drawing. Available classes: `blank` (a fill-in-the-blank line; put `<i></i>` where the line goes), `star` inside `<div class="center">` (a gold-star sticker), `small` (green centered sign-off line) |

Example `extra_html`:
```html
<p class="blank">Pop quiz: who owns the budget? <i></i></p>
<div class="center"><div class="star">gold star<br>(Finance says<br>maybe)</div></div>
<p class="small">THE END. See you next quarter.</p>
```

## Keeping SVG out of JSON strings
Escaping every quote inside a JSON string is error-prone. Instead, save each drawing as its own file and point to it:
```json
{"type": "page", "title": "Keep It Short", "svg_file": "pages/p02.svg", "caption": "..."}
```
`svg_file` (and `extra_html_file` for the back page) are resolved relative to the spec file, and the file holds just the inner SVG markup (no `<svg>` wrapper). This is the recommended way to author new books; the example spec uses inline strings only because it was extracted from a finished book.

## Text rules
- `title`, `subtitle`, `caption`, `tip`, `grownup`, `footer`, `alt` are plain text; the builder HTML-escapes them. Don't put markup in them.
- `svg` and `extra_html` are inserted as-is. Quote attributes properly and close every tag.
- Avoid emoji: the handwriting fonts don't have them and they render as boxes or in a clashing style. Use plain punctuation such as `:)`.
- Curly quotes and dashes are fine; the fonts cover Latin text only (no CJK, Arabic, or Cyrillic).

## Minimal example
```json
{
  "book_title": "The Big Book of Standup Meetings",
  "pages": [
    {"type": "cover", "title": "The Big Book of Standup Meetings", "subtitle": "Stand up. Sit down. Repeat.",
     "alt": "A smiling sun over a tiny meeting room",
     "svg": "<g class=\"r\" data-c=\"#fdd835\"><circle cx=\"300\" cy=\"150\" r=\"70\"/></g>",
     "caption": "Every day we stand in a circle and say what we did. Today we color it.",
     "tip": "Color me: the sun, obviously", "footer": "Property of Engineering"},
    {"type": "page", "title": "Keep It Short", "alt": "A big clock",
     "svg": "<g class=\"r\" data-c=\"#e53935\"><circle cx=\"300\" cy=\"190\" r=\"120\"/></g><g class=\"l\"><path d=\"M300 190 V110 M300 190 L360 220\"/></g>",
     "caption": "Fifteen minutes is the whole meeting. Not fifteen minutes and then a discussion.",
     "tip": "Color me: the clock the color of impatience", "grownup": "Grown-up version: Section 2"}
  ]
}
```
