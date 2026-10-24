"""Package V2 sources and actual evidence; record measured elapsed production time."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import zipfile,hashlib,json,re
P=Path(__file__).parent;O=P/'output'
r=json.loads((O/'verification.json').read_text());rep=json.loads((O/'audio-repeatability.json').read_text());layout=json.loads((O/'layout-check.json').read_text())
assert r['video']['frames']=='900' and r['audio']['alignment_offset_samples']==0 and not layout['page_errors']
log=(O/'loudness.log').read_text();summary=log[log.rfind('Summary:'):]
L=re.search(r'I:\s*([-0-9.]+) LUFS',summary);TP=re.search(r'Peak:\s*([-0-9.]+) dBFS',summary)
start=datetime(2026,10,24,1,45,42,tzinfo=timezone.utc);end=datetime.now(timezone.utc);elapsed=round((end-start).total_seconds());m,s=divmod(elapsed,60);cum=886+elapsed;cm,cs=divmod(cum,60)
p=P/'DECISIONES.md';doc=p.read_text().split('## Resultados medidos')[0]
doc+='\n## Resultados medidos\n\n'
doc+=f"- Vídeo: **{r['video']['width']} × {r['video']['height']}**, **{r['video']['fps']} fps**, **{r['video']['frames']} fotogramas**, **{r['video']['duration']} s**, H.264 / {r['video']['pixel_format']}. Audio: AAC estéreo a **{r['audio']['sample_rate']} Hz**, **{r['audio']['duration']} s**.\n"
doc+=f"- Decodificación de principio a fin: **{r['complete_decode']}**. Fotogramas negros/vacíos: **{r['black_or_blank_frames']}**. Diferencia mínima entre fotogramas consecutivos reducidos: **{r['minimum_frame_difference']:.6f}**; no se detectan frames idénticos.\n"
doc+=f"- Audio AAC decodificado: pico de muestra **{r['audio']['decoded_peak_dbfs']:.3f} dBFS**, RMS **{r['audio']['decoded_rms_dbfs']:.3f} dBFS**, correlación con el WAV **{r['audio']['correlation_with_original_score']:.6f}**, desplazamiento **{r['audio']['alignment_offset_samples']} muestras**.\n"
if L and TP:doc+=f"- EBU R128 medido sobre el MP4: **{L.group(1)} LUFS integrados**, pico real **{TP.group(1)} dBFS**. No se presentan estas cifras como una escucha subjetiva.\n"
doc+=f"- Síntesis repetida: WAV idéntico, SHA-256 `{rep['sha256']}`.\n"
doc+='- Comprobación del navegador: trece instantes, sin errores de página; paneles plenamente visibles y textos principales dentro de 1920 × 1080. Las muescas del forfait son la excepción decorativa de 11 px documentada.\n'
doc+='- Se inspeccionaron en orden las 18 hojas extraídas del MP4, que representan sus 900 fotogramas, y se revisaron planos grandes de cada bloque, sus transiciones y el fotograma final 899. No se detectó texto principal cortado. Las salidas de texto entre capítulos, los recortes del paisaje y el barrido diagonal son intencionados. El cierre completo se sostiene desde aproximadamente 11,36 s hasta el último frame.\n'
doc+='- JavaScript pasa comprobación sintáctica como módulo ES; los scripts Python compilan. No se ejecutaron HyperFrames lint/check; la evidencia corresponde al render propio, al verificador y a la revisión descrita.\n'
if (O/'reproduction-check.json').exists():
 q=json.loads((O/'reproduction-check.json').read_text());doc+=f"- Comparación puntual de la captura del código final a 13 s con el frame 780 del MP4: error absoluto medio **{q['mean_absolute_pixel_error_0_255']:.4f} / 255**, incluyendo compresión. No es una prueba binaria de igualdad ni un segundo render completo.\n"
render_match=re.search(r'RENDER COMPLETE: ([0-9.]+)s',(O/'render.log').read_text())
if render_match:doc+=f"- El render definitivo registró **{render_match.group(1)} s** en su log.\n"
doc+='\nLos resultados legibles por máquina, las hojas de revisión, el WAV y los logs finales se incluyen en el ZIP. El render interrumpido no se incluye. El MP4 se entrega aparte.\n\n## Tiempo real de producción\n\n'
tz=ZoneInfo('Europe/Madrid');doc+=f'Primera medición de esta revisión: **{start.astimezone(tz).isoformat(timespec="seconds")}**. Cierre de verificación y preparación del paquete: **{end.astimezone(tz).isoformat(timespec="seconds")}**. Tiempo transcurrido medido de V2: **{m} min {s:02d} s**. Incluye construcción, pruebas visuales, correcciones, render interrumpido, render final, documentación y revisión hasta este punto; el empaquetado y la subida posteriores son operaciones adicionales.\n\n'
doc+=f'La primera fase de producción registró **14 min 46 s** en su documento. La suma de los dos intervalos de producción medidos es **{cm} min {cs:02d} s**. No incluye las rondas intermedias de conversación/soporte de descarga ni la publicación posterior. No se inventa un reparto de horas humanas.\n'
p.write_text(doc)
files=[x for x in P.iterdir() if x.is_file() and x.suffix in ['.py','.js','.json','.html','.md','.txt']]+[P/'.gitignore']
files+=list((P/'assets').rglob('*'))+list((P/'vendor').rglob('*'))
files+=[O/n for n in ['soundtrack.wav','verification.json','audio-repeatability.json','layout-check.json','loudness.log','render.log','final-frame.png','reproduction-check.json','preview-13.00.jpg'] if (O/n).exists()]
files+=list(O.glob('review-*.jpg'));files=[x for x in files if x.is_file()]
manifest=''.join(hashlib.sha256(x.read_bytes()).hexdigest()+'  '+str(x.relative_to(P))+'\n' for x in sorted(files))
with zipfile.ZipFile(O/'SKIM_fuentes_V2.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for x in files:z.write(x,'skim-incoming-v2/'+str(x.relative_to(P)))
 z.writestr('skim-incoming-v2/SHA256SUMS.txt',manifest)
with zipfile.ZipFile(O/'SKIM_fuentes_V2.zip') as z:assert z.testzip() is None;print('ZIP verified:',len(z.namelist()),'files')
print(f'V2 measured elapsed: {m} min {s:02d} s')
