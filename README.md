# Catálogo digital desde imágenes (`catalog-gen`)

Herramientas y **Cursor Skill** para generar un catálogo en **HTML/CSS** y exportarlo a **PDF** a partir de una carpeta de imágenes locales. El flujo prioriza **divulgación progresiva** (analizar → preguntar → ejecutar) y delega el procesamiento pesado a Python.

## Requisitos

- **Python 3.10+**
- Dependencias Python: ver [`requirements.txt`](requirements.txt)
- **WeasyPrint** suele necesitar librerías del sistema (Pango, Cairo, GDK-Pixbuf, etc.). Guía oficial: [instalación de WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

## Instalación

```bash
git clone https://github.com/mexicancreator/catalog-gen.git
cd catalog-gen
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso rápido (CLI)

1. Coloca tus fotos de producto y el **logo obligatorio** en una carpeta (ver reglas de nombre abajo).
2. Procesa imágenes y genera `manifest.json`:

   ```bash
   python3 scripts/image_processor.py --input "/ruta/a/tus/fotos" --output "./mi-salida"
   ```

3. Copia [`templates/base.html`](templates/base.html) a `mi-salida/index.html` y reemplaza los placeholders (`{{CATALOG_TITLE}}`, `{{PRIMARY_COLOR}}`, `{{BODY_STYLE_CLASS}}`, `{{LOGO_SRC}}`, `{{PRODUCTS_HTML}}`, etc.) según `manifest.json`.
4. Genera el PDF:

   ```bash
   python3 scripts/pdf_converter.py --html "./mi-salida/index.html" --output "./mi-salida/catalogo_final.pdf"
   ```

Con **Cursor** (o otro agente), sigue las instrucciones de [`SKILL.md`](SKILL.md): listar imágenes, verificar logo, preguntar título / estilo / color, luego ejecutar los scripts y redactar el HTML.

## Reglas del logo

Debe existir **exactamente** un archivo llamado `logo.png`, `logo.jpg`, `logo.jpeg` o `logo.svg` (el nombre base `logo` puede ir en mayúsculas o minúsculas). Sin eso, el procesador falla a propósito: renombra tu logo antes de continuar.

## Usar como Cursor Skill

Copia esta carpeta (o el repo clonado) a una de estas ubicaciones:

| Ámbito | Ruta |
|--------|------|
| Personal | `~/.cursor/skills/digital-catalog-from-images/` (dentro, el archivo `SKILL.md` en la raíz de esa carpeta del skill) |
| Por proyecto | `.cursor/skills/digital-catalog-from-images/` en tu repositorio |

El directorio del skill debe contener al menos `SKILL.md`; los scripts pueden referenciarse por ruta relativa al clon del repo o copiarlos junto al skill si prefieres un paquete autocontenido.

## Estructura del repositorio

```
catalog-gen/
├── README.md
├── LICENSE
├── requirements.txt
├── SKILL.md                 # Instrucciones para el agente
├── scripts/
│   ├── image_processor.py
│   └── pdf_converter.py
└── templates/
    └── base.html
```

## Qué **no** subir a GitHub (privacidad)

Este repo está pensado para **código y plantillas**, no para tus activos personales.

- No incluyas fotos de producto, logos de clientes ni PDFs generados con datos reales **salvo** que tengas derecho y quieras un ejemplo explícito (mejor datos ficticios).
- Trabaja con una carpeta de entrada **fuera** del repo, o añade al `.gitignore` local cualquier directorio donde guardes material privado (por ejemplo `mis-fotos/`, `cliente-x/`).
- No subas `.env`, claves API ni rutas internas de tu máquina en issues o commits.

El [`.gitignore`](.gitignore) ya ignora caché de Python, entornos virtuales y carpetas típicas de salida (`output/`, `out/`, `build/`). Amplía el archivo si usas otros nombres para material sensible.

## Licencia

Ver [LICENSE](LICENSE) (MIT).

## Contribuciones

Issues y pull requests son bienvenidos. Mantén los cambios alineados con el flujo descrito en `SKILL.md` (logo obligatorio, scripts para imágenes/PDF, HTML como capa de diseño).
