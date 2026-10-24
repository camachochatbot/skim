"""SKIM V2: original cinematic electronic score, synthesized without samples."""
import json,numpy as np
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
from pathlib import Path
P=Path(__file__).parent;(P/'output').mkdir(exist_ok=True)
spec=json.loads((P/'timing.json').read_text());sr=spec['audio']['sample_rate'];N=sr*spec['duration'];beat=60/spec['audio']['bpm'];rng=np.random.default_rng(spec['seed']);out=np.zeros((N,2),np.float64)
def tm(d):return np.arange(round(d*sr))/sr
def hz(m):return 440*2**((m-69)/12)
def sin(f,t):return np.sin(2*np.pi*f*t)
def filt(x,cut,kind='lowpass',order=2):return sosfilt(butter(order,cut,fs=sr,btype=kind,output='sos'),x)
def add(x,start,gain=1,pan=0):
 i=round(start*sr)
 if i<0:x=x[-i:];i=0
 n=min(len(x),N-i)
 if n<=0:return
 x=x[:n]*gain;out[i:i+n,0]+=x*np.sqrt((1-pan)/2);out[i:i+n,1]+=x*np.sqrt((1+pan)/2)
def saw(f,t,harmonics=15):
 y=np.zeros_like(t)
 for k in range(1,harmonics+1):y+=sin(f*k,t)/k
 return y*(2/np.pi)
def supersaw(m,t):
 f=hz(m);return sum(saw(f*(1+d),t,12) for d in [-.006,-.002,0,.0025,.0065])/5
# Opening: deep pulses, filtered cinematic chord and a pitched upward transition.
for s in [0,.5,1,1.5,2,2.5]:
 t=tm(.38);phase=2*np.pi*np.cumsum(42+62*np.exp(-t*27))/sr
 add(np.sin(phase)*np.exp(-t*14),s,gain=.35)
t=tm(3.3);env=(1-np.exp(-t*2))*np.exp(-np.maximum(t-2.65,0)*6)
for m in [53,60,65,68]:
 sig=filt(supersaw(m,t),1300)*env
 add(sig,0,gain=.10,pan=(-.6 if m%2 else .6))
# Layered kick: sine body, short saturation and an original noise transient.
for k in range(24):
 start=3+k*beat;t=tm(.42);freq=45+125*np.exp(-t*39);phase=2*np.pi*np.cumsum(freq)/sr
 kick=np.tanh(np.sin(phase)*1.8)*np.exp(-t*12)
 click=filt(rng.normal(0,1,len(t)),[2200,8000],'bandpass')*np.exp(-t*350)
 add(kick+click*.22,start,gain=.8)
# Snare/clap has several offset synthetic noise attacks, not a sample.
for k in range(12):
 start=3.5+k;t=tm(.26);noise=filt(rng.normal(0,1,len(t)),[900,8500],'bandpass')
 env=np.zeros_like(t)
 for lag,g in [(0,1),(.012,.72),(.027,.64),(.046,.5)]:env+=g*np.exp(-np.maximum(t-lag,0)*55)*(t>=lag)
 add(noise*env,start,gain=.22,pan=-.15)
 add(sin(188,t)*np.exp(-t*30),start,gain=.16,pan=.1)
 add(filt(noise,3500)*np.exp(-t*15),start+.025,gain=.12,pan=.45)
# Sixteenth hats and offbeat open hats, with deterministic dynamics and stereo motion.
for k in range(96):
 start=3+k*.125
 if start>=14.65:break
 t=tm(.055 if k%4!=2 else .19);n=filt(rng.normal(0,1,len(t)),7400,'highpass')
 env=np.exp(-t*(70 if k%4!=2 else 23));vel=.06+(k%4==2)*.045+rng.uniform(-.012,.012)
 add(n*env,start,gain=vel,pan=.35*np.sin(k*1.7))
# F minor, Db, Ab, Eb, F minor: sub plus a filtered, saturated mid bass.
roots=[41,37,44,39,41,41]
for bar,root in enumerate(roots):
 start=3+bar*2
 for off in [0,.75,1.5,2,2.75,3.5]:
  t=tm(.24);f=hz(root);env=(1-np.exp(-t*200))*np.exp(-t*10)
  sub=sin(f,t);mid=filt(saw(f,t,16),900 if bar<2 else 1500)
  add((sub*.85+np.tanh(mid*2)*.35)*env,start+off*beat,gain=.42)
 # Wide chord stabs with a rolling sidechain envelope and harmonic motion.
 third=3 if bar in [0,4,5] else 4
 for off in [0,1.5,2.5,3.5]:
  t=tm(.45);env=(1-np.exp(-t*100))*np.exp(-t*6.5);duck=.25+.75*(1-np.exp(-t*22))
  for idx,interval in enumerate([12,12+third,19]):
   sig=filt(supersaw(root+interval,t),2600+bar*160)*env*duck
   add(sig,start+off*beat,gain=.105,pan=[-.65,.5,.1][idx])
# A small memorable lead phrase rather than a constant high register arpeggio.
phrase=[(0,72),(.75,75),(1.5,77),(2.5,80),(3.25,79)]
for bar in range(5):
 for off,m in phrase:
  start=4.5+bar*2+off*beat
  if start>13.9:continue
  t=tm(.35);f=hz(m);env=(1-np.exp(-t*170))*np.exp(-t*10)
  lead=(sin(f,t)+.3*sin(f*2,t)+.16*sin(f*3,t)+.07*sin(f*5,t))*env
  add(lead,start,gain=.16,pan=-.15)
  add(lead,start+.375,gain=.052,pan=.6)
  add(lead,start+.75,gain=.022,pan=-.6)
# Three original transition risers/impacts align exactly with the visual chapters.
for cut in [3,7,11]:
 t=tm(.75);n=filt(rng.normal(0,1,len(t)),[700,9500],'bandpass');env=(t/.75)**2
 freq=170+1900*(t/.75)**2;tonal=np.sin(2*np.pi*np.cumsum(freq)/sr)
 add(n*env*.3+tonal*env*.12,cut-.75,gain=.47,pan=-.25)
 t=tm(.8);add((sin(43,t)+.3*sin(86,t))*np.exp(-t*8),cut,gain=.46)
 n=filt(rng.normal(0,1,len(t)),[2500,11000],'bandpass')
 add(n*np.exp(-t*8),cut,gain=.12,pan=.3)
# Interface tactile pings: short additive resonances, quiet and timed individually.
for i,start in enumerate([.65,4.08,4.43,5.43,7.18,7.43,8.08,8.73]):
 t=tm(.13);f=[660,880,990,1100][i%4];x=(sin(f,t)+.15*sin(f*2.71,t))*np.exp(-t*38)
 add(x,start,gain=.09,pan=np.sin(i)*.4)
# Original tom fill before the drop; a final broad F minor chord lets the CTA breathe.
for start,f in [(2.5,150),(2.625,125),(2.75,100),(2.875,80)]:
 t=tm(.16);ph=2*np.pi*np.cumsum(f+40*np.exp(-t*40))/sr;add(np.sin(ph)*np.exp(-t*28),start,gain=.3,pan=(f-110)/120)
t=tm(3.9);env=(1-np.exp(-t*12))*np.exp(-t*.65)
for idx,m in enumerate([53,60,65,68,72]):
 sig=filt(supersaw(m,t),2200)*env
 add(sig,11.05,gain=.09,pan=(-.75+idx*.375))
# Remove DC/infra bass, soft bus saturation, and leave headroom for AAC reconstruction.
out[:,0]=filt(out[:,0],25,'highpass');out[:,1]=filt(out[:,1],25,'highpass')
out=np.tanh(out*1.25);out*=.77/max(np.max(abs(out)),1e-9)
fade=np.ones(N);fade[:240]=np.linspace(0,1,240);n=int(.6*sr);fade[-n:]=np.linspace(1,0,n)**1.3;out*=fade[:,None]
wavfile.write(P/'output/soundtrack.wav',sr,(out*32767).astype(np.int16))
print(json.dumps({'samples':N,'duration':N/sr,'bpm':spec['audio']['bpm'],'peak_dbfs':20*np.log10(np.max(abs(out))),'rms_dbfs':20*np.log10(np.sqrt(np.mean(out*out)))},indent=2))
