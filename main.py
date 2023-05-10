import time
import blockchain
import threading
import key_Generate
import MNIST_training_DP
import MNIST_training_pure
import MNIST_training_krum
import p2p
import sys
import json
import signer
import decen_training
from blockchain import Blockchain
from RingSign_Pure import RingSign
from Crypto.PublicKey import RSA
import re
import Hash

# _first_block = block.Block().first_block()
# print(_first_block)

if __name__ == '__main__':
    Hash.getR()
    # p2p-grpc initializaiton
    file = open("ipport.txt", 'w').close()
    key = RSA.generate(1024)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    ipport = sys.argv[1]
    port = sys.argv[2]
    num = 5
    #da_file = open('public_key1.pem', 'r')
    #da_pub_key = da_file.read()
    #da_file = open('private_key1.pem','r')
    #da_private = da_file.read()
    signer.set_id_num(port,num)
    p2p.setkey(public_key,private_key)
    p2p.set_address(ipport, port)
    # 设置全局变量SELF_IP_PORT, PORT
    #with open('svkey.json', 'r', encoding='utf8') as fp:
    #    svkey = json.load(fp)
    #    sk = svkey[port][0]
    #    vk = svkey[port][1]
    #    signer.init_signer(int(sk,base=16), int(vk,base=16))
    Node = p2p.Node()
    # 创建一个Node，包含SELF_IP_PORT, PORT，以及Node_list
    Node.grpcNetworkStart()
    time.sleep(15)    #等待所有节点准备就绪
    MNIST_training_krum.run(0)