# DECISIONES · SKIM Incoming · V3 «20 formas de activar el invierno»

## Nuevo encargo y referencia real

El usuario pidió añadir las veinte animaciones enumeradas en una imagen y dejó expresamente sin efecto el prompt anterior: sólo debía mantenerse la promoción de SKIM. Por eso se abandona la narración anterior de cuatro bloques y la obligación de quince segundos. Se elige una pieza de **27 s**: veinte estilos × 1,2 s = 24 s, más tres segundos de cierre. Se conserva 1920 × 1080 a 60 fps como formato de entrega práctico.

La referencia suministrada es una **imagen estática con una lista**. No se ha visto el vídeo del que proviene ni se afirma reproducir su movimiento exacto. Se interpretan los estilos por sus rasgos visuales y de movimiento. No se utiliza la cara de la persona de la captura ni se incorpora la captura al anuncio.

## Dirección creativa

Una campaña gráfica rápida y variada, con SKIM como ancla. El nombre, las diagonales, la nieve y el viaje en grupo conectan cambios de color y textura. Cobalto, azul noche, blanco cálido, verde ácido, coral y magenta dan energía; la escena art déco introduce un contraste más sobrio. Los rótulos son grandes, de pocas palabras, y el cierre estabiliza la marca y la llamada a la acción.

No se convierte la lista de estilos en el contenido del anuncio: no hay un presentador ni veinte nombres técnicos sobreimpresos. Los estilos sirven para hablar de invierno, grupo, viaje, material, organización y recuerdos. Los hechos comerciales se limitan al contexto dado: SKIM organiza viajes de esquí para escolares y grupos. No se añaden precios, reservas reales, cifras de clientes, horarios o condiciones de seguro.

## Correspondencia con los veinte estilos

| # | Estilo de la referencia | Interpretación animada para SKIM |
|---|---|---|
| 1 | Particles | Miles de partículas dispersas convergen en la silueta tipográfica SKIM; nieve en profundidad aparente. |
| 2 | Liquid morph | Contorno líquido con radios trigonométricos variables alrededor de «MODO NIEVE». No se presenta como simulación de fluidos. |
| 3 | Neon glow | Arcos elípticos rotatorios, halo cian/magenta y rótulo de activación. |
| 4 | Y2K chrome | Wordmark extruido, biselado y metálico, con giro e iluminación/reflejos procedurales. |
| 5 | Kinetic type | Palabras grandes entran desde direcciones opuestas, en diagonal, con aceleración controlada. |
| 6 | Paper cutout | Capas de montañas con sombras, bordes irregulares y autobús recortado en movimiento. |
| 7 | Holographic | Forfait con degradado iridiscente, franjas de luz, inclinación y deformación de perspectiva aproximada. |
| 8 | Isometric | Proyección isométrica dibujada de un pequeño núcleo conectado; bus y nodos en movimiento. |
| 9 | ASCII art | La máscara de SKIM se reconstruye con caracteres que cambian; ondas y texto monoespaciado. |
| 10 | Clay 3D | Botas y casco de formas suaves, materiales mates y paleta pastel; giro y elevación controlados. |
| 11 | Retro VHS | Atardecer gráfico, líneas de barrido, separación de color, vibración y pequeñas interferencias. |
| 12 | Comic book | Trama de puntos, estallido radial, letras inclinadas y pulso de impacto. |
| 13 | Split-flap | Cinco paneles mecánicos cambian caracteres, se dividen en mitades y muestran el movimiento de la bisagra. |
| 14 | Hand-drawn | Montañas y ruta se revelan con trazos irregulares y pequeñas variaciones de dibujo. |
| 15 | Blueprint | Cuadrícula azul, líneas y nodos que se despliegan como un plan de viaje conectado. |
| 16 | Physics | Doce cuerpos con iconos caen, colisionan entre sí y rebotan en los bordes y el suelo. |
| 17 | Pixel art | Escena de 240 × 135 píxeles escalada sin suavizado, con esquiador y desplazamiento del paisaje. |
| 18 | Bauhaus | Círculo, barras y triángulo en colores primarios, con movimiento y tipografía de composición gráfica. |
| 19 | Art deco | Abanicos y marcos dorados, simetría parcial y aparición progresiva sobre fondo oscuro. |
| 20 | Neo-brutalism | Verde ácido, bordes negros gruesos, sombra dura y gran bloque de marca inclinado que oscila. |

Cada bloque dura tres pulsos de la música. El cierre 24–27 s muestra SKIM Incoming y «Organiza el viaje de tu grupo», con una línea que describe su actividad. Tiene una entrada breve del wordmark y después mantiene el mensaje completo. No se funde a negro al terminar.

## Técnica y fuente reproducible

Canvas 2D compone texto, vectores, máscaras, papel, grano, partículas, ASCII, píxeles y la simulación de cuerpos. Three.js **0.170.0** renderiza dos escenas: cromo y arcilla. El cromo utiliza un SVG generado desde la tipografía DejaVu incluida, extrusión y biseles; su mapa cúbico de reflejos también se dibuja con código. La arcilla utiliza geometría extruida y materiales mates. No se importan modelos 3D ni texturas fotográficas.

Las fuentes y sus licencias están en `assets/`. Three.js y SVGLoader están incluidos localmente con su aviso de licencia. No hacen falta servicios externos para renderizar. `timing.json` estructura los veinte estilos, tiempos, textos de composición, cierre y tempo. `seek(t)` calcula un instante sin depender del reloj real. La física se precalcula con pasos de 1/120 s y semilla fija, por lo que buscar un instante anterior o posterior produce el mismo estado.

Playwright captura fotogramas `f / 60`; FFmpeg codifica H.264 YUV420p con rango TV y AAC estéreo a 48 kHz. La entrega tiene 1.620 fotogramas. La reproducción completa se describe en README.md. La identidad binaria entre distintos navegadores, GPU o codificadores no está garantizada.

Se mantienen los principios de composición reproducible y revisión de las habilidades de motion graphics consultadas. Sus referencias auxiliares no estuvieron accesibles; se usa el render propio. No se ejecutaron ni se atribuyen comprobaciones HyperFrames lint/check.

## Música y efectos originales

Banda sonora electrónica original a **150 BPM**, con centro tonal en mi menor. Los bloques de 1,2 s coinciden con tres pulsos de 0,4 s. Se sintetizan bombo, caja/clap, charles, subgrave y bajo medio, acordes de voces desafinadas, una frase melódica y retardos estéreo. El cierre simplifica la percusión y resuelve en mi menor.

Los estilos tienen acentos propios creados con osciladores, ruido, filtros y envolventes: sonido líquido, resonancia metálica, flick de papel, chirrido holográfico, clic mecánico, interferencia VHS, golpe de cómic, blips de píxel y golpes suaves de rebote. Los impactos de suelo de la escena física se programan con el mismo algoritmo y semilla de 120 Hz que la imagen. No se leen archivos de samples ni música ajena. No se usan modelos generativos de audio, imagen o vídeo ni stock.

La mezcla incluye filtrado de infragraves, saturación suave, margen de pico y una liberación final de 0,65 s. La duración del WAV es exactamente 27 s, con 1.296.000 muestras por canal.

## Iteraciones y correcciones reales

- Se pasó del universo alpino continuo de V2 a una sucesión gráfica de estilos a pantalla completa; no se reutiliza su guion.
- Se prepararon imágenes de todos los estilos antes de exportar. El primer texto del líquido era blanco sobre cian claro: se cambió a azul noche para aumentar contraste.
- En neobrutalismo, «EMPIEZA CONTIGO» se cruzaba con la tarjeta de SKIM. Se dividió el titular en tres líneas y se ajustó la línea inferior.
- En física, los cuerpos cruzaban el titular y reducían su contraste. Se añadió una superficie clara detrás del mensaje, manteniendo los cuerpos visibles alrededor.
- Los paneles mecánicos recibieron una cara de bisagra que varía en altura para hacer visible el giro durante el cambio de caracteres.
- La comprobación del primer MP4 detectó que el bloque de cómic quedaba casi estático tras el barrido de entrada: movimiento acumulado 0,0539 en la ventana examinada, frente al umbral 0,5. La causa era que su estallido y su tipografía tenían posiciones fijas; los otros diecinueve estilos sí mostraban movimiento interno.
- Se añadió un pulso radial y un pequeño giro/escala al cómic. Esos movimientos vuelven a su estado inicial en los extremos para mantener la continuidad con los barridos vecinos.
- Se renderizaron de nuevo únicamente los 72 fotogramas de cómic, 13,2–14,4 s. El montaje conserva los otros tramos validados y vuelve a codificar el vídeo una vez a CRF 16. El audio se toma del WAV original. `repair_comic.py` conserva el procedimiento; el render completo desde cero con el código final también incorpora la corrección sin necesitar ese archivo base.

## Alcance de verificación

Se revisan capturas de composición y, por separado, imágenes extraídas del MP4. El verificador decodifica todo el archivo, genera dieciocho láminas que representan los 1.620 fotogramas y extrae una imagen de cada estilo y el último frame. Los rótulos grandes se comprueban con métricas reales del canvas en veintidós instantes de composición formada. Los recortes durante entradas y las líneas decorativas fuera de cuadro son deliberados.

Los paneles mecánicos y el plano técnico pueden tener algunos frames idénticos cuando terminan de formarse: son pausas de lectura, no se afirma que todos los pares de frames sean distintos. Se verifica movimiento interno en cada estilo y se documentan los valores medidos.

No hay escucha directa disponible en las herramientas de esta sesión. El audio se revisa técnicamente mediante duración, señal, picos, loudness, correlación y desplazamiento respecto al WAV. No se presenta esa comprobación como una escucha humana ni se afirma haber visto la referencia en movimiento.


## Resultados finales y tiempo medido

El archivo final pasó decodificación completa: H.264, 1920 × 1080, 60 fps, 1.620 fotogramas y 27,000 s; AAC estéreo a 48 kHz y 27,000 s. Se detectaron cero fotogramas vacíos. Los veinte estilos superaron la comprobación de movimiento interno; el cómic corregido obtuvo 43,2851. La comprobación de texto pasó en veintidós instantes sin errores de página.

Se inspeccionaron visualmente las dieciocho láminas extraídas del MP4 que representan todos los fotogramas, el mosaico de veinte estilos y capturas grandes del cómic, neobrutalismo y último frame. Esta revisión fue por imágenes consecutivas, no una reproducción audiovisual en tiempo real.

Audio medido: −14,5 LUFS integrados, pico real −1,9 dBTP; desplazamiento respecto al WAV: 0 muestras; correlación 0,999838. Se regeneró el WAV y se obtuvo el mismo SHA-256: `579d556e9e4ad0fa67ce296e34440aa675fb6862dc907c108f5fe55084a70c48`. También se comprobó la regeneración idéntica del SVG.

Inicio registrado de V3: 2026-10-24T13:04:14+00:00. Cierre de documentación y comienzo de empaquetado: 2026-10-24T13:41:38.827763+00:00 (15:41:38 en Madrid). Tiempo transcurrido real de esta revisión V3 hasta este punto: **37 min 24 s**; incluye implementación, síntesis, render, espera y revisión. No incluye versiones anteriores ni la posterior subida a GitHub. El render completo registró 244,2 s y la captura de la corrección regional 13,6 s. No se atribuye este tiempo a trabajo humano ni se inventa un desglose de dedicación.
