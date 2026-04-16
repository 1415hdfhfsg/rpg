#!/usr/bin/env python3
"""
Compose multiple images into one using AI.

Usage:
  python3 compose.py --images "person.png,bg.jpg" \
    --instruction "place the person naturally in front of the background" \
    --output composed.png
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from pollinations import generate_and_save


def main():
    parser = argparse.ArgumentParser(description="Compose multiple images")
    parser.add_argument("--images", required=True,
                        help="Comma-separated image paths or URLs")
    parser.add_argument("--instruction", "-t", required=True,
                        help="How to compose the images")
    parser.add_argument("--model", "-m", default="gptimage",
                        help="Model (gptimage recommended for composition)")
    parser.add_argument("--width", "-W", type=int, default=1024)
    parser.add_argument("--height", "-H", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    image_list = [img.strip() for img in args.images.split(",")]

    # For composition, we describe the images in the prompt
    # and use the first image as the base for img2img
    prompt = f"Compose these elements: {args.instruction}"

    # Use first image as input reference
    first_image = image_list[0]
    if os.path.isfile(first_image):
        from edit import image_to_data_url
        first_image = image_to_data_url(first_image)

    if len(image_list) > 1:
        extra = ", ".join(image_list[1:])
        prompt += f" (additional references: {extra})"

    print(f"Composing {len(image_list)} images...", file=sys.stderr)
    print(f"Instruction: {args.instruction}", file=sys.stderr)

    result = generate_and_save(
        prompt=prompt,
        output_path=args.output,
        model=args.model,
        width=args.width,
        height=args.height,
        seed=args.seed,
        input_image_url=first_image,
    )

    print(result)


if __name__ == "__main__":
    main()
