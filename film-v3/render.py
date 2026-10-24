"""Serve local source, seek exact frames in Chromium and stream JPEG frames to FFmpeg."""
import argparse, asyncio, functools, http.server, json, subprocess, threading, time
from pathlib import Path
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent
(P/'output').mkdir(exist_ok=True)
async def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--start',type=float,default=0);ap.add_argument('--frames',type=int);ap.add_argument('--video-only',action='store_true');ap.add_argument('--output',default='SKIM_20_estilos_V3.mp4');ap.add_argument('--times',default=','.join(str(round(i*1.2+.8,2)) for i in range(20))+',25.5,26.983333');ap.add_argument('--port',type=int,default=8765);a=ap.parse_args()
 spec=json.loads((P/'timing.json').read_text())
 server=http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(P)))
 server.RequestHandlerClass.log_message=lambda *args:None
 threading.Thread(target=server.serve_forever,daemon=True).start()
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--hide-scrollbars'])
  page=await browser.new_page(viewport={'width':spec['width'],'height':spec['height']},device_scale_factor=1)
  page.on('pageerror',lambda e:print('PAGE ERROR:',e,flush=True))
  await page.goto(f'http://127.0.0.1:{a.port}/index.html');await page.wait_for_function('window.READY === true',timeout=60000)
  if a.preview:
   for t in [float(x) for x in a.times.split(',')]:
    await page.evaluate('(t)=>window.seek(t)',t);await page.screenshot(path=str(P/f'output/preview-{t:05.2f}.jpg'),type='jpeg',quality=95)
   print('PREVIEWS READY',flush=True)
  else:
   count=a.frames if a.frames is not None else round((spec['duration']-a.start)*spec['fps'])
   assert count>0 and a.start+count/spec['fps']<=spec['duration']+1e-6
   cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','image2pipe','-vcodec','mjpeg','-framerate',str(spec['fps']),'-i','pipe:0']
   if not a.video_only:cmd+=['-i',str(P/'output/soundtrack.wav'),'-map','0:v:0','-map','1:a:0']
   cmd+=['-c:v','libx264','-preset','medium','-crf','17','-vf','scale=in_range=pc:out_range=tv,format=yuv420p','-color_range','tv','-pix_fmt','yuv420p','-r',str(spec['fps'])]
   if not a.video_only:cmd+=['-c:a','aac','-b:a','320k','-ar','48000']
   cmd+=['-t',str(count/spec['fps']),'-movflags','+faststart',str(P/'output'/a.output)]
   enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
   start=time.monotonic()
   for f in range(count):
    await page.evaluate('(t)=>window.seek(t)',a.start+f/spec['fps'])
    data=await page.screenshot(type='jpeg',quality=97,animations='allow')
    enc.stdin.write(data)
    if f%60==0:print(f'{f}/{spec["fps"]*spec["duration"]} · {time.monotonic()-start:.1f}s',flush=True)
   enc.stdin.close();code=enc.wait();assert code==0,f'FFmpeg exit {code}'
   print(f'RENDER COMPLETE: {time.monotonic()-start:.1f}s',flush=True)
  await browser.close()
 server.shutdown()
if __name__=='__main__':asyncio.run(main())
