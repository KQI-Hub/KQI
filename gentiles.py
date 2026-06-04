import math

from diffmap import diffmap

π = math.pi
datfile_lines = ["minidctmap = []\nminidctdiffmap = []"]

for v in range(8):
    for u in range(8):
        floatmap = []
        pixmap = []
        for y in range(8):
            for x in range(8):
                floatmap.append(math.cos(((2 * x) + 1)*(u * π) / 16) * math.cos( ( (2 * y) + 1)*(v * π) / 16))
        for f in floatmap:
            pixmap.append( int((f*128)+127.5) )

        # this adds the appends to the minidctmap inside the generated python file
        datfile_lines.append(f"minidctmap.append("+str(pixmap)+")")
        datfile_lines.append(f"minidctdiffmap.append("+str(diffmap(pixmap))+")")

# this code here generates a folder full of pgm files with all 64 possible tiles
#        pgm = "P2\n8 8\n255\n"
#        pgm_data = []
#        for px in pixmap:
#            pgm_data.append(str(px))
#        pgm += " ".join(pgm_data)
#        pgm += "\n"
#        open(f"tiles/{u}_{v}.pgm", "w").write(pgm)

# this generates a python file containing the tilemap
open(f"minidcttilemap.py", "w").write("\n".join(datfile_lines)+'\nopen(f"minidcttilemap.py", "w").write("""minidctmap="""+str(minidctmap).replace(" ", "")+"\\n"+"minidctdiffmap="+str(minidctdiffmap).replace(" ", ""))')
