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
                      print(width, height, cx, cy, chkmp)
                      raise e
   return bmp

def flat_bitmap_to_chunkmap(bmp: list, width: int, height: int):
    chunkmap = []

    for y in range(0, height, 2):
        for x in range(0, width, 2):
            # A B
            # C D

            a = bmp[y * width + x]
            b = bmp[y * width + x + 1] if x + 1 < width else 0
            c = bmp[(y + 1) * width + x] if y + 1 < height else 0
            d = bmp[(y + 1) * width + x + 1] if x + 1 < width and y + 1 < height else 0

            chunkmap.append([a, b, c, d])

    return chunkmap
