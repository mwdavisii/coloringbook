# SVG cookbook

Everything a page's drawing needs. All drawings share one canvas: `viewBox="0 0 600 380"` (the builder adds the `<svg>` wrapper; you write only the inside).

## Contents
1. The three group types
2. Text
3. Layout and legibility rules
4. Crayon palette
5. Metaphor menu (abstract idea to drawable image)
6. Snippets
7. Pre-flight checklist

## 1. The three group types

At page load, a script duplicates every `.r` group into a **colored layer** (waxy, randomly offset and tilted a few pixels, so it goes outside the lines like a kid) and leaves the original as the **outline** (wobbly dark crayon line).

| Group | Use for | Example |
|---|---|---|
| `<g class="r" data-c="#e53935">` | Closed shapes to color in: circles, rects, closed paths, ellipses | a ball, a door, a robot body |
| `<g class="l">` | Lines only, no fill: stick-figure limbs, arrows, faces, details, ground lines | eyes, smile, arrow |
| `<g class="k" style="--k:#d32f2f">` | Thick colored strokes: big red X, green check mark | "NO" cross, "YES" tick |

Hard rules (the build lint checks the first three):
1. Every `.r` needs `data-c`.
2. No `fill=` or `stroke=` attributes on shapes inside `.r`/`.l`/`.k` groups; CSS owns them.
3. No `transform=` on the `.r` group itself. To rotate or move a colored shape, wrap it: `<g transform="rotate(-4 140 290)"><g class="r" data-c="#c8e6c9"><rect .../></g></g>`. A `transform` on the shape inside is fine too (used for butterfly wings).
4. Draw **colored fills first, details after**: later elements sit on top. Put dark backgrounds (shadows, night) first and light details (eyes, labels) after.
5. For eyes on a dark area, make them a light `.r` circle (e.g. `#fff59d`) plus a small black `.r` pupil, since the dark outline vanishes on dark fill.
6. Open paths (a line, a smile) inside `.r` would get filled into a wedge. Put them in `.l`.

## 2. Text

```svg
<text x="300" y="60" text-anchor="middle">normal label (25px)</text>
<text class="s" x="300" y="90" text-anchor="middle">small label (19px)</text>
<text class="b" x="300" y="130" text-anchor="middle">BIG WORD (34px)</text>
```
- Text is dark handwriting by default. Never use `fill`/`font-size` attributes.
- Handwriting runs about 0.4 x font-size wide per character. A 20-character `class="s"` label is about 150 px wide.
- Keep to 6 labels or fewer per drawing. Labels on or next to the thing they name.
- Text inside a colored shape: place it after the shape. Light fills only (pastels), so the dark text stays readable.

## 3. Layout and legibility rules
- One hero image that fills most of the canvas; supporting props at the edges. Whitespace is fine.
- Stroke is 3.6 px with a wobble of about 5 px. Anything under about 10 px (tiny eyes, fine hatching) turns into noise. Eyes as r = 4 to 8 circles work; pupils at r = 2 to 4 are OK.
- Stay inside x 10..590, y 10..370. The text at y > 370 gets clipped.
- Leave 20 px of air between neighbors; the wobble and the offset color layer both bleed a few pixels.
- Fills can be strong colors for big things (#e53935 ball) and pastels for things holding text (#e1f5fe bubble).

## 4. Crayon palette
| Name | Hex | | Name | Hex |
|---|---|---|---|---|
| red | `#e53935` | | pink | `#f48fb1` / `#f06292` |
| orange | `#fb8c00` / `#ffa726` | | brown | `#8d6e63` |
| yellow | `#fdd835` / `#ffeb3b` | | gray | `#9e9e9e` / `#cfd8dc` |
| green | `#43a047` / `#66bb6a` | | pale yellow (eyes, signs) | `#fff59d` |
| light green | `#aed581` / `#c8e6c9` | | pale blue (bubbles) | `#e1f5fe` |
| blue | `#1e88e5` / `#42a5f5` | | sky | `#90caf9` / `#81d4fa` |
| purple | `#8e24aa` / `#ab47bc` | | dark purple (shadows) | `#4527a0` |

## 5. Metaphor menu
Abstract business ideas are hard to draw directly; pick a physical stand-in.

| Idea | Image |
|---|---|
| a decision / approval | giant rubber stamp, YES and NO papers |
| a gate / review / security | door, turnstile, padlock, bouncer |
| risk vs. reward / trade-off | seesaw with different-size balls |
| doing nothing is costly | big scary ball, melting ice cream, sinking boat |
| shadow IT / hidden work | eyes under a bed, mushrooms, iceberg |
| bottleneck / manual process | one tiny door with a long line, sweaty person with a tray |
| backlog | tall pile of papers, laundry mountain |
| ownership / boundaries | silos, fences, flags, keys |
| cost / budget | piggy bank, coins, price tag on a knob |
| growth / upskilling / change | caterpillar, chrysalis, butterfly, seedling |
| speed vs. slow | rocket vs. snail (with briefcase) |
| integration / glue work | puzzle pieces, pipes, bridges between islands |
| pipeline / workflow | boxes with arrows, conveyor belt |
| automation / AI | friendly robot (maybe taped together if homemade) |
| shared platform | bus full of passengers, a big bowl everyone eats from |
| duplication / waste | two identical things, one crossed out, coins flying away |
| customer needs | speech bubbles: what they said vs. what they need |
| accountability | one stick figure holding a clipboard or star badge |
| complexity | spaghetti, tangled wires |
| a deadline | calendar, clock, bomb with a very friendly fuse |

## 6. Snippets
Adapt freely; coordinates assume the 600 x 380 canvas.

**Stick figure** (face, arms, legs; swap arm paths for poses). Put the head and body in `.l`:
```svg
<g class="l">
  <circle cx="110" cy="215" r="26"/>
  <path d="M110 241 V305 M110 258 L75 225 M110 258 L145 225 M110 305 L85 350 M110 305 L135 350"/>
  <circle cx="102" cy="211" r="2"/><circle cx="118" cy="211" r="2"/>
  <path d="M100 229 Q110 238 120 229"/>   <!-- smile; flip the Q for a frown -->
</g>
```
Moods: angry brows `M97 207 L107 212 M123 207 L113 212`; glasses = two `r=8` circles plus `M488 213 H492`; sweat = `.r` ellipses `rx=5 ry=8` in `#4fc3f7`.

**Speech bubble with tail** (colored pastel; text goes after):
```svg
<g class="r" data-c="#e1f5fe"><ellipse cx="150" cy="72" rx="125" ry="48"/><path d="M105 112 L108 172 L150 118 Z"/></g>
<text x="150" y="68" text-anchor="middle">first line</text>
<text x="150" y="96" text-anchor="middle">second line</text>
```
Two lines of 12 to 14 characters fit a bubble of rx = 120.

**Arrow** (right-pointing, in `.l`): `M132 135 L158 135 M158 135 L150 128 M158 135 L150 142`. Down arrow: `M360 82 V98 M360 98 L353 90 M360 98 L367 90`.

**Cloud** (three circles; text after): `<g class="r" data-c="#e1bee7"><circle cx="330" cy="56" r="20"/><circle cx="362" cy="46" r="24"/><circle cx="394" cy="58" r="20"/></g>`

**Sun with rays:** `<g class="r" data-c="#fdd835"><circle cx="520" cy="80" r="40"/></g><g class="l"><path d="M520 22 V6 M520 138 V154 M462 80 H446 M578 80 H594 M478 38 L467 27 M562 122 L573 133 M562 38 L573 27 M478 122 L467 133"/></g>`

**Seesaw** (heavy side down; beam is a thin polygon, fulcrum a triangle):
```svg
<g class="r" data-c="#9e9e9e"><path d="M300 262 L252 345 L348 345 Z"/></g>
<g class="r" data-c="#fb8c00"><path d="M70 214 L530 294 L530 310 L70 230 Z"/></g>
<g class="r" data-c="#66bb6a"><circle cx="110" cy="199" r="22"/></g>
<g class="r" data-c="#e53935"><circle cx="470" cy="218" r="70"/></g>
<g class="l"><path d="M30 346 L570 346"/></g>
```
The ball sits on the beam: center y = beam y at that x minus radius.

**Silo with padlock** (repeat at x0 = 30, 140, 250, ...):
```svg
<g class="r" data-c="#ef5350"><path d="M30 130 L30 250 A40 12 0 0 0 110 250 L110 130 Z"/><ellipse cx="70" cy="130" rx="40" ry="12"/></g>
<g class="r" data-c="#fdd835"><rect x="58" y="176" width="24" height="20"/></g>
<g class="l"><path d="M62 176 V168 A8 8 0 0 1 78 168 V176"/></g>
```

**Arched door with knob and sign:**
```svg
<g class="r" data-c="#8d6e63"><path d="M215 335 V150 A85 85 0 0 1 385 150 V335 Z"/></g>
<g class="r" data-c="#fdd835"><circle cx="360" cy="245" r="12"/></g>
<g class="l"><rect x="240" y="170" width="120" height="60"/><rect x="240" y="255" width="120" height="65"/></g>
<g class="r" data-c="#fff59d"><rect x="240" y="22" width="120" height="40" rx="6"/></g>
<text class="s" x="300" y="49" text-anchor="middle">FRONT DOOR</text>
```

**Bus (shared platform):** body `rect 200,250,200x72 rx16 #ffeb3b`; windows `rect` pale blue `#81d4fa`; wheels `.r` black circles r=17 at cy=330 (overlapping the bottom edge); label `class="s"` at y=307 above the wheels.

**Robot (friendly):** head `rect rx14`, body `rect rx16`, arms `rect rx14` in a lighter blue, antenna `M165 50 V27` in `.l` with a red `.r` circle on top, eyes pale-yellow `.r` circles, mouth `M140 112 H190`. Homemade version: gray head and body, a tape strip `<g transform="rotate(-10 470 246)"><g class="r" data-c="#ffe082"><rect x="428" y="240" width="84" height="12"/></g></g>`, a loose wire `M470 185 q-10 -26 6 -36`.

**Big crossed-out X over something:** `<g class="k" style="--k:#d32f2f"><path d="M410 160 L530 312 M530 160 L410 312"/></g>`. Check mark: `<g class="k" style="--k:#2e7d32"><path d="M105 318 L130 336 L185 292"/></g>`.

**Calendar:** white `.r` rect 110x90 rx8, red header rect on top, ring lines in `.l`, `class="s"` text such as "3 YEARS".

**Clock:** yellow `.r` circle r=48, hands in `.l`: `M510 100 V68 M510 100 L534 112`.

**Coin:** gold `.r` circle r=18 to 30 with a `$` text on top.

**Pipeline of boxes:** four pastel `.r` rects 110x70 rx10 at x = 20, 160, 300, 440; label text at y = 144 center; arrows between at y = 135.

**Piggy bank:** body ellipse rx=125 ry=88 pink; snout ellipse rx=30 ry=24 darker pink; ear triangle; four rounded-rect legs; black pupil; coin slot line `M228 126 L302 128`; coin above it.

**Caterpillar:** five green circles (alternating two greens) r=22, head r=27 with antennae `.l`. Chrysalis: tall ellipse hanging from a line. Butterfly: four wing ellipses with `transform="rotate(+-25 cx cy)"`, a thin dark body ellipse.

**Rocket:** body ellipse rx=70 ry=28, nose `M482 106 Q546 130 482 154 Z` red, two fin triangles, round blue window, flame polygon, speed lines in `.l`.

**Snail with briefcase:** purple shell circle with a spiral path in `.l`, green body ellipse, head circle, two stalk lines, brown `.r` rect for the briefcase with a handle path.

**Grass/ground:** a green `.r` rect across the bottom plus a wavy `.l` line: `M0 338 q15 -16 30 0 t30 0 t30 0 ...` (repeat `t30 0` to reach 600).

**Server tower with crown:** indigo rect rx14, pale-indigo drawer rects, yellow crown path `M228 95 L238 56 L266 80 L300 38 L334 80 L362 56 L372 95 Z`, a face on the top drawer.

## 7. Pre-flight checklist
- [ ] Every colored shape is in a `.r` with `data-c`; every line is in `.l`.
- [ ] No `fill=`, `stroke=`, or `transform=` on `.r` groups.
- [ ] Labels: at most 6, each at least 19 px, inside x 10..590 and y < 370.
- [ ] Dark fills drawn before the light things on top of them.
- [ ] The picture makes the page's point with the labels alone.
- [ ] Built, linted clean, and checked on the contact sheet.
