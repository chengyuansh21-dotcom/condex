# QA Checklist

## Functional Acceptance

The Codex/condx workflow should support:

- uploaded architectural images
- automatic image diagnosis
- 3-5 clarifying questions when needed
- professional Chinese optimization suggestions
- English image-edit prompt generation
- image edit call through Codex/condx using `gpt-image-2` when available
- optimized image output
- Chinese explanation after generation
- 4K or long-edge upscale output
- at least six built-in style presets
- Chinese user input and bilingual prompt handling

## Visual Acceptance

The optimized image should satisfy:

- original architectural subject remains recognizable
- massing, perspective, facade proportions, openings, roads, and site relations are basically unchanged
- materials look more realistic
- lighting has clearer hierarchy
- people and vegetation have believable scale
- image is cleaner and sharper for PPT/report use
- no obvious AI distortion, melted edges, impossible reflections, or incoherent signage

## Common Failure Modes

Actively avoid:

- changed facade design or extra floors
- shifted windows, roofline, road alignment, or site boundary
- warped perspective or melted building edges
- unreadable or invented signage text
- trees blocking the architectural subject
- oversized people, cars, lamps, or furniture
- over-cinematic, fantasy, cyberpunk, or dreamlike atmosphere unless explicitly requested
- materials that do not match the building type
- mixed lighting directions
- streetscape elements that conflict with Chinese urban context

## MVP Scope

Implement first:

- single-image upload or attached image input
- image analysis
- question flow
- style selection
- prompt builder
- built-in `gpt-image-2` image edit/render call
- 4K upscale/post-process
- result explanation
- simple iterative revision input

Defer to V2:

- manual region masking
- before/after slider
- side-by-side variants
- project style prompt library
- batch rendering
- reference image upload
- persistent version history

Defer to V3:

- SketchUp/Rhino/Revit export plugins
- D5/Enscape workflow plugins
- team collaboration canvas
- client annotation
- automated presentation deck generation
- video walkthrough style consistency

## Test Matrix

Use these image categories:

- SketchUp white model commercial street
- D5 early residential entrance render
- Enscape office building daylight render
- Lumion landscape node
- interior retail space
- city renewal street block
- night commercial street
- aerial masterplan atmosphere image

Run each through:

- default presentation
- premium commercial
- urban renewal
- night commercial
- material-only
- people-landscape-only
- 4K upscale
