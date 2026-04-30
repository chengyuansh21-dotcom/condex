#!/usr/bin/env python3
"""Upscale and lightly polish an image for PPT/report use with Pillow."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


def fit_size(width: int, height: int, long_edge: int) -> tuple[int, int]:
    current_long = max(width, height)
    if current_long >= long_edge:
        return width, height
    scale = long_edge / current_long
    return round(width * scale), round(height * scale)


def upscale(input_path: Path, output_path: Path, long_edge: int, sharpen: float, contrast: float) -> None:
    image = Image.open(input_path).convert("RGB")
    target_size = fit_size(image.width, image.height, long_edge)
    if target_size != image.size:
        image = image.resize(target_size, Image.Resampling.LANCZOS)

    if contrast != 1:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if sharpen > 0:
        image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=int(120 * sharpen), threshold=3))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, quality=95, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--long-edge", type=int, default=4096)
    parser.add_argument("--sharpen", type=float, default=1.0)
    parser.add_argument("--contrast", type=float, default=1.03)
    args = parser.parse_args()

    upscale(args.input, args.output, args.long_edge, args.sharpen, args.contrast)


if __name__ == "__main__":
    main()
