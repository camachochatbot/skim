"""Serve local source, seek exact frames in Chromium and stream JPEG frames to FFmpeg."""
import argparse, asyncio, functools, http.server, json, subprocess, threading, time
from pathlib import Path
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent
(P/'output').mkdir(exist_ok=True)
async def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--port',type=int,default=8765);a=ap.parse_args()
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
   for t in [0.8,2.5,3.7,5.2,6.4,7.4,8.8,10.5,11.6,13,14.983333]:
    await page.evaluate('(t)=>window.seek(t)',t);await page.screenshot(path=str(P/f'output/preview-{t:05.2f}.jpg'),type='jpeg',quality=95)
   print('PREVIEWS READY',flush=True)
  else:
   cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','image2pipe','-vcodec','mjpeg','-framerate',str(spec['fps']),'-i','pipe:0','-i',str(P/'output/soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r',str(spec['fps']),'-c:a','aac','-b:a','320k','-ar','48000','-t',str(spec['duration']),'-movflags','+faststart',str(P/'output/SKIM_Incoming_La_Molina.mp4')]
   enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
   start=time.monotonic()
   for f in range(spec['fps']*spec['duration']):
    await page.evaluate('(t)=>window.seek(t)',f/spec['fps'])
    data=await page.screenshot(type='jpeg',quality=97,animations='allow')
    enc.stdin.write(data)
    if f%60==0:print(f'{f}/900 · {time.monotonic()-start:.1f}s',flush=True)
   enc.stdin.close();code=enc.wait();assert code==0,f'FFmpeg exit {code}'
   print(f'RENDER COMPLETE: {time.monotonic()-start:.1f}s',flush=True)
  await browser.close()
 server.shutdown()
if __name__=='__main__':asyncio.run(main())
