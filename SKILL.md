---
name: digital-catalog-from-images
description: >-
  Guía el diseño de catálogos digitales desde imágenes locales usando HTML5/CSS3
  y exportación a PDF con Python. Exige un logo renombrado (logo.png, logo.jpg o
  logo.svg), divulgación progresiva (analizar → preguntar → ejecutar) y delegación
  del procesamiento pesado a scripts. Usar cuando el usuario pida un catálogo PDF,
  brochure de productos, maquetación desde fotos o el flujo catalog-gen.
version: "1.0.0"
---

# Catálogo digital desde imágenes locales

## Filosofía

1. **Divulgación progresiva**: primero analizar el material, luego recopilar decisiones del usuario, y solo entonces generar archivos y ejecutar conversión.
2. **HTML/CSS como motor de diseño**: el agente redacta y ajusta el `index.html` final (layout, tipografía, jerarquía). El trabajo repetitivo de imágenes y el render a PDF va a **scripts Python**.
3. **Eficiencia de tokens**: no redimensionar ni normalizar imágenes “a mano” en el chat; invocar `image_processor.py`. No implementar conversión PDF en línea; invocar `pdf_converter.py`.

## Advertencia — logo obligatorio

Si **no** existe en la carpeta de trabajo un archivo llamado exactamente `logo.png`, `logo.jpg` (o `logo.jpeg`) o `logo.svg`, **no** continúes con el procesamiento ni la maquetación. Solicita al usuario que renombre su logo a uno de esos nombres antes de proceder.

> Si el agente no detecta un archivo llamado `logo.png` o `logo.jpg` (o `logo.svg`), debe solicitar al usuario que lo renombre antes de proceder.

## Protocolo de decisión (orden estricto)

No generes `index.html` ni ejecutes conversión a PDF hasta completar **todos** los pasos:

| Paso | Acción del agente |
|------|-------------------|
| **a** | Listar imágenes en la carpeta que indique el usuario (extensiones habituales: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`; logos y productos). |
| **b** | Verificar existencia de logo: `logo.png`, `logo.jpg`, `logo.jpeg` o `logo.svg` (comparación **insensible a mayúsculas** en el nombre base `logo`). Si falta → parar y pedir renombrado. |
| **c** | Preguntar al usuario (si no lo ha dado ya): **título del catálogo**, **estilo visual** (`Minimal`, `Modern` o `Bold`) y **color principal** (nombre o hex, p. ej. `#1a5f7a`). |

Solo después: ejecutar comandos de la sección siguiente, redactar/completar `index.html` a partir de `templates/base.html` y el manifiesto, y generar el PDF.

## Comandos de ejecución

Desde la raíz del proyecto de catálogo (donde estén `scripts/`, `templates/` y la carpeta de imágenes del usuario), usar rutas absolutas o relativas coherentes. Sustituir `RUTA_IMAGENES` y `RUTA_SALIDA`.

**1. Procesar imágenes y generar manifiesto**

```bash
python3 scripts/image_processor.py --input "RUTA_IMAGENES" --output "RUTA_SALIDA"
```

- Entrada: carpeta con fotos de producto + logo obligatorio (`logo.*` según reglas).
- Salida: imágenes normalizadas, copia del logo y `manifest.json` (rutas relativas al directorio de salida para enlazar desde el HTML).

**2. Convertir HTML a PDF**

Tras tener `index.html` en `RUTA_SALIDA` (o la ruta que corresponda), con rutas de recursos resolviendo bien respecto a ese archivo:

```bash
python3 scripts/pdf_converter.py --html "RUTA_SALIDA/index.html" --output "RUTA_SALIDA/catalogo_final.pdf"
```

## Redacción del HTML final

1. Copiar o fusionar `templates/base.html` hacia `index.html` en el directorio de salida del usuario.
2. Sustituir placeholders documentados en el template por: título, estilo, color, bloque de productos (según `manifest.json`).
3. Asegurar que `<img src="...">` apunte a archivos existentes bajo el mismo directorio base que `index.html` (o usar rutas relativas coherentes con lo generado por `image_processor.py`).

## Prerequisites (seguridad y entorno)

Instalar solo desde fuentes confiables (`pip`, gestor del SO). Revisar dependencias del sistema para el backend elegido. En el repositorio público, las versiones recomendadas están en `requirements.txt` (raíz del proyecto).

| Componente | Uso |
|------------|-----|
| **Python 3.10+** | Intérprete para los scripts. |
| **Pillow** (`pip install pillow`) | Redimensionado y normalización de raster en `image_processor.py`. |
| **WeasyPrint** (`pip install weasyprint`) | Conversión HTML/CSS → PDF en `pdf_converter.py`. En Linux suele requerir bibliotecas del sistema (p. ej. Pango, Cairo); ver [documentación oficial de WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation). |

**Nota**: Si WeasyPrint no es viable en el entorno del usuario, se puede adaptar `pdf_converter.py` para usar **Playwright** (`pip install playwright` + `playwright install chromium`) y `page.pdf()`; eso debe acordarse explícitamente y documentarse en el mismo bloque de prerequisites al cambiar el script.
