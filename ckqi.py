#!/usr/bin/env python3
"""#   #    #####    #
#  #   #       #   #
# #    #     # #    #
#  #   #      ##     #
#   #    ##### ##     #

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
 -q QUALITY
    Compression quality (1..100), Default 80
 -s
    Enable 4:2:0 Chroma Subsampling, smaller files but lower quality
 -e EFFORT
    !!Unimplemented!! Set scQOI2 Compression Effort
    Higher values give better compression without quality loss but are slower
Advanced options:
 -d DESCRIPTION
    Embeds a description of the image into the file
    This is usually unnecessary but can be helpful in certain cases
 -l LICENSE
    Embeds license information into the image
    Layout: SPDX Copyright_Year Author_Name
 -nm
    Skip adding standard KQI metadata (File Creation time and Encoder information)
 -a FILE_PATH
    !!Unimplemented!! Specify Alpha Channel (PGM)
    If unspecified, no alpha is added or it is derived from the input image
 -na
    Ignore alpha channel on input image (implicit if -a is specified)
 -i FILE_PATH
    !!Unimplemented!! Embed ICC Color Profile into image
 -c COMMENT
    Add a comment into the KQI bitstream
""")
    sys.exit()

src = sys.argv[1]
out = sys.argv[2]

subsample = False
alpha = True
metadata = True
effort = None
quality = 80
enc_params = " ".join(sys.argv[3:])
comments = []
license = []
description = None
diff_coeff = None

cli_args = []
for arg in sys.argv[3:]:
    if arg.startswith("-"):
        cli_args.append(arg)
    else:
        cli_args[-1]+=" "+arg

for arg in cli_args:
    if arg.startswith("-s"):
        subsample = True
    if arg.startswith("-q"):
        quality = int(arg[3:])
    if arg.startswith("-na"):
        alpha = False
    if arg.startswith("-nm"):
        metadata = False
    if arg.startswith("-c"):
        comments.append(arg[3:])
    if arg.startswith("-d"):
        description = arg[3:]
    if arg.startswith("-l"):
        ls = arg[3:].split()
        license.append(" ".join(ls[0:1])) # SPDX
        license.append("") # License Pretty Name
        license.append(" ".join(ls[2:])) # Author
        license.append(" ".join(ls[1:2])) # Year
    if arg.startswith("--distance"):
        diff_coeff = float(arg[11:])

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

print(f"Encoding [q{quality}, Entropy Effort: {effort}]")
kqi_bytes = encode(input_bitmap, quality, subsample=subsample, alpha=alpha, metadata=metadata, enc_params=enc_params, comments=comments, description=description, license=license, diff_coeff=diff_coeff)
w, h = len(input_bitmap[0]), len(input_bitmap)
print(f"Compressed to {len(kqi_bytes)} bytes ({round((len(kqi_bytes)*8)/(w*h), 3)} bpp) at {w} x {h}.")

open(out, "wb").write(kqi_bytes)
