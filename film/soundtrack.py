"""Original deterministic 128 BPM electronic score. Oscillators and noise only."""
import json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
from pathlib import Path
P=Path(__file__).parent
(P/'output').mkdir(exist_ok=True)
spec=json.loads((P/'timing.json').read_text()); sr=spec['audio']['sample_rate']; duration=spec['duration']; bpm=spec['audio']['bpm']; N=sr*duration
rng=np.random.default_rng(spec['seed']); out=np.zeros((N,2),np.float64); beat=60/bpm

def add(x,start,pan=0,gain=1):
 i=round(start*sr)
 if i<0:x=x[-i:];i=0
 n=min(len(x),N-i)
 if n<=0:return
 x=x[:n]*gain
 out[i:i+n,0]+=x*np.sqrt((1-pan)/2);out[i:i+n,1]+=x*np.sqrt((1+pan)/2)

def times(d):return np.arange(round(d*sr))/sr

def osc(freq,t):return np.sin(2*np.pi*freq*t)

def note(m):return 440*2**((m-69)/12)

# Tuned, descending sine kick with a synthesized click; no sample files.
for k in range(32):
 t=times(.36); freq=46+95*np.exp(-t*36); phase=2*np.pi*np.cumsum(freq)/sr
 kick=np.sin(phase)*np.exp(-t*13)+rng.normal(0,1,len(t))*np.exp(-t*250)*.16
 add(kick,k*beat,gain=.84 if k<24 else .7)
 if k%2==1:
  t=times(.19);noise=rng.normal(0,1,len(t));noise=sosfilt(butter(2,1800,fs=sr,btype='highpass',output='sos'),noise)
  snare=noise*np.exp(-t*28)*.36+osc(185,t)*np.exp(-t*40)*.22
  add(snare,k*beat,gain=.65)
# Syncopated metallic closed/open hats.
for k in range(64):
 t=times(.07 if k%2==0 else .13);noise=rng.normal(0,1,len(t));noise=sosfilt(butter(2,6500,fs=sr,btype='highpass',output='sos'),noise)
 add(noise*np.exp(-t*(65 if k%2==0 else 32)),k*beat/2,pan=(-1 if k%2 else 1)*.35,gain=.11)
# D minor / Bb / F / C progression, 4-beat bars. Rounded bass and wide chord bed.
roots=[38,34,41,36,38,34,41,36]
for bar,root in enumerate(roots):
 for k in [0,1.5,2,3.5]:
  t=times(.31);f=note(root);bass=(osc(f,t)+.28*osc(f*2,t)+.12*osc(f*3,t));env=(1-np.exp(-t*100))*np.exp(-t*9)
  add(bass*env,bar*4*beat+k*beat,gain=.37)
 t=times(4*beat+.35);env=np.minimum(t/.14,1)*np.minimum((len(t)/sr-t)/.35,1)
 third=3 if bar%4 in [0] else 4
 for interval in [12,12+third,19,26]:
  f=note(root+interval)
  for pan,detune in [(-.65,.998),(.65,1.002)]:
   # Harmonic stack with slow timbral shimmer; ducked by the kick.
   sig=(osc(f*detune,t)+.18*osc(f*2*detune,t)+.06*osc(f*3*detune,t))
   duck=.45+.55*(1-np.exp(-(t%beat)*10))
   add(sig*env*duck,bar*4*beat,pan,gain=.054)
# Sparkling sixteenth-note arpeggio entering with the descent.
pattern=[74,77,81,86,81,77,72,77,74,77,81,84,81,79,77,72]
for k in range(104):
 start=3+k*beat/4
 if start>14.2:break
 t=times(.28);f=note(pattern[k%16]);env=(1-np.exp(-t*220))*np.exp(-t*17)
 sig=(osc(f,t)+.24*osc(f*2,t))*env
 add(sig,start,pan=np.sin(k*1.7)*.65,gain=.13)
 add(sig,start+beat*.75,pan=-np.sin(k*1.7)*.65,gain=.045)
# Deliberate swooshes/impacts at the three chapter cuts.
for cut in spec['audio']['transition_seconds']:
 t=times(.65);noise=rng.normal(0,1,len(t));noise=sosfilt(butter(2,[700,8500],fs=sr,btype='bandpass',output='sos'),noise)
 env=(t/.65)**2
 add(noise*env,cut-.65,pan=-.25,gain=.16)
 t=times(.8);add((osc(52,t)+.3*osc(104,t))*np.exp(-t*8),cut,gain=.45)
 t=times(.42);noise=rng.normal(0,1,len(t));noise=sosfilt(butter(2,4200,fs=sr,btype='highpass',output='sos'),noise)
 add(noise*np.exp(-t*10),cut,pan=.3,gain=.12)
# Resolved, clean logo chime, entirely additive synthesis.
for n in [62,69,74,77]:
 t=times(2.4);sig=(osc(note(n),t)+.24*osc(note(n)*2.003,t))*np.exp(-t*2.5)*(1-np.exp(-t*180))
 add(sig,11.15+(n-62)*.012,pan=(n-70)/20,gain=.14)
# Gentle saturation, deterministic headroom, short entrance and final release.
out=np.tanh(out*.9);out*=.88/max(np.max(np.abs(out)),1e-6)
fade=np.ones(N);fade[:240]=np.linspace(0,1,240);tail=int(.52*sr);fade[-tail:]=np.linspace(1,0,tail)**1.4;out*=fade[:,None]
wavfile.write(P/'output/soundtrack.wav',sr,(out*32767).astype(np.int16))
print(json.dumps({'samples':N,'seconds':N/sr,'sample_peak_dbfs':float(20*np.log10(np.max(abs(out)))),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(out*out))))},indent=2))
