def ppm_from_list(bitmap, desc = None):
    ppmhead = "P6\n" # raw format
    ppmbody = bytearray() # byte array

    if desc:
        ppmhead += "# {desc}\n"

    ppmhead += f"{len(bitmap[0])} {len(bitmap)}\n"
    ppmhead += "255\n"

    for row in bitmap:
        for pixel in row:
            ppmbody.append(pixel[0])
            ppmbody.append(pixel[1])
            ppmbody.append(pixel[2])

    return ppmhead.encode() + bytes(ppmbody)

def ppm_to_list(bytes):
    if not bytes.startswith(b"P6"):
        raise Exception("Unsupported PPM!")