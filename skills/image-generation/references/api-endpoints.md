# API Endpoints Reference

## Pollinations.ai (Primary — No Auth Required)

### Image Generation
```
GET https://image.pollinations.ai/prompt/{prompt}
```

Parameters (query string):
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `flux` | Generation model |
| `width` | int | 1024 | Width in pixels |
| `height` | int | 1024 | Height in pixels |
| `seed` | int | random | Reproducibility seed |
| `nologo` | bool | false | Remove watermark |
| `enhance` | bool | false | AI prompt enhancement |
| `safe` | bool | false | NSFW filter |
| `image` | string | — | Input image URL (for img2img with kontext/nanobanana) |

### List Models
```
GET https://image.pollinations.ai/models
```

### Example URLs
```
# Text to image
https://image.pollinations.ai/prompt/a%20red%20dragon?model=flux&width=1024&height=1024

# Image to image (edit)
https://image.pollinations.ai/prompt/make%20it%20sunset?model=kontext&image=https://example.com/photo.jpg
```

## Tripo3D (3D Generation — API Key Required)

Base: `https://api.tripo3d.ai/v2/openapi`

### Upload Image
```
POST /upload
Content-Type: multipart/form-data
Authorization: Bearer {TRIPO_API_KEY}
```

### Create Task
```
POST /task
Content-Type: application/json
Authorization: Bearer {TRIPO_API_KEY}

{
  "type": "image_to_model",
  "file": {"type": "image_token", "image_token": "..."},
  "output_format": "glb"
}
```

### Poll Task Status
```
GET /task/{task_id}
Authorization: Bearer {TRIPO_API_KEY}
```

Response statuses: `queued` → `running` → `success` / `failed`
