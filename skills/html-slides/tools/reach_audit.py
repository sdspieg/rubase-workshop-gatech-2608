import asyncio,sys
async def main(url):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1366,'height':800})
        await pg.goto(url); await pg.wait_for_timeout(2400)
        n=await pg.evaluate("document.querySelectorAll('.slide').length")
        tot=bad=0; worst=[]
        for i in range(n):
            await pg.evaluate(f"go({i})"); await pg.wait_for_timeout(55)
            await pg.evaluate("setFrags(cur,document.querySelectorAll('.slide.on [data-frag]').length)")
            await pg.wait_for_timeout(45)
            # ask review.js's OWN resolver, which is what actually decides selection
            r=await pg.evaluate("""(()=>{const s=document.querySelector('.slide.on');let t=0,bl=0;
              for(const el of s.querySelectorAll('img, image, .card, .ob-note')){
                const q=el.getBoundingClientRect(); if(q.width<24||q.height<14) continue;
                const x=q.x+q.width/2, y=q.y+q.height/2;
                const got=window.__gtrPick? window.__gtrPick(x,y):null; t++;
                if(got!==el && !(el.contains&&el.contains(got))) bl++;}
              return {sid:s.dataset.sid,t,bl};})()""")
            tot+=r['t']; bad+=r['bl']
            if r['bl']: worst.append((r['sid'],r['bl'],r['t']))
        print(f"unreachable by the review resolver: {bad} of {tot}, on {len(worst)} slides")
        worst.sort(key=lambda x:-x[1]); print('   worst:', ', '.join(f"{s} {b}/{t}" for s,b,t in worst[:6]))
        await b.close()
asyncio.run(main(sys.argv[1]))
