from ppmgen import ppm_from_list, ppm_to_list
from kqitool import decode, generator_is_my_name

#input = open("400SD4.ppm", "rb").read()
#bitmap = convppm_to_list(input)
#output = encode(bitmap)
#open("400SD4.kqi", "wb").write(output)

inputf = open("randomly-generated.kqi", "rb").read()
bmp = decode(inputf)
ppm = ppm_from_list(bmp)
open("randomly-generated.ppm", "wb").write(ppm)

#pgm = ["P2\n8 8\n255\n"]
#for v in out:
#    pgm.append(str(v))
#pgm = " ".join(pgm)+"\n"

#kqi = generator_is_my_name()
#open("randomly-generated.kqi", "wb").write(kqi)
