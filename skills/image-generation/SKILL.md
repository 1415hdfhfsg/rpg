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

## Korean Instagram Aesthetic (Default Reference)

**All photo-style images automatically use Korean Instagram (한국 인스타 감성) as
the default aesthetic reference.** This is applied automatically — no user action needed.

What gets applied:
- **Color grading**: muted warm tones, soft pastels, lowered contrast, lifted blacks,
  VSCO-style faded film look, subtle pink/peach undertones
- **Mood**: 감성(gamsong) atmosphere, calm/serene, clean minimalist composition,
  effortlessly aesthetic
- **Lighting**: soft diffused natural light, window light or golden hour,
  gentle even illumination, light and airy
- **Editing**: Lightroom-style, warm but not oversaturated skin, creamy whites,
  soft and dreamy processing

When it IS applied (auto):
- Person / portrait photos
- Food / cafe photos
- Landscape / scenery
- Architecture / interior
- Product photos

When it is NOT applied:
- Fantasy, anime, pixel-art, comic-book, cyberpunk, 3D render, etc.
- User explicitly requests a different aesthetic (e.g. "dark moody", "cyberpunk")

## Reality Grounding Protocol (MANDATORY)

**Before writing ANY prompt, Claude MUST verify physical reality.**
Do NOT write "pretty words" — write what a CAMERA would actually capture.

### Step A — Study the Real Subject
Ask yourself: "이 피사체가 실제로 어떻게 생겼는가?"

- **형상**: 실제 물체의 형태, 크기, 비율, 자세를 정확히 묘사
  - ❌ "a hamster on paper bedding" (모호)
  - ✅ "장모 골든햄스터가 완전히 납작하게 엎드려 있다. 몸이 찐빵처럼 퍼져 있고,
       앞발은 앞으로 쭉 뻗거나 얼굴 밑에 접혀 있다. 뒷다리는 뒤로 펴져 있다.
       긴 털이 바닥에 방사형으로 퍼져 종이와 뒤섞인다."
- **재질**: 종이바닥 = 사무용지를 잘게 찢은 흰색 스트립, 일부 구겨짐, 두께 불균일
  - ❌ "paper substrate" (학술 용어)
  - ✅ "shredded strips of white office paper, crumpled and layered unevenly,
       some strips curled, creating a messy nest texture"

### Step B — Verify Light × Material Interaction
Ask yourself: "이 조명이 이 재질에 닿으면 실제로 어떻게 보이는가?"

Real-world light behavior by material:
| Material | Light Interaction |
|----------|------------------|
| 긴 동물 털 (golden fur) | 형광등 → 털 끝에 차가운 흰색 하이라이트, 털 사이 그림자는 따뜻한 금색, 기름기에 따라 약간의 윤기 |
| 찢긴 종이 | 형광등 → 흰색이지만 순백 아님, 약간 누르스름, 접힌 부분에 미세 그림자, 매트한 반사 |
| 유리잔 (iced latte) | 창가 자연광 → 얼음에 하이라이트, 액체 내부 투과광, 결로 물방울에 작은 반사점들 |
| 대리석 테이블 | 자연광 → 표면 무늬가 반투명하게 비침, 광택면에 창문 반사 |
| 벚꽃잎 | 역광 → 반투명하게 빛이 투과, 꽃잎 핏줄 보임, 테두리 밝은 림라이트 |
| 피부 (인물) | 창가광 → subsurface scattering으로 귀/손가락 끝이 약간 붉게 투과 |
| 빵 껍질 | 측광 → 균열 부분 그림자 강조, 광택 부분에 오일 반사, 기공 내부 어둡게 |

### Step C — Use Real Composition Patterns
Ask yourself: "이 장면을 실제로 촬영한다면 카메라를 어디에 두는가?"

Real-world photography patterns:
| Subject | Real Composition |
|---------|-----------------|
| 케이지 속 햄스터 | 위에서 내려다봄 (top-down) 또는 케이지 문 열고 눈높이, 폰 가까이 대고 촬영, 한쪽에 케이지 철망이나 물병 일부 보임 |
| 카페 음식 | 45도 또는 탑뷰, 접시 전체 + 음료 일부, 테이블 가장자리 보임, 냅킨/수저 자연스럽게 |
| 인스타 셀카/인물 | 약간 위에서, 자연광 창가, 3/4 얼굴, 배경에 카페/거리 흐림 |
| 벚꽃 풍경 | 벚꽃 터널 아래에서 앞으로 촬영, 또는 나무 올려보기, 사람 뒷모습 작게 |
| 반려동물 | 눈높이로 낮춰서, 또는 위에서, 폰 셀카 앵글, 약간 흔들릴 수 있는 캐주얼 |
| 제품 | 45도, 깔끔한 배경, 주변에 소품 1-2개 |

### Step D — Self-Check Before Generating
프롬프트 완성 후, 다음을 확인:

1. **형상 테스트**: "이 묘사대로 그리면 실제 피사체와 같은가?"
   - 햄스터 발가락 수? 눈 크기? 귀 모양? 꼬리 길이?
2. **빛 테스트**: "이 조명에서 이 재질이 실제로 이렇게 보이는가?"
   - 형광등 아래 금색 털 = 차가운 하이라이트, 순백이 아닌 약간 푸른끼
3. **구도 테스트**: "실제로 이 상황에서 사람이 카메라를 이 위치에 두는가?"
   - 케이지 안 햄스터를 85mm로 찍지 않음 → 폰 카메라, 광각, 가까이
4. **재질 테스트**: "종이바닥이라고 했는데 실제로 종이가 보이는가?"
   - 찢긴 종이 스트립의 형태, 구김, 두께가 묘사되었는가?

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

### 10. Preview (HTML with PNG Download)
Generate a local HTML page that fetches the image client-side and offers
a PNG download button. Useful when the server environment blocks API access.
```bash
python3 skills/image-generation/scripts/preview.py \
  --prompt "bread on a table" -q ultra -d maximum \
  --composition close-up --lighting golden --style photorealistic \
  --prompt-ko "테이블 위의 빵" \
  --output preview.html --open
```
The HTML page includes: settings card, EN/KO prompt display,
live image preview, PNG download button, regenerate button, copy prompt button.

## Models Available (via Pollinations.ai) — Quality Curated

Low-quality models excluded. All models below produce high-fidelity output.

### Photorealistic / Top Tier
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `gptimage-large` | Best photorealism, text rendering, print-ready | Slow | ★★★★★ |
| `gptimage` | Photorealistic, text in images | Slow | ★★★★★ |

### Creative / Artistic
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `grok-imagine-pro` | Bold creative, few content restrictions | Slow | ★★★★★ |
| `grok-imagine` | Unconventional artistic | Medium | ★★★★ |
| `seedream5` | Latest artistic, rich color | Medium | ★★★★ |
| `seedream-pro` | Premium artistic, concept art | Slow | ★★★★★ |
| `seedream` | Solid artistic, illustrations | Medium | ★★★ |

### Text / Special
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `qwen-image` | Text accuracy, LoRA, layer editing | Medium | ★★★★ |

### All-rounder
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `flux` | Reliable default, good prompt adherence | Medium | ★★★★ |

### Editing / Img2Img
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `kontext` | Instruction-based editing, style transfer | Medium | ★★★★ |
| `nanobanana-pro` | Premium multi-turn editing | Slow | ★★★★ |
| `nanobanana-2` | Improved editing | Medium | ★★★ |
| `nanobanana` | Gemini-based editing | Medium | ★★★ |

### Cinematic / Commercial
| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `wan-image-pro` | Cinematic stills, film frames | Slow | ★★★★ |
| `nova-canvas` | Stable commercial/product photos | Medium | ★★★ |

### Auto-Selection by Quality Tier
| Tier | Generate | Edit | Compose | Artistic |
|------|----------|------|---------|----------|
| draft | flux | kontext | gptimage | seedream |
| standard | flux | kontext | gptimage | seedream5 |
| high | gptimage | nanobanana-2 | gptimage-large | seedream-pro |
| ultra | **gptimage-large** | **nanobanana-pro** | **gptimage-large** | **grok-imagine-pro** |

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

## Situation-Based Model Routing (MANDATORY)

Claude MUST auto-select the optimal model based on what the user is asking for.
The user should never need to know model names — Claude picks the best one.

### Routing Rules

**By content type** — what is being generated:
| User says (예시) | Model | Why |
|-----------------|-------|-----|
| "사진 찍은 것처럼", "실제 사진", "포토", real photo | `gptimage-large` | 실사 최강 |
| "로고 만들어줘", "텍스트 넣어줘", text in image | `gptimage-large` | 텍스트 렌더링 최고 |
| "일러스트", "컨셉아트", "그림", illustration | `seedream-pro` | 예술적 표현 최강 |
| "애니메이션", "만화", anime, cartoon | `seedream5` | 스타일 표현 우수 |
| "독특하게", "창의적으로", "자유롭게", creative | `grok-imagine-pro` | 대담한 해석 |
| "영화 장면", "시네마틱", cinematic still | `wan-image-pro` | 필름 프레임 특화 |
| "제품 사진", "상품", "이커머스", product | `nova-canvas` | 상업 사진 안정적 |
| "타이포그래피", "폰트 디자인", typography | `qwen-image` | 텍스트 정확도 + LoRA |
| general, 기본 | `flux` | 올라운더 |

**By action** — what is being done:
| User says (예시) | Model | Why |
|-----------------|-------|-----|
| "이 사진 수정해줘", "배경 바꿔줘", edit photo | `kontext` | 지시 기반 편집 최강 |
| "필터 적용", "느낌 바꿔줘", apply filter | `kontext` | 스타일 변환 특화 |
| "여러 번 수정", "계속 고쳐", multi-turn edit | `nanobanana-pro` | 멀티턴 편집 |
| "합성해줘", "합쳐줘", compose images | `gptimage-large` | 합성 품질 최고 |
| "배경 제거", remove background | `kontext` | 빠르고 정확 |
| "스타일 변환", style transfer | `kontext` | 자연스러운 변환 |

**By quality request:**
| User says | Quality Tier | Model auto-selected |
|-----------|-------------|-------------------|
| "빨리", "대충", "시안", quick/draft | draft | flux |
| (기본, 별말 없음) | standard | flux |
| "고화질", "잘 만들어줘", high quality | high | gptimage |
| "최고 화질", "인쇄용", "완벽하게", maximum | ultra | gptimage-large |

### Model Switch Mid-Conversation

When the user is unsatisfied with results, Claude should proactively suggest:
- "실사 느낌이 부족하다면 → gptimage-large로 바꿔볼까요?"
- "더 예술적인 느낌을 원하시면 → grok-imagine-pro가 적합합니다"
- "텍스트가 깨진다면 → qwen-image가 텍스트 렌더링에 특화되어 있습니다"

### Example Flow
```
사용자: 영화 포스터 만들어줘. 제목은 "THE LAST KNIGHT"

Claude 판단:
  - 영화 포스터 → 시네마틱 → wan-image-pro? 
  - 하지만 "THE LAST KNIGHT" 텍스트 포함 → gptimage-large가 텍스트 정확
  - 결론: gptimage-large (텍스트 > 시네마틱 우선)
  - composition: portrait (포스터는 세로)
  - lighting: dramatic
```

## Auto-Routing Summary

When a user makes a request, Claude should:

1. **Detect intent** — generate / edit / filter / compose / analyze
2. **Detect content type** — photo / illustration / cinematic / product / text
3. **Choose model** — using routing rules above (user never needs to know model names)
4. **Apply presets** — auto-match style/filter/composition/lighting from context
5. **Set dimensions** — match purpose (SNS, print, game icon, etc.)
6. **Preview prompt** — ALWAYS show the prompt card first (with model choice reason)
7. **Wait for approval** — never generate without user confirmation
8. **Execute script** — run the approved command
9. **Verify output** — read the generated image and check quality
10. **Suggest alternatives** — if result is unsatisfying, recommend a different model

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
