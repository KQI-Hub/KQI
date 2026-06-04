from ppmgen import ppm_from_list, ppm_to_list, pgm_from_list
from kqitool import decode, generator_is_my_name, bitmap_to_chunkmap, chunkmap_to_bitmap

#input = open("400SD4.ppm", "rb").read()
#bitmap = convppm_to_list(input)
#output = encode(bitmap)
#open("400SD4.kqi", "wb").write(output)

#inputf = open("randomly-generated-1024x1024.kqi", "rb").read()
#bmp = decode(inputf)
#ppm = ppm_from_list(bmp)
#open("randomly-generated.ppm", "wb").write(ppm)

#pgm = ["P2\n8 8\n255\n"]
#for v in out:
#    pgm.append(str(v))
#pgm = " ".join(pgm)+"\n"

#kqi = generator_is_my_name(1024, 1024)
#open("randomly-generated-1024x1024.kqi", "wb").write(kqi)

inputfile = open("rtx0.ppm", "rb").read()
listed = ppm_to_list(inputfile)
gh = bitmap_to_chunkmap(listed)
hg = chunkmap_to_bitmap(gh, len(listed[0]), len(listed))
ppmed = ppm_from_list(hg)
open("ieatsand.ppm", "wb").write(ppmed)
