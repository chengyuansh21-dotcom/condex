#!/usr/bin/env python3
"""Build a conservative architectural rendering edit prompt from a JSON brief."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STYLE_SUMMARIES = {
    "default-presentation": "realistic daylight presentation render with balanced materials, clean shadows, moderate planting, natural people scale, and restrained color grading",
    "premium-commercial": "high-end commercial architecture visualization with refined facade materials, warm storefront lighting, polished paving, active but uncrowded pedestrians, and upscale retail atmosphere",
    "urban-renewal": "believable Chinese urban renewal streetscape with repaired public realm, human-scale street life, restrained greenery, local context, and cleaned-up existing facades",
    "night-commercial": "controlled night commercial visualization with warm interior glow, storefront lighting, evening sky, subtle reflections, balanced contrast, and no excessive neon",
    "residential-entrance": "refined residential arrival scene with warm entry lighting, tactile stone/metal/wood materials, layered planting, calm pedestrian scale, and welcoming atmosphere",
    "interior-retail": "realistic interior commercial visualization with improved material tactility, lighting hierarchy, furniture quality, clean reflections, and believable human scale",
    "landscape-node": "landscape presentation image with richer planting hierarchy, ground texture, sunlight and shadows, benches, subtle activity, and clear view of the design",
    "aerial-masterplan": "aerial masterplan atmosphere render with clear roofs, roads, landscape structure, atmospheric depth, scale-appropriate vehicles and people, and crisp presentation polish",
    "material-only": "material realism pass only, improving texture, glass reflections, contact shadows, edge clarity, and subtle weathering without adding new objects",
    "people-landscape-only": "people and landscape enrichment only, adding realistic pedestrians, planting, street furniture, and scale cues without altering architecture",
}

DEFAULT_RETENTION = [
    "original building massing",
    "camera angle and perspective",
    "facade proportions and window positions",
    "roofline and floor count",
    "road, site, and landscape layout relationships",
    "main interior spatial layout when present",
]

DEFAULT_ENHANCEMENTS = [
    "material realism",
    "lighting and shadow hierarchy",
    "people and activity at believable scale",
    "planting and landscape atmosphere",
    "street or interior props only where appropriate",
    "sky, color grading, clarity, and presentation polish",
]

NEGATIVE = [
    "do not change the architectural design",
    "do not alter massing, perspective, facade rhythm, windows, roofline, roads, or site geometry",
    "no fantasy style, excessive cinematic grading, cyberpunk mood, or dreamy AI look",
    "no unreadable invented signage text",
    "no warped geometry, melted edges, duplicated windows, oversized people, or mismatched local context",
    "do not hide the main building with trees or foreground objects",
]


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def load_brief(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_prompt(brief: dict[str, Any], style: str) -> dict[str, Any]:
    style_text = STYLE_SUMMARIES.get(style, STYLE_SUMMARIES["default-presentation"])
    subject = brief.get("subject", "architectural rendering")
    view = brief.get("view", "same view as the source image")
    user_intent = brief.get("user_intent", brief.get("intent", ""))
    preserve = DEFAULT_RETENTION + listify(brief.get("preserve"))
    enhance = listify(brief.get("enhance")) or DEFAULT_ENHANCEMENTS
    locale = brief.get("locale", "Chinese urban/architectural context when applicable")

    edit_prompt = (
        f"Improve this {subject} into a realistic, presentation-ready architectural visualization. "
        f"Keep the {view}. Strictly preserve {', '.join(preserve)}. "
        f"Enhance only: {', '.join(enhance)}. "
        f"Style direction: {style_text}. "
        f"Use context appropriate to {locale}. "
    )
    if user_intent:
        edit_prompt += f"User design intent to interpret faithfully: {user_intent}. "
    edit_prompt += (
        "The final image should be suitable for architecture report pages, PPT presentations, "
        "urban renewal proposals, investment presentation, or design text layouts."
    )

    return {
        "style": style,
        "edit_prompt": edit_prompt,
        "negative_prompt": "; ".join(NEGATIVE),
        "retention_rules": preserve,
        "enhancement_scope": enhance,
        "explanation_template": {
            "title": "已完成一版优化。",
            "retained": ["原建筑体量", "原相机角度和透视关系", "原道路、场地和主要空间关系", "原立面主要比例和开窗节奏"],
            "optimized": ["材质真实感", "光照和阴影层次", "人物/绿化/配景", "天空和整体色彩氛围", "清晰度和汇报图质感"],
            "next_options": ["更商业", "更高级", "更生活化", "改成夜景", "只调整局部", "输出 4K"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", help="Path to a UTF-8 JSON brief.")
    parser.add_argument("--style", default="default-presentation", choices=sorted(STYLE_SUMMARIES))
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    result = build_prompt(load_brief(args.brief), args.style)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
