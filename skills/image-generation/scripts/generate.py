#!/usr/bin/env python3
"""
Text-to-Image generation.
Usage:
  python3 generate.py --prompt "a dragon in a forest" --output dragon.png
  python3 generate.py --prompt "logo for coffee shop" --style logo --output logo.png
  python3 generate.py --prompt "game item sword" --purpose game-icon --output sword.png
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, AVAILABLE_MODELS, DEFAULT_MODEL
from prompt_builder import build_prompt, get_dimensions, list_dimensions


def main():
    parser = argparse.ArgumentParser(description="Generate images from text prompts")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL,
                        choices=AVAILABLE_MODELS, help="Generation model")
    parser.add_argument("--style", "-s", default=None,
                        help="Quick style (e.g. anime, pixel-art, fantasy)")
    parser.add_argument("--filter", "-f", default=None,
                        help="Filter preset (e.g. cinematic/wes-anderson)")
    parser.add_argument("--width", "-W", type=int, default=None, help="Width in px")
    parser.add_argument("--height", "-H", type=int, default=None, help="Height in px")
    parser.add_argument("--purpose", default=None,
                        help="Auto-size by purpose (e.g. instagram-feed, youtube-thumbnail)")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument("--enhance", action="store_true", help="AI-enhance the prompt")
    parser.add_argument("--no-quality-tags", action="store_true",
                        help="Skip appending quality boost tags")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    args = parser.parse_args()

    # Resolve dimensions
    if args.purpose and not (args.width and args.height):
        w, h = get_dimensions(args.purpose)
        args.width = args.width or w
        args.height = args.height or h

    # Build filters list
    filters = None
    if args.filter:
        filters = [f.strip() for f in args.filter.split(",")]

    # Build final prompt
    final_prompt = build_prompt(
        base_prompt=args.prompt,
        filters=filters,
        style=args.style,
        quality_tags=not args.no_quality_tags,
    )

    print(f"Prompt: {final_prompt}", file=sys.stderr)

    result = generate_and_save(
        prompt=final_prompt,
        output_path=args.output,
        model=args.model,
        width=args.width,
        height=args.height,
        seed=args.seed,
        enhance=args.enhance,
    )

    print(result)


if __name__ == "__main__":
    main()
