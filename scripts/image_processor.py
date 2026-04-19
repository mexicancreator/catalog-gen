#!/usr/bin/env python3
"""
Escanea una carpeta de imágenes, localiza el logo (logo.*) y normaliza
fotos de producto para maquetación HTML consistente. Genera manifest.json.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps

LOGO_NAMES = {"logo.png", "logo.jpg", "logo.jpeg", "logo.svg"}
RASTER_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
# SVG se copia tal cual (WeasyPrint lo renderiza en HTML).
ALL_IMAGE_EXT = RASTER_EXT | {".svg"}

PRODUCT_MAX_SIDE = 900
LOGO_MAX_HEIGHT = 120
PRODUCT_CANVAS = (4, 3)  # ratio ancho:alto


def _is_logo(path: Path) -> bool:
    return path.name.lower() in LOGO_NAMES


def _iter_images(folder: Path) -> Iterable[Path]:
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in ALL_IMAGE_EXT:
            yield p


def _title_from_stem(stem: str) -> str:
    s = re.sub(r"[_\-]+", " ", stem)
    s = re.sub(r"\s+", " ", s).strip()
    return s.title() if s else "Producto"


def _fit_ratio(img: Image.Image, ratio_w: int, ratio_h: int) -> Image.Image:
    """Escala y recorta al centro al ratio dado (ancho:alto)."""
    tw, th = img.size
    target_ratio = ratio_w / ratio_h
    current_ratio = tw / th
    if current_ratio > target_ratio:
        # Demasiado ancho → recortar lados
        new_w = int(th * target_ratio)
        left = (tw - new_w) // 2
        img = img.crop((left, 0, left + new_w, th))
    elif current_ratio < target_ratio:
        # Demasiado alto → recortar arriba/abajo
        new_h = int(tw / target_ratio)
        top = (th - new_h) // 2
        img = img.crop((0, top, tw, top + new_h))
    return img


def _normalize_raster(src: Path, dst: Path, max_side: int, ratio: tuple[int, int]) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        im = _fit_ratio(im, ratio[0], ratio[1])
        im.thumbnail((max_side, int(max_side * ratio[1] / ratio[0])), Image.Resampling.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, format="JPEG", quality=88, optimize=True)


def process(input_dir: Path, output_dir: Path) -> dict:
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()
    if not input_dir.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_dir}")

    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    logo_src: Path | None = None
    product_sources: list[Path] = []

    for path in _iter_images(input_dir):
        if _is_logo(path):
            if logo_src is not None:
                raise ValueError(
                    f"Varios logos candidatos: {logo_src.name} y {path.name}. "
                    "Debe haber solo un logo.png|jpg|jpeg|svg."
                )
            logo_src = path
        else:
            product_sources.append(path)

    if logo_src is None:
        raise FileNotFoundError(
            "Logo obligatorio no encontrado. El usuario debe nombrar el archivo "
            "como logo.png, logo.jpg, logo.jpeg o logo.svg en la carpeta indicada."
        )

    # Logo de salida
    logo_ext = logo_src.suffix.lower()
    logo_rel = f"assets/logo{logo_ext}"
    logo_dst = output_dir / logo_rel
    logo_dst.parent.mkdir(parents=True, exist_ok=True)

    if logo_ext == ".svg":
        shutil.copy2(logo_src, logo_dst)
    else:
        with Image.open(logo_src) as lim:
            lim = ImageOps.exif_transpose(lim)
            if lim.mode in ("RGBA", "P"):
                lim = lim.convert("RGBA")
                bg = Image.new("RGB", lim.size, (255, 255, 255))
                bg.paste(lim, mask=lim.split()[-1] if lim.mode == "RGBA" else None)
                lim = bg
            else:
                lim = lim.convert("RGB")
            lim.thumbnail((LOGO_MAX_HEIGHT * 4, LOGO_MAX_HEIGHT), Image.Resampling.LANCZOS)
            lim.save(logo_dst, format="PNG" if logo_ext == ".png" else "JPEG", quality=92)

    products: list[dict] = []
    for idx, src in enumerate(product_sources, start=1):
        ext = src.suffix.lower()
        safe = f"product_{idx:03d}.jpg"
        rel = f"images/{safe}"
        dst = output_dir / rel

        if ext == ".svg":
            shutil.copy2(src, output_dir / "images" / f"product_{idx:03d}.svg")
            products.append(
                {
                    "id": f"product_{idx:03d}",
                    "file": f"images/product_{idx:03d}.svg",
                    "caption": _title_from_stem(src.stem),
                }
            )
            continue

        _normalize_raster(src, dst, PRODUCT_MAX_SIDE, PRODUCT_CANVAS)
        products.append(
            {
                "id": f"product_{idx:03d}",
                "file": rel,
                "caption": _title_from_stem(src.stem),
            }
        )

    manifest = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "logo": logo_rel,
        "style_hint": "Sustituir en HTML: Minimal | Modern | Bold",
        "products": products,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Normaliza imágenes y genera manifest.json")
    parser.add_argument("--input", required=True, type=Path, help="Carpeta con imágenes y logo")
    parser.add_argument("--output", required=True, type=Path, help="Directorio de salida")
    args = parser.parse_args()
    manifest = process(args.input, args.output)
    print(json.dumps({"ok": True, "manifest": "manifest.json", "products": len(manifest["products"])}, indent=2))


if __name__ == "__main__":
    main()
