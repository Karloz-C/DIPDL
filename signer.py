from RingSign_Pure import RingSign
import p2p

global signer

def init_signer(sk,pk):
    global signer
    signer = RingSign(sk, pk)
    return
def get_signer():
    global signer
    return signer


global id,size
def set_id(port):
    global id,size
    f = open('ipport.txt', 'r')
    ipport = f.readlines()
    size = str(len(ipport))
    id = port
def set_id_num(port,num):
    global id,size
    f = open('ipport.txt', 'r')
    ipport = f.readlines()
    size = str(num)
    id = port
def get_id():
    global id
    return id
def get_size():
    global size
    return size