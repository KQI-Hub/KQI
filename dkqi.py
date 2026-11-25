#!/usr/bin/env python3
"""#   #    #####     #####
#  #   #       #     #
# #    #     # #     #
#  #   #      ##     #
#   #    ##### ##  #####

            r e f e r e n c e   d e c o d e r [v{VER}]
KMI: "KQI Model for Images" (KQI Reference Software) decoder (dkqi)
"""

from kqi import VER, decode

from ppmgen import pam_from_list, ppm_from_list, pgm_from_list # pgm/ppm support
from qoicom import encode as qoi_enc # qoi support

import sys

print(__doc__.replace("{VER}", VER))

if len(sys.argv) < 3:
    print(f"""
USAGE: {sys.argv[0]} input.kqi output.[ppm/pam/qoi]
 INPUT
    The compressed input file (KQI)
 OUTPUT
    The PPM, PGM, PAM, or QOI output file
""")
    sys.exit()

src = sys.argv[1]
out = sys.argv[2]

kqi_data = open(src, "rb").read()

out_format = sys.argv[2].split(".")[-1].lower()

image = decode(kqi_data)

if out_format == "ppm":
    out_bytes = ppm_from_list(image)
elif out_format == "pgm":
    out_bytes = pgm_from_list(image)
elif out_format in ("pam"):
    out_bytes = pam_from_list(image)
elif out_format in ("qoi"):
    out_bytes = qoi_enc(image)
else:
    raise ValueError("Unsupported import format!")

#print(f"Encoding [Input: {input_format}, q{quality}, effort: {effort}]")

#w, h = len(input_bitmap[0]), len(input_bitmap)
#print(f"Compressed to {len(kqi_bytes)} bytes ({round(len(kqi_bytes)/(w*h), 3)} bpp) at {w} x {h}.")

open(out, "wb").write(out_bytes)
