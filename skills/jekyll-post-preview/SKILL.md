---
name: jekyll-post-preview
description: >-
  Visually verify a Jekyll / al-folio blog post — embedded HTML/CSS/JS widgets,
  figures, tables, math — by building the site and screenshotting it in light
  AND dark with headless Chrome, then reading the images back to check them.
  Use this whenever you edit a post in the WindChimeRan.github.io blog and need
  to SEE the rendered result before publishing: "screenshot the post", "does
  the widget render", "check the figure in dark mode", "is the table aligned",
  "did the diagram come out right", "preview my draft", "the spacing looks off".
  Prefer this over the MCP Chrome tab for anything Jekyll — the MCP tab captures
  blank for backgrounded pages, so it cannot verify rendered blog content.
  Use it after any change to a widget's CSS/HTML, and as the last step before
  publishing a post that contains a custom figure or interactive element.
---

# Jekyll post preview

The point of this skill is to close the loop on visual work: you change a
widget or figure in a blog post, and you actually *see* the result instead of
guessing from the source. The blog's posts embed hand-written HTML/CSS/JS
(slider widgets, SVG-ish CSS diagrams, booktabs tables), and those break in
ways the markdown source never reveals — a class name collides with Bootstrap,
a box-shadow clips, a color is invisible in dark mode. The only way to know is
to render it and look.

## The loop

1. **Build** the site to a temp dir.
2. **Shoot** the page in light and dark with `scripts/shoot.py`, optionally
   cropping named elements.
3. **Read** the resulting `.view.png` files and judge them.
4. **Fix** the post, rebuild, reshoot. Repeat until it looks right.

Then publish (commit + push) only once you've seen it.

## Build

The repo is at `/Users/ran/WindChimeRan.github.io`. Build to a throwaway dir so
you never disturb the user's own `_site/` or their running server:

```bash
cd /Users/ran/WindChimeRan.github.io
bundle exec jekyll build -d /tmp/site-preview            # published posts
bundle exec jekyll build --drafts -d /tmp/site-preview   # include _drafts
```

The build prints a Python/`jinja2` `Markup` traceback from a notebook page on
this site. That is pre-existing noise, not your failure. To detect a *real*
error, look for Liquid/conversion problems specifically:

```bash
bundle exec jekyll build -d /tmp/site-preview 2>&1 | grep -i "Liquid Exception\|Conversion error"
```

Empty output means the build is fine. A draft dated in the future is silently
excluded by `--drafts`; if a post seems missing, check its `date:`.

## Shoot

`scripts/shoot.py` does the fiddly part: it serves the built dir on an
ephemeral port (so absolute `/assets/...` URLs resolve), forces each theme,
screenshots with headless Chrome at 2× scale, and — for any CSS selectors you
name — locates the element and crops it out, downscaled so the image is safe to
Read.

```bash
python3 ~/.claude/skills/jekyll-post-preview/scripts/shoot.py \
  --root /tmp/site-preview \
  --path blog/2026/my-post/ \
  --selector ".hier" --selector ".bsw" \
  --out /tmp/shots
```

Outputs in `--out`:
- `light.png`, `dark.png` — full page (tall).
- `light__<selector>.view.png`, `dark__<selector>.view.png` — cropped element,
  downscaled to ≤1600px. **Read these.**
- `light__<selector>.png` — full-resolution crop. Read this only when you need
  to inspect fine detail (a 1px border, anti-aliasing, sub-pixel alignment);
  the big full-page PNGs can be rejected for size, which is why the `.view`
  crops exist.

Omit `--selector` to get only the full-page shots. `--themes light` if you only
care about one. Set `SHOOT_DEBUG=1` to print the measured element rectangles.

## Read

Read the `.view.png` crops and judge them against intent: does the widget
render at all, is it legible in both themes, are colors visible against the
dark background, is spacing/alignment right, does interactive state look
sane. Then fix the post and reshoot. A typical iteration is one Edit + one
shoot + one Read.

## Why headless Chrome, not the MCP browser tab

The MCP `claude-in-chrome` `computer` screenshot returns a blank image for any
tab that is backgrounded (`document.visibilityState === "hidden"`), which is
the normal state during automation. It cannot verify rendered blog content. The
script drives Chrome from the CLI instead, where the page always paints.

## Gotchas worth knowing

- **The user's `localhost:8080` serves `_site/` statically and does not rebuild
  on edit.** If you change a post and refresh 8080, you see the old version.
  Always run a build (the script reads from your fresh `--root`, so it is never
  stale). The 8080 server is for the user to eyeball; the script is for you.

- **Embedded-widget class names collide with Bootstrap/MDB.** Every post page
  loads full `bootstrap.min.css` and `mdb.min.css`. A widget element classed
  `row`, `card`, `container`, `btn`, `table`, `badge`, `progress`, `alert`,
  etc. inherits their rules and renders wrong (a bare `row` gets
  `margin-left:-15px` and shifts left). Prefix widget classes (`kvw-row`,
  `hbadge`, …). To check a suspect name, grep the compiled CSS:
  ```bash
  grep -o '\.row[ ,{:]' /tmp/site-preview/assets/css/bootstrap.min.css | head
  ```

- **Geometry is measured at the screenshot's window width.** Element position
  depends on viewport width, so the script measures and screenshots at the same
  `--width` (default 1280). If you change `--width`, both move together; you
  don't need to think about it. This is only a concern if you hand-roll the
  recipe below.

- **Theme is forced by injecting `data-theme`.** The site reads light/dark from
  `data-theme` on `<html>`. The script writes a one-line `<script>` setter into
  a temporary variant file. Don't rely on the OS appearance; set it explicitly.

## Hand-rolling it (when the script doesn't fit)

If you need something the script doesn't do (a hover state, a specific
viewport, a mid-page scroll), the raw recipe is:

```bash
# 1. serve the built dir so /assets resolves
cd /tmp/site-preview && python3 -m http.server 4324 &

# 2. write a theme variant of the page (inject before </head>)
#    <script>document.documentElement.setAttribute("data-theme","dark")</script>

# 3. screenshot with headless Chrome at 2x (NOT the MCP tab)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --window-size=1280,6400 \
  --force-device-scale-factor=2 --virtual-time-budget=12000 \
  --screenshot=/tmp/shot.png "http://127.0.0.1:4324/.../_dark.html"

# 4. locate an element: inject a probe that writes its rect into document.title,
#    read it back with --dump-dom (same --window-size as the screenshot!)
#    <script>addEventListener('load',()=>setTimeout(()=>{var e=document.querySelector('.x');
#      document.title=JSON.stringify(e.getBoundingClientRect());},800))</script>
#    Do NOT wrap the measurement in requestAnimationFrame or document.fonts.ready
#    — neither fires under Chrome's --virtual-time clock, so the title never sets.

# 5. crop from the 2x image (coords are CSS px * 2), then downscale to Read
sips -c <h*2> <w*2> --cropOffset <top*2> <left*2> /tmp/shot.png --out /tmp/crop.png
sips -Z 1600 /tmp/crop.png --out /tmp/crop.view.png
```

The script encodes the version of this that works; reach for the raw form only
when you've outgrown it.
