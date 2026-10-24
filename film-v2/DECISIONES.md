# DECISIONES · SKIM Incoming · V2 «Todo conectado»

## Motivo de esta revisión

La primera versión cumplía las dimensiones y la duración, pero el usuario la consideró visualmente pobre y pidió cambiar también la música. Aclaró que quería **ambas cosas: más interfaces animadas y más escenas/transiciones**. Esta revisión cambia la dirección: el paisaje deja de ser una isla o maqueta flotante y se combina con una capa de interfaces de campaña más presente. No se da por aprobada la estética por el hecho de haberla renderizado.

La escena sigue siendo 3D estilizada, no fotorrealista. Todo se genera mediante código. No se han usado modelos generativos de imagen, vídeo o audio, fotografías, metraje, música de terceros ni muestras de sonido. El relieve es una interpretación artística de La Molina, no una representación topográfica ni una visualización oficial de sus instalaciones.

## Dirección visual y jerarquía

Se mantiene blanco nieve, azul hielo y azul noche, con ventanas cálidas en la base. La pantalla completa aporta profundidad y continuidad. Las crestas tienen detalle de ruido fractal y materiales que distinguen nieve y roca según pendiente. Se sustituyen los árboles de conos alternados por ramas trianguladas irregulares con variación de color. Los esquiadores tienen torso, postura flexionada, brazos, guantes, casco, gafas y bastones. Se sigue al protagonista desde atrás, con huellas progresivas y polvo de nieve. No se pretende simular anatomía o dinámica física real.

La interfaz usa tarjetas opacas con perspectiva ligera, sombras, tamaños distintos y animaciones de entrada escalonadas. Los textos se mantienen en coordenadas de pantalla para proteger la lectura. La tipografía principal pasa a DejaVu Sans Bold; el wordmark conserva una variante inclinada. No se proporcionó logo ni manual oficial. El contraste del margen izquierdo se reforzó tras comprobar fondos de nieve clara.

## Escenas y nueve interfaces

| Intervalo | Planos, objetos e interfaces | Texto principal |
|---|---|---|
| 0–3 s | Vuelo panorámico; huellas dibujan SKIM; mapa con curvas de nivel y recorrido animado a La Molina. | Tu grupo. La Molina. |
| 3–7 s | Barrido hacia la cámara de seguimiento; esquiador con estela; forfait con chip y barras; equipo 3D en su propio escenario iluminado; tarjeta de clases con progreso. | Todo listo para disfrutar. |
| 7–11 s | Órbita de la base: refugios, mesas con platos/tazas y autobús. Mapa de coordinación conectado mediante rutas a alojamiento, comidas y seguro. | Vosotros disfrutáis. SKIM coordina. |
| 11–15 s | Retirada al paisaje; las funciones se reúnen en siete nodos alrededor de SKIM; nombre y CTA quedan sostenidos. | SKIM Incoming. Organiza el viaje de tu grupo. |

Las nueve interfaces son: destino, forfait, alquiler/equipo, clases, coordinación, alojamiento, comidas, seguro y constelación de cierre. Los iconos, mapas, barras y recorridos son vectoriales, hechos en código. No se presenta una lista larga de servicios: se muestran en grupos narrativos y se conectan con objetos o escenas.

El forfait y los mapas son elementos conceptuales de un anuncio, no pases válidos, rutas reales, reservas confirmadas o datos operativos. No se incorporan nombres de clientes, precios, horarios, cantidades de pasajeros, métricas de negocio o condiciones de póliza inventadas. Los estados y marcas gráficas representan la propuesta indicada en el encargo.

## Música completamente nueva

Composición electrónica original a **120 BPM**, con centro tonal en **fa menor**. La entrada crea tensión durante tres segundos; el ritmo principal entra exactamente en el descenso. Las transiciones a los 3, 7 y 11 segundos caen en la cuadrícula de medio segundo. Los bloques de 3–7 y 7–11 tienen ocho pulsos cada uno. No se atribuye este tempo a una pista externa: se define en el propio código.

Se sintetizan seno, series armónicas de diente de sierra, ruido filtrado y envolventes. La instrumentación incluye bombo con cuerpo y ataque diferenciados, caja/clap con varios ataques de ruido, charles cerrados/abiertos, subgrave y bajo medio saturado, acordes de varias voces desafinadas, una frase melódica con retardos estéreo, toms antes del descenso, barridos y pequeños pings para interfaces. Un acorde amplio acompaña el cierre y la liberación final dura 0,6 segundos.

Las voces de sintetizador tienen más contenido armónico que los senos simples de la primera versión. El bombo y el bajo reciben más presencia, mientras que la melodía tiene pausas. La mezcla incluye filtrado de infragraves, saturación suave y margen de pico antes de AAC. Todo se genera con NumPy/SciPy; no se cargan archivos de muestras.

## Técnica y reproducción

Three.js 0.170.0, GSAP 3.12.5, HTML/CSS y SVG. El escenario principal y el material de alquiler usan renderizadores separados para integrar un objeto 3D real dentro de una tarjeta. El terreno, los árboles instanciados, el telesilla ocupado, personajes, refugios, autobús y partículas son geometría procedural. Las texturas de texto y de nieve se construyen con canvas. Las bibliotecas y fuentes están incluidas con sus avisos de licencia.

`timing.json` contiene semilla, duración, fps, textos principales, tiempos y transformaciones de interfaces, parámetros de cámaras y tempo. `seek(t)` determina cada fotograma sin acumulación física ni reloj real. Playwright captura los instantes `f / 60`; FFmpeg codifica H.264 con formato YUV420p y rango TV explícito, más AAC estéreo de 48 kHz. El límite es idéntico al del encargo: quince segundos y 900 fotogramas.

La reproducción se documenta en README.md. El código permite regenerar la pieza; no se afirma igualdad binaria entre versiones de navegador, GPU, plataforma y codificador distintas. La entrega anterior sigue disponible en el historial de GitHub.

## Iteraciones y descartes reales

- Se abandonó la isla flotante, la composición exclusivamente de maqueta y la música de la primera entrega.
- Se probó un campo de montañas más grande. El objetivo de cámara quedaba bajo y el relieve ocupaba demasiado cielo, con apariencia de techo. Se rehicieron las crestas con picos localizados, se ajustó la amplitud del ruido y se elevó el objetivo panorámico.
- La primera prueba del nuevo bosque seguía alternando conos claros y oscuros. Se sustituyó por abanicos de ramas irregulares, se redujo el tamaño/densidad y se amplió el corredor de pista para evitar árboles enormes frente a cámara.
- El primer seguimiento mostraba al esquiador de frente. Se cambió el desplazamiento de cámara para seguirlo desde atrás y mantener la llegada a la base en la dirección de avance.
- Se revisaron hombros, rodillas y balanceo de cuerpo, curvas de los esquís y polvo analítico. Son movimientos artísticos, no una simulación biomecánica.
- La primera maqueta del equipo tenía extremos esféricos y botas de cajas apiladas. Se sustituyeron por esquís extruidos con puntas curvas y botas de perfil con biseles y hebillas.
- Se volvieron opacas las tarjetas que dejaban pasar los árboles del fondo y se amplió el degradado bajo los titulares para evitar pérdida de letras sobre nieve clara.
- Se eliminó un cambio instantáneo del desplazamiento horizontal de cámara; ahora se interpola en las transiciones.
- La comprobación de layout marcó el forfait por sus muescas laterales: cada muesca sobresale deliberadamente 11 px. Se registró esa excepción decorativa y se añadió una comprobación de texto independiente. No se recortó ni se ocultó texto para hacer pasar la prueba.
- Se revisaron especialmente 2,85 / 3 / 3,1 s, 6,9 / 7 s y 11 s. La caída de texto entre capítulos y el barrido diagonal son intencionados. El CTA no tiene salida al final.

- Durante un primer render de V2 se reconsideraron las proporciones del plano cercano: casco, torso y guantes seguían pareciendo demasiado grandes. Se interrumpió ese render después de superar 720 fotogramas, se ajustaron las proporciones y se lanzó un render completo nuevo. El archivo interrumpido no forma parte de la entrega.
- Se cacheó el mapa de sombras del escenario estático. Los elementos móviles dejan de proyectarse en ese mapa y los esquiadores reciben sombras de contacto suaves que siguen su posición. Es una aproximación artística explícita, no una simulación física de sombras.

## Alcance de revisión

Se distinguen las capturas de la composición fuente y las del MP4 exportado. El verificador decodifica el archivo completo y genera hojas numeradas que representan todos sus fotogramas; también extrae el frame 899. La revisión visual se hace con estas secuencias y vistas de mayor tamaño. No se afirma haber visto el vídeo con reproducción audiovisual en tiempo real.

No hay herramienta de escucha directa en esta sesión. La banda sonora se verifica técnicamente: duración, finitud, margen de pico, ausencia de silencio inesperado y correspondencia temporal con la señal original. No se presenta esa comprobación como una escucha humana ni como una aprobación subjetiva de la música por el usuario.

## Resultados medidos

- Vídeo: **1920 × 1080**, **60/1 fps**, **900 fotogramas**, **15.000000 s**, H.264 / yuv420p. Audio: AAC estéreo a **48000 Hz**, **15.000000 s**.
- Decodificación de principio a fin: **passed**. Fotogramas negros/vacíos: **0**. Diferencia mínima entre fotogramas consecutivos reducidos: **0.021991**; no se detectan frames idénticos.
- Audio AAC decodificado: pico de muestra **-2.315 dBFS**, RMS **-16.958 dBFS**, correlación con el WAV **0.999764**, desplazamiento **0 muestras**.
- EBU R128 medido sobre el MP4: **-15.8 LUFS integrados**, pico real **-2.3 dBFS**. No se presentan estas cifras como una escucha subjetiva.
- Síntesis repetida: WAV idéntico, SHA-256 `cef7e35023aa1268c69643e4c7b4ebb596c3ec0615db838e24c17a7a0e2021b2`.
- Comprobación del navegador: trece instantes, sin errores de página; paneles plenamente visibles y textos principales dentro de 1920 × 1080. Las muescas del forfait son la excepción decorativa de 11 px documentada.
- Se inspeccionaron en orden las 18 hojas extraídas del MP4, que representan sus 900 fotogramas, y se revisaron planos grandes de cada bloque, sus transiciones y el fotograma final 899. No se detectó texto principal cortado. Las salidas de texto entre capítulos, los recortes del paisaje y el barrido diagonal son intencionados. El cierre completo se sostiene desde aproximadamente 11,36 s hasta el último frame.
- JavaScript pasa comprobación sintáctica como módulo ES; los scripts Python compilan. No se ejecutaron HyperFrames lint/check; la evidencia corresponde al render propio, al verificador y a la revisión descrita.
- Comparación puntual de la captura del código final a 13 s con el frame 780 del MP4: error absoluto medio **1.4444 / 255**, incluyendo compresión. No es una prueba binaria de igualdad ni un segundo render completo.
- El render definitivo registró **405.0 s** en su log.

Los resultados legibles por máquina, las hojas de revisión, el WAV y los logs finales se incluyen en el ZIP. El render interrumpido no se incluye. El MP4 se entrega aparte.

## Tiempo real de producción

Primera medición de esta revisión: **2026-10-24T03:45:42+02:00**. Cierre de verificación y preparación del paquete: **2026-10-24T04:17:18+02:00**. Tiempo transcurrido medido de V2: **31 min 36 s**. Incluye construcción, pruebas visuales, correcciones, render interrumpido, render final, documentación y revisión hasta este punto; el empaquetado y la subida posteriores son operaciones adicionales.

La primera fase de producción registró **14 min 46 s** en su documento. La suma de los dos intervalos de producción medidos es **46 min 22 s**. No incluye las rondas intermedias de conversación/soporte de descarga ni la publicación posterior. No se inventa un reparto de horas humanas.
