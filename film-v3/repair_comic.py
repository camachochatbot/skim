"""Re-render only the corrected 72-frame comic segment and reuse the validated other regions."""
import subprocess,shutil
from pathlib import Path
P=Path(__file__).parent;O=P/'output';movie=O/'SKIM_20_estilos_V3.mp4';base=O/'render-before-comic.mp4'
assert movie.exists();shutil.copyfile(movie,base)
subprocess.run(['python','render.py','--port','8804','--start','13.2','--frames','72','--video-only','--output','comic-patch.mp4'],cwd=P,check=True)
fc='[0:v]trim=end_frame=792,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=864,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-i',str(base),'-i',str(O/'comic-patch.mp4'),'-i',str(O/'soundtrack.wav'),'-filter_complex',fc,'-map','[v]','-map','2:a:0','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_range','tv','-r','60','-c:a','aac','-b:a','320k','-ar','48000','-t','27','-movflags','+faststart',str(movie)],check=True)
print('Comic region replaced; retained video regions re-encoded once. Run verify.py on the final file.')
