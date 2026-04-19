# catalog-gen

Generación de **catálogos digitales** a partir de imágenes locales: maquetación en **HTML5/CSS3** y exportación a **PDF** con Python. Pensado para usarse con un agente (p. ej. **Cursor**) siguiendo el flujo definido en `SKILL.md`.

## Objetivo

Estandarizar un flujo en el que el agente **valida** material (imágenes, logo obligatorio), **recopila** criterios de diseño (título, estilo, color) y **delega** el tratamiento de imágenes y el render del PDF a scripts, concentrando la creatividad en el HTML final.

## Componentes

| Elemento | Función |
|----------|---------|
| `SKILL.md` | Instrucciones para el agente (orden de pasos, comandos, prerequisitos). |
| `scripts/image_processor.py` | Escaneo de carpeta, detección de `logo.*`, normalización de fotos de producto y `manifest.json`. |
| `scripts/pdf_converter.py` | Conversión de `index.html` a PDF vía **WeasyPrint**. |
| `templates/base.html` | Plantilla con layout en flex/grid y placeholders para título, logo y galería. |

## Requisitos

- Python **3.10+**
- Dependencias: [`requirements.txt`](requirements.txt) (`pillow`, `weasyprint`)
- Sistema: bibliotecas que exija [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) en su plataforma (p. ej. Pango/Cairo en Linux).

## Instalación

```bash
git clone https://github.com/mexicancreator/catalog-gen.git
cd catalog-gen
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso (resumen)

1. Carpeta de entrada con fotos de producto y logo nombrado `logo.png`, `logo.jpg`, `logo.jpeg` o `logo.svg`.
2. `python3 scripts/image_processor.py --input <carpeta> --output <salida>`
3. Generar `index.html` a partir de `templates/base.html` y `manifest.json` (sustitución de placeholders).
4. `python3 scripts/pdf_converter.py --html <salida>/index.html --output <salida>/catalogo_final.pdf`

El detalle del protocolo y las reglas del logo están en **`SKILL.md`**.

## Skill en Cursor

Copiar el contenido del repositorio (al menos `SKILL.md` y rutas coherentes a `scripts/`) bajo:

- `~/.cursor/skills/digital-catalog-from-images/`, o  
- `.cursor/skills/digital-catalog-from-images/` en un proyecto.

## Licencia

[MIT](LICENSE) — Copyright (c) 2026 mexicancreator.
