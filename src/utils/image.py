"""Image helpers for fixture-oriented evaluation and smoke runs."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


def resolve_image_path(path: str) -> str:
    return str(Path(path))


def load_image_for_vlm(path: str):
    """Load raster images directly and render simple SVG fixtures lazily via Pillow."""

    image_path = Path(path)
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for real-model image loading. Install requirements-gpu.txt first."
        ) from exc

    if image_path.suffix.lower() != ".svg":
        return Image.open(image_path).convert("RGB")

    root = ET.fromstring(image_path.read_text(encoding="utf-8"))
    width = _extract_svg_dimension(root.attrib.get("width"), fallback=640)
    height = _extract_svg_dimension(root.attrib.get("height"), fallback=400)
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    for node in root.findall(".//svg:text", namespace):
        x = int(float(node.attrib.get("x", "0")))
        y = int(float(node.attrib.get("y", "0")))
        text = "".join(node.itertext()).strip()
        if text:
            draw.text((x, y), text, fill="black")
    return image


def _extract_svg_dimension(raw_value: str | None, fallback: int) -> int:
    if not raw_value:
        return fallback
    match = re.search(r"\d+", raw_value)
    return int(match.group(0)) if match else fallback
