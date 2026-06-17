#!/usr/bin/env python3
"""Screenshot a built Jekyll page in light + dark, and crop named elements.

Why this exists, in one breath: the MCP Chrome tab captures blank for any
backgrounded tab (document.visibilityState == "hidden"), so we drive a
headless Chrome from the CLI instead. A blog page's absolute /assets/...
URLs only resolve when the page is served from the site root, so we spin up
an ephemeral http.server over the built directory. Theme is forced by
injecting a one-line <script> that sets data-theme before paint. Elements
are located by injecting a probe that writes getBoundingClientRect into
document.title, read back via --dump-dom, then cropped from the 2x
screenshot with sips. Every one of those is a step that's easy to get
subtly wrong by hand; this script encodes the version that works.

Usage:
  python shoot.py --root /tmp/site-build --path blog/2026/my-post/ \\
      --selector ".hier" --selector ".bsw" --out /tmp/shots

  # whole-page only, both themes:
  python shoot.py --root /tmp/site-build --path blog/2026/my-post/ --out /tmp/shots

Outputs into --out:
  <theme>.png                full page (tall)
  <theme>__<selector>.png    full-resolution crop of the element
  <theme>__<selector>.view.png   downscaled (<=1600px) — Read THIS one

Then Read the .view.png files. Read a full-resolution crop only when you
need to inspect fine detail (a 1px border, anti-aliasing); the big ones can
be rejected for size, which is why the .view.png exists.
"""
import argparse
import http.server
import json
import os
import re
import socket
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCALE = 2  # --force-device-scale-factor; screenshot pixels = CSS pixels * SCALE
PAD = 18   # CSS px of breathing room around a cropped element
VIEW_MAX = 1600  # downscale crops to this longest edge before you Read them


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # the per-asset request log is pure noise here
        pass


def serve(root: str):
    port = free_port()

    def handler(*a, **k):
        return QuietHandler(*a, directory=root, **k)

    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def chrome(args: list, capture=False):
    # The budget must outlast the probe's settle (below): screenshot and
    # geometry-dump are separate Chrome runs, so they must agree on the final
    # layout, which means both must wait out font-swap reflow.
    base = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--virtual-time-budget=12000"]
    return subprocess.run(base + args, text=True,
                          stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)


def sips_dims(png: str):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", png],
                         capture_output=True, text=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h


def variant_html(src: str, theme: str, selectors: list) -> str:
    """Inject a theme-setter (before paint) and a geometry probe (after load)."""
    theme_js = (f'<script>document.documentElement.setAttribute'
                f'("data-theme","{theme}")</script>')
    html = src.replace("</head>", theme_js + "</head>", 1)
    if selectors:
        sel_json = json.dumps(selectors)
        # Measure on a plain timer after load. Under --virtual-time-budget
        # Chrome finishes loading resources (fonts included) before advancing
        # the virtual clock, so the layout is already settled when this fires;
        # measured positions match the screenshot. Two traps avoided here:
        # requestAnimationFrame callbacks do NOT fire under the virtual clock
        # (so don't wrap the measurement in rAF — the title never gets set),
        # and document.fonts.ready never resolves under it either.
        probe = (
            "<script>window.addEventListener('load',function(){setTimeout(function(){"
            "var sels=" + sel_json + ";var out={};sels.forEach(function(s){"
            "var e=document.querySelector(s);if(e){var r=e.getBoundingClientRect();"
            "out[s]={t:Math.round(r.top+scrollY),l:Math.round(r.left+scrollX),"
            "w:Math.round(r.width),h:Math.round(r.height)};}});"
            "document.title=JSON.stringify(out);},800);});</script>"
        )
        html = html.replace("</body>", probe + "</body>", 1)
    return html


def crop(png: str, rect: dict, out: str):
    """Crop the element (CSS rect) out of the 2x screenshot, with padding."""
    img_w, img_h = sips_dims(png)
    top = max(0, int((rect["t"] - PAD) * SCALE))
    left = max(0, int((rect["l"] - PAD) * SCALE))
    h = min(img_h - top, int((rect["h"] + 2 * PAD) * SCALE))
    w = min(img_w - left, int((rect["w"] + 2 * PAD) * SCALE))
    subprocess.run(["sips", "-c", str(h), str(w), "--cropOffset", str(top), str(left),
                    png, "--out", out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    view = out.rsplit(".", 1)[0] + ".view.png"
    subprocess.run(["sips", "-Z", str(VIEW_MAX), out, "--out", view],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return view


def safe(sel: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", sel).strip("_") or "sel"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="built site root (jekyll -d target)")
    ap.add_argument("--path", required=True, help="page path under root, e.g. blog/2026/x/")
    ap.add_argument("--selector", action="append", default=[],
                    help="CSS selector to locate + crop (repeatable)")
    ap.add_argument("--themes", default="light,dark")
    ap.add_argument("--out", default="/tmp/shots")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=6400, help="tall, to capture long pages")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    page_dir = Path(root) / args.path
    index = page_dir / "index.html"
    if not index.exists():
        sys.exit(f"no index.html at {index} — did you build the site to --root?")
    Path(args.out).mkdir(parents=True, exist_ok=True)
    selectors = args.selector
    themes = [t.strip() for t in args.themes.split(",") if t.strip()]

    if not Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")

    httpd, port = serve(root)
    written = []
    try:
        src = index.read_text()
        for theme in themes:
            vfile = page_dir / f"_shoot_{theme}.html"
            vfile.write_text(variant_html(src, theme, selectors))
            written.append(vfile)
            url = f"http://127.0.0.1:{port}/{args.path.rstrip('/')}/_shoot_{theme}.html"

            full = f"{args.out}/{theme}.png"
            chrome([f"--window-size={args.width},{args.height}",
                    f"--force-device-scale-factor={SCALE}",
                    f"--screenshot={full}", url])
            print(f"[{theme}] full page -> {full}")

            if selectors:
                # Measure geometry at the SAME window width as the screenshot —
                # layout (and therefore element positions) depends on viewport
                # width, and Chrome's default headless width is 800, not ours.
                dom = chrome([f"--window-size={args.width},{args.height}",
                              "--dump-dom", url], capture=True).stdout
                m = re.search(r"<title>(\{.*?\})</title>", dom)
                rects = json.loads(m.group(1)) if m else {}
                if os.environ.get("SHOOT_DEBUG"):
                    print(f"[{theme}] rects: {rects}", file=sys.stderr)
                for sel in selectors:
                    r = rects.get(sel)
                    if not r:
                        print(f"[{theme}] selector not found: {sel}")
                        continue
                    out = f"{args.out}/{theme}__{safe(sel)}.png"
                    view = crop(full, r, out)
                    print(f"[{theme}] {sel} -> {view}  (Read this one)")
    finally:
        httpd.shutdown()
        for f in written:
            f.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
