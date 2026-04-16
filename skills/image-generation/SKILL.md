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

### 1. Generate (Text → Image) — with Quality & Detail Control
```bash
# Quick draft (512px, fast)
python3 skills/image-generation/scripts/generate.py \
  --prompt "a fantasy castle" -q draft --output draft.png

# Standard (1024px, default)
python3 skills/image-generation/scripts/generate.py \
  --prompt "a fantasy castle at sunset" --output castle.png

# High quality with auto detail expansion (1280px)
python3 skills/image-generation/scripts/generate.py \
  --prompt "a fantasy castle at sunset" -q high --output castle_hq.png

# Ultra quality, maximum detail, composition + lighting control (1440px)
python3 skills/image-generation/scripts/generate.py \
  --prompt "freshly baked bread on a rustic wooden table" \
  -q ultra -d maximum --composition close-up --lighting golden \
  --output bread_ultra.png
```

**Quality tiers**: draft → standard → high → ultra
**Detail levels**: minimal → normal → detailed → maximum
Higher tiers auto-select better models, larger sizes, and richer prompts.

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

## Prompt Preview Workflow (MANDATORY)

**IMPORTANT: Claude MUST always preview the prompt before generating.**

When a user requests ANY image generation, editing, or transformation,
follow this exact workflow:

### Step 1 — Analyze & Build Prompt
1. Detect intent (generate / edit / filter / compose / style transfer)
2. Detect subject category (food, person, landscape, fantasy, etc.)
3. Choose quality tier, model, dimensions, composition, lighting
4. Run `generate.py --show-prompt` to build the final prompt

### Step 2 — Present Prompt Card to User
Show the user a structured preview card with BOTH English prompt AND
Korean translation. The Korean version helps the user understand exactly
what will be generated and request precise modifications.

```
========== Image Generation Plan ==========
Subject:      food (자동 감지)
Quality:      ultra
Detail:       maximum
Model:        gptimage
Size:         1440x1440
Composition:  close-up
Lighting:     golden
Style:        photorealistic
Filter:       —

--- Prompt (EN) ---
freshly baked bread, glistening surface texture, visible moisture
and oils, rich appetizing color variations, natural color gradients,
crispy crunchy flaky moist textures clearly distinguishable, ...

--- Prompt (KO) ---
갓 구운 빵, 반짝이는 표면 질감, 수분과 기름기가 보이는,
풍부하고 식욕을 자극하는 색상 변화, 자연스러운 색상 그라데이션,
바삭하고 촉촉한 질감이 뚜렷하게 구분되는, ...

--- Command ---
python3 skills/image-generation/scripts/generate.py \
  --prompt "freshly baked bread" -q ultra -d maximum \
  --composition close-up --lighting golden \
  --style photorealistic --output bread_ultra.png
================================================
```

**Korean translation rules:**
- Translate the FULL expanded prompt, not just the user's original input
- Translate segment by segment so the user can see which detail maps to which
- Use natural Korean, not machine-translated awkward phrasing
- Mark auto-added details with (자동) so the user knows what was expanded
- If the user's original request was in Korean, show the original Korean
  first, then the English prompt that will actually be sent to the API

### Step 3 — Ask for Approval
Ask the user:
- "이대로 생성할까요?" (Proceed as-is?)
- Or suggest alternatives: "구도를 overhead로 바꾸면 음식 사진에 더 적합할 수 있습니다"

### Step 4 — User Response Handling
- **승인** ("응", "ㅇ", "좋아", "진행", "ok", "yes") → Execute the command
- **수정 요청** ("프롬프트에 X 추가해줘", "모델 바꿔줘") → Rebuild and show again
- **거부** ("아니", "취소") → Stop, ask what to change

### Step 5 — Generate & Verify
1. Execute the approved command
2. Read the generated image file to verify output
3. Show the result to the user

## Smart Suggestions

When building the preview card, Claude should proactively suggest:
- **Composition**: "음식 사진은 overhead(탑뷰)가 인스타 느낌, close-up이 맛집 느낌입니다"
- **Lighting**: "인물 사진에는 studio나 rim 조명이 잘 어울립니다"
- **Model**: "텍스트가 포함된 이미지는 gptimage가 가장 정확합니다"
- **Filter**: "이 사진에 cinematic/wes-anderson 필터를 추천합니다"
- **Quality**: "빠른 확인용이면 draft, 최종본이면 ultra를 추천합니다"

## Auto-Routing

When a user makes a request, Claude should:

1. **Detect intent** — generate / edit / filter / compose / analyze
2. **Choose model** — based on task (see model table above)
3. **Apply presets** — auto-match style/filter from context
4. **Set dimensions** — match purpose (SNS, print, game icon, etc.)
5. **Preview prompt** — ALWAYS show the prompt card first (Step 2 above)
6. **Wait for approval** — never generate without user confirmation
7. **Execute script** — run the approved command
8. **Verify output** — read the generated image and check quality

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
