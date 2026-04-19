#!/usr/bin/env python3
"""
Convierte index.html (+ CSS y recursos relativos) a catalogo_final.pdf usando WeasyPrint.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def convert(html_path: Path, pdf_path: Path) -> None:
    try:
        from weasyprint import HTML
    except ImportError as e:  # pragma: no cover - mensaje de instalación
        print(
            "Falta WeasyPrint. Instale con: pip install weasyprint\n"
            "En Linux puede necesitar paquetes del sistema (Pango, Cairo).",
            file=sys.stderr,
        )
        raise SystemExit(1) from e

    html_path = html_path.resolve()
    if not html_path.is_file():
        raise FileNotFoundError(f"No existe el HTML: {html_path}")

    pdf_path = pdf_path.resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    base_url = html_path.parent.as_uri() + "/"

    HTML(filename=str(html_path), base_url=base_url).write_pdf(str(pdf_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="HTML/CSS → PDF (WeasyPrint)")
    parser.add_argument("--html", required=True, type=Path, help="Ruta a index.html")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Ruta del PDF de salida (p. ej. catalogo_final.pdf)",
    )
    args = parser.parse_args()
    convert(args.html, args.output)
    print(f"PDF generado: {args.output.resolve()}")


if __name__ == "__main__":
    main()
