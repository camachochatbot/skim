"""Validate settled headline bounds for all twenty styles and the closing card."""
import asyncio,http.server,functools,threading,json
from pathlib import Path
from playwright.async_api import async_playwright
P=Path(__file__).parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
async def main():
 s=http.server.ThreadingHTTPServer(('127.0.0.1',8810),functools.partial(Quiet,directory=str(P)));threading.Thread(target=s.serve_forever,daemon=True).start();errs=[];rows=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage']);page=await b.new_page(viewport={'width':1920,'height':1080});page.on('pageerror',lambda e:errs.append(str(e)))
  await page.goto('http://127.0.0.1:8810/');await page.wait_for_function('window.READY===true',timeout=60000)
  for t in [round(i*1.2+.8,2) for i in range(20)]+[24.8,26.983333]:
   await page.evaluate('(t)=>seek(t)',t);boxes=await page.evaluate('window.TEXT_BOXES')
   for q in boxes:assert q['left']>=0 and q['right']<=1920 and q['top']>=0 and q['bottom']<=1080,(t,q)
   rows.append({'t':t,'headlines':boxes})
  await b.close()
 s.shutdown();assert not errs,errs;(P/'output/layout-check.json').write_text(json.dumps({'page_errors':errs,'samples':rows,'note':'Canvas text metrics at settled style frames; animated entrance clipping and vector/3D shapes inspected visually.'},indent=2)+'\n');print('Text bounds passed:',len(rows),'times; no page errors.')
asyncio.run(main())
