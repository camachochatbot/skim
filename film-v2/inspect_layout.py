"""Check the actual seekable composition for readable, in-frame panels and runtime errors."""
import asyncio,functools,http.server,json,threading
from pathlib import Path
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
async def main():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',8790),functools.partial(Quiet,directory=str(P)));threading.Thread(target=server.serve_forever,daemon=True).start()
 errors=[];results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  page=await b.new_page(viewport={'width':1920,'height':1080});page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto('http://127.0.0.1:8790/');await page.wait_for_function('window.READY===true')
  for t in [.95,2.1,3.6,4.9,5.9,6.3,7.8,8.8,9.5,10.4,11.9,13,14.983333]:
   await page.evaluate('(t)=>seek(t)',t)
   r=await page.evaluate('''()=>Array.from(document.querySelectorAll('.interface,.copy')).filter(e=>+getComputedStyle(e).opacity>.98).map(e=>{let r=e.getBoundingClientRect();return {id:e.id,left:r.left,top:r.top,right:r.right,bottom:r.bottom,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth}})''')
   for q in r:
    assert q['left']>=0 and q['top']>=0 and q['right']<=1920 and q['bottom']<=1080,(t,q)
    allowance=12 if q['id']=='pass' else 1  # Ticket's two 11px edge notches intentionally overhang.
    assert q['scrollWidth']<=q['clientWidth']+allowance,(t,q)
   text_bounds=await page.evaluate('''()=>Array.from(document.querySelectorAll('.interface h2,.interface p,.pass-name,.pass-footer,.copy h1')).filter(e=>+getComputedStyle(e.closest('.interface,.copy')).opacity>.98).map(e=>{let range=document.createRange();range.selectNodeContents(e);let r=range.getBoundingClientRect();return {text:e.textContent,left:r.left,right:r.right,top:r.top,bottom:r.bottom}})''')
   for q in text_bounds:assert q['left']>=0 and q['right']<=1920 and q['top']>=0 and q['bottom']<=1080,(t,q)
   results.append({'time':t,'fully_visible_panels':r,'text_bounds':text_bounds})
  await page.evaluate('seek(13)');await page.screenshot(path=str(P/'output/final-source-check.png'))
  await b.close()
 server.shutdown();assert not errors,errors
 (P/'output/layout-check.json').write_text(json.dumps({'page_errors':errors,'results':results},indent=2)+'\n');print('Layout check passed: 13 sample times, no page errors, all fully visible interfaces in frame.')
asyncio.run(main())
