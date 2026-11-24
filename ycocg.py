def rgb_to_ycocg_r(img: list):
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
    return y, co, cg

def ycocg_r_to_rgb(y: list, co: list, cg: list):
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
    return img
