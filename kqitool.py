import itertools
from random import randint

from minidcttilemap import minidctmap, minidctdiffmap
from bittools import byte_to_boollist, boollist_to_int_var, mk_uintvar, generate_boollist
from diffmap import diffmap

def generateheader(version, width, height, channelmode, colspace, xdblength):
    iscontainer = bool(xdblength)
    head = bytearray()
    head.append(version)
    head.extend(width.to_bytes(4, 'little'))
    head.extend(height.to_bytes(4, 'little'))
    flags = []
    flags.extend(generate_boollist(channelmode, 4))
    flags.extend(generate_boollist(colspace, 2))
    flags.append(iscontainer)
    flags.append(False)
    flags = boollist_to_int_var(flags)
    head.append(flags)
    if iscontainer:
        xdblength.extend(mk_uintvar())
    return head

def bitmap_to_chunkmap(bmp: list):
    chunkmap = []
    rows = len(bmp)
    rows = (rows+7) //8 # amount of rows of chunks
    cols = len(bmp[0])
    cols = (cols+7) //8 # amount of chunks per row
    tiles = rows*cols
    for t in range(tiles):
        chunkmap.append([])
        crow = t%cols
        ccol = t//cols
        for i in range(8):
            for l in range(8):
                pxc = (ccol*8)+i
                pxr = crow*8+l
                if len(bmp) <= pxc:
                    pxc = -1
                if len(bmp[0]) <= pxr:
                    pxr = -1
                chunkmap[t].append(bmp[pxc][pxr])
    return chunkmap

def convert_transforms(inversion, bshift, floor):
    b1 = [inversion]
    if bshift < 0:
        bshift += 128
    b1.extend(generate_boollist(bshift, 7))
    b1 = boollist_to_int_var(b1)
    b2 = floor
    return bytes([b1, b2])

def generate_minidct_tile(index, inversion: bool, bshift, floor):
    bytesobject = bytearray()
    base = [True, True]

    if index > 63 or 0 > index:
        raise ValueError("Invalid Tile! Range is 0 to 63")
    #if bshift > 63 or -64 > bshift:
    #    raise ValueError("Invalid Bitshift! Range is -64 to 63")
    #if floor > 255 or 0 > floor:
    #    raise ValueError("Invalid Floor! Range is 0 to 255")

    base.extend(generate_boollist(index, 6))
    base = boollist_to_int_var(base)
    bytesobject.append(base)
    if type(inversion) is tuple:
        bytesobject.extend(convert_transforms(inversion[0], bshift[0], floor[0]))
        bytesobject.extend(convert_transforms(inversion[1], bshift[1], floor[1]))
        bytesobject.extend(convert_transforms(inversion[2], bshift[2], floor[2]))
    else:
        bytesobject.extend(convert_transforms(inversion, bshift, floor))
    return bytesobject

def calculate_tile_count(n, p):
    n = (n+bool(n % 8)) //8
    p = (p+bool(p % 8)) //8
    return n*p

def generator_is_my_name(width, height):
    tfile = bytearray(b"KQIF")
    tfile.extend(generateheader(0, width, height, 3, 1, 0))
    tc = calculate_tile_count(width, height)
    for _ in range(tc):
        tfile.extend(generate_minidct_tile(randint(0, 63), (bool(randint(0, 1)), bool(randint(0, 1)), bool(randint(0, 1))), (randint(-2, 2), randint(-2, 2), randint(-2, 2)), (randint(0, 64), randint(0, 64), randint(0, 64))))
    return bytes(tfile)

def encode(bitmap: list):
    return b"KQIF"

def parseheader(header: bytes):
    version = header[0]
    width = int.from_bytes(header[1:5], "little")
    height = int.from_bytes(header[5:9], "little")
    css = byte_to_boollist(header[9])
    channelmode = boollist_to_int_var(css[0:4])
    chmds = ["No Image Data", "Grayscale", "Grayscale, Alpha", "RGB", "RGBA"]
    colspace = boollist_to_int_var(css[4:6])
    colspaces = ["sRGB with Linear Alpha", "All channels Linear"]
    iscontainer = css[6]
    rffu = css[7]
    xdblength = None
    if iscontainer:
        uintvar_buffer = []
        trail = header[10:]
        for b in trail:
            bl = byte_to_boollist(b)
            if bl[0]:
                uintvar_buffer.append(bl[1:])
            else:
                break
        xdblength = boollist_to_int_var(uintvar_buffer)
    return version, width, height, channelmode, colspace, iscontainer, xdblength

    print(f"""KQI Version: {version}
Width: {width}
Height: {height}
Channels: {chmds[channelmode]}
Color Space: {colspaces[colspace]}
XDB Contained?: {iscontainer}
Extra Bit: {rffu}""")

def chunk_to_param(c1, c2):
    if c1 > 127:
        inv = True
        bsft = c1 - 128
    else:
        inv = False
        bsft = c1
    flor = c2
    return inv, bsft, flor

def sshift(val, shft):
    if shft >= 0:
        return ((val-127) << shft)+127
    else:
        return ((val-127) >> -shft)+127

def clamp_to_byte(val):
    return max(min(255, val), 0)

def tiletransform(tile: list, inv, bsft, flor):
    buff = []
    tmp = []
    if inv:
        for byt in tile:
            tmp.append(255-byt)
        tile = tmp
        tmp = []
    if flor:
        for byt in tile:
            tmp.append(min(255, (byt+flor)))
        tile = tmp
        tmp = []
    if bsft:
        if bsft > 63:
            bsft -= 128
        for byt in tile:
            tmp.append(clamp_to_byte(sshift(byt, bsft)))
        tile = tmp
        tmp = []
    return tile

def decodechunk(chunk: bytes):
    ch = len(chunk)
    if ch == 3:
        ch = 0
    elif ch == 7:
        ch = 1
    else:
        raise Exception("Invalid MiniDCT Chunk! Tuple Length is Incorrect!")
    boing = byte_to_boollist(chunk[0])
    sig = boing[0:2]
    if not sig == [True, True]:
        print(sig)
        print(chunk[0])
        raise Exception("Invalid MiniDCT Chunk! Signature is not 11")
    cords = boing[2:8]
    tile = minidctmap[boollist_to_int_var(cords)]
    if ch:
        inv, bsft, flor = chunk_to_param(chunk[1], chunk[2])
        redbuff = tiletransform(tile, inv, bsft, flor)
        inv, bsft, flor = chunk_to_param(chunk[3], chunk[4])
        greenbuff = tiletransform(tile, inv, bsft, flor)
        inv, bsft, flor = chunk_to_param(chunk[5], chunk[6])
        bluebuff = tiletransform(tile, inv, bsft, flor)
        buff = []
        for i in range(64):
            buff.append((redbuff[i], greenbuff[i], bluebuff[i]))
    else:
        inv, bsft, flor = chunk_to_param(chunk[1], chunk[2])
        buff = tiletransform(tile, inv, bsft, flor)
    return buff

def decode(kqibytes: bytes):
    if not kqibytes.startswith(b'KQIF'):
        raise Exception("Invalid KQI Image!")
    header = kqibytes[4:]
    version, width, height, channelmode, colspace, iscontainer, xdblength = parseheader(header)
    if channelmode == 0:
        raise Exception("KQC container, not KQI image!")
    if iscontainer:
        print("Container mode is not supported, skipping...")
    if channelmode == 1 or channelmode == 2:
        tultype = 3
    elif channelmode == 3 or channelmode == 4:
        tultype = 7
    data = kqibytes[14:]
    decoded = []
    for i in range(len(data)//tultype):
        if tultype == 3:
            decoded.append(decodechunk([data[i*3],data[i*3+1],data[i*3+2]]))
        else:
            decoded.append(decodechunk([data[i*7],data[i*7+1],data[i*7+2],data[i*7+3],data[i*7+4],data[i*7+5],data[i*7+6]]))
    return chunkmap_to_bitmap(decoded, width, height)

def in_range(w: int, h: int, cx: int, cy: int):
    if cx > w-1:
        return False
    if cy > h-1:
        return False
    return True

def chunkmap_to_bitmap(chkmp: list, width: int, height: int, gray: bool = False):
   tilewidth = width // 8
   if width % 8:
       tilewidth += 1
   tileheight = height // 8
   if height % 8:
       tileheight += 1

   bmp = []
   for h in range(height):
       bmp.append([])
       for p in range(width):
           if gray:
               bmp[h].append(0)
           else:
               bmp[h].append((0,0,0))

   for h in range(tileheight):
      for w in range(tilewidth):
          pos = w+h*tilewidth
          for l in range(64):
              cx = l%8
              cy = l//8
              xpos = w*8+cx
              ypos = h*8+cy
              if in_range(width, height, xpos, ypos):
                  try:
                      bmp[ypos][xpos] = chkmp[pos][l]
                  except Exception as e:
                      print(width, height, cx, cy)
                      raise e

   return bmp
