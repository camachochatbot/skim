# SKIM Incoming · 20 estilos · V3

Nueva campaña gráfica de **27 segundos**, 1920 × 1080, 60 fps. Se abandona el guion de las versiones anteriores. Veinte interpretaciones de los estilos enumerados en la imagen del usuario duran 1,2 s cada una; el cierre de marca ocupa 24–27 s. El objetivo es promocionar los viajes de esquí de SKIM para escolares y grupos.

## Renderizar

Herramientas usadas: Python 3.12.14, Chromium 154.0.8037.57 y FFmpeg 7.1.5 en Linux. Dependencias Python fijadas en `requirements.txt`. Three.js **0.170.0**, SVGLoader y fuentes DejaVu se incluyen localmente con sus licencias. No hacen falta CDN, npm, claves ni servicios externos para renderizar.

```bash
cd skim-incoming-v3
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python soundtrack.py
python render.py
python inspect_layout.py
python verify.py
```

El MP4 se guarda en `output/SKIM_20_estilos_V3.mp4`. Chromium se busca en `/usr/bin/chromium`; cambia `executable_path` si tu instalación está en otra ruta. El servidor de captura sólo escucha en 127.0.0.1. El render toma los instantes exactos `f / 60` y produce 1.620 fotogramas.

Para generar una imagen de cada estilo y el cierre:

```bash
python render.py --preview
```

Para ver o cambiar un instante, sirve la carpeta con `python -m http.server 8000 --bind 127.0.0.1`, abre `index.html` y escribe `await seek(4.4)` en la consola del navegador. La composición queda pausada a propósito. No depende de un reloj en tiempo real ni del orden de llamadas.

## Archivos

- `timing.json`: duración, fps, semilla, estilos, intervalos, textos de composición, cierre y tempo. Los elementos tipográficos especiales tienen también sus ajustes en `scene.js`.
- `scene.js`: Canvas 2D para composición, partículas, letras, vectores, grano, ASCII, papel, simulación física y píxeles. Three.js renderiza el wordmark de cromo y los objetos de arcilla con materiales e iluminación propios. Sus reflejos se generan con canvas.
- `prepare_wordmark.py`: regenera el SVG de SKIM a partir de la tipografía incluida. El SVG ya está preparado; este paso es opcional.
- `soundtrack.py`: compone y sintetiza música y efectos. Incluye el mismo algoritmo de rebotes a 120 Hz que la imagen para las señales de impacto. No lee samples.
- `render.py`: captura y codifica H.264 YUV420p / AAC estéreo.
- `inspect_layout.py`: verifica los límites del texto grande en las composiciones ya formadas de cada estilo y el cierre.
- `verify.py`: decodifica todo el MP4, comprueba streams, duración, señal y alineación de audio, revisa movimiento por estilo y genera láminas de todos los frames y una imagen de cada estilo.
- `DECISIONES.md`: correspondencia con la referencia, dirección, descartes, iteraciones, pruebas y tiempo real.

Las fuentes conservan su licencia en `assets/FONT-LICENSE.txt`. Three.js y SVGLoader conservan el aviso en `vendor/THREE-LICENSE.txt`. No se usa la cara de la imagen de referencia ni se afirma haber visto el movimiento del vídeo original: la referencia suministrada es una imagen estática con una lista.

La música y los efectos se crean con osciladores, ruido, filtros y envolventes. Las imágenes son construidas por código; no se usan generación de imagen/vídeo/audio, stock o música ajena. La reproducción es editable y determinista con las versiones indicadas; no se garantiza igualdad binaria entre navegadores, GPU y codificadores distintos.
