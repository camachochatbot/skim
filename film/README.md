# SKIM Incoming · La Molina

Película procedural de 15 s, 1920 × 1080 y 60 fps. Paisaje artístico inspirado en La Molina; no es una reconstrucción topográfica. No se han usado modelos generativos, fotografías, vídeos, música externa ni muestras sonoras.

## Reproducir el render

Requisitos del sistema: Python 3.12, Chromium, FFmpeg con libx264 y AAC. El render original usa Chromium 154.0.8037.57 y FFmpeg 7.1.5 en Linux. Python usa las versiones de `requirements.txt`.

```bash
cd film
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python soundtrack.py
python render.py
python verify.py
```

`render.py` abre Chromium en `/usr/bin/chromium`. Si está instalado en otra ruta, modifica `executable_path`. El servidor sólo escucha en 127.0.0.1. No hace falta iniciar servicios externos ni aportar claves. El resultado se escribe en `output/SKIM_Incoming_La_Molina.mp4`. Las dependencias JS de ejecución se incluyen en `vendor/`, con sus licencias. Para refrescarlas desde sus versiones fijadas: `npm ci --cache /tmp/skim-npm-cache` y `python vendor.py`.

Para ver el diseño interactivo, ejecuta `python -m http.server 8000 --bind 127.0.0.1` y abre `index.html`. La composición queda pausada intencionadamente: en la consola del navegador, `await seek(8.5)` muestra exactamente ese instante. `python render.py --preview` produce los encuadres de control. Todos los movimientos se calculan en función del tiempo; no hay simulación acumulativa ni imágenes aleatorias distintas entre frames.

## Editar

- `timing.json`: dimensiones, fps, duración, semilla, capítulos, textos, cámaras y eventos musicales. La pieza entregada tiene 900 fotogramas. Cambiar duración o estructura exige revisar también la coreografía musical y el verificador, cuyas aserciones protegen esta entrega concreta.
- `scene.js`: geometría, materiales, recorrido, personajes y transformaciones; `seek(t)` controla el mundo.
- `index.html`: jerarquía tipográfica, márgenes, dibujo vectorial de huellas y cierre.
- `soundtrack.py`: síntesis de percusión, bajo, acordes, arpegios, impactos y barridos. El WAV se regenera sin archivos de muestras.
- `render.py`: captura determinista a `f / fps` y codificación H.264 + AAC.
- `verify.py`: verifica streams, 900 frames, duración, decodificación, señal de audio y genera hojas de revisión de todos los fotogramas exportados.

Las fuentes DejaVu se incluyen con su licencia en `assets/FONT-LICENSE.txt`. Las licencias de Three.js y GSAP están en `vendor/`. El nombre se representa con un wordmark tipográfico, porque no se aportó un logotipo oficial.
