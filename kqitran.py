#!/usr/bin/env python3
"""kmi/kqitran [v0.0.0]"""
import sys, mcv
from datetime import datetime

print(__doc__)

if len(sys.argv) < 3:
    print(f"""
USAGE: {sys.argv[0]} MODE FILE.kqi [options...]
 MODE
    kqitran's operation mode
     i (inspect mode)
         gets information about a KQI File
 FILE
    the KQI file to inspect
""")
    sys.exit()

mode = sys.argv[1]
src = sys.argv[2]
src_fn = sys.argv[2].split('/')[-1]

kqi_data = open(src, "rb").read()

def kqi_to_chunks(kqi_bytes: bytes, verbose: bool = False):
    if kqi_bytes[0:4] != b'kqif':
        raise ValueError("Not a KQI Image!")
    img_w = int.from_bytes(kqi_bytes[4:8], "little")
    img_h = int.from_bytes(kqi_bytes[8:12], "little")
    channels = kqi_bytes[12]
    colorspace = kqi_bytes[13]
    is_subsampled = bool(kqi_bytes[14])
    reserved = kqi_bytes[15]

    bw = 16 # start at the start of the 1st chunk
    chunk_layout = []
    chunk_data = []
    while True:
        TwoCC = kqi_bytes[bw:bw+2]
        if TwoCC == b'eF':
            break
        if len(TwoCC) != 2:
            raise EOFError("Read past end of KQI file, eF marker missed")

        chk_len = int.from_bytes(kqi_bytes[bw+2:bw+8], "little")

        chunk_layout.append(TwoCC.decode('ascii'))
        chunk_data.append(kqi_bytes[bw+8:bw+8+chk_len])

        if TwoCC in (b'sY', b'sO', b'sG', b'tC', b'tE', b'tL', b'tD', b'tX', b'aL', b'cS'):
            if verbose:
                print(f"{TwoCC.decode('ascii')} Chunk Found: {chk_len} Bytes")
        else:
            print(f"Unknown {TwoCC.decode('ascii')} Chunk Found: {chk_len} Bytes") # simply print unknown chunk statistics
        bw+=chk_len+8
    return img_w, img_h, channels, colorspace, is_subsampled, reserved, chunk_layout, chunk_data

cli_args = []
for arg in sys.argv[3:]:
    if arg.startswith("-"):
        cli_args.append(arg)
    else:
        cli_args[-1]+=" "+arg

if mode == 'i':
    print("Reading...")
    img_w, img_h, channels, colorspace, is_subsampled, reserved, chunk_layout, chunk_data = kqi_to_chunks(kqi_data)
    print(f"{src_fn} - {img_w}x{img_h}, {channels} channels, {('sRGB', 'Linear RGB', 'Custom/ICC')[colorspace]}, px_fmt YCoCgRC{('444', '420')[is_subsampled]}, {len(chunk_layout)} chunks")
    print('Chunk Layout:')
    print('  '+' '.join(chunk_layout))
    if 'tC' in chunk_layout:
        print('File created on', datetime.fromisoformat(chunk_data[chunk_layout.index('tC')].decode('UTF-8')).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"))
    if 'tE' in chunk_layout:
        enc_info = mcv.load(chunk_data[chunk_layout.index('tE')].decode('UTF-8'))
        if all(key in enc_info for key in ('name', 'version', 'build_date', 'params', 'input_fn', 'output_fn')):
            print(f"encoder - {enc_info['name']} v{enc_info['version']}")
            if enc_info['build_date']:
                print('built on', enc_info['build_date'])
            if enc_info['params']:
                print('encode parameters:', enc_info['params'])
            if enc_info['input_fn']:
                print('encoder input:', enc_info['input_fn'])
            if enc_info['output_fn']:
                print('original filename:', enc_info['output_fn'])
        else:
            print("File has invalid tE chunk!")
    if 'tL' in chunk_layout:
        license_info = mcv.load(chunk_data[chunk_layout.index('tL')].decode('UTF-8'))
        if all(key in license_info for key in ('name', 'year', 'author', 'license')):
            print(f"Copyright (c) {enc_info['year']} {enc_info['author']}")
            if license_info['license']:
                print('SPDX:', license_info['license'])
            if license_info['name']:
                print('Pretty name:', license_info['name'])
        else:
            print("File has invalid tL chunk!")
    if 'tD' in chunk_layout:
        print('Image description:', chunk_data[chunk_layout.index('tD')].decode('UTF-8'))
    for c, b in zip(chunk_layout, chunk_data):
        if c == 'tX':
            print('KQI Comment:', b.decode('UTF-8'))

for arg in cli_args:
    pass
