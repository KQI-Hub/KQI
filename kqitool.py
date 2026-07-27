from ppmgen import ppm_to_list, blank_bitmap_list, ppm_from_list, pgm_from_list
from predictation import predict_None, predict_Left, predict_Up, predict_UpL, predict_UpR, predict_LL, predict_Avg, predict_Paeth, unpredict_Left, unpredict_Up, unpredict_UpL, unpredict_UpR, unpredict_LL, unpredict_Avg, unpredict_Paeth
from bittools import intclamp

quanization_biases = [0, 0, 1, 2, 4, 8, 16, 32, 64, 128]

"""
KQI KRILTT's predictors:
None - raw pixel values
Left - difference from pixel to the left (Edge case: pixels at y0 are raw)
Up - difference from pixel above (Edge case: pixels at x0 are raw)
UpL - difference from pixel up 1 and left 1  (Edge case: pixels at y0 and x0 are raw)
UpR - difference from pixel up 1 and right 1  (Edge case: pixels at y0 are raw, out-of-plane pixels are black)
LL - difference from pixel left to the left (Edge case: pixels at y0 and y1 are raw)
Avg - difference from the average between the pixel up by 1 and the pixel left by 1 (Edge case: pixel at x0y0 is raw, all others on x0 use the left predictor, and others on y0 use the up predictor)
Paeth - the paeth filter from PNG (Edge case: out-of-plane pixels are black, x0y0 is raw)
"""

def denoise(bmap: list, tollerence: int):
    scale = len(bmap)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(bmap[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            cup = False if y == 0 else True
            cdn = False if y == scale-1 else True
            clf = False if x == 0 else True
            crt = False if x == scale-1 else True
            if gray:
                pot = 0
                if cup:
                    pot += bmap[y-1][x]
                if cdn:
                    pot += bmap[y+1][x]
                if clf:
                    pot += bmap[y][x-1]
                if crt:
                    pot += bmap[y][x+1]

                div = cup+cdn+clf+crt
                pot = pot//div

                if abs(pot-bmap[y][x]) > tollerence:
                     new[y][x] = intclamp(pot)
                else:
                    new[y][x] = bmap[y][x]
            else:
                new[y][x] = [0, 0, 0]
                for c in (0,1,2):
                    pot = 0
                    if cup:
                        pot += bmap[y-1][x][c]
                    if cdn:
                        pot += bmap[y+1][x][c]
                    if clf:
                        pot += bmap[y][x-1][c]
                    if crt:
                        pot += bmap[y][x+1][c]

                    div = cup+cdn+clf+crt
                    pot = pot//div

                    if abs(pot-bmap[y][x][c]) > tollerence:
                         new[y][x][c] = intclamp(pot)
                    else:
                        new[y][x][c] = bmap[y][x][c]
    return new

def quantize(residual: list, level: int):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False
    b = quanization_biases[level]

    for y in range(scale):
        for x in range(scale):
            if gray:
                new[y][x] = intclamp((residual[y][x]+b)>>level)
            else:
                new[y][x] = [0, 0, 0]
                for c in (0,1,2):
                    new[y][x][c] = intclamp((residual[y][x][c]+b)>>level)
    return new

def dequantize(residual: list, level: int):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if gray:
                new[y][x] = intclamp(residual[y][x]<<level)
            else:
                new[y][x] = [0, 0, 0]
                for c in (0,1,2):
                    new[y][x][c] = intclamp(residual[y][x][c]<<level)
    return new

def dekriltt(tlc, trc, blc, brc, scale):
    img = blank_bitmap_list(scale, scale)
    for y in range(scale):
        for x in range(scale):
            fx = x / (scale - 1)
            fy = y / (scale - 1)
            tl = (1 - fx) * (1 - fy)
            tr = fx * (1 - fy)
            bl = (1 - fx) * fy
            br = fx * fy
            value = []
            for col in (0,1,2):
                value.append(intclamp(tlc[col]*tl + trc[col]*tr + blc[col]*bl + brc[col]*br))
            img[y][x] = tuple(value)
    return img

def to_gray(ls: list):
    gray = []
    for row in ls:
        gray.append([])
        for pix in row:
            col = (pix[0]+pix[1]+pix[1]+pix[2])//4
            gray[-1].append(col)
    return gray

def reconstruct_tile(base: list, residual: list):
    if type(residual[0][0]) == int:
        gray = True
    else:
        gray = False

    tile = blank_bitmap_list(len(base), len(base[0]))
    for y in range(len(base)):
        for x in range(len(base[0])):
            tile[y][x] = [0, 0, 0]
            for c in (0,1,2):
                if gray:
                    tile[y][x][c] = (residual[y][x] + base[y][x][c]+128)%256
                else:
                    tile[y][x][c] = (residual[y][x][c] + base[y][x][c]+128)%256
    return tile

def getpredictor(predictor: str, reverse: bool = False):
    if predictor == "None":
        if reverse:
            return predict_None
        else:
            return predict_None
    elif predictor == "Left":
        if reverse:
            return unpredict_Left
        else:
            return predict_Left
    elif predictor == "Up":
        if reverse:
            return unpredict_Up
        else:
            return predict_Up
    elif predictor == "UpL":
        if reverse:
            return unpredict_UpL
        else:
            return predict_UpL
    elif predictor == "UpR":
        if reverse:
            return unpredict_UpR
        else:
            return predict_UpR
    elif predictor == "LL":
        if reverse:
            return unpredict_LL
        else:
            return predict_LL
    elif predictor == "Avg":
        if reverse:
            return unpredict_Avg
        else:
            return predict_Avg
    elif predictor == "Paeth":
        if reverse:
            return unpredict_Paeth
        else:
            return predict_Paeth
    else:
        raise ValueError

def kriltt(tile: list, scale: int, predictor: str = "None", quantize_strength = 1, gray_residual: bool = False, denoise_tollerence: int = 12):
    tlc = tile[0][0]
    trc = tile[0][scale-1]
    blc = tile[scale-1][0]
    brc = tile[scale-1][scale-1]
    #print(tlc, trc, blc, brc)
    basis = dekriltt(tlc, trc, blc, brc, scale)
    #print(basis)
    residual = blank_bitmap_list(scale, scale)
    for y in range(scale):
        for x in range(scale):
            residual[y][x] = [0, 0, 0]
            for c in (0,1,2):
                residual[y][x][c] = (tile[y][x][c] - basis[y][x][c]-128)%256
    open("gradient.ppm", "wb").write(ppm_from_list(basis))
    #open("residual.ppm", "wb").write(ppm_from_list(residual))

    if gray_residual:
        grayscale_residual = to_gray(residual)
        del residual
        residual = grayscale_residual

    predictorfunc = getpredictor(predictor)

    if denoise_tollerence == -1:
        denoised_residual = residual
    else:
        denoised_residual = denoise(residual, denoise_tollerence)
    if quantize_strength == 0:
        quantized_residual = denoised_residual
    else:
        quantized_residual = quantize(denoised_residual, quantize_strength)
    predicted_residual = predictorfunc(quantized_residual)

    unpredictorfunc = getpredictor(predictor, True)
    unpredicted_residual = unpredictorfunc(predicted_residual)
    dequantized_residual = dequantize(unpredicted_residual, quantize_strength)

    #open("residual.ppm", "wb").write(pgm_from_list(residual))
    #open("residualp.ppm", "wb").write(pgm_from_list(predicted_residual))
    #open("residualrs.ppm", "wb").write(pgm_from_list(unpredicted_residual))

    restored_lossy = reconstruct_tile(basis, dequantized_residual)
    open("restored_lossy.ppm", "wb").write(ppm_from_list(restored_lossy))

source = open("tile.ppm", "rb").read()

tile = ppm_to_list(source)
kriltt(tile, 8, predictor = "None", gray_residual=False, denoise_tollerence=-1, quantize_strength=5)
#tile is input data, predictor is the predictor to use, gray_residual discards chroma data from the residual, denoise_tollerence defines how leanient the denoiser is (-1 to disable it), quantize_strength is how many bits to shift to shift right in encoding and left in decoding.

#img = [[10, 20, 30, 40], [10, 20, 30, 40], [10, 20, 30, 40], [10, 20, 30, 40]]
#enc = predict_Left(img)
#dec = unpredict_Left(enc)

#print(img)
#print(enc)
#print(dec)
