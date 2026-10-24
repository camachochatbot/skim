"""Package source and measured evidence, recording actual elapsed production time."""
from pathlib import Path
from datetime import datetime, timezone
import json, zipfile, hashlib
P=Path(__file__).parent;out=P/'output'
report=json.loads((out/'verification.json').read_text())
start=datetime(2026,10,24,1,5,2,tzinfo=timezone.utc)
end=datetime.now(timezone.utc);elapsed=round((end-start).total_seconds());minutes,seconds=divmod(elapsed,60)
doc=P/'DECISIONES.md';s=doc.read_text().replace('Los resultados medidos y el intervalo real de trabajo se incorporan al final de este documento al concluir la verificación.','')
s+='''## Resultados de verificación

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

'''
s+=f'Inicio medido: **{start.isoformat()}**. Cierre de verificación y documentación para empaquetado: **{end.isoformat(timespec="seconds")}**. Tiempo total transcurrido: **{minutes} min {seconds:02d} s**. Son tiempos de reloj reales de esta sesión, incluyendo inspección, construcción, correcciones, render, revisión y preparación de entrega; no son una estimación de horas de trabajo humano. El render completo registró **286,8 s** en su log. No se inventa un reparto por fases.\n'
doc.write_text(s)
# All editable source, runtime modules, licences and actual review evidence.
files=[p for p in P.iterdir() if p.is_file() and p.suffix in ['.py','.json','.html','.js','.md','.txt']]+[P/'.gitignore']
files+=list((P/'assets').rglob('*'))+list((P/'vendor').rglob('*'))
files += [out/'soundtrack.wav',out/'verification.json',out/'reproduction-check.json',out/'loudness.log',out/'render.log',out/'final-frame.png']+list(out.glob('review-*.jpg'))
files=[p for p in files if p.is_file()]
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(P))+'\n' for p in sorted(files))
(out/'SOURCE_SHA256SUMS.txt').write_text(manifest)
with zipfile.ZipFile(out/'SKIM_fuentes.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,'skim-incoming/'+str(p.relative_to(P)))
 z.writestr('skim-incoming/SHA256SUMS.txt',manifest)
with zipfile.ZipFile(out/'SKIM_fuentes.zip') as z:
 assert z.testzip() is None
 assert 'skim-incoming/scene.js' in z.namelist()
 assert 'skim-incoming/DECISIONES.md' in z.namelist()
 print('ZIP verified:',len(z.namelist()),'files')
for p in [out/'SKIM_Incoming_La_Molina.mp4',out/'SKIM_fuentes.zip',doc]:
 print(p, p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
print(f'Production elapsed: {minutes} min {seconds:02d} s')
