"""Original 150 BPM electronic campaign score + 20 synthesized style cues. No samples."""
import json,math,numpy as np
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
from pathlib import Path
P=Path(__file__).parent;O=P/'output';O.mkdir(exist_ok=True);S=json.loads((P/'timing.json').read_text());sr=S['audio']['sample_rate'];N=sr*S['duration'];beat=60/S['audio']['bpm'];rng=np.random.default_rng(S['seed']);out=np.zeros((N,2))
def tm(d):return np.arange(round(d*sr))/sr
def hz(m):return 440*2**((m-69)/12)
def osc(f,t):return np.sin(2*np.pi*f*t)
def filt(x,cut,kind='lowpass'):return sosfilt(butter(2,cut,btype=kind,fs=sr,output='sos'),x)
def add(x,start,gain=1,pan=0):
 i=round(start*sr)
 if i<0:x=x[-i:];i=0
 n=min(len(x),N-i)
 if n<1:return
 x=x[:n]*gain;out[i:i+n,0]+=x*np.sqrt((1-pan)/2);out[i:i+n,1]+=x*np.sqrt((1+pan)/2)
def saw(f,t,n=13):return sum(osc(f*k,t)/k for k in range(1,n+1))*2/np.pi
def stack(m,t):return sum(saw(hz(m)*(1+d),t,10) for d in [-.006,-.002,0,.002,.006])/5
# Tight, saturated low end and a restrained sixteenth-note percussion groove.
for k in range(60):
 t=tm(.32);f=46+130*np.exp(-t*46);ph=2*np.pi*np.cumsum(f)/sr;body=np.tanh(np.sin(ph)*1.5)*np.exp(-t*14);click=filt(rng.normal(0,1,len(t)),[2600,9000],'bandpass')*np.exp(-t*300)
 add(body+.14*click,k*beat,gain=.76)
 if k%2:
  t=tm(.2);n=filt(rng.normal(0,1,len(t)),[1000,8500],'bandpass');env=sum(g*np.exp(-np.maximum(t-lag,0)*55)*(t>=lag) for lag,g in [(0,1),(.014,.6),(.029,.5)])
  add(n*env*.7+osc(190,t)*np.exp(-t*32)*.3,k*beat,gain=.25,pan=.08)
for k in range(240):
 start=k*beat/4
 if start>=23.9:break
 t=tm(.05 if k%4!=2 else .14);n=filt(rng.normal(0,1,len(t)),7200,'highpass');env=np.exp(-t*(85 if k%4!=2 else 29));add(n*env,start,gain=.045+(k%4==2)*.04,pan=np.sin(k*1.3)*.45)
roots=[40,36,43,38,40,36,43,38,36,40]
for bar,root in enumerate(roots):
 start=bar*2.4;third=3 if root==40 else 4
 for off in [0,.75,1.5,2.5,3.25,4,4.75,5.5]:
  t=tm(.19);env=(1-np.exp(-t*180))*np.exp(-t*15);f=hz(root);sig=osc(f,t)*.85+np.tanh(filt(saw(f,t),1000)*2)*.35;add(sig*env,start+off*beat,gain=.39)
 for off in [.5,2,3.5,5]:
  t=tm(.38);env=(1-np.exp(-t*100))*np.exp(-t*8);duck=.4+.6*(1-np.exp(-t*25))
  for j,it in enumerate([12,12+third,19]):add(filt(stack(root+it,t),2800)*env*duck,start+off*beat,gain=.095,pan=[-.65,.1,.65][j])
 # Phrase moves in small memorable bursts rather than filling every gap.
 for j,(off,note) in enumerate([(0,76),(1,79),(2.5,83),(4,81),(5,79)]):
  t=tm(.25);env=(1-np.exp(-t*170))*np.exp(-t*15);lead=(osc(hz(note),t)+.27*osc(hz(note)*2,t)+.12*osc(hz(note)*3,t))*env
  add(lead,start+off*beat,gain=.09,pan=-.15);add(lead,start+(off+.75)*beat,gain=.025,pan=.5)
# Signature cues for each requested animation language, synthesized from oscillators/noise.
for i in range(20):
 start=i*1.2;t=tm(.24);n=rng.normal(0,1,len(t));f=440*2**((i%5)/5)
 if i in [0,2,6,8,14]:
  phase=2*np.pi*np.cumsum(f+(1200 if i==6 else 450)*np.exp(-t*25))/sr;sig=(np.sin(phase)+.15*np.sin(phase*2.7))*np.exp(-t*25);add(sig,start+.08,gain=.1,pan=(i%3-1)*.35)
 elif i==1:
  phase=2*np.pi*np.cumsum(190+480*np.exp(-t*18))/sr;add(np.sin(phase)*np.exp(-t*18),start+.05,gain=.18)
 elif i==3:
  sig=sum(osc(550*k,t)/k for k in [1,1.48,2.08,3.17])*np.exp(-t*12);add(sig,start+.04,gain=.12,pan=.2)
 elif i in [4,11,19]:
  add(osc(75,t)*np.exp(-t*32)+filt(n,[800,4500],'bandpass')*np.exp(-t*55)*.35,start+.02,gain=.3)
 elif i in [5,13]:
  add(filt(n,[1300,6500],'bandpass')*np.exp(-t*(45 if i==5 else 14)),start+.06,gain=.12,pan=-.2)
 elif i in [7,9,17]:
  phase=2*np.pi*np.cumsum(150+350*np.exp(-t*35))/sr;add(np.sin(phase)*np.exp(-t*28),start+.08,gain=.22)
 elif i==10:
  add(filt(n,5000,'highpass')*np.exp(-t*11),start,gain=.08)
 elif i==12:
  for j in range(5):add(filt(n,[1300,5000],'bandpass')*np.exp(-t*140),start+.05+j*.052,gain=.16,pan=(j-2)*.15)
 elif i==16:
  for j,m in enumerate([76,79,83,88]):
   tt=tm(.12);square=np.sign(osc(hz(m),tt));add(filt(square,4200)*np.exp(-tt*25),start+.05+j*.12,gain=.07,pan=(j-1.5)*.2)
 elif i==18:
  sig=(osc(hz(64),t)+.4*osc(hz(64)*2,t)+.15*osc(hz(64)*3,t))*np.exp(-t*8);add(sig,start+.05,gain=.2)
 # Narrow, quick suction on the cut, instead of a loud crash every time.
 if i>0:
  tt=tm(.11);nn=filt(rng.normal(0,1,len(tt)),[2200,9000],'bandpass');add(nn*(tt/.11)**2,start-.11,gain=.04,pan=.2)
# Bounce timing comes from the same seeded 120 Hz wall/floor simulation as the image.
def hh(i):
 x=math.sin(i*12.9898+S['seed'])*43758.5453;return x-math.floor(x)
b=[dict(x=130+hh(i)*1650,y=-80-hh(i+33)*500,vx=(hh(i+50)-.5)*900,vy=160+hh(i+20)*350,r=65+hh(i+80)*45) for i in range(12)];events=[]
for fr in range(144):
 dt=1/120
 for o in b:
  o['vy']+=1400*dt;o['x']+=o['vx']*dt;o['y']+=o['vy']*dt
  if o['x']<o['r']:o['x']=o['r'];o['vx']=abs(o['vx'])*.9
  if o['x']>1920-o['r']:o['x']=1920-o['r'];o['vx']=-abs(o['vx'])*.9
  if o['y']>940-o['r']:
   events.append((18+(fr+1)/120,min(1,abs(o['vy'])/1400),o['x']/960-1));o['y']=940-o['r'];o['vy']=-abs(o['vy'])*.8;o['vx']*=.97
 for i in range(len(b)):
  for j in range(i+1,len(b)):
   a,z=b[i],b[j];dx=z['x']-a['x'];dy=z['y']-a['y'];d=math.hypot(dx,dy);r=a['r']+z['r']
   if .001<d<r:
    nx,ny=dx/d,dy/d;over=(r-d)*.5;a['x']-=nx*over;a['y']-=ny*over;z['x']+=nx*over;z['y']+=ny*over;v=(z['vx']-a['vx'])*nx+(z['vy']-a['vy'])*ny
    if v<0:imp=-v*.9;a['vx']-=imp*nx;a['vy']-=imp*ny;z['vx']+=imp*nx;z['vy']+=imp*ny
for start,gain,pan in events:
 t=tm(.10);phase=2*np.pi*np.cumsum(130+250*np.exp(-t*50))/sr;add(np.sin(phase)*np.exp(-t*45),start,gain=.14*gain,pan=pan*.6)
# Close on E minor; rhythm simplifies, the brand and CTA get a three-second hold.
for start in [24,24.8,25.6]:
 t=tm(.4);ph=2*np.pi*np.cumsum(45+110*np.exp(-t*40))/sr;add(np.sin(ph)*np.exp(-t*12),start,gain=.6)
t=tm(3)
for j,m in enumerate([52,59,64,67,71]):
 env=(1-np.exp(-t*20))*np.exp(-t*.8);add(filt(stack(m,t),2300)*env,24,gain=.12,pan=(j-2)*.3)
for j,m in enumerate([76,79,83]):
 t=tm(1.2);add(osc(hz(m),t)*np.exp(-t*4)*(1-np.exp(-t*120)),24+j*.08,gain=.09,pan=(j-1)*.4)
out[:,0]=filt(out[:,0],25,'highpass');out[:,1]=filt(out[:,1],25,'highpass');out=np.tanh(out*1.5);out*=.80/max(np.max(abs(out)),1e-9)
fade=np.ones(N);fade[:240]=np.linspace(0,1,240);n=int(.65*sr);fade[-n:]=np.linspace(1,0,n)**1.3;out*=fade[:,None]
wavfile.write(O/'soundtrack.wav',sr,(out*32767).astype(np.int16));(O/'audio-cues.json').write_text(json.dumps({'bpm':150,'style_seconds':[i*1.2 for i in range(20)],'bounce_cues':events,'closing':24},indent=2)+'\n')
print(json.dumps({'samples':N,'duration':N/sr,'peak_dbfs':20*np.log10(np.max(abs(out))),'rms_dbfs':20*np.log10(np.sqrt(np.mean(out*out)))},indent=2))
