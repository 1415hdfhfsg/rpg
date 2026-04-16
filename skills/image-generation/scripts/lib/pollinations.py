"""
Pollinations.ai API wrapper.
Free, no API key required for basic usage.
Docs: https://github.com/pollinations/pollinations/blob/main/APIDOCS.md
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
import sys

BASE_URL = "https://image.pollinations.ai"

AVAILABLE_MODELS = [
    "flux",           # General purpose, high quality (default)
    "turbo",          # Fast drafts
    "gptimage",       # Photorealistic, text rendering
    "kontext",        # Image editing, img2img
    "seedream",       # Creative/artistic
    "seedream-pro",   # Premium artistic
    "nanobanana",     # Editing, multi-turn (Gemini 2.5 Flash Image)
    "nanobanana-pro", # Premium editing
    "zimage",         # Alternative generation
]

# Models that support image-to-image
IMG2IMG_MODELS = ["kontext", "nanobanana", "nanobanana-pro", "gptimage"]

# Model quality rankings (higher = better detail rendering)
MODEL_DETAIL_RANK = {
    "gptimage":       5,  # Best photorealistic detail
    "seedream-pro":   5,  # Best artistic detail
    "nanobanana-pro": 4,
    "flux":           4,  # Strong all-rounder
    "seedream":       3,
    "nanobanana":     3,
    "kontext":        3,  # Best for edits
    "zimage":         2,
    "turbo":          1,  # Speed over quality
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
        return current_model  # user explicitly chose

    quality_model_map = {
        "draft":    {"generate": "turbo",    "edit": "kontext", "compose": "turbo"},
        "standard": {"generate": "flux",     "edit": "kontext", "compose": "gptimage"},
        "high":     {"generate": "flux",     "edit": "nanobanana", "compose": "gptimage"},
        "ultra":    {"generate": "gptimage", "edit": "nanobanana-pro", "compose": "gptimage"},
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
        "generate": "flux",
        "edit": "kontext",
        "photorealistic": "gptimage",
        "artistic": "seedream",
        "fast": "turbo",
        "text_in_image": "gptimage",
        "style_transfer": "kontext",
        "filter": "kontext",
        "compose": "gptimage",
    }
    return task_map.get(task, DEFAULT_MODEL)
