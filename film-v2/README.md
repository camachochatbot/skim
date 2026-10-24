# SKIM Incoming · Todo conectado · V2

Revisión con nueve interfaces animadas, cámaras de paisaje/descenso/base/cierre, terreno continuo y una banda sonora electrónica original distinta de la primera versión. 1920 × 1080, 60 fps, exactamente 15 segundos. Todo está construido con código; no se usan modelos de generación, stock ni muestras de audio.

## Renderizar

Requisitos usados: Linux, Python 3.12.14, Chromium 154.0.8037.57 en `/usr/bin/chromium`, FFmpeg 7.1.5 con libx264/AAC. Dependencias Python fijadas en `requirements.txt`. Los módulos JS Three.js 0.170.0 y GSAP 3.12.5, sus avisos de licencia y las tipografías DejaVu se incluyen localmente. No se necesita npm ni una CDN para ejecutar la composición.

```bash
cd skim-incoming-v2
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python soundtrack.py
python render.py
python verify.py
python inspect_layout.py
```

El vídeo se escribe en `output/SKIM_Incoming_La_Molina_V2.mp4`. El render escucha sólo en 127.0.0.1. Si Chromium está instalado en otra ruta, modifica `executable_path` en `render.py` y `inspect_layout.py`. Los procesos no necesitan persistir entre ejecuciones.

Para generar encuadres de control:

```bash
python render.py --preview
python render.py --preview --times 2.85,3,3.1,5.9,6.9,7,11
```

Para comparar una captura fuente con el MP4 después de renderizar: `python render.py --preview --times 13` y luego `python extract_evidence.py`. Este segundo script extrae también fotogramas de los bloques principales.

Para ver la composición editable, sirve la carpeta con `python -m http.server 8000 --bind 127.0.0.1`, abre `index.html` y usa `await seek(5.9)` en la consola del navegador. La composición es intencionadamente pausada y no depende del reloj real.

## Estructura

- `timing.json`: dimensiones, duración, fps, semilla, capítulos, textos principales, parámetros de cámara, entradas/salidas y transformaciones de las nueve interfaces, y tempo musical.
- `scene.js`: relieve, bosque instanciado, arquitectura, autobús, telesilla, esquiadores, nieve, material 3D, iconos y mapas vectoriales, y función `seek(t)`.
- `index.html`: composición tipográfica y paneles. Son interfaces conceptuales de campaña, no reservas o pases reales. No hay cifras comerciales ni métricas de negocio.
- `soundtrack.py`: toda la composición y síntesis; genera WAV estéreo de 720.000 muestras por canal a 48 kHz. No lee ningún sample.
- `render.py`: captura los 900 fotogramas y codifica H.264 YUV420p con rango TV y AAC.
- `verify.py`: valida el MP4, decodifica todos los frames, analiza audio y su alineación con la síntesis y crea 18 hojas que cubren cada fotograma.
- `inspect_layout.py`: comprueba errores del navegador y límites de interfaces completamente visibles en trece instantes.
- `DECISIONES.md`: cambios de dirección, descartes, iteraciones, resultados medidos, alcance real de la revisión y tiempo empleado.

El ZIP conserva las evidencias de revisión y el WAV. El MP4 se entrega aparte, sin duplicarlo dentro del ZIP. Cambiar la duración requiere adaptar la composición musical y las aserciones del verificador: esta entrega está expresamente fijada a quince segundos.

## Licencias y límites

Fuentes DejaVu y su licencia en `assets/`. Avisos originales de Three.js y GSAP en `vendor/`. El wordmark es tipográfico porque no se proporcionó un logo oficial. La montaña es una interpretación artística de La Molina. El código es reproducible con estas herramientas; no se garantiza igualdad binaria entre GPU, navegador y codificador distintos.
