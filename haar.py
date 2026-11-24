companded_table = [-510, -501, -491, -481, -471, -461, -451, -441, -431, -421, -411, -401, -391, -381, -371, -361, -351, -343, -335, -327, -319, -311, -303, -295, -287, -279, -271, -263, -255, -247, -239, -231, -223, -219, -215, -211, -207, -203, -199, -195, -191, -187, -183, -179, -175, -171, -167, -163, -159, -155, -151, -147, -143, -139, -135, -131, -127, -123, -119, -115, -111, -107, -103, -99, -95, -93, -91, -89, -87, -85, -83, -81, -79, -77, -75, -73, -71, -69, -67, -65, -63, -61, -59, -57, -55, -53, -51, -49, -47, -45, -43, -41, -39, -37, -35, -33, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184, 188, 192, 196, 200, 204, 208, 212, 216, 220, 224, 232, 240, 248, 256, 264, 272, 280, 288, 296, 304, 312, 320, 328, 336, 344, 352, 362, 372, 382, 392, 402, 412, 422, 432, 442, 452, 462, 472, 482, 492, 502, 510]

def haar_transform(a, b, c, d):
    s = a+b+c+d
    h = b+d-(a+c)
    v = c+d-(a+b)
    d = b+c-(a+d)
    return s, h, v, d

def rev_haar_transform(s, h, v, d):
    a = s-h-v-d
    b = s+h-(v-d)
    c = s-h+(v+d)
    d = s+h+(v-d)
    return a, b, c, d

def clamp(i, m, n):
    return min(max(i, m), n)

def haar_on_plane(chunkimg, wd, hd):
    si = []
    hi = []
    vi = []
    di = []

    for p in chunkimg:
        s, h, v, d = haar_transform(p[0], p[1], p[2], p[3])
        si.append(round((s/4)))
        hi.append(compand(h)),
        vi.append(compand(v)),
        di.append(compand(d))

    return si, hi, vi, di

def unhaar_plane(si, hi, vi, di):
    r = []
    for c in range(len(si)):
        s, h, v, d = si[c]*4, companded_table[hi[c]], companded_table[vi[c]], companded_table[di[c]]
        a, b, c, d = rev_haar_transform(s, h, v, d)
        a, b, c, d = round(a/4), round(b/4), round(c/4), round(d/4)
        r.append([clamp(a, 0, 255), clamp(b, 0, 255), clamp(c, 0, 255), clamp(d, 0, 255)])
    return r

compand_lut = [
    min(range(256), key=lambda i: abs(companded_table[i] - n))
    for n in range(-510, 511)
]

def compand(n):
    return compand_lut[max(0, min(1020, n + 510))]
