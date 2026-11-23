import ppmgen

fp_in_y = "y.pgm"
fp_in_co = "co.pgm"
fp_in_cg = "cg.pgm"
with open(fp_in_y, 'rb') as inp:
    y = ppmgen.ppm_to_list(inp.read())
with open(fp_in_co, 'rb') as inp:
    co = ppmgen.ppm_to_list(inp.read())
with open(fp_in_cg, 'rb') as inp:
    cg = ppmgen.ppm_to_list(inp.read())

img = []
for rwi in range(len(y)):
    img.append([])
    for pxi in range(len(y[0])):
        Y = y[rwi][pxi]
        Co = (co[rwi][pxi]*2)-256
        Cg = (cg[rwi][pxi]*2)-256

        tmp = Y - Cg//2
        G = Cg + tmp
        B = tmp - Co//2
        R = B + Co

        R = max(0, min(255, R))
        G = max(0, min(255, G))
        B = max(0, min(255, B))

        img[-1].append((R,G,B))

open("recon.ppm", "wb").write(ppmgen.ppm_from_list(img))
