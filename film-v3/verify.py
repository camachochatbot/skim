"""Verify V3 MP4, audio alignment, every decoded frame and all twenty style segments."""
from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.io import wavfile
from scipy.signal import correlate,correlation_lags
P=Path(__file__).parent;O=P/'output';S=json.loads((P/'timing.json').read_text());video=O/'SKIM_20_estilos_V3.mp4';frames=S['fps']*S['duration']
def run(a):return subprocess.run(a,check=True,capture_output=True,text=True).stdout
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'])==(S['width'],S['height']);assert v['r_frame_rate']==v['avg_frame_rate']=='60/1';assert int(v['nb_read_frames'])==frames==1620;assert float(v['duration'])==float(a['duration'])==S['duration']==27;assert a['sample_rate']=='48000' and a['channels']==2
run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-vf','scale=240:135','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE);font=ImageFont.truetype(str(P/'assets/Text.ttf'),12);motions=[];previous=None;blank=0
for sheet in range(18):
 im=Image.new('RGB',(2400,9*157),'#071c32');d=ImageDraw.Draw(im)
 for slot in range(90):
  f=sheet*90+slot;raw=proc.stdout.read(240*135*3);assert len(raw)==240*135*3;arr=np.frombuffer(raw,np.uint8)
  if arr.std()<2 and arr.max()<12:blank+=1
  if previous is not None:motions.append(float(np.abs(arr.astype(np.int16)-previous).mean()))
  previous=arr.astype(np.int16);pic=Image.frombytes('RGB',(240,135),raw);x=(slot%10)*240;y=(slot//10)*157;im.paste(pic,(x,y));d.text((x+4,y+137),f'{f:04d} · {f/60:05.2f}s',font=font,fill='#b8f3ff')
 im.save(O/f'review-{sheet+1:02d}.jpg',quality=92)
assert proc.wait()==0 and blank==0
# Intentional reading holds can repeat frames; each style must show internal motion beyond the entrance.
style_motion=[]
for i in range(20):
 m=float(sum(motions[i*72+20:i*72+60]));assert m>.5,(i,m);style_motion.append({'style':S['scenes'][i]['style'],'settled_window_motion':m})
# Extract every style midpoint from the actual MP4, plus the held closing and final frame.
for i in range(20):
 frame=48+i*72;run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-update','1',str(O/f'style-{i+1:02d}.jpg')])
for frame,name in [(1530,'closing.jpg'),(1619,'final-frame.png')]:run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-update','1',str(O/name)])
over=Image.new('RGB',(1920,5*300),'#071c32');d=ImageDraw.Draw(over);fnt=ImageFont.truetype(str(P/'assets/Text.ttf'),16)
for i in range(20):
 pic=Image.open(O/f'style-{i+1:02d}.jpg').resize((480,270));x=i%4*480;y=i//4*300;over.paste(pic,(x,y));d.text((x+7,y+274),f'{i+1:02d} · '+S['scenes'][i]['style'],font=fnt,fill='white')
over.save(O/'all-styles-export.jpg',quality=94)
r=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','pipe:1'],check=True,capture_output=True);audio=np.frombuffer(r.stdout,np.float32).reshape(-1,2);peak=float(abs(audio).max());rms=float(np.sqrt(np.mean(audio**2)));assert np.isfinite(audio).all() and peak<1 and rms>.02
_,src=wavfile.read(O/'soundtrack.wav');original=src.astype(float).mean(axis=1)/32768;decoded=audio[:len(original)].mean(axis=1);cc=correlate(decoded[::8],original[::8],mode='full',method='fft');lags=correlation_lags(len(decoded[::8]),len(original[::8]),mode='full');lag=int(lags[np.argmax(cc)])*8;cor=float(np.corrcoef(decoded,original)[0,1]);assert abs(lag)<=48 and cor>.98
blocks=[np.sqrt(np.mean(audio[i:i+4800]**2)) for i in range(0,27*48000,4800)];assert min(blocks[:-6])>.002;assert abs(audio[:len(original)][-240:]).max()<.04
report={'video':{'codec':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frames':v['nb_read_frames'],'duration':v['duration'],'pixel_format':v['pix_fmt']},'audio':{'codec':a['codec_name'],'channels':2,'sample_rate':a['sample_rate'],'duration':a['duration'],'peak_dbfs':20*np.log10(peak),'rms_dbfs':20*np.log10(rms),'alignment_offset_samples':lag,'correlation_with_original':cor},'decode':'passed','blank_frames':blank,'review_sheets':18,'represented_frames':frames,'identical_adjacent_pairs':sum(x==0 for x in motions),'reading_holds':'Repeated frames are allowed for settled split-flap/blueprint holds; each style has verified internal motion.','style_motion':style_motion}
(O/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
