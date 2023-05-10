# coding:utf-8
import base64
import binascii
import grpc
import grpc_pb2
import grpc_pb2_grpc
from google.protobuf.json_format import    MessageToJson
import time
import re
import hashlib
import threading
import p2p
from subprocess import *
import signer
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import bytes_to_long,long_to_bytes
import random

_compiNum = re.compile("^\d+$")  # 判斷全數字用
_compiW = re.compile("^\w{64}")

#匿名网络函数之一:
def anonymous(i,nodes,request):
    des_node = set()
    des_node.add(i)
    nodes_mid=list(set(nodes)-des_node)
    #request.route_list=[]
    channel = grpc.insecure_channel(i)
    stub = grpc_pb2_grpc.ConsensusStub(channel)
    des_pk=stub.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
    des_pk=RSA.importKey(des_pk)
    des_pk=PKCS1_OAEP.new(des_pk)
    an_index=[]
    x_random=[]
    #如果节点数小于4个，则放弃使用匿名网络
    if len(nodes)<4:
        for num_ in range(3):
            request.route_list.append('none'.encode())
        ver=des_pk.encrypt(i.encode())
        request.route_list.append(ver)
        request.route_list.append(p2p.SELF_IP_PORT.encode())
        return request,i
    else:
        #选取三个中间节点
        for num_ in range(3):
            while True:
                index_=random.randint(0,len(nodes_mid)-1)
                if index_ not in an_index:
                    break
            an_index.append(index_)

            while True:
                x=random.randint(0,2)
                if x not in x_random:
                    x_random.append(x)
                    break

        print("该数据包建立的路径为：",p2p.SELF_IP_PORT,'->',nodes_mid[an_index[0]],'->',nodes_mid[an_index[1]],'->',nodes_mid[an_index[2]],'->',i)

        #接下来对信息层层加密
        ver=des_pk.encrypt(i.encode())
        for x in x_random:
            if x+1<3:
                channel_1 = grpc.insecure_channel(nodes_mid[an_index[x]])
                stub_1 = grpc_pb2_grpc.ConsensusStub(channel_1)
                pk_1=stub_1.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                pk_1 = RSA.importKey(pk_1)
                pk_1=PKCS1_OAEP.new(pk_1)
                request.route_list.append(pk_1.encrypt(nodes_mid[an_index[x+1]].encode()))
            if x==2:
                channel_1 = grpc.insecure_channel(nodes_mid[an_index[2]])
                stub_1 = grpc_pb2_grpc.ConsensusStub(channel_1)
                pk_1=stub_1.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                pk_1 = RSA.importKey(pk_1)
                pk_1=PKCS1_OAEP.new(pk_1)
                request.route_list.append(pk_1.encrypt(i.encode()))
        request.route_list.append(ver)
        request.route_list.append(p2p.SELF_IP_PORT.encode())

    #request.route_list=route
        return request,nodes_mid[an_index[0]]

def signing(data):
    pat = r'[A-Z0-9]{64}'
    p1 = run(['./ringsign.exe', signer.get_size(), signer.get_id(), '0', hashlib.md5(data).hexdigest()], capture_output=True,check=True)
    sign = re.findall(r'[A-Z0-9]{64}',str(p1.stdout))
    sign = [int(i,16) for i in sign]
    return sign


def verifying(data, str_sign):
    arg = ['./ringsign.exe', signer.get_size(), signer.get_id(), '1', hashlib.md5(data).hexdigest()]
    for i in str_sign:
        arg.append(hex(int(i))[2:])
        #print(i)
    p2 = run(arg, capture_output=True,check=True)

    return bool(str(p2.stdout)[-2:-1])



def hash_block(block: grpc_pb2.Block) -> str:
    hash_str = block.SerializeToString()
    s = hashlib.sha256()  # Get the hash algorithm.
    s.update(hash_str)  # Hash the data.
    hash = s.hexdigest()  # Get he hash value.
    return hash


global pre_prepare_receive

class Blockchain:
    def __init__(self):
        self.node_id = p2p.PORT
        self.nodes = set()
        self.chain = []
        self.role = self.leader_select()
        self.lastBlock = None
        self.prepare_message_receive = []
        self.commit_message_receive = []
        # Genesis block
        block = self.create_block(None)
        self.add_block(block)

    def add_block(self, block):
        self.chain.append(block)
        self.lastBlock = block

    def create_block(self, tensor) -> grpc_pb2.Block:
        if self.lastBlock is None:
            block = grpc_pb2.Block(
                height=1,
                timestamp=int(time.time()),
                previoushash=b'',
                txshash=[],
                krumgrad=b''
            )
        else:
            block = grpc_pb2.Block(
                height=self.lastBlock.height + 1,
                timestamp=int(time.time()),
                previoushash=hash_block(self.lastBlock),
                txshash=[],
                krumgrad=tensor
            )
        return block

    def leader_select(self):
        if self.node_id == "50061":
            return 'leader'
        else:
            return 'member'

    def block_hash(self, Block):
        return Block.block_hash

    def block_height(self, block):
        return block.height

    def block_tx(self, block):
        return block.tx

    def consensus_process(self, tensor):
        # PRE-PREPARE
        global block, pre_prepare_receive
        if self.role == 'leader':
            block = self.create_block(tensor)
            t = threading.Thread(target=self.pre_prepare(block))
            t.start()
            t.join()
        # PREPARE
        if self.role == 'member':
            for i in range(10):
                time.sleep(5)
                if pre_prepare_receive is not None:
                    t = threading.Thread(target=self.prepare(pre_prepare_receive, tensor))
                    t.start()
                    t.join()
                    count1 = 0
                    time.sleep(3)
                    for response in self.prepare_message_receive:
                        count1 += 1
                    if count1 > len(self.nodes) * 2 / 3:
                        # COMMIT
                        t = threading.Thread(target=self.commit())
                        t.start()
                        t.join()
                        count2 = 0
                        for commit_response in self.commit_message_receive:
                            count2 += 1
                        if count2 > len(self.nodes) * 2 / 3:
                            self.add_block(pre_prepare_receive)
                            pre_prepare_receive = None
                            break
                    pre_prepare_receive = None
                    break
                else:
                    continue
        else:
            time.sleep(5)
            t = threading.Thread(target=self.prepare(block, tensor))
            t.start()
            t.join()
            count1 = 0
            time.sleep(3)
            for response in self.prepare_message_receive:
                count1 += 1
            if count1 > len(self.nodes) * 2 / 3:
                # COMMIT
                t = threading.Thread(target=self.commit())
                t.start()
                t.join()
                count2 = 0
                for commit_response in self.commit_message_receive:
                    count2 += 1
                if count2 > len(self.nodes) * 2 / 3:
                    self.add_block(block)



    # PRE-PREPARE
    def pre_prepare(self, block):
        request = grpc_pb2.PrePrepareMsg()
        request.data.node_id = self.node_id
        # https://stackoverflow.com/questions/18376190/attributeerror-assignment-not-allowed-to-composite-field-task-in-protocol-mes/22771612#22771612
        request.data.block.CopyFrom(block)
        a = request.data.SerializeToString()
        temp_sign = signing(a)
        s=list()
        for i in temp_sign:
            s.append(str(i))
        request.signature = ",".join(s)
        self_node = set()
        self_node.add(p2p.SELF_IP_PORT)
        print(self_node)
        nodes = set(p2p.Node.get_nodes_list()) - self_node
        #print("print nodes in broadcast:")
        print(nodes)
        for i in nodes:
            channel = grpc.insecure_channel(i)
            stub = grpc_pb2_grpc.ConsensusStub(channel)
            try:
                #print("PRE-PREPARE checkpoint 1")
                response = stub.PrePrepare(request)
                #print("PRE-PREPARE checkpoint 2")
                #print(response.Result)
            #except:
            #    
                # PREPARE_flag=False
            #    break
            except Exception as e:
                print("CONNECTION FAILED IN PRE—PREPARE PHASE!")
                print("get except: %s" % str(e))

    # PREPARE PHASE
    # 1. verify pre_prepare message
    # 2. broadcast prepare message if step 1 is passed
    def prepare(self, block, tensor):
        request = grpc_pb2.PrepareMsg()
        request.data.node_id = self.node_id
        # krum_grad=Tensor.deserialize_torch_tensor(block.krumgrad)
        # krum_grad1=Tensor.deserialize_torch_tensor(tensor)
        if tensor == block.krumgrad:
            # if krum_grad.equal(krum_grad1):
            request.data.vote = '1'
        else:
            request.data.vote = '0'
        a = request.data.SerializeToString()
        temp_sign = signing(a)
        s = list()
        for i in temp_sign:
            s.append(str(i))
        request.signature = ",".join(s)

        self_node = set()
        self_node.add(p2p.SELF_IP_PORT)
        print(self_node)
        nodes = set(p2p.Node.get_nodes_list()) - self_node
        #print("print PERPARE nodes in broadcast:")
        print(nodes)
        for i in nodes:
            request,des_ip=anonymous(i,nodes,request)
            #request.route_list=route
            channel = grpc.insecure_channel(des_ip)
            stub = grpc_pb2_grpc.ConsensusStub(channel)
            try:
                # print("PREPARE checkpoint 1")
                response = stub.Prepare(request)
                #response = stub.Prepare(request)
                # print("PREPARE checkpoint 2")
                #print(response.Result)
                # PREPARE_flag=True
                self.prepare_message_receive.append(response)
            except:
                print("CONNECTION FAILED IN PREPARE PHASE!")
                # PREPARE_flag=False
                break

    # COMMIT PHASE
    # 1. verify if 2N/3 prepare messages are received
    # 2. broadcast commit message if step 1 is passed
    def commit(self):
        request = grpc_pb2.CommitMsg()
        request.data.node_id = self.node_id
        request.data.vote = '1'
        a = request.data.SerializeToString()

        temp_sign = signing(a)
        s = list()
        for i in temp_sign:
            s.append(str(i))
        request.signature = ",".join(s)

        self_node = set()
        self_node.add(p2p.SELF_IP_PORT)
        #print(self_node)
        nodes = set(p2p.Node.get_nodes_list()) - self_node
        #print("print nodes in broadcast:")
        print(nodes)
        for i in nodes:
            print(i)
            request,des_ip=anonymous(i,nodes,request)
            channel = grpc.insecure_channel(des_ip)
            stub = grpc_pb2_grpc.ConsensusStub(channel)
            try:
                print("COMMIT checkpoint 1")
                response = stub.Commit(request)
                print("COMMIT checkpoint 2")
                print(response.Result)
                self.commit_message_receive.append(response)
            except:
                print("CONNECTION FAILED IN COMMIT PHASE!")
                # PREPARE_flag=False
                break


# Consensus using gRPC
class Consensus(grpc_pb2_grpc.ConsensusServicer):
    def tell_public_key(self,request,context):
        text=request.value
        return grpc_pb2.Message(value=p2p.Public_key.decode())

    def PrePrepare(self, request, context):
        global pre_prepare_receive
        a = request.data.SerializeToString()
        if verifying(a, request.signature.split(',')):
            #print("Pre-prepare message is checked")
            pre_prepare_receive = grpc_pb2.Block()
            pre_prepare_receive.CopyFrom(request.data.block)
            #print("Pre-prepare block is received")
            return grpc_pb2.ConsensusRsp(Result='Pre-prepare Received Successfully')

    def Prepare(self, request, context):
        #print("Prepare message is received")
        #vk = VerifyingKey.from_string(bytes.fromhex(svkey[request.data.node_id][1]), curve=NIST384p)
        sk = RSA.importKey(p2p.Private_key)
        sk=PKCS1_OAEP.new(sk)
        try:
            myip=sk.decrypt(request.route_list[3]).decode()
            print("上一个中转节点ip:",request.route_list[4].decode())
            a = request.data.SerializeToString()
            if verifying(a, request.signature.split(',')):
                if request.data.vote == '1':
                    #print("vote=====1")
                    return grpc_pb2.ConsensusRsp(Result='Prepare Received Successfully')

        #无法解密则说明是中间节点，则接下来进行信息的转发
        except:       
            for x in range(3):
                try:
                    des=sk.decrypt(request.route_list[x]).decode()
                    break
                except:
                    ll=0          
            print("上一个中转节点ip端口为：",request.route_list[4].decode())
            channel = grpc.insecure_channel(des)
            stub = grpc_pb2_grpc.ConsensusStub(channel)
            print('下一中转节点or最终节点ip端口为：',des) 
            request.route_list[4]=p2p.SELF_IP_PORT.encode()
            response = stub.Prepare(request)
            return grpc_pb2.ConsensusRsp(Result='Prepare Received Successfully') 

    def Commit(self, request, context):
        #print("Commit message is received")
        #vk = VerifyingKey.from_string(bytes.fromhex(svkey[request.data.node_id][1]), curve=NIST384p)
        sk = RSA.importKey(p2p.Private_key)
        sk=PKCS1_OAEP.new(sk)
        try:
            myip=sk.decrypt(request.route_list[3]).decode()
            print("上一个中转节点ip:",request.route_list[4].decode())
            a = request.data.SerializeToString()
            if verifying( a, request.signature.split(',')):
                if request.data.vote == '1':
                    return grpc_pb2.ConsensusRsp(Result='Commit Received Successfully')

        #无法解密则说明是中间节点，则接下来进行信息的转发
        except:
            for x in range(3):
                try:
                    des=sk.decrypt(request.route_list[x]).decode()
                    break
                except:
                    ll=0          
            print("上一个中转节点ip端口为：",request.route_list[4].decode())
            channel = grpc.insecure_channel(des)
            stub = grpc_pb2_grpc.ConsensusStub(channel)
            print('下一中转节点or最终节点ip端口为：',des) 
            request.route_list[4]=p2p.SELF_IP_PORT.encode()
            response = stub.Commit(request)
            return grpc_pb2.ConsensusRsp(Result='Commit Received Successfully')
