"""
KMI - KQI Model For images
---
Reference Implementation of the KQ Image codec.
"""

from ycocg import rgb_to_ycocg_r, ycocg_r_to_rgb
from haar import haar_on_plane, unhaar_plane
from chunking import bitmap_to_chunkmap, chunkmap_to_bitmap, flat_bitmap_to_chunkmap
from huffman import huffman_enc, huffman_dec # whatever. mari make huffman a drop-in easy thing later pls
from scqoi2 import compress, decompress

from ppmgen import pam_from_list, ppm_from_list, pgm_from_list, ppm_to_list, pgm_from_flat_list # pgm/ppm support
from qoicom import encode as qoi_enc, decode as qoi_dec # qoi support

def kqi_haar_plane(channel, img_w, img_h, img_hw, img_hh):
    chunked_image = bitmap_to_chunkmap(channel)
    s, h, v, d = haar_on_plane(chunked_image, img_w, img_h)
    chunked_s = flat_bitmap_to_chunkmap(s, img_hw, img_hh)
    ss, sh, sv, sd = haar_on_plane(chunked_s, img_hw, img_hh)
    return ss, sh, sv, sd, h, v, d

def flatten(lst):
    out = []
    for item in lst:
        out.extend(item)
    return out

src_img = qoi_dec(open("sunset.qoi", "rb").read())

img_w = len(src_img[0])
img_h = len(src_img)
img_hw, img_hh = (img_w+1)//2, (img_h+1)//2

img_y, img_co, img_cg = rgb_to_ycocg_r(src_img)
yss, ysh, ysv, ysd, yh, yv, yd = kqi_haar_plane(img_y, img_w, img_h, img_hw, img_hh)
coss, cosh, cosv, cosd, coh, cov, cod = kqi_haar_plane(img_co, img_w, img_h, img_hw, img_hh)
cgss, cgsh, cgsv, cgsd, cgh, cgv, cgd = kqi_haar_plane(img_cg, img_w, img_h, img_hw, img_hh)

yds = unhaar_plane(yss, ysh, ysv, ysd)
yds = flatten(chunkmap_to_bitmap(yds, img_hw, img_hh))
cdimg = unhaar_plane(yds, yh, yv, yd)
dimg_y = chunkmap_to_bitmap(cdimg, img_w, img_h)

cods = unhaar_plane(coss, cosh, cosv, cosd)
cods = flatten(chunkmap_to_bitmap(cods, img_hw, img_hh))
cdimg = unhaar_plane(cods, coh, cov, cod)
dimg_co = chunkmap_to_bitmap(cdimg, img_w, img_h)

cgds = unhaar_plane(cgss, cgsh, cgsv, cgsd)
cgds = flatten(chunkmap_to_bitmap(cgds, img_hw, img_hh))
cdimg = unhaar_plane(cgds, cgh, cgv, cgd)
dimg_cg = chunkmap_to_bitmap(cdimg, img_w, img_h)

dimg = ycocg_r_to_rgb(dimg_y, dimg_co, dimg_cg)

open("sunsety.pgm", "wb").write(pgm_from_list(dimg_y))
open("sunset.ppm", "wb").write(ppm_from_list(dimg))
