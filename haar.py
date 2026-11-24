def haar_transform(a, b, c, d):
    s = a+b+c+d
    h = b+d-(a+c)
    v = c+d-(a+b)
    d = b+c-(a+d)
    return s, h, v, d

def rev_haar_transform(s, h, v, d):
    a = s+h+v+d
    b = s-h+(v-d)
    c = s+h-(v-d)
    d = s-h-(v+d)
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
        hi.append(round((h+510)/4)),
        vi.append(round((v+510)/4)),
        di.append(round((d+510)/4))

    return si, hi, vi, di

def unhaar_plane(si, hi, vi, di):
    r = []
    for c in range(len(si)):
        s, h, v, d = si[c]*4, 510-hi[c]*4, 510-vi[c]*4, 510-di[c]*4
        a, b, c, d = rev_haar_transform(s, h, v, d)
        a, b, c, d = round(a/4), b//4, c//4, d//4
        r.append([clamp(a, 0, 255), clamp(b, 0, 255), clamp(c, 0, 255), clamp(d, 0, 255)])
    return r
