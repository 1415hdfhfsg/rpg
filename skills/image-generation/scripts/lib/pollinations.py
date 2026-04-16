"""
Pollinations.ai API wrapper.
Free, no API key required for basic usage.
Docs: https://github.com/pollinations/pollinations/blob/main/APIDOCS.md

Curated model list — low-quality models excluded.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
import sys

BASE_URL = "https://image.pollinations.ai"

# -----------------------------------------------------------------------
# Curated high-quality models only
# Excluded: turbo (low detail), klein (weak), zimage (mediocre),
#           p-image / p-image-edit (unverified quality), wan-image (keep pro only)
# -----------------------------------------------------------------------
AVAILABLE_MODELS = [
    # --- Photorealistic / Top Tier ---
    "gptimage-large",  # GPT Image 1.5 — best photorealism, text rendering
    "gptimage",        # GPT Image 1   — strong photorealism, text rendering
    # --- Creative / Artistic ---
    "grok-imagine-pro", # Grok premium  — bold creative, few restrictions
    "grok-imagine",     # Grok standard — creative, unconventional
    "seedream5",        # Seedream v5   — latest artistic, rich color
    "seedream-pro",     # Seedream premium — high-end artistic
    "seedream",         # Seedream standard — solid artistic
    # --- Text Rendering / Special ---
    "qwen-image",      # Qwen Image    — text accuracy, LoRA, layer editing
    # --- All-rounder ---
    "flux",            # FLUX.1        — reliable, fast, good prompt adherence
    # --- Editing / Img2Img ---
    "kontext",         # FLUX Kontext   — instruction-based editing best
    "nanobanana-pro",  # NB Pro         — premium multi-turn editing
    "nanobanana-2",    # NB v2          — improved editing
    "nanobanana",      # NB standard    — Gemini-based editing
    # --- Cinematic / Commercial ---
    "wan-image-pro",   # Wan Pro        — cinematic stills
    "nova-canvas",     # Nova Canvas    — stable commercial/product
]

# Models that support image-to-image
IMG2IMG_MODELS = [
    "kontext", "nanobanana", "nanobanana-2", "nanobanana-pro",
    "gptimage", "gptimage-large",
]

# Quality ranking (1-5, higher = better output fidelity)
MODEL_QUALITY_RANK = {
    "gptimage-large":  5,
    "gptimage":        5,
    "grok-imagine-pro": 5,
    "seedream-pro":    5,
    "nanobanana-pro":  4,
    "seedream5":       4,
    "grok-imagine":    4,
    "qwen-image":      4,
    "flux":            4,
    "wan-image-pro":   4,
    "kontext":         4,
    "nanobanana-2":    3,
    "seedream":        3,
    "nanobanana":      3,
    "nova-canvas":     3,
}

DEFAULT_MODEL = "flux"
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def auto_select_model(quality="standard", task="generate", current_model=None):
    """
    Recommend the best model based on quality tier and task.
    If the user explicitly chose a model, respect that choice.
    """
    if current_model and current_model != DEFAULT_MODEL:
        return current_model

    quality_model_map = {
        "draft":    {
            "generate": "flux",
            "edit": "kontext",
            "compose": "gptimage",
            "artistic": "seedream",
            "cinematic": "flux",
        },
        "standard": {
            "generate": "flux",
            "edit": "kontext",
            "compose": "gptimage",
            "artistic": "seedream5",
            "cinematic": "wan-image-pro",
        },
        "high":     {
            "generate": "gptimage",
            "edit": "nanobanana-2",
            "compose": "gptimage-large",
            "artistic": "seedream-pro",
            "cinematic": "wan-image-pro",
        },
        "ultra":    {
            "generate": "gptimage-large",
            "edit": "nanobanana-pro",
            "compose": "gptimage-large",
            "artistic": "grok-imagine-pro",
            "cinematic": "wan-image-pro",
        },
    }

    tier = quality_model_map.get(quality, quality_model_map["standard"])
    return tier.get(task, "flux")


def generate_image_url(prompt, model=None, width=None, height=None,
                       seed=None, enhance=False, safe=False,
                       input_image_url=None):
    """Build a Pollinations image generation URL."""
    model = model or DEFAULT_MODEL
    width = width or DEFAULT_WIDTH
    height = height or DEFAULT_HEIGHT

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{BASE_URL}/prompt/{encoded_prompt}"

    params = {
        "model": model,
        "width": str(width),
        "height": str(height),
        "nologo": "true",
    }

    if seed is not None:
        params["seed"] = str(seed)
    if enhance:
        params["enhance"] = "true"
    if safe:
        params["safe"] = "true"
    if input_image_url and model in IMG2IMG_MODELS:
        params["image"] = input_image_url

    query = urllib.parse.urlencode(params)
    return f"{url}?{query}"


def download_image(url, output_path, retries=MAX_RETRIES):
    """Download an image from URL with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            print(f"[{attempt}/{retries}] Requesting image...", file=sys.stderr)
            req = urllib.request.Request(url, headers={
                "User-Agent": "ImageGenSkill/2.0"
            })
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()

            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(data)

            size_kb = len(data) / 1024
            print(f"Saved: {output_path} ({size_kb:.1f} KB)", file=sys.stderr)
            return output_path

        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
            if attempt < retries:
                wait = RETRY_DELAY * attempt
                print(f"Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                raise RuntimeError(f"Failed after {retries} attempts: {e}")


def generate_and_save(prompt, output_path, model=None, width=None,
                      height=None, seed=None, enhance=False,
                      safe=False, input_image_url=None):
    """Generate an image and save it to disk."""
    url = generate_image_url(
        prompt=prompt,
        model=model,
        width=width,
        height=height,
        seed=seed,
        enhance=enhance,
        safe=safe,
        input_image_url=input_image_url,
    )
    print(f"Model: {model or DEFAULT_MODEL}", file=sys.stderr)
    print(f"Size: {width or DEFAULT_WIDTH}x{height or DEFAULT_HEIGHT}", file=sys.stderr)
    print(f"Enhance: {enhance}", file=sys.stderr)
    print(f"URL: {url[:200]}...", file=sys.stderr)
    return download_image(url, output_path)


def list_models():
    """Return list of available models."""
    return AVAILABLE_MODELS


def get_best_model(task="generate"):
    """Suggest the best model for a given task."""
    task_map = {
        "generate":      "flux",
        "edit":          "kontext",
        "photorealistic": "gptimage-large",
        "artistic":      "seedream-pro",
        "text_in_image": "gptimage-large",
        "style_transfer": "kontext",
        "filter":        "kontext",
        "compose":       "gptimage-large",
        "cinematic":     "wan-image-pro",
        "creative":      "grok-imagine-pro",
        "commercial":    "nova-canvas",
    }
    return task_map.get(task, DEFAULT_MODEL)
