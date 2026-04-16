#!/usr/bin/env python3
"""
Apply photo filter presets to images.
Transforms images using predefined style/mood/cinematic presets.

Usage:
  python3 apply_filter.py --input photo.jpg --filter cinematic/wes-anderson --output filtered.png
  python3 apply_filter.py --input photo.jpg --filter mood/dreamy,weather/autumn --output filtered.png
  python3 apply_filter.py --list                    # List all available filters
  python3 apply_filter.py --list --category mood    # List filters in a category
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, IMG2IMG_MODELS
from prompt_builder import load_filter, load_all_filters
from edit import image_to_data_url


def list_filters(category=None):
    """Print all available filters."""
    all_filters = load_all_filters()
    if not all_filters:
        print("No filters found. Check presets/photo-filters/ directory.")
        return

    current_cat = None
    for key, flt in sorted(all_filters.items()):
        cat = key.split("/")[0]

        if category and cat != category:
            continue

        if cat != current_cat:
            current_cat = cat
            print(f"\n=== {cat.upper()} ===")

        name = flt.get("name", flt["id"])
        desc = flt.get("description", "")
        print(f"  {key:35s} {name} — {desc}")

    print(f"\nTotal: {len(all_filters)} filters")


def main():
    parser = argparse.ArgumentParser(description="Apply photo filter presets")
    parser.add_argument("--input", "-i", help="Input image path or URL")
    parser.add_argument("--filter", "-f", help="Filter(s), comma-separated (e.g. cinematic/wes-anderson,mood/dreamy)")
    parser.add_argument("--model", "-m", default="kontext",
                        choices=IMG2IMG_MODELS, help="Model for transformation")
    parser.add_argument("--width", "-W", type=int, default=None)
    parser.add_argument("--height", "-H", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--list", "-l", action="store_true", help="List available filters")
    parser.add_argument("--category", "-c", default=None, help="Filter by category when listing")
    args = parser.parse_args()

    if args.list:
        list_filters(args.category)
        return

    if not args.input or not args.filter or not args.output:
        parser.error("--input, --filter, and --output are required (unless --list)")

    # Parse filters
    filter_keys = [f.strip() for f in args.filter.split(",")]

    # Build combined prompt from filters
    prompt_parts = []
    best_model = args.model

    for fk in filter_keys:
        flt = load_filter(fk)
        if flt is None:
            print(f"Warning: Filter '{fk}' not found, skipping.", file=sys.stderr)
            continue

        name = flt.get("name", flt["id"])
        modifier = flt.get("prompt_modifier", "")
        print(f"Applying: {fk} ({name})", file=sys.stderr)

        if modifier:
            prompt_parts.append(modifier.strip())

        # Use filter's recommended model if available
        if flt.get("model") and best_model == "kontext":
            best_model = flt["model"]

    if not prompt_parts:
        print("Error: No valid filters found.", file=sys.stderr)
        sys.exit(1)

    final_prompt = "Transform this image: " + ", ".join(prompt_parts)

    # Resolve input image
    if args.input.startswith(("http://", "https://", "data:")):
        image_url = args.input
    elif os.path.isfile(args.input):
        image_url = image_to_data_url(args.input)
    else:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Model: {best_model}", file=sys.stderr)
    print(f"Prompt: {final_prompt}", file=sys.stderr)

    result = generate_and_save(
        prompt=final_prompt,
        output_path=args.output,
        model=best_model,
        width=args.width,
        height=args.height,
        seed=args.seed,
        input_image_url=image_url,
    )

    print(result)


if __name__ == "__main__":
    main()
