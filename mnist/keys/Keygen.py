from importlib import import_module


import sys
sys.path.append('../')
from RingSign_Pure import genK

keys=[]
for i in range(10):
    keys.append(genK())

with open("./PK.txt","w") as f:
    for i in range(len(keys)):
        pk=keys[i][0]
        f.write(pk+"\n")

for i in range(10):
    with open("./keys"+"%d"%(i)+".txt","w") as f:
        f.write(keys[i][0]+"\n")
        f.write(keys[i][1])
        