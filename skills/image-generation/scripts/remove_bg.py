#!/usr/bin/env python3
"""
Remove background from images.
Uses Kontext model to isolate the subject.

Usage:
  python3 remove_bg.py --input product.jpg --output product_nobg.png
  python3 remove_bg.py --input person.jpg --bg white --output person_white.png
  python3 remove_bg.py --input item.png --bg "a tropical beach" --output item_beach.png
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, IMG2IMG_MODELS
from edit import image_to_data_url

BG_PRESETS = {
    "transparent": "Remove the background completely, make it transparent, isolate the subject",
    "white": "Remove the background and replace with pure clean white background",
    "black": "Remove the background and replace with pure black background",
    "gradient": "Remove the background and replace with a smooth professional gradient",
    "blur": "Keep the subject sharp and blur the entire background heavily, bokeh effect",
    "studio": "Replace background with professional studio lighting setup, neutral gray",
}


def main():
    parser = argparse.ArgumentParser(description="Remove or replace background")
    parser.add_argument("--input", "-i", required=True, help="Input image")
    parser.add_argument("--bg", "-b", default="transparent",
                        help="Background: transparent/white/black/gradient/blur/studio or custom text")
    parser.add_argument("--model", "-m", default="kontext",
                        choices=IMG2IMG_MODELS)
    parser.add_argument("--width", "-W", type=int, default=None)
    parser.add_argument("--height", "-H", type=int, default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    # Build prompt
    if args.bg in BG_PRESETS:
        prompt = BG_PRESETS[args.bg]
    else:
        prompt = f"Remove the background and replace it with: {args.bg}. Keep the subject intact."

    # Resolve input
    if args.input.startswith(("http://", "https://", "data:")):
        image_url = args.input
    elif os.path.isfile(args.input):
        image_url = image_to_data_url(args.input)
    else:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Background: {args.bg}", file=sys.stderr)

    result = generate_and_save(
        prompt=prompt,
        output_path=args.output,
        model=args.model,
        width=args.width,
        height=args.height,
        input_image_url=image_url,
    )

    print(result)


if __name__ == "__main__":
    main()
