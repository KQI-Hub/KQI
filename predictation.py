from ppmgen import blank_bitmap_list
from bittools import intclamp

def predict_None(residual: list):
    return residual

def predict_Left(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if x == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(residual[y][x-1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(residual[y][x-1][c] - residual[y][x][c]+128)
    return new

def unpredict_Left(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if x == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(new[y][x-1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(new[y][x-1][c] - residual[y][x][c]+128)
    return new

def predict_Up(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(residual[y-1][x] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(residual[y-1][x][c] - residual[y][x][c]+128)
    return new

def unpredict_Up(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(new[y-1][x] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(new[y-1][x][c] - residual[y][x][c]+128)
    return new

def predict_UpL(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 or x == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(residual[y-1][x-1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(residual[y-1][x-1][c] - residual[y][x][c]+128)
    return new

def unpredict_UpL(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 or x == 0:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(new[y-1][x-1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(new[y-1][x-1][c] - residual[y][x][c]+128)
    return new

def predict_UpR(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 or x == scale-1:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(residual[y-1][x+1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(residual[y-1][x+1][c] - residual[y][x][c]+128)
    return new

def unpredict_UpR(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 or x == scale-1:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(new[y-1][x+1] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(new[y-1][x+1][c] - residual[y][x][c]+128)
    return new

def predict_LL(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if x == 0 or x == 1:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(residual[y][x-2] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(residual[y][x-2][c] - residual[y][x][c]+128)
    return new

def unpredict_LL(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if x == 0 or x == 1:
                new[y][x] = residual[y][x]
            else:
                if gray:
                    new[y][x] = intclamp(new[y][x-2] - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        new[y][x][c] = intclamp(new[y][x-2][c] - residual[y][x][c]+128)
    return new

def predict_Avg(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 and x == 0:
                new[y][x] = residual[y][x]
            else:
                yz = (y == 0)
                xz = (x == 0)
                if gray:
                    if yz:
                        new[y][x] = intclamp(residual[y][x-1] - residual[y][x]+128)
                    elif xz:
                        new[y][x] = intclamp(residual[y-1][x] - residual[y][x]+128)
                    else:
                        prv = (residual[y-1][x] + residual[y][x-1])//2
                        new[y][x] = intclamp(prv - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        if yz:
                            new[y][x][c] = intclamp(residual[y][x-1][c] - residual[y][x][c]+128)
                        elif xz:
                            new[y][x][c] = intclamp(residual[y-1][x][c] - residual[y][x][c]+128)
                        else:
                            prv = (residual[y-1][x][c] + residual[y][x-1][c])//2
                            new[y][x][c] = intclamp(prv - residual[y][x][c]+128)
    return new

def unpredict_Avg(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 and x == 0:
                new[y][x] = residual[y][x]
            else:
                yz = (y == 0)
                xz = (x == 0)
                if gray:
                    if yz:
                        new[y][x] = intclamp(new[y][x-1] - residual[y][x]+128)
                    elif xz:
                        new[y][x] = intclamp(new[y-1][x] - residual[y][x]+128)
                    else:
                        prv = (new[y-1][x] + new[y][x-1])//2
                        new[y][x] = intclamp(prv - residual[y][x]+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for c in (0,1,2):
                        if yz:
                            new[y][x][c] = intclamp(new[y][x-1][c] - residual[y][x][c]+128)
                        elif xz:
                            new[y][x][c] = intclamp(new[y-1][x][c] - residual[y][x][c]+128)
                        else:
                            prv = (new[y-1][x][c] + new[y][x-1][c])//2
                            new[y][x][c] = intclamp(prv - residual[y][x][c]+128)
    return new

def predict_Paeth(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 and x == 0:
                new[y][x] = residual[y][x]
            else:
                yz = (y == 0)
                xz = (x == 0)
                if gray:
                    if xz:
                        a = 0
                    else:
                        a = residual[y][x-1]
                    if yz:
                        b = 0
                    else:
                        b = residual[y-1][x]
                    if yz or xz:
                        c = 0
                    else:
                        c = residual[y-1][x-1]

                    p = a + b - c

                    pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)

                    if pa <= pb and pa <= pc:
                        pth = a
                    elif pb <= pc:
                        pth = b
                    else:
                        pth = c

                    new[y][x] = intclamp(residual[y][x]+pth+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for ch in (0,1,2):
                        if xz:
                            a = 0
                        else:
                            a = residual[y][x-1][ch]
                        if yz:
                            b = 0
                        else:
                            b = residual[y-1][x][ch]
                        if yz or xz:
                            c = 0
                        else:
                            c = residual[y-1][x-1][ch]

                        p = a + b - c

                        pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)

                        if pa <= pb and pa <= pc:
                            pth = a
                        elif pb <= pc:
                            pth = b
                        else:
                            pth = c

                        new[y][x][ch] = intclamp(residual[y][x][ch]+pth+128)
    return new

def unpredict_Paeth(residual: list):
    scale = len(residual)
    new = blank_bitmap_list(scale, scale)
    gray = True if type(residual[0][0]) == int else False

    for y in range(scale):
        for x in range(scale):
            if y == 0 and x == 0:
                new[y][x] = residual[y][x]
            else:
                yz = (y == 0)
                xz = (x == 0)
                if gray:
                    if xz:
                        a = 0
                    else:
                        a = new[y][x-1]
                    if yz:
                        b = 0
                    else:
                        b = new[y-1][x]
                    if yz or xz:
                        c = 0
                    else:
                        c = new[y-1][x-1]

                    p = a + b - c

                    pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)

                    if pa <= pb and pa <= pc:
                        pth = a
                    elif pb <= pc:
                        pth = b
                    else:
                        pth = c

                    new[y][x] = intclamp(residual[y][x]-pth+128)
                else:
                    new[y][x] = [0, 0, 0]
                    for ch in (0,1,2):
                        if xz:
                            a = 0
                        else:
                            a = new[y][x-1][ch]
                        if yz:
                            b = 0
                        else:
                            b = new[y-1][x][ch]
                        if yz or xz:
                            c = 0
                        else:
                            c = new[y-1][x-1][ch]

                        p = a + b - c

                        pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)

                        if pa <= pb and pa <= pc:
                            pth = a
                        elif pb <= pc:
                            pth = b
                        else:
                            pth = c

                        new[y][x][ch] = intclamp(residual[y][x][ch]-pth+128)
    return new