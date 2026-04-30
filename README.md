# ArchRender Optimizer

`archrender-optimizer` is a Codex/condx skill for improving architectural renderings with `gpt-image-2`. It helps analyze uploaded renderings, clarify the intended visualization direction, build a conservative image-edit prompt, run the built-in image editing workflow, and explain the result in Chinese.

The core principle is simple: improve the image without changing the design.

## What It Does

- Analyzes architectural effect images, SketchUp/D5/Enscape/Lumion exports, interiors, streetscapes, landscape nodes, and aerial views.
- Builds professional English prompts for `gpt-image-2` while preserving Chinese design intent.
- Keeps building massing, camera angle, perspective, facade proportions, window positions, site relationships, and interior layout stable.
- Improves only controlled visual layers: materials, lighting, shadows, people, planting, street props, sky, atmosphere, clarity, and presentation polish.
- Provides Chinese output notes covering retained content, optimized content, and next adjustment options.
- Includes JSON example briefs and a local upscale helper for PPT/report output.

## Recommended Condx Prompt

```text
使用 $archrender-optimizer 优化这张建筑效果图。请保留原建筑体量、相机角度、立面比例、道路和场地关系，只增强材质、灯光、人物、绿化、天空和清晰度。使用 gpt-image-2 生成一版汇报级效果图，并说明保留内容、优化内容和下一步可调整方向。
```

More request templates are available in `examples/condx-request-templates.md`.

## Directory Structure

```text
archrender-optimizer/
  SKILL.md
  README.md
  agents/
    openai.yaml
  examples/
    brief-premium-commercial.json
    brief-urban-renewal.json
    brief-night-commercial.json
    brief-interior-retail.json
    condx-request-templates.md
  references/
    style_presets.md
    qa_checklist.md
  scripts/
    build_archrender_prompt.py
    upscale_image.py
```

## Style Presets

Built-in directions include:

- default presentation
- premium commercial
- urban renewal
- night commercial
- residential entrance
- interior retail
- landscape node
- aerial masterplan
- material only
- people and landscape only

See `references/style_presets.md` for the full preset language.

## Prompt Builder Example

```bash
python scripts/build_archrender_prompt.py --brief examples/brief-premium-commercial.json --style premium-commercial --pretty
```

This outputs:

- `edit_prompt`: English prompt for the image edit
- `negative_prompt`: failure modes to avoid
- `retention_rules`: non-negotiable preservation rules
- `enhancement_scope`: visual layers to improve
- `explanation_template`: Chinese result summary structure

## Upscale Helper

```bash
python scripts/upscale_image.py input.png output_4k.png --long-edge 4096
```

This is a lightweight Pillow-based fallback for presentation polish. It is not a replacement for a dedicated super-resolution workflow.

## Quality Standard

The optimized image should:

- keep the original architectural subject recognizable
- preserve massing, perspective, facade proportions, openings, roads, and site relationships
- improve material realism and light hierarchy
- keep people, cars, furniture, trees, and signage at believable scale
- avoid obvious AI artifacts, warped geometry, changed facade design, unreadable signage, or over-stylized atmosphere

## Installation

Place this folder under your Codex skills directory:

```text
~/.codex/skills/archrender-optimizer
```

Then invoke it in Codex/condx with:

```text
$archrender-optimizer
```
