# Available Models

## Image Generation Models (via Pollinations.ai)

| Model | Type | Best For | Speed | Quality | Notes |
|-------|------|----------|-------|---------|-------|
| `flux` | Text→Image | General purpose, default | Medium | High | Best all-rounder |
| `turbo` | Text→Image | Fast drafts, iteration | Fast | Medium | Good for prototyping |
| `gptimage` | Text→Image + Img2Img | Photorealistic, text rendering | Slow | Very High | Best for text in images |
| `kontext` | Img2Img + Edit | Image editing, style transfer | Medium | High | Best for edits (FLUX.1 Kontext) |
| `seedream` | Text→Image | Creative, artistic | Medium | High | ByteDance Seedream |
| `seedream-pro` | Text→Image | Premium artistic | Slow | Very High | Premium tier |
| `nanobanana` | Text→Image + Img2Img + Edit | Multi-turn editing | Medium | High | Gemini 2.5 Flash Image |
| `nanobanana-pro` | Text→Image + Img2Img + Edit | Premium editing | Slow | Very High | Premium tier |
| `zimage` | Text→Image | Alternative generation | Medium | High | Alternative pipeline |

## Model Selection Guide

### By Task
- **Generate from text** → `flux` (default) or `seedream` (artistic)
- **Edit existing photo** → `kontext` (instruction-based) or `nanobanana` (multi-turn)
- **Text in image** → `gptimage` (best at rendering text)
- **Quick draft** → `turbo`
- **Photorealistic** → `gptimage`
- **Style transfer** → `kontext`
- **Filter application** → `kontext`

### By Speed Priority
1. `turbo` — Fastest
2. `flux` / `kontext` / `nanobanana` — Medium
3. `gptimage` / `seedream-pro` / `nanobanana-pro` — Slowest but highest quality

### Image-to-Image Capable
Only these models accept an input image:
- `kontext` — Best for edits
- `nanobanana` — Best for multi-step edits
- `nanobanana-pro` — Premium editing
- `gptimage` — Composition and photorealistic edits

## 3D Generation (via Tripo3D API)

| Feature | Detail |
|---------|--------|
| Input | Single 2D image |
| Output | GLB, FBX, OBJ, STL |
| Speed | 30-120 seconds |
| Free tier | 300 credits/month |
| API key | Required (TRIPO_API_KEY) |

## Rate Limits (Pollinations.ai)

| Tier | Rate | Auth |
|------|------|------|
| Anonymous | 1 req / 15s | None |
| Seed (free) | 1 req / 5s | Token |
| Flower (paid) | 1 req / 3s | Token |
| Nectar (enterprise) | Unlimited | Token |
