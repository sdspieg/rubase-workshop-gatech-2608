import numpy as np, json
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
ROOT='/mnt/c/Users/Stephan/GT-Workshop-Offline/gatech'
im=Image.open(f'{ROOT}/img/orig/gt2025_omics-13.png').convert('RGB')
a=np.asarray(im).astype(np.float32); H,W,_=a.shape
plate=np.load('/tmp/plate.npy')
fg=np.abs(a-plate).max(2)>=10
fg=ndi.binary_closing(fg,np.ones((3,3)))
for x0,y0,x1,y1 in [(0,0,470,150),(1640,0,1800,165),(1600,915,1800,1012),(0,900,110,1012)]:
    fg[y0:y1,x0:x1]=False
fg=ndi.binary_opening(fg,np.ones((2,2)))

RECTS={
 'dna':        [(55,420,470,678),(470,400,800,678),(770,468,890,528)],
 'genes':      [(255,375,600,462),(600,400,730,455)],
 'chromosome': [(20,238,300,302),(140,262,460,412),(55,352,205,500)],
 'cell':       [(308,222,482,282),(452,222,716,396),(698,288,1016,352)],
 'protein':    [(38,558,702,942)],
 'machine':    [(652,600,1078,908),(732,622,1072,682)],
 'livingcell': [(1068,498,1702,948)],
 'community':  [(1118,188,1800,618)],
}
FORCE_SPLIT=[(80,282,774,673)]
# whole blobs whose bbox falls in one of these zones are forced to that owner
ZONE_OVERRIDE=[((160,590,420,690),'protein')]
PRIORITY=['chromosome','genes','cell','dna','machine','protein','livingcell','community']
NAMES=list(RECTS)
def rmask(rs):
    m=np.zeros((H,W),bool)
    for x0,y0,x1,y1 in rs: m[y0:y1,x0:x1]=True
    return m
RM={k:rmask(v) for k,v in RECTS.items()}

lab,n=ndi.label(fg, structure=np.ones((3,3)))
own=np.zeros((H,W),np.int8)   # index into NAMES, -1 = unassigned
own[:]=-1
whole=shared=0
allblob=[]
report=[]
for i in range(1,n+1):
    sl=ndi.find_objects(lab==i)[0]
    sub=(lab[sl]==i); npx=sub.sum()
    if npx<40: continue
    shares={k:(RM[k][sl]&sub).sum()/npx for k in NAMES}
    best=max(shares.values())
    cands=[k for k in PRIORITY if shares[k]>=best-1e-9]
    bb=(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)
    forced=any(abs(bb[0]-f[0])<12 and abs(bb[1]-f[1])<12 and abs(bb[2]-f[2])<12 and abs(bb[3]-f[3])<12 for f in FORCE_SPLIT)
    zov=[o for z,o in ZONE_OVERRIDE if bb[0]>=z[0] and bb[1]>=z[1] and bb[2]<=z[2] and bb[3]<=z[3]]
    if zov:
        own[sl][sub]=NAMES.index(zov[0]); whole+=1; report.append((npx,zov[0],'zone',sl)); allblob.append((npx,zov[0],sl)); continue
    if best>=0.80 and not forced:
        own[sl][sub]=NAMES.index(cands[0]); whole+=1
        report.append((npx,cands[0],'whole',sl))
        allblob.append((npx,cands[0],sl))
    else:
        # pixel-wise split by priority within rects
        rem=sub.copy()
        for k in [q for q in PRIORITY if q!='genes']:
            take=rem&RM[k][sl]
            if take.any():
                o=own[sl]; o[take]=NAMES.index(k); own[sl]=o
                rem&=~take
        shared+=1
        report.append((npx,'+'.join(f'{k}:{shares[k]:.2f}' for k in NAMES if shares[k]>.05),'SPLIT',sl))
report.sort(reverse=True, key=lambda r:r[0])
for npx,who,kind,sl in report[:14]:
    print(f'{npx:7d} {kind:6s} x{sl[1].start:4d}-{sl[1].stop:<4d} y{sl[0].start:4d}-{sl[0].stop:<4d} {who}')
print(f'... {whole} whole-assigned blobs, {shared} split')
R_,G_,B_=a[...,0],a[...,1],a[...,2]
yellow=(R_>85)&(G_>60)&(R_>B_+22)
swap=(own==NAMES.index('genes'))&yellow
swap|= (own==NAMES.index('dna'))&yellow&(np.arange(H)[:,None]<430)
own[swap]=NAMES.index('chromosome')
print('yellow px moved genes->chromosome:', int(swap.sum()))
luma=a.mean(2)
chromo=(own==NAMES.index('chromosome'))
near=ndi.binary_dilation(chromo,np.ones((7,7)))
rim=(own==NAMES.index('genes'))&near&(luma<170)
own[rim]=NAMES.index('chromosome')
print('dark rim px moved genes->chromosome:', int(rim.sum()))
un=(own<0)&fg
print('--- blobs per owner ---')
for o in NAMES:
    bs=[b for b in allblob if b[1]==o]
    print(o, [(b[0],b[2][1].start,b[2][0].start,b[2][1].stop,b[2][0].stop) for b in sorted(bs,reverse=True)][:9])
print('UNASSIGNED fg px:', int(un.sum()), f'({un.sum()/fg.sum()*100:.2f}%)')

CROP=(30,185,1800,935); cx0,cy0,cx1,cy1=CROP
Image.fromarray(np.clip(plate,0,255).astype(np.uint8)).crop(CROP).save(f'{ROOT}/img/omics/plate.png')
rgb=np.asarray(im).astype(np.uint8)
soft_src=np.zeros((H,W),np.float32)
manifest={}
for k in NAMES:
    m=(own==NAMES.index(k))
    md=ndi.binary_dilation(m,np.ones((3,3)))
    alpha=np.asarray(Image.fromarray((md*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))).astype(np.float32)/255.
    keep=(alpha>0)[...,None]
    Image.fromarray(np.dstack([(rgb*keep).astype(np.uint8),(alpha*255).astype(np.uint8)])).crop(CROP).save(f'{ROOT}/img/omics/{k}.png',optimize=True)
    ys,xs=np.where(m)
    manifest[k]=dict(px=int(m.sum()),box=[int(xs.min())-cx0,int(ys.min())-cy0,int(xs.max())-cx0,int(ys.max())-cy0])
    print(f'  {k:11s} {int(m.sum()):7d}px  box={manifest[k]["box"]}')
json.dump(manifest,open(f'{ROOT}/img/omics/manifest.json','w'),indent=1)
