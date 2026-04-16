#!/usr/bin/env python3
"""
Style transfer: transform an image into a different artistic style.

Usage:
  python3 style_transfer.py --input photo.jpg --style anime --output anime_version.png
  python3 style_transfer.py --input photo.jpg --style "oil-painting" --output painted.png
  python3 style_transfer.py --list   # Show available styles
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save, IMG2IMG_MODELS
from edit import image_to_data_url

STYLES = {
    "anime": "Transform into anime style, cel shading, vibrant colors, clean lines, anime character design",
    "pixel-art": "Convert to 16-bit pixel art, retro game style, limited color palette, crisp pixels",
    "oil-painting": "Transform into an oil painting on canvas, visible brushstrokes, rich colors, museum quality",
    "watercolor": "Convert to watercolor painting, soft edges, paper texture, artistic wet-on-wet technique",
    "pencil-sketch": "Transform into detailed pencil sketch, hatching, crosshatching, monochrome graphite drawing",
    "ink-wash": "Convert to ink wash painting, sumi-e style, traditional East Asian brush art, minimalist",
    "pop-art": "Transform into pop art, bold colors, Ben-Day dots, Andy Warhol inspired, high contrast",
    "comic-book": "Convert to comic book art, ink outlines, halftone dots, bold colors, superhero comic style",
    "ghibli": "Transform into Studio Ghibli animation style, hand-drawn, soft watercolor, warm atmosphere",
    "low-poly": "Convert to low-poly 3D render style, geometric facets, clean flat colors, modern art",
    "impressionist": "Transform into impressionist painting, Monet style, dappled light, visible brushwork",
    "cyberpunk": "Transform into cyberpunk aesthetic, neon lights, holographic, dark futuristic, high tech",
    "vector-flat": "Convert to flat vector illustration, minimalist design, clean shapes, limited palette",
    "charcoal": "Transform into charcoal drawing, rich blacks, dramatic shading, textured paper feel",
    "stained-glass": "Convert to stained glass art style, bold outlines, translucent colored segments, medieval",
    "vaporwave": "Transform into vaporwave aesthetic, pink/purple/cyan, glitch effects, retro 90s digital",
    "ukiyo-e": "Convert to ukiyo-e woodblock print style, Japanese art, flat colors, bold outlines",
    "art-nouveau": "Transform into Art Nouveau style, organic curves, decorative borders, Alphonse Mucha inspired",
}


def main():
    parser = argparse.ArgumentParser(description="Style transfer")
    parser.add_argument("--input", "-i", help="Input image path or URL")
    parser.add_argument("--style", "-s", help="Target style name")
    parser.add_argument("--custom", default=None,
                        help="Custom style description (overrides --style)")
    parser.add_argument("--model", "-m", default="kontext",
                        choices=IMG2IMG_MODELS)
    parser.add_argument("--width", "-W", type=int, default=None)
    parser.add_argument("--height", "-H", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--list", "-l", action="store_true", help="List available styles")
    args = parser.parse_args()

    if args.list:
        print("Available styles:\n")
        for name, desc in sorted(STYLES.items()):
            print(f"  {name:20s}  {desc[:70]}...")
        return

    if not args.input or not args.output:
        parser.error("--input and --output are required")
    if not args.style and not args.custom:
        parser.error("--style or --custom is required")

    # Resolve style prompt
    if args.custom:
        style_prompt = args.custom
    else:
        style_prompt = STYLES.get(args.style)
        if not style_prompt:
            print(f"Error: Unknown style '{args.style}'. Use --list to see options.",
                  file=sys.stderr)
            sys.exit(1)

    # Resolve input
    if args.input.startswith(("http://", "https://", "data:")):
        image_url = args.input
    elif os.path.isfile(args.input):
        image_url = image_to_data_url(args.input)
    else:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Style: {args.style or 'custom'}", file=sys.stderr)

    result = generate_and_save(
        prompt=style_prompt,
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
