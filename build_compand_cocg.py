companded=[-255]
l = -255
for _ in range(24):
    l+=4
    companded.append(l)
for _ in range(55):
    l+=2
    companded.append(l)
for _ in range(48):
    l+=1
    companded.append(l)
companded.append(0) # 128
l=0
for _ in range(48):
    l+=1
    companded.append(l)
for _ in range(55):
    l+=2
    companded.append(l)
for _ in range(24):
    l+=4
    companded.append(l)
companded[255]=255

print(companded)
print(len(companded))
