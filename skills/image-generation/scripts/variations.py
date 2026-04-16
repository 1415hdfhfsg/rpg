#!/usr/bin/env python3
"""
Generate multiple style variations of a single image.
Takes one photo and produces N different styled versions.

Usage:
  python3 variations.py --input photo.jpg --count 5 --output-dir variations/
  python3 variations.py --input photo.jpg --styles "mood/dreamy,era/polaroid-70s,cinematic/noir" --output-dir variations/
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, IMG2IMG_MODELS
from prompt_builder import load_filter, load_all_filters
from edit import image_to_data_url

# Default variation set when user doesn't specify
DEFAULT_VARIATIONS = [
    "cinematic/teal-orange",
    "mood/dreamy",
    "era/polaroid-70s",
    "cinematic/wes-anderson",
    "lighting/golden-hour",
    "artistic/anime",
    "color-grade/bw-high-contrast",
    "weather/autumn",
    "cinematic/noir",
    "mood/vibrant",
]


def main():
    parser = argparse.ArgumentParser(description="Generate style variations")
    parser.add_argument("--input", "-i", required=True, help="Input image")
    parser.add_argument("--styles", "-s", default=None,
                        help="Comma-separated filter keys to use")
    parser.add_argument("--count", "-n", type=int, default=5,
                        help="Number of variations (if --styles not specified)")
    parser.add_argument("--model", "-m", default="kontext",
                        choices=IMG2IMG_MODELS)
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    args = parser.parse_args()

    # Resolve input
    if args.input.startswith(("http://", "https://")):
        image_url = args.input
    elif os.path.isfile(args.input):
        image_url = image_to_data_url(args.input)
    else:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Determine which filters to apply
    if args.styles:
        filter_keys = [s.strip() for s in args.styles.split(",")]
    else:
        filter_keys = DEFAULT_VARIATIONS[:args.count]

    os.makedirs(args.output_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(args.input))[0]

    print(f"Generating {len(filter_keys)} variations...\n", file=sys.stderr)

    results = []
    for i, fk in enumerate(filter_keys, 1):
        flt = load_filter(fk)
        if flt is None:
            print(f"[{i}/{len(filter_keys)}] Skip: '{fk}' not found", file=sys.stderr)
            continue

        name = flt.get("name", flt["id"])
        modifier = flt.get("prompt_modifier", fk)
        safe_name = flt["id"].replace(" ", "_")
        output_path = os.path.join(args.output_dir, f"{basename}_{safe_name}.png")

        prompt = f"Transform this image: {modifier}"
        print(f"[{i}/{len(filter_keys)}] {fk} ({name})", file=sys.stderr)

        try:
            result = generate_and_save(
                prompt=prompt,
                output_path=output_path,
                model=args.model,
                input_image_url=image_url,
            )
            results.append(result)
        except Exception as e:
            print(f"  Failed: {e}", file=sys.stderr)

    print(f"\nDone: {len(results)}/{len(filter_keys)} variations saved to {args.output_dir}")


if __name__ == "__main__":
    main()
