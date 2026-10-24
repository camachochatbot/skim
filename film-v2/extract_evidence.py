"""Extract review stills from the actual V2 MP4 and compare a source-frame check."""
from pathlib import Path
import subprocess,json,numpy as np
from PIL import Image
P=Path(__file__).parent;O=P/'output';video=O/'SKIM_Incoming_La_Molina_V2.mp4'
for frame,name in [(354,'poster-equipment.jpg'),(570,'poster-base.jpg'),(780,'reproduction-check.png'),(216,'poster-descent.jpg')]:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-update','1',str(O/name)],check=True)
x=np.asarray(Image.open(O/'reproduction-check.png')).astype(float);y=np.asarray(Image.open(O/'preview-13.00.jpg')).astype(float)
mae=float(np.abs(x-y).mean());assert mae<3,mae
(O/'reproduction-check.json').write_text(json.dumps({'time_seconds':13,'mean_absolute_pixel_error_0_255':mae,'threshold':3,'note':'Source preview versus exported MP4 frame 780, including lossy JPEG and H.264.'},indent=2)+'\n')
print('Source/export frame check MAE:',mae)
