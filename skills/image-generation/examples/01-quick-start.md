# Quick Start Examples

## Basic Image Generation

```bash
# Simple text-to-image
python3 skills/image-generation/scripts/generate.py \
  --prompt "a cozy coffee shop interior, warm lighting" \
  --output coffee_shop.png

# With style preset
python3 skills/image-generation/scripts/generate.py \
  --prompt "a mountain landscape" \
  --style watercolor \
  --output mountain.png

# For Instagram (auto-sized 1024x1024)
python3 skills/image-generation/scripts/generate.py \
  --prompt "aesthetic breakfast flat lay" \
  --purpose instagram-feed \
  --output breakfast.png

# YouTube thumbnail (auto-sized 1280x720)
python3 skills/image-generation/scripts/generate.py \
  --prompt "shocked face looking at giant robot" \
  --purpose youtube-thumbnail \
  --model gptimage \
  --output thumbnail.png
```

## Photo Editing

```bash
# Change background
python3 skills/image-generation/scripts/edit.py \
  --input my_photo.jpg \
  --instruction "replace background with a tropical beach sunset" \
  --output beach_photo.png

# Style modification
python3 skills/image-generation/scripts/edit.py \
  --input portrait.jpg \
  --instruction "add professional studio lighting, blur background" \
  --output pro_portrait.png
```

## Filter Application

```bash
# Single filter
python3 skills/image-generation/scripts/apply_filter.py \
  --input photo.jpg \
  --filter cinematic/wes-anderson \
  --output wes.png

# Combined filters
python3 skills/image-generation/scripts/apply_filter.py \
  --input photo.jpg \
  --filter mood/dreamy,lighting/golden-hour \
  --output dreamy_golden.png

# List all available filters
python3 skills/image-generation/scripts/apply_filter.py --list
```

## Style Transfer

```bash
# Photo to anime
python3 skills/image-generation/scripts/style_transfer.py \
  --input photo.jpg --style anime --output anime.png

# Photo to oil painting
python3 skills/image-generation/scripts/style_transfer.py \
  --input landscape.jpg --style oil-painting --output painting.png

# List all styles
python3 skills/image-generation/scripts/style_transfer.py --list
```

## Multiple Variations

```bash
# Auto-select 5 different styles
python3 skills/image-generation/scripts/variations.py \
  --input photo.jpg --count 5 --output-dir my_variations/

# Specific styles
python3 skills/image-generation/scripts/variations.py \
  --input photo.jpg \
  --styles "cinematic/noir,artistic/anime,era/polaroid-70s" \
  --output-dir my_variations/
```

## Background Removal

```bash
# Remove to white
python3 skills/image-generation/scripts/remove_bg.py \
  --input product.jpg --bg white --output product_clean.png

# Replace with custom scene
python3 skills/image-generation/scripts/remove_bg.py \
  --input person.jpg --bg "a futuristic city skyline" --output cyber.png
```
