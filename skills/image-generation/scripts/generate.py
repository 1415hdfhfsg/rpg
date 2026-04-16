#!/usr/bin/env python3
"""
Text-to-Image generation with quality tiers and detail enhancement.

Usage:
  # Quick draft
  python3 generate.py -p "a dragon" -q draft -o dragon.png

  # Standard (default)
  python3 generate.py -p "a dragon in a forest" -o dragon.png

  # High quality with detail expansion
  python3 generate.py -p "a dragon in a forest" -q high -o dragon.png

  # Ultra quality, maximum detail, specific composition
  python3 generate.py -p "freshly baked bread on a wooden table" \
    -q ultra -d maximum --composition close-up --lighting golden -o bread.png

  # With style and purpose
  python3 generate.py -p "coffee shop logo" --style logo --purpose instagram-feed -o logo.png
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import (
    generate_and_save, auto_select_model, AVAILABLE_MODELS, DEFAULT_MODEL,
)
from prompt_builder import (
    build_prompt, get_dimensions, get_quality_tier, detect_subject,
    list_compositions, list_lighting, list_quality_tiers,
    COMPOSITION_PRESETS, LIGHTING_PRESETS,
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images from text prompts with quality control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality tiers:
  draft     Fast preview (512px, turbo model)
  standard  Balanced quality (1024px, flux model)  [default]
  high      Rich detail (1280px, flux + enhance)
  ultra     Maximum fidelity (1440px, gptimage + enhance + detail boost)

Detail levels:
  minimal   User prompt only, no expansion
  normal    User prompt + quality tags  [default]
  detailed  Auto-expand with subject-aware details
  maximum   Full detail expansion + micro-detail boosters

Compositions: close-up, portrait, full-body, wide, aerial, macro,
              dutch-angle, low-angle, overhead, three-quarter

Lighting: natural, golden, dramatic, studio, neon, volumetric, rim, ambient, cinematic
        """,
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--quality", "-q", default="standard",
                        choices=["draft", "standard", "high", "ultra"],
                        help="Quality tier (default: standard)")
    parser.add_argument("--detail", "-d", default=None,
                        choices=["minimal", "normal", "detailed", "maximum"],
                        help="Detail expansion level (auto-set by quality if omitted)")
    parser.add_argument("--model", "-m", default=None,
                        choices=AVAILABLE_MODELS, help="Override model selection")
    parser.add_argument("--style", "-s", default=None,
                        help="Quick style (e.g. anime, photorealistic, fantasy)")
    parser.add_argument("--filter", "-f", default=None,
                        help="Filter preset (e.g. cinematic/wes-anderson)")
    parser.add_argument("--composition", default=None,
                        choices=list(COMPOSITION_PRESETS.keys()),
                        help="Camera/composition preset")
    parser.add_argument("--lighting", default=None,
                        choices=list(LIGHTING_PRESETS.keys()),
                        help="Lighting preset")
    parser.add_argument("--width", "-W", type=int, default=None, help="Width in px")
    parser.add_argument("--height", "-H", type=int, default=None, help="Height in px")
    parser.add_argument("--purpose", default=None,
                        help="Auto-size (e.g. instagram-feed, youtube-thumbnail)")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument("--no-enhance", action="store_true",
                        help="Disable Pollinations AI prompt enhancement")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--show-prompt", action="store_true",
                        help="Only print the final prompt, don't generate")
    args = parser.parse_args()

    # --- Resolve detail level (auto from quality if not set) ---
    detail_level = args.detail
    if detail_level is None:
        detail_level = {
            "draft": "minimal",
            "standard": "normal",
            "high": "detailed",
            "ultra": "maximum",
        }[args.quality]

    # --- Get quality tier config ---
    tier = get_quality_tier(args.quality)

    # --- Resolve dimensions ---
    width = args.width
    height = args.height
    if args.purpose and not (width and height):
        pw, ph = get_dimensions(args.purpose)
        width = width or pw
        height = height or ph
    if not width:
        width = tier["width"]
    if not height:
        height = tier["height"]

    # --- Resolve model ---
    model = args.model or auto_select_model(
        quality=args.quality, task="generate", current_model=args.model
    )

    # --- Resolve enhance ---
    enhance = tier["enhance"] and not args.no_enhance

    # --- Build filters list ---
    filters = None
    if args.filter:
        filters = [f.strip() for f in args.filter.split(",")]

    # --- Detect subject for info ---
    subject = detect_subject(args.prompt)

    # --- Build final prompt ---
    final_prompt = build_prompt(
        base_prompt=args.prompt,
        filters=filters,
        style=args.style,
        quality=args.quality,
        composition=args.composition,
        lighting=args.lighting,
        detail_level=detail_level,
    )

    # --- Report ---
    print(f"Subject detected: {subject}", file=sys.stderr)
    print(f"Quality: {args.quality} | Detail: {detail_level}", file=sys.stderr)
    print(f"Model: {model} | Size: {width}x{height} | Enhance: {enhance}", file=sys.stderr)
    print(f"Prompt ({len(final_prompt)} chars):", file=sys.stderr)
    print(f"  {final_prompt}", file=sys.stderr)

    if args.show_prompt:
        print(final_prompt)
        return

    # --- Generate ---
    result = generate_and_save(
        prompt=final_prompt,
        output_path=args.output,
        model=model,
        width=width,
        height=height,
        seed=args.seed,
        enhance=enhance,
    )

    print(result)


if __name__ == "__main__":
    main()
