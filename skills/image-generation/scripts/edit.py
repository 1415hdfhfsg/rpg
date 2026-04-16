#!/usr/bin/env python3
"""
Image editing via natural language instructions.
Uses Kontext or NanoBanana models for instruction-based editing.

Usage:
  python3 edit.py --input photo.jpg --instruction "remove the background" --output edited.png
  python3 edit.py --input photo.jpg --instruction "make it sunset" --output sunset.png
"""

import argparse
import sys
import os
import base64
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, IMG2IMG_MODELS


def image_to_data_url(image_path):
    """Convert a local image file to a data URL for API consumption."""
    with open(image_path, "rb") as f:
        data = f.read()

    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
        ".gif": "image/gif", ".bmp": "image/bmp",
    }
    mime = mime_map.get(ext, "image/png")
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main():
    parser = argparse.ArgumentParser(description="Edit images with natural language")
    parser.add_argument("--input", "-i", required=True, help="Input image path or URL")
    parser.add_argument("--instruction", "-t", required=True,
                        help="Editing instruction in natural language")
    parser.add_argument("--model", "-m", default="kontext",
                        choices=IMG2IMG_MODELS, help="Editing model")
    parser.add_argument("--width", "-W", type=int, default=None)
    parser.add_argument("--height", "-H", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    args = parser.parse_args()

    # Resolve input image URL
    if args.input.startswith(("http://", "https://", "data:")):
        image_url = args.input
    elif os.path.isfile(args.input):
        image_url = image_to_data_url(args.input)
    else:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Model: {args.model}", file=sys.stderr)
    print(f"Instruction: {args.instruction}", file=sys.stderr)

    result = generate_and_save(
        prompt=args.instruction,
        output_path=args.output,
        model=args.model,
        width=args.width,
        height=args.height,
        seed=args.seed,
        input_image_url=image_url,
    )

    print(result)


if __name__ == "__main__":
    main()
