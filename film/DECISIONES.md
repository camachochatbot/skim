# DECISIONES · SKIM Incoming / La Molina

## Intención y dirección

Campaña de invierno para viajes de esquí de escolares y grupos. La idea es convertir la coordinación de SKIM en un recorrido físico: del paisaje al descenso, del descenso al equipo y de ahí a la base alpina. La montaña es una interpretación artística de La Molina, sin pretensión cartográfica. No se han añadido cifras comerciales, precios, disponibilidad, contactos, certificaciones ni promesas de cobertura.

Se ha elegido una maqueta 3D estilizada con relieve facetado, personajes geométricos y luz lateral. Permite mantener un universo continuo y reconocer servicios en sólo quince segundos. El blanco nieve y el azul hielo contrastan con un fondo azul noche. Las ventanas cálidas aportan una pequeña señal de acogida sin cambiar la paleta principal. No se proporcionaron logo ni manual: SKIM es un wordmark tipográfico en cursiva y no se presenta como identidad oficial.

La tipografía se mantiene fuera de la perspectiva 3D para proteger la lectura. El bloque principal tiene margen izquierdo de 104 píxeles y un degradado oscuro detrás. Los objetos siguen en perspectiva. Los textos solicitados se conservan en español. El cierre termina visible: no se funde a negro ni se corta durante una animación de salida.

## Recorrido y representación de servicios

| Tiempo | Imagen y acción | Mensaje |
|---|---|---|
| 0–3 s | Travelling hacia la cumbre; huellas vectoriales dobles dibujan SKIM. El telesilla ya conecta el paisaje. | Tu grupo. La Molina. |
| 3–7 s | La cámara se acerca al esquiador; aparecen un forfait con código de barras y un par de esquís con fijaciones. Un grupo aprende junto al pórtico de escuela. | Todo listo para disfrutar. |
| 7–11 s | Acercamiento a los refugios con ventanas, mesas con platos y tazas, autobús ocupado y grupo. Líneas luminosas enlazan la base con el punto SKIM. Un escudo con cruz representa el seguro. | Vosotros disfrutáis. SKIM coordina. |
| 11–15 s | Retirada de cámara para reunir todo el mundo; nombre grande y CTA sostenido. | SKIM Incoming. Organiza el viaje de tu grupo. |

Los servicios se cuentan mediante objetos y relaciones, sin una lista sobreimpresa. El forfait representa el acceso; los esquís, el alquiler; el pórtico y los alumnos, las clases; los chalets, el alojamiento; platos y tazas, las comidas; el escudo, el seguro; el autobús, el desplazamiento conjunto; y el punto SKIM con rutas, la coordinación presencial. Son símbolos de los servicios indicados por el encargo; el escudo no especifica condiciones de ninguna póliza.

## Construcción técnica

Three.js 0.170.0 genera geometría, materiales, luces, niebla, sombras y partículas. El relieve de primer plano usa una malla paramétrica; las montañas de fondo, anillos triangulados irregulares. La pista sigue una curva Catmull–Rom. Se generan árboles, esquiadores, sillas, pilonas, edificios, vehículo, equipo y objetos de mesa con primitivas. No hay modelos 3D ni texturas fotográficas importadas.

HTML/CSS y SVG se usan para texto y huellas de apertura. GSAP 3.12.5 proporciona una línea temporal pausada; `seek(t)` calcula todas las posiciones. La semilla está fijada. El JSON contiene resolución, fps, duración, capítulos, textos, eventos musicales y vistas de cámara. Las demás expresiones de movimiento están explícitas en `scene.js`.

El render usa Playwright y Chromium con WebGL por SwiftShader, captura cada instante `f / 60` y envía los 900 fotogramas a FFmpeg. H.264, YUV 4:2:0, CRF 17, AAC estéreo a 320 kb/s y 48 kHz; `faststart` facilita la reproducción. Se incluyen fuentes y módulos JS locales para no depender de CDNs al renderizar. Reproducible significa que se puede regenerar la composición y la música con el código incluido; la identidad binaria entre versiones de navegador, GPU y codificador no está garantizada.

Se consultaron las habilidades HyperFrames y Motion Graphics Starter Kit. Sus recursos auxiliares no pudieron leerse con el proveedor disponible. No se utilizó ni se afirma haber ejecutado el CLI de HyperFrames: se optó por un render propio determinista en Three.js, apropiado al encargo. No se usaron clips, capturas de práctica, efectos sonoros ni músicas de ese kit. DejaVu se tomó de la instalación local y conserva su licencia.

## Música y sincronización

Composición original a 128 BPM con centro tonal en re menor. `soundtrack.py` sintetiza a 48 kHz usando NumPy y SciPy: bombo de seno con caída de frecuencia, caja de ruido filtrado y seno, charles de ruido pasa-altos, bajo aditivo, acordes con desafinación estéreo, arpegio y retardos, impactos graves y barridos de ruido. No se carga ninguna muestra de sonido ni música ajena; no se usa un modelo generativo de audio.

El arpegio entra con el descenso. Los eventos en 3, 7 y 11 segundos tienen barrido previo e impacto y coinciden con las transiciones visuales. Un acorde de campanas sintetizadas subraya el cierre. La señal tiene margen antes de 0 dBFS y una liberación final de 0,52 segundos para evitar un corte abrupto. El audio ocupa los quince segundos de la pieza.

## Enfoques descartados e iteraciones reales

- Se descartaron metraje, imágenes generadas, música externa y muestras: el encargo exige construcción íntegra con código.
- Se prefirió la estilización a un supuesto fotorrealismo: una escena reconocible y continua resulta más legible que muchos recursos complejos fugaces en quince segundos.
- Se descartó una pantalla con siete servicios escritos; las funciones se convirtieron en objetos conectados.
- El primer intento de instalación npm no pudo escribir en la caché del directorio personal. Se resolvió usando una caché dentro de `/workspace`, manteniendo la verificación normal del gestor.
- La primera previsualización detectó un error de precedencia en una exponenciación de JavaScript; se corrigió antes de renderizar.
- Los primeros encuadres mostraban refugio y autobús demasiado bajos. Se cambió el objetivo de cámara de la tercera escena y el cierre para mantenerlos dentro del plano.
- Se eliminaron tres montañas de primer plano que intersecaban el terreno y producían aristas visuales extrañas. El paisaje lejano mantiene la profundidad.
- Las huellas SKIM en espacio 3D resultaban demasiado pequeñas y rasantes. Se sustituyeron por trazos vectoriales dobles, visibles y animados en la apertura. Se corrigió además la medición de longitud del SVG para consultar el path original, no el elemento `use`.
- Se reforzó el plano de seguimiento del esquiador antes de revelar el material. Se añadieron ocupantes al autobús y desplazamiento del grupo cerca de la base.
- Un árbol claro reducía el contraste al final de «disfrutar». Se amplió el degradado oscuro detrás del texto y se oscureció el pie.
- Tras el render se empaquetaron localmente las dependencias JS y se trasladaron cámaras y textos al JSON. Se repitió la previsualización con esas rutas locales; no es un segundo render completo. Los valores visuales permanecen iguales.

## Alcance de la revisión

La revisión visual del MP4 se realiza por fotogramas exportados, en orden, mediante hojas numeradas que cubren los 900 frames, más vistas de mayor tamaño de escenas, transiciones y último fotograma. No se confunde una captura del HTML con una comprobación del MP4. La reproducción auditiva subjetiva no está disponible en las herramientas de esta sesión: el audio se comprueba técnicamente, incluida su correspondencia temporal con la pista original. No se afirma una escucha humana ni una revisión audiovisual en un reproductor a velocidad real.


## Resultados de verificación

- MP4 H.264 de 1920 × 1080, 60/1 fps, **900 fotogramas**, duración de vídeo **15,000000 s**. Audio AAC estéreo, 48 kHz, también **15,000000 s**.
- Decodificación completa con FFmpeg, sin errores. Cero fotogramas negros o vacíos; no hay fotogramas consecutivos congelados según comparación reducida.
- Se inspeccionaron en orden las 18 hojas del MP4 que representan los 900 fotogramas. Entradas de textos, desplazamientos y transiciones mantienen su continuidad; no se detectó un salto de composición ni texto principal cortado. Los planos incluyen recortes deliberados del paisaje, árboles y telesilla en los márgenes; el CTA queda dentro de la zona segura.
- Se revisó además el último fotograma exportado, 899, a resolución completa: nombre, INCOMING y «Organiza el viaje de tu grupo.» están enteros y visibles. El cierre permanece plenamente formado desde aproximadamente 11,48 s hasta el final.
- El pico de muestra decodificado es **−0,161 dBFS**; la señal es finita, sin muestras a 0 dBFS ni silencios inesperados. EBU R128 sobre el MP4: **−15,6 LUFS integrados**, **−0,1 dBFS de pico real**. No hay escucha subjetiva disponible; estas mediciones no se presentan como una escucha humana.
- La correlación entre el audio original y el decodificado es **0,999544**, con un desplazamiento medido de **0 muestras**. Los eventos musicales se programaron en los mismos 3, 7 y 11 segundos de las transiciones.
- La pista WAV se sintetizó de nuevo y produjo exactamente el mismo SHA-256: `bf35cc877b278478f9006f75cca677814fd18df17d1a2b6f6db5e50e83baefc2`.
- La previsualización del código final con módulos locales se comparó con el fotograma exportado a 13 s: error absoluto medio **1,2053 / 255**, incluyendo las pérdidas JPEG/H.264. Es una comprobación puntual de reproducción, no un segundo render completo ni una prueba binaria de igualdad.
- Los scripts Python pasan compilación sintáctica. La previsualización final de Chromium termina sin errores de página. No se ejecutaron HyperFrames lint/check; el verificador propio y las pruebas reales descritas son la evidencia disponible.

El detalle legible por máquina está en `output/verification.json`; las hojas, `output/review-01.jpg` a `review-18.jpg`; la medición de loudness, `output/loudness.log`. La fuente editable, dependencias locales, licencias y síntesis musical se entregan juntas. El MP4 se entrega aparte para no duplicarlo dentro del ZIP.

## Tiempo real empleado

Inicio medido: **2026-10-24T01:05:02+00:00**. Cierre de verificación y documentación para empaquetado: **2026-10-24T01:19:47+00:00**. Tiempo total transcurrido: **14 min 46 s**. Son tiempos de reloj reales de esta sesión, incluyendo inspección, construcción, correcciones, render, revisión y preparación de entrega; no son una estimación de horas de trabajo humano. El render completo registró **286,8 s** en su log. No se inventa un reparto por fases.
