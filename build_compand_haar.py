companded=[-510]
l = -511
for _ in range(16):
    l+=10
    companded.append(l)
for _ in range(16):
    l+=8
    companded.append(l)
for _ in range(32):
    l+=4
    companded.append(l)
for _ in range(32):
    l+=2
    companded.append(l)
for _ in range(31):
    l+=1
    companded.append(l)
companded.append(1) # 128
l=1
for _ in range(31):
    l+=1
    companded.append(l)
for _ in range(32):
    l+=2
    companded.append(l)
for _ in range(32):
    l+=4
    companded.append(l)
for _ in range(16):
    l+=8
    companded.append(l)
for _ in range(16):
    l+=10
    companded.append(l)
companded[255]=510

print(companded)
