"""
Prompt builder utility.
Combines user prompts with style presets, filter modifiers, and quality tags.
"""

import os
import yaml

PRESETS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "presets", "photo-filters"
)

# Dimension presets by purpose
DIMENSIONS = {
    "instagram-feed":    (1024, 1024),
    "instagram-story":   (1080, 1920),
    "youtube-thumbnail":  (1280, 720),
    "twitter-banner":    (1500, 500),
    "desktop-wallpaper": (1920, 1080),
    "mobile-wallpaper":  (1080, 1920),
    "game-icon":         (512, 512),
    "game-character":    (768, 1024),
    "a4-print":          (2480, 3508),
    "business-card":     (1050, 600),
    "pinterest-pin":     (1000, 1500),
    "tiktok":            (1080, 1920),
    "square":            (1024, 1024),
    "landscape":         (1280, 720),
    "portrait":          (720, 1280),
}


def load_filter(filter_path):
    """
    Load a filter preset by path like 'cinematic/wes-anderson'.
    Returns the filter dict or None.
    """
    parts = filter_path.strip().split("/")
    if len(parts) != 2:
        return None

    category, name = parts
    yaml_path = os.path.join(PRESETS_DIR, f"{category}.yaml")

    if not os.path.exists(yaml_path):
        return None

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    filters = data.get("filters", [])
    for flt in filters:
        if flt.get("id") == name:
            return flt

    return None


def load_all_filters():
    """Load all filter presets from all category files."""
    all_filters = {}
    if not os.path.isdir(PRESETS_DIR):
        return all_filters

    for fname in sorted(os.listdir(PRESETS_DIR)):
        if not fname.endswith(".yaml"):
            continue
        category = fname.replace(".yaml", "")
        fpath = os.path.join(PRESETS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for flt in data.get("filters", []):
            key = f"{category}/{flt['id']}"
            all_filters[key] = flt

    return all_filters


def build_prompt(base_prompt, filters=None, style=None, quality_tags=True):
    """
    Build a final prompt by combining:
    - base_prompt: user's description
    - filters: list of filter paths (e.g. ['cinematic/wes-anderson', 'mood/dreamy'])
    - style: a quick style keyword
    - quality_tags: append quality boosters
    """
    parts = [base_prompt.strip()]

    # Apply filter modifiers
    if filters:
        for fp in filters:
            flt = load_filter(fp)
            if flt and flt.get("prompt_modifier"):
                parts.append(flt["prompt_modifier"].strip())

    # Apply quick style
    quick_styles = {
        "photorealistic": "8k, ultra realistic, cinematic lighting, sharp focus, DSLR",
        "anime": "anime style, cel shading, vibrant colors, clean lines",
        "pixel-art": "16-bit pixel art, retro game style, limited palette",
        "oil-painting": "oil on canvas, impressionist brushstrokes, museum quality",
        "flat-design": "flat vector illustration, minimal, geometric, pastel colors",
        "isometric": "isometric view, 3D render, clean shapes, bright colors",
        "watercolor": "watercolor painting, soft edges, paper texture, artistic",
        "cyberpunk": "neon lights, futuristic city, cyberpunk, blade runner aesthetic",
        "pencil-sketch": "pencil drawing, hatching, monochrome, sketchbook style",
        "3d-render": "octane render, 3D, PBR materials, ray tracing, studio lighting",
        "logo": "minimalist logo design, vector, professional, brand identity, clean",
        "ui-icon": "flat icon, app store ready, simple, recognizable, clean edges",
        "fantasy": "fantasy art, dramatic lighting, epic composition, detailed",
        "ghibli": "studio ghibli style, hand drawn, soft watercolor, warm atmosphere",
        "comic-book": "comic book art style, ink lines, halftone dots, bold colors",
        "pop-art": "pop art style, bold colors, Ben-Day dots, Andy Warhol inspired",
        "ink-wash": "ink wash painting, sumi-e, traditional East Asian brush art",
        "low-poly": "low poly 3D render, geometric, faceted, clean colors",
    }
    if style and style in quick_styles:
        parts.append(quick_styles[style])

    # Quality tags
    if quality_tags:
        parts.append("masterpiece, best quality, highly detailed")

    return ", ".join(parts)


def get_dimensions(purpose=None):
    """Get width, height for a given purpose."""
    if purpose and purpose in DIMENSIONS:
        return DIMENSIONS[purpose]
    return (1024, 1024)


def list_dimensions():
    """Return all available dimension presets."""
    return DIMENSIONS.copy()
