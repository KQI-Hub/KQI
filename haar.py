import ppmgen, bittools

def wavelet(a, b, c, d):
    s = a+b+c+d
    h = b+d-(a+c)
    v = c+d-(a+b)
    d = b+c-(a+d)
    return s, h, v, d

def bitmap_to_chunkmap(bmp: list):
    chunkmap = []
    rows = len(bmp)
    rows = (rows+1) //2 # amount of rows of chunks
    cols = len(bmp[0])
    cols = (cols+1) //2 # amount of chunks per row
    tiles = rows*cols
    for t in range(tiles):
        chunkmap.append([])
        crow = t%cols
        ccol = t//cols
        for i in range(2):
            for l in range(2):
                pxc = (ccol*2)+i
                pxr = crow*2+l
                if len(bmp) <= pxc:
                    pxc = -1
                if len(bmp[0]) <= pxr:
                    pxr = -1
                chunkmap[t].append(bmp[pxc][pxr])
    return chunkmap

def in_range(w: int, h: int, cx: int, cy: int):
    if cx > w-1:
        return False
    if cy > h-1:
        return False
    return True

def chunkmap_to_bitmap(chkmp: list, width: int, height: int):
   tilewidth = width // 2
   if width % 2:
       tilewidth += 1
   tileheight = height // 2
   if height % 2:
       tileheight += 1

   bmp = []
   for h in range(height):
       bmp.append([])
       for p in range(width):
            bmp[h].append(0)

   for h in range(tileheight):
      for w in range(tilewidth):
          pos = w+h*tilewidth
          for l in range(4):
              cx = l%2
              cy = l//2
              xpos = w*2+cx
              ypos = h*2+cy
              if in_range(width, height, xpos, ypos):
                  try:
                      bmp[ypos][xpos] = chkmp[pos][l]
                  except Exception as e:
                      print(width, height, cx, cy)
                      raise e

   return bmp

def clamp(i, m, n):
    return min(max(i, m), n)

image = ppmgen.ppm_to_list(open("rtx0.pgm", "rb").read())
chunkimg = bitmap_to_chunkmap(image)

si = []
hi = []
vi = []
di = []

for p in chunkimg:
    s, h, v, d = wavelet(p[0], p[1], p[2], p[3])
    si.append(round((s/4)))
    hi.append(round((h+510)/4)),
    vi.append(round((v+510)/4)),
    di.append(round((d+510)/4))

wd, hd = (len(image[0])+1)//2, (len(image)+1)//2

sb = ppmgen.pgm_from_flat_list(si, wd, hd)
hb = ppmgen.pgm_from_flat_list(hi, wd, hd)
vb = ppmgen.pgm_from_flat_list(vi, wd, hd)
db = ppmgen.pgm_from_flat_list(di, wd, hd)

open("s.pgm", "wb").write(sb)
open("h.pgm", "wb").write(hb)
open("v.pgm", "wb").write(vb)
open("d.pgm", "wb").write(db)

#    s = a+b+c+d -- sum
 #   h = b+d-(a+c) -- horizontal diff
  #  v = c+d-(a+b) -- vertical diff
   # d = b+c-(a+d) -- diagonal diff

r = []
for c in range(len(si)):
    s, h, v, d = si[c]*4, 510-hi[c]*4, 510-vi[c]*4, 510-di[c]*4
    a = round((s+h+v+d)/4)
    b = (s-h+v-d)//4
    c = (s+h-v-d)//4
    d = (s-h-v+d)//4
    r.append([clamp(a, 0, 255), clamp(b, 0, 255), clamp(c, 0, 255), clamp(d, 0, 255)])

rm = chunkmap_to_bitmap(r, wd*2, hd*2)

rb = ppmgen.pgm_from_list(rm)
open("r.pgm", "wb").write(rb)