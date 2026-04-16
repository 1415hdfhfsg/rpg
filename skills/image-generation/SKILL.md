---
name: image-generation
description: >
  Generate, edit, compose, and transform images using AI.
  Use when the user asks to: create/generate images, edit/retouch photos,
  apply filters or style transfer, compose multiple images, create variations,
  remove backgrounds, convert 2D to 3D, or analyze images.
  Covers all domains: game assets, design, social media, product photos,
  illustrations, portraits, and more.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# Image Generation Skill

Multi-purpose AI image generation, editing, and transformation skill.
Uses free APIs (primarily Pollinations.ai) — no API key required for core features.

## Available Commands

All scripts are in `skills/image-generation/scripts/`.

### 1. Generate (Text → Image)
```bash
python3 skills/image-generation/scripts/generate.py \
  --prompt "a fantasy castle at sunset" \
  --style fantasy \
  --model flux \
  --width 1024 --height 1024 \
  --output output.png
```

### 2. Edit (Image + Instruction → Image)
```bash
python3 skills/image-generation/scripts/edit.py \
  --input photo.jpg \
  --instruction "change the background to a beach at sunset" \
  --model kontext \
  --output edited.png
```

### 3. Apply Filter (Image + Filter Preset → Image)
```bash
python3 skills/image-generation/scripts/apply_filter.py \
  --input photo.jpg \
  --filter cinematic/wes-anderson \
  --output filtered.png
```

Multiple filters at once:
```bash
python3 skills/image-generation/scripts/apply_filter.py \
  --input photo.jpg \
  --filter mood/dreamy,weather/autumn \
  --output filtered.png
```

### 4. Compose (Multiple Images → One)
```bash
python3 skills/image-generation/scripts/compose.py \
  --images "person.png,background.jpg" \
  --instruction "place the person in front of the background naturally" \
  --output composed.png
```

### 5. Variations (One Image → Multiple Styles)
```bash
python3 skills/image-generation/scripts/variations.py \
  --input photo.jpg \
  --count 5 \
  --output-dir variations/
```

### 6. Style Transfer
```bash
python3 skills/image-generation/scripts/style_transfer.py \
  --input photo.jpg \
  --style anime \
  --output styled.png
```

### 7. Remove Background
```bash
python3 skills/image-generation/scripts/remove_bg.py \
  --input product.jpg \
  --output product_nobg.png
```

### 8. 2D → 3D (requires Tripo API key)
```bash
python3 skills/image-generation/scripts/to_3d.py \
  --input character.png \
  --format glb \
  --output model.glb
```

### 9. Analyze (Image → Description/Prompt)
```bash
python3 skills/image-generation/scripts/analyze.py \
  --input artwork.jpg
```

## Models Available (via Pollinations.ai)

| Model | Best For | Speed |
|-------|----------|-------|
| `flux` | General purpose, high quality (default) | Medium |
| `turbo` | Fast drafts, iteration | Fast |
| `gptimage` | Photorealistic, text in images | Slow |
| `kontext` | Image editing, img2img | Medium |
| `seedream` | Creative, artistic | Medium |
| `seedream-pro` | Premium artistic | Slow |
| `nanobanana` | Editing, multi-turn | Medium |
| `nanobanana-pro` | Premium editing | Slow |

## Filter Presets

88 filters across 10 categories in `presets/photo-filters/`:

| Category | File | Count |
|----------|------|-------|
| Mood | `mood.yaml` | 10 |
| Era | `era.yaml` | 8 |
| Cinematic | `cinematic.yaml` | 10 |
| Color Grade | `color-grade.yaml` | 12 |
| Lighting | `lighting.yaml` | 8 |
| Weather | `weather.yaml` | 8 |
| Artistic | `artistic.yaml` | 12 |
| Portrait | `portrait.yaml` | 8 |
| Commercial | `commercial.yaml` | 6 |
| Purpose | `purpose.yaml` | 6 |

## Auto-Routing

When a user makes a request, Claude should:

1. **Detect intent** — generate / edit / filter / compose / analyze
2. **Choose model** — based on task (see model table above)
3. **Apply presets** — auto-match style/filter from context
4. **Set dimensions** — match purpose (SNS, print, game icon, etc.)
5. **Execute script** — run the appropriate command
6. **Verify output** — read the generated image and check quality

## Dimension Presets

| Purpose | Size | Ratio |
|---------|------|-------|
| Instagram Feed | 1024x1024 | 1:1 |
| Instagram Story | 1080x1920 | 9:16 |
| YouTube Thumbnail | 1280x720 | 16:9 |
| Twitter/X Banner | 1500x500 | 3:1 |
| Desktop Wallpaper | 1920x1080 | 16:9 |
| Mobile Wallpaper | 1080x1920 | 9:16 |
| Game Icon | 512x512 | 1:1 |
| Game Character | 768x1024 | 3:4 |
| A4 Print | 2480x3508 | ~1:1.4 |
| Business Card | 1050x600 | ~16:9 |

## Environment Variables (Optional)

```bash
export TRIPO_API_KEY="..."        # For 3D generation
export POLLINATIONS_TOKEN="..."   # For higher rate limits
```
