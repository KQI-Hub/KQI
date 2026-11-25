#!/usr/bin/env python3
"""#   #    #####     #####
#  #   #       #     #
# #    #     # #     #
#  #   #      ##     #
#   #    ##### ##  #####

            r e f e r e n c e   e n c o d e r [v{VER}]
KMI: "KQI Model for Images" (KQI Reference Software) encoder (ckqi)
"""

from kqi import VER, encode, decode

from ppmgen import ppm_to_list # pgm/ppm support
from qoicom import decode as qoi_dec # qoi support

import sys

print(__doc__.replace("{VER}", VER))

if len(sys.argv) < 3:
    print(f"""
USAGE: {sys.argv[0]} input.[ppm/qoi/kqi] output.kqi [options...]
 INPUT
    the input can be KQI, PPM, PGM, QOI
 OUTPUT
    the compressed KQI output file

Basic options:
 -q=QUALITY
    !!Unimplemented!! Compression quality (0..100), Default
 -s
    Enable 4:2:0 Chroma Subsampling, smaller files but lower quality
 -e=EFFORT
    !!Unimplemented!! scQOI2 Compresson Effort
Advanced options:
 -u
    !!Unimplemented!! Disable all metadata
 -a=FILE_PATH
    !!Unimplemented!! Specify Alpha Channel (PGM)
    If unspecified, no alpha is added or it is derrived fron the input image
 -n
    Ignore alpha channel on input image (implicit if -a is specified)
 -c=FILE_PATH
    !!Unimplemented!! Embed ICC Color Profile into image
""")
    sys.exit()

src = sys.argv[1]
out = sys.argv[2]

subsample = False
alpha = True
effort = None
quality = 100
for arg in sys.argv[3:]:
    if arg.startswith("-s"):
        subsample = True
    if arg.startswith("-n"):
        alpha = False

ppm_data = open(src, "rb").read()

input_format = "???"
format_magic = { "KQI":b'kqif', "QOI":b'qoif', "PPM":b'P6', "PGM":b'P5' }

for imgfrm in format_magic:
    if ppm_data.startswith(format_magic[imgfrm]):
        input_format = imgfrm
        break

if input_format == "KQI":
    input_bitmap = decode(ppm_data)
elif input_format == "QOI":
    input_bitmap = qoi_dec(ppm_data)
elif input_format in ("PPM", "PGM"):
    input_bitmap = ppm_to_list(ppm_data)
else:
    raise ValueError("Unsupported import format!")

print(f"Encoding [Input: {input_format}, q{quality}, effort: {effort}]")
kqi_bytes = encode(input_bitmap, subsample=subsample, alpha=alpha)
w, h = len(input_bitmap[0]), len(input_bitmap)
print(f"Compressed to {len(kqi_bytes)} bytes ({round(len(kqi_bytes)/(w*h), 3)} bpp) at {w} x {h}.")

open(out, "wb").write(kqi_bytes)
