import ppmgen

fp_in = "skydtpls.ppm"
with open(fp_in, 'rb') as inp:
    img = ppmgen.ppm_to_list(inp.read())

y, co, cg = [], [], []
for row in img:
    y.append([])
    co.append([])
    cg.append([])
    for px in row:
        R, G, B = px[0], px[1], px[2]
        Co = R - B
        tmp = B + Co//2
        Cg = G - tmp
        Y = tmp + Cg//2

        Y = max(0, min(255, Y))
        Co = max(0, min(255, (Co+256)//2))
        Cg = max(0, min(255, (Cg+256)//2))

        y[-1].append(Y)
        co[-1].append(Co)
        cg[-1].append(Cg)

open("y.pgm", "wb").write(ppmgen.pgm_from_list(y))
open("co.pgm", "wb").write(ppmgen.pgm_from_list(co))
open("cg.pgm", "wb").write(ppmgen.pgm_from_list(cg))
