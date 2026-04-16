"""
Prompt builder utility.
Builds structured, detail-rich prompts from user descriptions.

Prompt Architecture:
  [Subject & Action] + [Environment & Scene] + [Style & Medium] +
  [Composition & Camera] + [Lighting & Atmosphere] + [Color & Tone] +
  [Texture & Material] + [Quality Tier Tags]

The detail_enhance() system expands brief user prompts into structured,
high-fidelity generation prompts by inferring missing visual dimensions.
"""

import os
import re
import yaml

PRESETS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "presets", "photo-filters"
)

# ---------------------------------------------------------------------------
# Dimension presets by purpose
# ---------------------------------------------------------------------------
DIMENSIONS = {
    "instagram-feed":    (1024, 1024),
    "instagram-story":   (1080, 1920),
    "youtube-thumbnail": (1280, 720),
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

# ---------------------------------------------------------------------------
# Quality tier system
# ---------------------------------------------------------------------------
QUALITY_TIERS = {
    "draft": {
        "description": "Fast preview, low detail",
        "width": 512, "height": 512,
        "tags": "good quality",
        "model_hint": "turbo",
        "enhance": False,
    },
    "standard": {
        "description": "Balanced quality and speed",
        "width": 1024, "height": 1024,
        "tags": (
            "high quality, detailed, sharp focus, well-composed, "
            "professional color grading"
        ),
        "model_hint": "flux",
        "enhance": False,
    },
    "high": {
        "description": "High fidelity, rich detail",
        "width": 1280, "height": 1280,
        "tags": (
            "masterpiece, best quality, highly detailed, razor sharp focus, "
            "professional photography, 8k uhd, high resolution, "
            "intricate details, rich textures, natural color depth, "
            "accurate shadows, volumetric atmosphere"
        ),
        "model_hint": "flux",
        "enhance": True,
    },
    "ultra": {
        "description": "Maximum quality, publication-ready",
        "width": 1920, "height": 1920,
        "tags": (
            "masterpiece, best quality, extraordinarily detailed, "
            "ultra high resolution, 16k uhd, photorealistic fidelity, "
            "razor sharp focus across entire frame, "
            "intricate fine details visible at pixel level, "
            "professional large-format photography, award winning, "
            "gallery exhibition quality, flawless composition, "
            "accurate global illumination, physically correct light transport, "
            "true-to-life color science, micro-contrast preserved"
        ),
        "model_hint": "gptimage",
        "enhance": True,
    },
}

# ---------------------------------------------------------------------------
# Korean Instagram Aesthetic — Default Reference for Photo/Edit
# ---------------------------------------------------------------------------
# Applied automatically to photo-style generations (person, food, landscape,
# architecture, product). NOT applied to fantasy, anime, pixel-art, etc.
KOREAN_INSTAGRAM_AESTHETIC = {
    "color_grading": (
        "Korean Instagram aesthetic color grading, "
        "muted warm desaturated tones, soft pastel color palette, "
        "lowered contrast with lifted blacks, "
        "warm highlights with slightly cool shadows, "
        "VSCO-style faded film look, "
        "subtle pink and peach undertones"
    ),
    "mood": (
        "Korean 감성 (gamsong) emotional atmosphere, "
        "calm serene contemplative mood, "
        "clean minimalist composition with breathing space, "
        "effortlessly aesthetic, not overly styled"
    ),
    "lighting": (
        "soft diffused natural light, "
        "window light or golden hour preferred, "
        "gentle even illumination without harsh shadows, "
        "light and airy feel"
    ),
    "editing": (
        "subtle Lightroom-style editing, "
        "skin tones warm but not oversaturated, "
        "whites slightly creamy not pure, "
        "overall soft and dreamy processing"
    ),
}

# Subject categories that receive Korean Instagram treatment
KOREAN_AESTHETIC_SUBJECTS = {
    "person", "food", "landscape", "architecture", "product", "default",
}

# Subject categories that skip Korean Instagram treatment
NON_KOREAN_AESTHETIC_STYLES = {
    "anime", "pixel-art", "comic-book", "pop-art", "low-poly",
    "vector-flat", "cyberpunk", "fantasy", "3d-render",
}

# ---------------------------------------------------------------------------
# Subject-aware detail expansion templates
# ---------------------------------------------------------------------------
# Each key is a detected subject category; value is a dict of visual dimensions
# that get merged into the prompt when the user hasn't specified them.
DETAIL_TEMPLATES = {
    "person": {
        "skin": "realistic skin texture with fine pores, warm healthy skin tone, Korean beauty standard natural glow",
        "eyes": "detailed eyes with visible iris patterns and natural reflections",
        "hair": "individual hair strands visible, natural hair texture with soft sheen",
        "clothing": "fabric weave and texture clearly visible, realistic folds and creases",
        "vibe": "Korean street fashion aesthetic, effortlessly styled, natural candid pose",
    },
    "food": {
        "surface": "glistening surface texture, visible moisture and oils",
        "color": "appetizing warm color tones, natural color gradients, Korean cafe plating aesthetic",
        "texture": "crispy crunchy flaky moist textures clearly distinguishable",
        "steam": "subtle steam or heat haze rising from warm areas",
        "plating": "aesthetic Korean cafe-style plating on ceramic dish, minimalist tableware",
        "setting": "clean bright cafe table or wooden surface, soft background blur, latte or drink beside dish",
    },
    "landscape": {
        "atmosphere": "atmospheric perspective with depth haze, dreamy soft air quality",
        "sky": "soft pastel sky with gentle cloud formations",
        "foliage": "individual leaves and branches with natural variation, seasonal Korean scenery",
        "depth": "clear foreground, midground, and background separation with soft transitions",
        "korean": "Korean scenery vibes, Hangang park or Jeju or cherry blossom or autumn foliage feel",
    },
    "architecture": {
        "material": "visible material textures: concrete, glass, wood, Korean hanok details if traditional",
        "detail": "architectural details clearly rendered, clean modern or traditional Korean aesthetic",
        "scale": "sense of scale with environmental context",
        "light": "soft light interaction with surfaces, warm interior glow from windows",
        "vibe": "Korean cafe interior or Bukchon hanok village or modern Seoul architecture feel",
    },
    "animal": {
        "fur": "individual fur strands with natural color variation and sheen",
        "eyes": "expressive eyes with realistic reflections and depth",
        "anatomy": "anatomically accurate proportions and posture",
        "environment": "natural habitat context with appropriate vegetation",
    },
    "product": {
        "material": "product material clearly visible: metal brushing, plastic sheen, glass clarity",
        "reflection": "accurate surface reflections and highlights",
        "edges": "clean sharp product edges with precise manufacturing detail",
        "setting": "Korean minimalist flat lay or clean marble surface, aesthetic props",
    },
    "fantasy": {
        "magic": "magical effects with glowing particles, energy wisps, ethereal light",
        "armor": "intricate armor engravings, battle-worn scratches, metallic reflections",
        "creature": "anatomically believable creature design with realistic textures",
        "environment": "otherworldly atmosphere with dramatic volumetric lighting",
    },
    "default": {
        "detail": "fine intricate details visible throughout",
        "texture": "realistic surface textures and material qualities",
        "depth": "natural depth of field with clear focal plane",
    },
}

# Subject detection keywords
SUBJECT_KEYWORDS = {
    "person": [
        "person", "man", "woman", "girl", "boy", "portrait", "face", "people",
        "model", "child", "selfie", "headshot", "인물", "사람", "여자", "남자",
        "소녀", "소년", "아이", "초상", "셀카",
    ],
    "food": [
        "food", "bread", "cake", "pizza", "sushi", "coffee", "dish", "meal",
        "dessert", "fruit", "meat", "pasta", "burger", "cook", "bake",
        "음식", "빵", "케이크", "커피", "요리", "디저트", "과일", "고기",
        "떡", "라면", "김치", "치킨", "피자",
    ],
    "landscape": [
        "landscape", "mountain", "ocean", "forest", "river", "field", "sky",
        "beach", "valley", "lake", "sunset", "sunrise", "scenery",
        "풍경", "산", "바다", "숲", "강", "하늘", "해변", "호수",
        "노을", "일출", "들판",
    ],
    "architecture": [
        "building", "house", "castle", "cathedral", "temple", "city",
        "interior", "room", "tower", "bridge", "palace", "church",
        "건물", "집", "성", "사원", "도시", "방", "다리", "궁전",
    ],
    "animal": [
        "cat", "dog", "bird", "horse", "dragon", "wolf", "fox", "rabbit",
        "animal", "pet", "wildlife",
        "고양이", "강아지", "개", "새", "말", "용", "늑대", "토끼", "동물",
    ],
    "product": [
        "product", "bottle", "phone", "watch", "shoe", "bag", "car",
        "device", "gadget", "package", "cosmetic",
        "제품", "병", "폰", "시계", "신발", "가방", "자동차", "화장품",
    ],
    "fantasy": [
        "fantasy", "magic", "wizard", "knight", "elf", "demon", "dragon",
        "sword", "spell", "dungeon", "rpg", "medieval", "enchanted",
        "판타지", "마법", "기사", "엘프", "악마", "검", "던전", "중세",
    ],
}

# ---------------------------------------------------------------------------
# Composition / Camera presets
# ---------------------------------------------------------------------------
COMPOSITION_PRESETS = {
    "close-up": "extreme close-up shot, macro detail, shallow depth of field, f/2.8",
    "portrait": "medium close-up portrait framing, 85mm lens, f/1.8 bokeh background",
    "full-body": "full body shot, 50mm lens, environmental context visible",
    "wide": "wide angle establishing shot, 24mm lens, expansive view",
    "aerial": "aerial drone perspective, bird's eye view, sweeping landscape",
    "macro": "macro photography, extreme magnification, razor thin depth of field, focus stacking",
    "dutch-angle": "dutch angle tilt, dynamic diagonal composition, dramatic perspective",
    "low-angle": "low angle hero shot, looking up, dramatic power perspective",
    "overhead": "top-down overhead flat lay, 90 degree angle, organized layout",
    "three-quarter": "three-quarter view, 45 degree angle, dimensional depth",
}

# ---------------------------------------------------------------------------
# Lighting presets (more detailed than filter versions)
# ---------------------------------------------------------------------------
LIGHTING_PRESETS = {
    "natural": "soft natural daylight, gentle shadows, true-to-life colors",
    "golden": "golden hour warm directional sunlight, long shadows, orange rim light",
    "dramatic": "dramatic chiaroscuro lighting, strong single key light, deep shadows",
    "studio": "three-point studio lighting setup, key fill and rim lights, controlled shadows",
    "neon": "colorful neon light sources, cyan and magenta spill, urban night",
    "volumetric": "volumetric god rays, light beams through atmosphere, dust particles visible",
    "rim": "strong rim backlighting, glowing edges, silhouette definition",
    "ambient": "soft ambient diffused light, overcast, minimal shadows, even illumination",
    "cinematic": "cinematic anamorphic lighting, lens flares, warm-cool contrast",
}


# ===========================================================================
# Core Functions
# ===========================================================================

def detect_subject(prompt):
    """Detect the primary subject category from a prompt."""
    prompt_lower = prompt.lower()
    scores = {}
    for category, keywords in SUBJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in prompt_lower)
        if score > 0:
            scores[category] = score
    if scores:
        return max(scores, key=scores.get)
    return "default"


def detail_enhance(prompt, subject=None):
    """
    Expand a user prompt with subject-appropriate detail dimensions.
    Only adds details the user hasn't already specified.

    'freshly baked bread' becomes:
    'freshly baked bread, glistening surface texture, visible moisture and oils,
     rich appetizing color variations, crispy crunchy flaky textures clearly
     distinguishable, subtle steam rising, professional plating...'
    """
    if subject is None:
        subject = detect_subject(prompt)

    template = DETAIL_TEMPLATES.get(subject, DETAIL_TEMPLATES["default"])
    prompt_lower = prompt.lower()

    # Only add detail dimensions not already mentioned
    additions = []
    for _dimension, detail_text in template.items():
        # Check if any significant word from the detail is already in the prompt
        detail_words = set(re.findall(r'\b[a-z]{4,}\b', detail_text.lower()))
        prompt_words = set(re.findall(r'\b[a-z]{4,}\b', prompt_lower))
        overlap = detail_words & prompt_words
        if len(overlap) < 2:  # add if fewer than 2 words overlap
            additions.append(detail_text)

    if additions:
        return prompt.strip() + ", " + ", ".join(additions)
    return prompt


def build_prompt(base_prompt, filters=None, style=None, quality="standard",
                 composition=None, lighting=None, detail_level="normal"):
    """
    Build a structured, detail-rich generation prompt.

    Args:
        base_prompt: User's core description
        filters: List of filter paths (e.g. ['cinematic/wes-anderson'])
        style: Quick style keyword
        quality: Quality tier — 'draft', 'standard', 'high', 'ultra'
        composition: Camera/composition preset name
        lighting: Lighting preset name
        detail_level: 'minimal', 'normal', 'detailed', 'maximum'
    """
    parts = []

    # --- 0. Detect subject for Korean aesthetic routing ---
    subject = detect_subject(base_prompt)
    apply_korean = (
        subject in KOREAN_AESTHETIC_SUBJECTS
        and (style not in NON_KOREAN_AESTHETIC_STYLES if style else True)
    )

    # --- 1. Subject (with optional detail expansion) ---
    if detail_level in ("detailed", "maximum"):
        enhanced = detail_enhance(base_prompt)
        parts.append(enhanced)
    else:
        parts.append(base_prompt.strip())

    # --- 2. Korean Instagram Aesthetic (auto-applied for photo subjects) ---
    if apply_korean and detail_level != "minimal":
        parts.append(KOREAN_INSTAGRAM_AESTHETIC["color_grading"])
        if detail_level in ("detailed", "maximum"):
            parts.append(KOREAN_INSTAGRAM_AESTHETIC["mood"])
            parts.append(KOREAN_INSTAGRAM_AESTHETIC["editing"])

    # --- 3. Composition / Camera ---
    if composition and composition in COMPOSITION_PRESETS:
        parts.append(COMPOSITION_PRESETS[composition])

    # --- 4. Lighting ---
    if lighting and lighting in LIGHTING_PRESETS:
        parts.append(LIGHTING_PRESETS[lighting])
    elif apply_korean and not lighting:
        # Default Korean Instagram lighting if none specified
        parts.append(KOREAN_INSTAGRAM_AESTHETIC["lighting"])

    # --- 5. Filter modifiers ---
    if filters:
        for fp in filters:
            flt = load_filter(fp)
            if flt and flt.get("prompt_modifier"):
                parts.append(flt["prompt_modifier"].strip())

    # --- 5. Style ---
    quick_styles = {
        "photorealistic": (
            "photorealistic, indistinguishable from a real photograph, "
            "shot on Canon EOS R5 with 85mm f/1.4 GM lens, "
            "natural film grain, accurate lens optics with subtle chromatic aberration, "
            "true optical bokeh with circular highlights, "
            "DSLR RAW photograph, Lightroom color grading, "
            "physically accurate light falloff, real shadow penumbra, "
            "no AI artifacts, no plastic skin, no uncanny smoothness, "
            "genuine photographic imperfections that make it real"
        ),
        "anime": (
            "anime illustration, cel shading, vibrant saturated colors, "
            "clean bold outlines, detailed anime art, studio quality"
        ),
        "pixel-art": (
            "16-bit pixel art, retro game sprite, limited color palette, "
            "crisp individual pixels, nostalgic SNES era"
        ),
        "oil-painting": (
            "oil painting on stretched canvas, visible impasto brushstrokes, "
            "rich color blending, museum gallery masterpiece, classical technique"
        ),
        "flat-design": (
            "flat vector illustration, minimal geometric shapes, "
            "limited pastel color palette, clean modern graphic design"
        ),
        "isometric": (
            "isometric 3D render, 30-degree angle, clean geometric shapes, "
            "bright cheerful colors, game asset style, anti-aliased edges"
        ),
        "watercolor": (
            "watercolor painting on cold-pressed paper, soft bleeding edges, "
            "wet-on-wet technique, transparent color washes, visible paper grain"
        ),
        "cyberpunk": (
            "cyberpunk aesthetic, neon lights reflecting on wet streets, "
            "holographic displays, dark futuristic cityscape, Blade Runner inspired"
        ),
        "pencil-sketch": (
            "detailed pencil drawing on textured paper, graphite shading, "
            "hatching crosshatching, monochrome, fine linework, sketchbook"
        ),
        "3d-render": (
            "octane render, physically based rendering, PBR materials, "
            "ray traced global illumination, studio lighting, 8k resolution"
        ),
        "logo": (
            "minimalist logo design, clean vector art, professional brand identity, "
            "scalable, negative space, iconic symbol, timeless design"
        ),
        "ui-icon": (
            "flat app icon, simple recognizable silhouette, clean edges, "
            "app store ready, consistent stroke width, grid-aligned"
        ),
        "fantasy": (
            "epic fantasy art, dramatic volumetric lighting, detailed armor "
            "and weapons, sweeping composition, concept art, AAA game quality"
        ),
        "ghibli": (
            "Studio Ghibli animation style, hand-painted watercolor backgrounds, "
            "soft warm atmosphere, lush nature, gentle lighting, Miyazaki"
        ),
        "comic-book": (
            "comic book art, bold black ink outlines, halftone dot shading, "
            "dynamic action composition, speech bubble ready, Marvel/DC style"
        ),
        "pop-art": (
            "pop art style, bold primary colors, Ben-Day dot pattern, "
            "Andy Warhol screen print, high contrast graphic, 1960s"
        ),
        "ink-wash": (
            "traditional ink wash painting, sumi-e brush technique, "
            "rice paper texture, black ink gradients, East Asian minimalism, zen"
        ),
        "low-poly": (
            "low poly 3D render, geometric triangular facets, flat shading, "
            "clean pastel colors, modern abstract, crystalline"
        ),
        "cinematic": (
            "cinematic film still, anamorphic lens, 2.39:1 aspect ratio feel, "
            "color graded, depth of field, movie-quality production value"
        ),
        "magazine": (
            "professional magazine photography, editorial quality, "
            "perfect exposure, color-managed, publication-ready, retouched"
        ),
    }
    if style and style in quick_styles:
        parts.append(quick_styles[style])

    # --- 6. Quality tier tags ---
    tier = QUALITY_TIERS.get(quality, QUALITY_TIERS["standard"])
    parts.append(tier["tags"])

    # --- 7. Extra detail-level boosters ---
    if detail_level == "maximum":
        parts.append(
            "extreme attention to micro details, every surface texture rendered, "
            "subsurface scattering on translucent materials, specular highlights "
            "on reflective surfaces, chromatic depth, tack sharp throughout, "
            "pore-level skin detail, fabric thread visibility, "
            "dust motes in light beams, fingerprint smudges on glass, "
            "condensation droplets, real optical lens characteristics, "
            "sensor noise at appropriate ISO, natural vignetting"
        )

    return ", ".join(parts)


def get_quality_tier(quality="standard"):
    """Return the quality tier configuration dict."""
    return QUALITY_TIERS.get(quality, QUALITY_TIERS["standard"])


def get_dimensions(purpose=None):
    """Get width, height for a given purpose."""
    if purpose and purpose in DIMENSIONS:
        return DIMENSIONS[purpose]
    return (1024, 1024)


def list_dimensions():
    """Return all available dimension presets."""
    return DIMENSIONS.copy()


def list_compositions():
    """Return all composition presets."""
    return COMPOSITION_PRESETS.copy()


def list_lighting():
    """Return all lighting presets."""
    return LIGHTING_PRESETS.copy()


def list_quality_tiers():
    """Return all quality tiers."""
    return {k: v["description"] for k, v in QUALITY_TIERS.items()}


# ---------------------------------------------------------------------------
# Filter loading (unchanged)
# ---------------------------------------------------------------------------

def load_filter(filter_path):
    """Load a filter preset by path like 'cinematic/wes-anderson'."""
    parts = filter_path.strip().split("/")
    if len(parts) != 2:
        return None
    category, name = parts
    yaml_path = os.path.join(PRESETS_DIR, f"{category}.yaml")
    if not os.path.exists(yaml_path):
        return None
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for flt in data.get("filters", []):
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
