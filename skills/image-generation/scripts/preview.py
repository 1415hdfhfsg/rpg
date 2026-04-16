#!/usr/bin/env python3
"""
Generate a local HTML preview page with download button.
Opens in the user's browser — fetches the image client-side and offers
PNG download, bypassing any server-side network restrictions.

Usage:
  python3 preview.py --prompt "a dragon" --output preview.html
  python3 preview.py --prompt "bread on a table" -q ultra -d maximum \
    --composition close-up --lighting golden --style photorealistic \
    --output preview.html --open
"""

import argparse
import html
import os
import sys
import webbrowser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import (
    generate_image_url, auto_select_model, AVAILABLE_MODELS, DEFAULT_MODEL,
)
from prompt_builder import (
    build_prompt, get_dimensions, get_quality_tier, detect_subject,
    COMPOSITION_PRESETS, LIGHTING_PRESETS,
)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Image Preview — {title}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,'Pretendard',sans-serif; background:#111; color:#eee; min-height:100vh; display:flex; flex-direction:column; align-items:center; padding:2rem; }}
  h1 {{ font-size:1.2rem; color:#ffe792; margin-bottom:1.5rem; }}
  .card {{ background:#1a1a1a; border:1px solid #333; border-radius:12px; padding:1.5rem; max-width:900px; width:100%; margin-bottom:1.5rem; }}
  .card h2 {{ font-size:0.85rem; color:#888; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem; }}
  .meta {{ display:grid; grid-template-columns:auto 1fr; gap:0.4rem 1rem; font-size:0.85rem; }}
  .meta dt {{ color:#888; }} .meta dd {{ color:#ccc; }}
  .prompt-box {{ background:#0e0e0e; border:1px solid #2a2a2a; border-radius:8px; padding:1rem; margin-top:0.75rem; font-size:0.8rem; line-height:1.6; color:#aaa; white-space:pre-wrap; word-break:break-all; max-height:200px; overflow-y:auto; }}
  .prompt-box.ko {{ color:#ddd; }}
  #img-container {{ text-align:center; margin:1rem 0; }}
  #img-container img {{ max-width:100%; border-radius:8px; border:1px solid #333; }}
  #loading {{ color:#ffe792; font-size:0.9rem; padding:2rem; }}
  #error {{ color:#ff6b6b; font-size:0.9rem; padding:1rem; display:none; }}
  .btn-row {{ display:flex; gap:0.75rem; flex-wrap:wrap; margin-top:1rem; justify-content:center; }}
  .btn {{ padding:0.6rem 1.5rem; border:none; border-radius:8px; font-size:0.85rem; font-weight:600; cursor:pointer; transition:all 0.15s; }}
  .btn-primary {{ background:#ffe792; color:#1a1a00; }}
  .btn-primary:hover {{ background:#ffd709; }}
  .btn-secondary {{ background:#2a2a2a; color:#ccc; border:1px solid #444; }}
  .btn-secondary:hover {{ background:#333; }}
  .btn:disabled {{ opacity:0.4; cursor:not-allowed; }}
  .size-info {{ font-size:0.75rem; color:#666; margin-top:0.5rem; text-align:center; }}
</style>
</head>
<body>

<h1>Image Generation Preview</h1>

<div class="card">
  <h2>Settings</h2>
  <dl class="meta">
    <dt>Subject</dt><dd>{subject}</dd>
    <dt>Quality</dt><dd>{quality}</dd>
    <dt>Detail</dt><dd>{detail}</dd>
    <dt>Model</dt><dd>{model}</dd>
    <dt>Size</dt><dd>{width} x {height}</dd>
    <dt>Composition</dt><dd>{composition}</dd>
    <dt>Lighting</dt><dd>{lighting}</dd>
    <dt>Style</dt><dd>{style}</dd>
  </dl>
</div>

<div class="card">
  <h2>Prompt (EN)</h2>
  <div class="prompt-box">{prompt_en}</div>
  <h2 style="margin-top:1rem;">Prompt (KO)</h2>
  <div class="prompt-box ko">{prompt_ko}</div>
</div>

<div class="card" style="text-align:center;">
  <h2>Result</h2>
  <div id="img-container">
    <div id="loading">Generating image...</div>
    <div id="error">Failed to load. Check your network connection.</div>
  </div>
  <div class="size-info" id="size-info"></div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btn-download" disabled onclick="downloadPNG()">Download PNG</button>
    <button class="btn btn-secondary" onclick="regenerate()">Regenerate (new seed)</button>
    <button class="btn btn-secondary" onclick="copyPrompt()">Copy Prompt</button>
  </div>
</div>

<script>
const API_URL = "{api_url}";
const FILENAME = "{filename}";
const PROMPT = `{prompt_escaped}`;
let imgBlob = null;

const img = new Image();
img.crossOrigin = "anonymous";
img.onload = function() {{
  document.getElementById('loading').style.display = 'none';
  document.getElementById('img-container').appendChild(img);
  document.getElementById('btn-download').disabled = false;
  // Convert to blob for download
  const canvas = document.createElement('canvas');
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  canvas.getContext('2d').drawImage(img, 0, 0);
  canvas.toBlob(function(blob) {{
    imgBlob = blob;
    const kb = (blob.size / 1024).toFixed(1);
    document.getElementById('size-info').textContent =
      img.naturalWidth + ' x ' + img.naturalHeight + ' — ' + kb + ' KB';
  }}, 'image/png');
}};
img.onerror = function() {{
  document.getElementById('loading').style.display = 'none';
  document.getElementById('error').style.display = 'block';
}};
img.src = API_URL;

function downloadPNG() {{
  if (!imgBlob) return;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(imgBlob);
  a.download = FILENAME;
  a.click();
  URL.revokeObjectURL(a.href);
}}

function regenerate() {{
  document.getElementById('loading').style.display = 'block';
  document.getElementById('error').style.display = 'none';
  document.getElementById('btn-download').disabled = true;
  const existing = document.getElementById('img-container').querySelector('img');
  if (existing) existing.remove();
  img.src = API_URL + '&seed=' + Math.floor(Math.random() * 999999);
}}

function copyPrompt() {{
  navigator.clipboard.writeText(PROMPT).then(() => {{
    const btn = event.target;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy Prompt', 1500);
  }});
}}
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML preview with PNG download"
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--prompt-ko", default=None,
                        help="Korean translation of prompt (auto-placeholder if omitted)")
    parser.add_argument("--quality", "-q", default="standard",
                        choices=["draft", "standard", "high", "ultra"])
    parser.add_argument("--detail", "-d", default=None,
                        choices=["minimal", "normal", "detailed", "maximum"])
    parser.add_argument("--model", "-m", default=None, choices=AVAILABLE_MODELS)
    parser.add_argument("--style", "-s", default=None)
    parser.add_argument("--filter", "-f", default=None)
    parser.add_argument("--composition", default=None,
                        choices=list(COMPOSITION_PRESETS.keys()))
    parser.add_argument("--lighting", default=None,
                        choices=list(LIGHTING_PRESETS.keys()))
    parser.add_argument("--width", "-W", type=int, default=None)
    parser.add_argument("--height", "-H", type=int, default=None)
    parser.add_argument("--purpose", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", "-o", required=True, help="Output HTML path")
    parser.add_argument("--png-name", default=None,
                        help="Download filename (default: from --output)")
    parser.add_argument("--open", action="store_true",
                        help="Auto-open in browser")
    args = parser.parse_args()

    # Resolve detail
    detail_level = args.detail or {
        "draft": "minimal", "standard": "normal",
        "high": "detailed", "ultra": "maximum",
    }[args.quality]

    # Resolve dimensions
    tier = get_quality_tier(args.quality)
    width = args.width
    height = args.height
    if args.purpose and not (width and height):
        pw, ph = get_dimensions(args.purpose)
        width = width or pw
        height = height or ph
    width = width or tier["width"]
    height = height or tier["height"]

    # Resolve model
    model = args.model or auto_select_model(quality=args.quality, task="generate")

    # Resolve enhance
    enhance = tier["enhance"]

    # Build filters
    filters = [f.strip() for f in args.filter.split(",")] if args.filter else None

    # Build prompt
    subject = detect_subject(args.prompt)
    final_prompt = build_prompt(
        base_prompt=args.prompt, filters=filters, style=args.style,
        quality=args.quality, composition=args.composition,
        lighting=args.lighting, detail_level=detail_level,
    )

    # Build API URL
    api_url = generate_image_url(
        prompt=final_prompt, model=model, width=width, height=height,
        seed=args.seed, enhance=enhance,
    )

    # PNG download filename
    png_name = args.png_name or os.path.splitext(
        os.path.basename(args.output))[0] + ".png"

    # Korean prompt placeholder
    prompt_ko = args.prompt_ko or "(Claude가 한글 번역을 여기에 삽입)"

    # Render HTML
    rendered = HTML_TEMPLATE.format(
        title=html.escape(args.prompt[:60]),
        subject=html.escape(subject),
        quality=html.escape(args.quality),
        detail=html.escape(detail_level),
        model=html.escape(model),
        width=width,
        height=height,
        composition=html.escape(args.composition or "—"),
        lighting=html.escape(args.lighting or "—"),
        style=html.escape(args.style or "—"),
        prompt_en=html.escape(final_prompt),
        prompt_ko=html.escape(prompt_ko),
        api_url=api_url,
        filename=html.escape(png_name),
        prompt_escaped=final_prompt.replace("`", "\\`").replace("\\", "\\\\"),
    )

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Preview saved: {args.output}", file=sys.stderr)
    print(f"PNG download name: {png_name}", file=sys.stderr)
    print(args.output)

    if args.open:
        webbrowser.open(f"file://{os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
