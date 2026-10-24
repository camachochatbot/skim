"""Validate actual export; decode every frame, measure audio and build complete visual review sheets."""
import json, subprocess, pathlib, numpy as np
from scipy.io import wavfile
from scipy.signal import correlate, correlation_lags
from PIL import Image, ImageDraw, ImageFont
P=pathlib.Path(__file__).resolve().parent; out=P/'output'; video=out/'SKIM_Incoming_La_Molina.mp4'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert v['r_frame_rate']=='60/1' and v['avg_frame_rate']=='60/1'
assert int(v['nb_read_frames'])==900
assert float(v['duration'])==15.0 and float(a['duration'])==15.0
assert a['sample_rate']=='48000' and a['channels']==2
run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
# Every exported frame is represented on one of 18 numbered sheets, not source previews.
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-vf','scale=320:180','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
font=ImageFont.truetype(str(P/'assets/Text.ttf'),13)
frame_means=[];motion=[];previous=None
for sheet in range(18):
 im=Image.new('RGB',(1600,10*202),'#081b2b');d=ImageDraw.Draw(im)
 for slot in range(50):
  f=sheet*50+slot; raw=proc.stdout.read(320*180*3);assert len(raw)==320*180*3
  arr=np.frombuffer(raw,np.uint8);frame_means.append(float(arr.mean()));
  if previous is not None:motion.append(float(np.mean(np.abs(arr.astype(np.int16)-previous))))
  previous=arr.astype(np.int16)
  frame=Image.frombytes('RGB',(320,180),raw);x=(slot%5)*320;y=(slot//5)*202
  im.paste(frame,(x,y));d.text((x+5,y+182),f'{f:03d} · {f/60:06.3f} s',font=font,fill='#a1e5fb')
 im.save(out/f'review-{sheet+1:02d}.jpg',quality=92)
assert proc.wait()==0
assert min(frame_means)>15 and max(frame_means)<235, 'Black/blank frame'
assert min(motion)>.001, 'Duplicate frozen frame'
# Higher resolution overview at scene midpoints plus transition shoulders.
proc=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf','fps=4,scale=480:270','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],check=True,capture_output=True)
assert len(proc.stdout)==60*480*270*3
for sheet in range(4):
 im=Image.new('RGB',(1920,5*300),'#081b2b');d=ImageDraw.Draw(im)
 for slot in range(15):
  f=sheet*15+slot;frame=Image.frombytes('RGB',(480,270),proc.stdout[f*480*270*3:(f+1)*480*270*3]);x=(slot%3)*640;y=(slot//3)*300
  im.paste(frame,(x,y));d.text((x+5,y+274),f'{f/4:.2f} s',font=font,fill='#a1e5fb')
 im.save(out/f'overview-{sheet+1}.jpg',quality=93)
# Check actual AAC signal (not just the source WAV).
r=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','pipe:1'],check=True,capture_output=True)
audio=np.frombuffer(r.stdout,np.float32).reshape(-1,2);peak=float(np.max(np.abs(audio)));rms=float(np.sqrt(np.mean(audio*audio)))
assert np.isfinite(audio).all() and peak<1 and rms>.02
assert np.max(np.abs(audio[:720000][-240:]))<.04
_,src=wavfile.read(out/'soundtrack.wav');original=src.astype(np.float64).mean(axis=1)/32768
decoded=audio[:len(original)].mean(axis=1)
cc=correlate(decoded[::8],original[::8],mode='full',method='fft');lags=correlation_lags(len(decoded[::8]),len(original[::8]),mode='full');lag_samples=int(lags[np.argmax(cc)])*8
assert abs(lag_samples)<=48, 'Soundtrack synchronization shifted by more than 1 ms'
correlation=float(np.corrcoef(decoded,original)[0,1]);assert correlation>.98
blocks=[float(np.sqrt(np.mean(audio[i:i+4800]**2))) for i in range(0,min(len(audio),720000),4800)]
assert min(blocks[:-5])>.003,'Unexpected silence before final release'
run(['ffmpeg','-v','error','-i',str(video),'-vf','select=eq(n\\,899)','-frames:v','1','-update','1',str(out/'final-frame.png')])
report={'video':{'codec':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frames':v['nb_read_frames'],'duration':v['duration'],'pixel_format':v['pix_fmt']},'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'duration':a['duration'],'decoded_peak_dbfs':20*np.log10(peak),'decoded_rms_dbfs':20*np.log10(rms),'alignment_offset_samples':lag_samples,'correlation_with_original_score':correlation},'complete_decode':'passed','black_or_blank_frames':0,'minimum_frame_difference':min(motion),'review_sheets':18,'frames_represented':900,'contact_sheet_sampling':'All 900 frames; 50 per sheet. Additional 4 fps overviews.','transition_times':[3,7,11]}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
