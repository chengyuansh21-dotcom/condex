---
name: archrender-optimizer
description: "Architectural rendering optimization workflow for uploaded effect images, conceptual renders, SketchUp/D5/Enscape/Lumion exports, interiors, streetscapes, landscapes, aerial views, and presentation images. Use when Codex/condx needs to analyze an architectural rendering, ask targeted design-direction questions, build a professional gpt-image-2 edit prompt, call the built-in image editing/generation capability, upscale to presentation/4K quality, and explain the result for Chinese or bilingual users."
---

# ArchRender Optimizer

Use this skill to turn an architectural effect image into a presentation-ready render while preserving the original design. Treat the work like an architectural visualization director: diagnose first, clarify intent, make controlled edits, and explain what changed.

## Core Rule

Preserve the project design before improving the image. Do not casually change massing, camera angle, facade rhythm, window positions, roofline, site geometry, road relationships, storefront layout, or interior spatial structure.

Default edits are limited to:

- material realism
- lighting and shadows
- people and activity
- planting and landscape atmosphere
- street/commercial props
- sky and weather mood
- color grading, clarity, and presentation polish

## Quick Workflow

1. Inspect the input image and identify image type, view type, likely source, strengths, and weak points.
2. Ask 3-5 concise questions only when the user's goal, style, edit scope, or preservation constraints are unclear.
3. Choose or adapt a style preset from `references/style_presets.md`.
4. Build an English image-edit prompt with strict preservation constraints.
5. Run image editing through Codex/condx's built-in image editing capability using `gpt-image-2` when model selection is available.
6. Upscale or post-process for report/PPT use when requested.
7. Return the optimized image plus a short Chinese explanation: retained content, optimized content, and next adjustment options.

## Analysis Checklist

For every uploaded image, explicitly reason through:

- **Subject**: commercial street, residential entrance, office facade, city renewal block, interior retail, landscape node, aerial masterplan, or other.
- **View**: street-level, eye-level facade, interior perspective, aerial, bird's-eye, night view, detail node.
- **Quality issues**: flat materials, weak shadows, empty foreground, poor vegetation, low-resolution edges, overexposed sky, dull color, scale mismatch, weak storefront detail.
- **Design risks**: fragile facade grid, signage text, existing context, important trees, road alignment, site boundary, interior circulation.
- **Edit scope**: full-scene enhancement, material-only, people/landscape-only, night conversion, commercial upgrade, 4K/post-processing only.

## Clarifying Questions

Ask only the minimum needed. Prefer checkboxes or short questions in Chinese.

Useful questions:

- 这张图用于什么场景：方案汇报、招商展示、文本排版、竞赛、社媒展示？
- 想要哪种方向：默认汇报级、高端商业、城市更新、夜景商业、住宅入口、室内商业、景观节点、鸟瞰总平？
- 哪些内容必须严格保留：体量、立面、窗户、材质、道路、树木、招牌、室内布局？
- 本次只做整体优化，还是只优化材质/灯光/人物绿化/天空/清晰度？
- 是否需要 4K 输出或适合 PPT 的横向/竖向比例？

If the user says "直接优化" or gives enough context, proceed with a conservative default preset.

## Prompt Builder

Use `scripts/build_archrender_prompt.py` for repeatable prompt generation from a JSON brief:

```bash
python scripts/build_archrender_prompt.py --brief brief.json --style premium-commercial
```

The script returns JSON containing:

- `edit_prompt`: English prompt for an image-edit model
- `negative_prompt`: items to avoid
- `retention_rules`: non-negotiable preservation constraints
- `explanation_template`: Chinese output skeleton

For hand-written prompts, use this structure:

```text
Improve this architectural rendering into a realistic, presentation-ready visualization.
Strictly preserve the original building massing, camera angle, perspective, facade proportions,
window positions, road/site relationships, and main spatial layout.

Enhance only: [materials, lighting, shadows, people, planting, street props, sky, atmosphere, clarity].
Style direction: [selected preset].
User intent: [translated Chinese intent].
Avoid: distorted geometry, changed facade design, unreadable text, fantasy style, excessive cinematic grading,
oversized people, mismatched local context, unrealistic vegetation, AI artifacts.
```

## Condx Image Editing Guidance

This skill is for direct use inside Codex/condx. Do not design a separate service layer, backend integration, or external calling flow.

- Use `gpt-image-2` for the actual rendering/editing pass when the tool exposes model choice.
- Prefer a single controlled edit pass first; generate variants only if the user asks.
- Use the uploaded image as the source image. Preserve the source composition and architecture.
- Translate Chinese design intent into an English edit prompt before image generation.
- Keep prompt JSON, selected style preset, and output explanation together in the conversation or project artifacts when useful for iteration.
- If the tool does not expose a model selector, still follow the `gpt-image-2` prompt discipline and use the available built-in image editing/generation call.

## Upscaling

Use `scripts/upscale_image.py` for a deterministic local fallback when no dedicated super-resolution service is available:

```bash
python scripts/upscale_image.py input.png output_4k.png --long-edge 4096
```

This is a presentation polish step, not a substitute for true render quality. For heavier production-grade enhancement, prefer a stronger local or tool-provided upscaler such as Real-ESRGAN or SwinIR when available.

## Output Format

After each generation, answer in Chinese:

```text
已完成一版优化。

保留内容：
- 原建筑体量；
- 原相机角度和透视关系；
- 原道路、场地和主要空间关系；
- 原立面主要比例和开窗节奏。

优化内容：
- ...

下一步可以继续选择：
1. 更商业；
2. 更高级；
3. 更生活化；
4. 改成夜景；
5. 只调整局部；
6. 输出 4K。
```

## References

- `references/style_presets.md`: built-in architectural visualization styles.
- `references/qa_checklist.md`: acceptance checklist, common failure modes, and MVP scope.
- `examples/`: sample briefs and Chinese condx request templates for quick testing.
