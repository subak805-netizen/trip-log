# -*- coding: utf-8 -*-
# 픽셀 아이콘 만들기 (32×32 칸 → 키워서 PNG). 외부 라이브러리 없이 PNG 직접 씀
import zlib, struct, sys, os, math
PAL = {'K':(11,10,5),'W':(255,252,247),'P':(247,198,217),'M':(165,230,186),'C':(239,232,212),'Y':(242,201,76),'S':(176,219,240),'B':(140,200,232),'R':(224,83,61),'T':(232,214,170)}
MASCOT = ['....KKKK....','..KKWKWKKK..','.KWWWWWWWWK.','KWWWWWWWWWWK','KWWKWWWWKWWK','KWPWWWWWWPWK','KWWWWKKWWWWK','.KWWWWWWWWK.','..KKKKKKKK..']
PLANE  = ['.....KK.....','....KYYK....','....KYYK....','KKKKKYYKKKKK','KYYYYYYYYYYK','.KKKKYYKKKK.','....KYYK....','...KYYYYK...','...KKKKKK...']
def canvas(bg): return [[bg]*32 for _ in range(32)]
def stamp(g, spr, x0, y0, sc=1):
    for y,row in enumerate(spr):
        for x,c in enumerate(row):
            if c=='.': continue
            for dy in range(sc):
                for dx in range(sc):
                    X,Y = x0+x*sc+dx, y0+y*sc+dy
                    if 0<=X<32 and 0<=Y<32: g[Y][X] = c
def png(g, path, scale, size=None):
    n = size or 32*scale
    raw = bytearray()
    for y in range(n):
        raw.append(0)
        for x in range(n):
            raw += bytes(PAL[g[y*32//n][x*32//n]])
    def chunk(t, d): return struct.pack('>I',len(d))+t+d+struct.pack('>I', zlib.crc32(t+d)&0xffffffff)
    data = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB', n, n, 8, 2, 0, 0, 0))+chunk(b'IDAT', zlib.compress(bytes(raw),9))+chunk(b'IEND', b'')
    open(path,'wb').write(data)

def variant_a():   # 민트 바탕 + 만두 + 노란 비행기
    g = canvas('M'); stamp(g, MASCOT, 4, 10, 2); stamp(g, PLANE, 19, 2, 1)
    for x in range(4,18,3): g[6][x] = 'K'   # 비행기 지나간 점선
    return g
def variant_b():   # 크림 바탕 + 노란 여행 가방 + 만두 스티커
    g = canvas('C')
    for y in range(9,28):
        for x in range(4,28):
            edge = y in (9,27) or x in (4,27)
            g[y][x] = 'K' if edge else ('M' if 12<=y<=13 else 'Y')
    for y in range(5,9):
        for x in range(11,21):
            if y==5 or x in (11,12,19,20): g[y][x] = 'K'
    for y in (28,): 
        for x in (7,8,23,24): g[y][x] = 'K'
    stamp(g, MASCOT, 10, 16, 1)
    return g
def variant_c():   # 하늘 바탕 + 지도 핀 안에 만두
    g = canvas('S')
    cx, cy, r = 16, 12.5, 10.5
    fill = [[False]*32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            inside = (x+.5-cx)**2+(y+.5-cy)**2 <= r*r
            # 아래 뾰족한 꼬리
            if cy <= y <= 30:
                half = min(r*0.92, (30.5-y)*0.58)
                if abs(x+.5-cx) <= half: inside = True
            fill[y][x] = inside
    for y in range(32):
        for x in range(32):
            if not fill[y][x]: continue
            edge = any(not (0<=x+dx<32 and 0<=y+dy<32 and fill[y+dy][x+dx]) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
            g[y][x] = 'K' if edge else 'P'
    stamp(g, MASCOT, 10, 8, 1)
    return g
out = sys.argv[1] if len(sys.argv)>1 else '.'
if len(sys.argv)>2 and sys.argv[2]=='final':   # 확정 = B 여행 가방 (10-13)
    g = variant_b()
    for name, size in (('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512),('favicon-32.png',32)):
        png(g, os.path.join(out, name), 1, size)
else:
    for name, fn in (('a',variant_a),('b',variant_b),('c',variant_c)):
        png(fn(), os.path.join(out, 'icon_'+name+'_preview.png'), 8)
print('ok')
