# Prompt Engineering Guide

## Prompt Structure

A good image generation prompt follows this pattern:

```
[Subject] + [Style/Medium] + [Composition] + [Lighting] + [Color] + [Quality Tags]
```

### Example
```
A medieval knight standing on a cliff (subject)
digital painting, fantasy art (style)
dramatic low angle, rule of thirds (composition)
volumetric lighting, golden hour (lighting)
rich warm tones, deep shadows (color)
masterpiece, highly detailed, 8k (quality)
```

## Quick Tips

### DO
- Be specific about the subject ("a gray tabby cat" not "a cat")
- Specify the medium/style ("oil painting", "photograph", "3D render")
- Describe lighting ("soft diffused light", "dramatic rim lighting")
- Mention camera angle if relevant ("bird's eye view", "close-up portrait")
- Use quality boosters ("masterpiece, best quality, highly detailed")

### DON'T
- Use vague descriptions ("a nice picture")
- Overload with conflicting styles ("realistic anime oil painting photo")
- Write extremely long prompts (diminishing returns after ~75 words)
- Use negative language ("not ugly") — describe what you WANT

## Style Keywords Quick Reference

### Photography Styles
- Portrait, landscape, macro, aerial, street, documentary
- DSLR, 35mm film, medium format, tilt-shift, long exposure

### Art Styles
- Oil painting, watercolor, pencil sketch, charcoal, pastel
- Digital art, concept art, matte painting, vector illustration

### 3D/Technical
- 3D render, octane render, unreal engine, isometric, low poly
- PBR materials, ray tracing, volumetric fog, subsurface scattering

### Mood/Atmosphere
- Dramatic, serene, eerie, whimsical, melancholic, epic
- Cozy, mysterious, ethereal, gritty, elegant

## Model-Specific Tips

### flux (default)
- Handles most prompts well
- Good with detailed descriptions
- Consistent quality

### kontext (editing)
- Give clear, specific editing instructions
- "Change X to Y" works better than vague requests
- Reference specific parts of the image

### gptimage (photorealistic)
- Excels at text rendering in images
- Best for photorealistic scenes
- Good at following complex compositions

### turbo (fast)
- Keep prompts simpler for best results
- Great for rapid iteration
- Use for exploring ideas before final generation
