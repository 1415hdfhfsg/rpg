#!/usr/bin/env python3
"""
Analyze an image and extract description, suggested prompt, colors, etc.
Uses the image's visual features to reverse-engineer a generation prompt.

Usage:
  python3 analyze.py --input artwork.jpg
  python3 analyze.py --input photo.jpg --format json
"""

import argparse
import sys
import os
import base64
import json


def analyze_local(image_path):
    """Analyze a local image file and provide basic metadata."""
    if not os.path.isfile(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    size_bytes = os.path.getsize(image_path)
    ext = os.path.splitext(image_path)[1].lower()

    # Try to get image dimensions using basic PNG/JPEG header parsing
    width, height = None, None
    with open(image_path, "rb") as f:
        header = f.read(32)

        # PNG
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            width = int.from_bytes(header[16:20], "big")
            height = int.from_bytes(header[20:24], "big")
        # JPEG
        elif header[:2] == b'\xff\xd8':
            f.seek(0)
            data = f.read()
            i = 2
            while i < len(data) - 1:
                if data[i] == 0xFF:
                    marker = data[i + 1]
                    if marker in (0xC0, 0xC2):  # SOF0 or SOF2
                        height = int.from_bytes(data[i+5:i+7], "big")
                        width = int.from_bytes(data[i+7:i+9], "big")
                        break
                    elif marker == 0xD9:  # EOI
                        break
                    else:
                        length = int.from_bytes(data[i+2:i+4], "big")
                        i += 2 + length
                else:
                    i += 1

    result = {
        "file": image_path,
        "format": ext.lstrip("."),
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "width": width,
        "height": height,
        "aspect_ratio": f"{width}:{height}" if width and height else None,
        "note": (
            "For full AI analysis (description, prompt extraction, style detection), "
            "use Claude Vision by reading this image file directly with the Read tool."
        ),
        "suggested_workflow": [
            "1. Read the image with Claude's Read tool for visual analysis",
            "2. Ask Claude to describe the image and suggest a recreation prompt",
            "3. Use generate.py with the suggested prompt to recreate or iterate",
        ],
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze an image")
    parser.add_argument("--input", "-i", required=True, help="Input image path")
    parser.add_argument("--format", "-f", default="text", choices=["text", "json"],
                        help="Output format")
    args = parser.parse_args()

    result = analyze_local(args.input)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"File:         {result['file']}")
        print(f"Format:       {result['format']}")
        print(f"Size:         {result['size_kb']} KB ({result['size_bytes']} bytes)")
        if result['width'] and result['height']:
            print(f"Dimensions:   {result['width']} x {result['height']}")
            print(f"Aspect Ratio: {result['aspect_ratio']}")
        print()
        print("Tip: For AI-powered analysis, use Claude Vision:")
        print("  → Read this image file, then ask Claude to describe it")
        print("  → Claude can extract style, colors, composition, and suggest prompts")


if __name__ == "__main__":
    main()
