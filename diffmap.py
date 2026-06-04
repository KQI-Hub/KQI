def diffmap(mylist: list):
    dm = []
    for i in range(len(mylist)-1):
        dm.append(abs(mylist[i]-mylist[i+1]))
    return dm
