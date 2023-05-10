from RingSign_Pure import genK
import json

keys = []


def SVkey():
    key = genK()
    keys.append(key)
    vk = key[0]
    sk = key[1]
    return sk, vk


def makejson(keynum):
    port = 50059
    keylist = {}
    for i in range(keynum):
        t = SVkey()
        keylist[port]=[t[0]]
        keylist[port].append(t[1])
        port += 2
    json_str = json.dumps(keylist, indent=4)
    with open('./keys/svkey.json', 'w') as json_file:
        json_file.write(json_str)

    with open("./keys//PKs.txt", "w") as f:
        for i in range(len(keys)):
            pk = keys[i][0]
            f.write(pk + "\n")
    for i in range(keynum):
        with open("./keys/key" + "%d" % (i*2+50051) + ".txt", "w") as f:
            f.write(keys[i][1] + "\n")
            f.write(keys[i][0])

    return


if __name__ == "__main__":
    makejson(5)
