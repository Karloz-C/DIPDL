# coding:utf-8
import threading
import time
import os
import socket
import random
import re
from concurrent import futures
import grpc
import blockchain
import grpc_pb2
import grpc_pb2_grpc
import bc_enum
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import bytes_to_long,long_to_bytes
import random
import pickle
import hashlib

global SELF_IP_PORT
global PORT
# SELF_IP_PORT = None
# PORT = None
GET_SELFNODE_FALG = False
Epoch_overing=False
link_broadcast_flag = False
Node_lists=list()
grad_list=list()
pk_list=list()

def set_address(ipport, port):
    global SELF_IP_PORT, PORT
    SELF_IP_PORT = ipport
    PORT = port
    return

def setkey(da_pub_key,da_private):
    global Public_key,Private_key
    Public_key=da_pub_key
    Private_key=da_private
    #print(type(Public_key))

class Node:
    def __init__(self):
        global SELF_IP_PORT, PORT
        self.PORT = PORT
        self.selfipport = SELF_IP_PORT
        self.node_list = self.get_nodes_list()

        #da_file = open('dir_auth_pub_key.pem', 'r')
        #da_pub_key = da_file.read()
        global Public_key
        global Private_key
        self.pubkey=Public_key

        #da_file = open('dir_auth_priv_key.pem','r')
        #da_private = da_file.read()
        self.prikey=Private_key


    def add(self, target):
        global Node_lists
        global flag
        fileObject = open('ipport.txt', 'a')
        test = self.get_nodes_list()
        if type(target) == str:
            if not (target in test):
                print("=> get new Node %s" % target)
                fileObject.write(target)
                #global target_list
                #target_list.append(target)
                fileObject.write('\n')
                # Node_lists.append(target)

                # def link_broadcast():
                #     global link_broadcast_flag
                #     if not link_broadcast_flag:
                #         link_broadcast_flag = True
                #         while link_broadcast_flag:
                #             time.sleep(random.randint(1, 5))
                #             link_broadcast_block = blockchain.Chain.getBlockFromHeight(blockchain.Chain.getHeight())
                #             link_broadcast_block.ExchangeBlock()
                #
                # print("start link_broadcast thread ......")
                # threading.Thread(target=link_broadcast).start()
        elif type(target) == list:
            for i in target:
                self.add(i)
        elif type(target) == tuple:
            self.add("%s:%s" % target)

    # get full node list
    @staticmethod
    def get_nodes_list():
        global Node_lists
        result = list()
        try:
            f = open('ipport.txt', 'r')
            ipport = f.readlines()
            for line in ipport:
                temp1 = line.strip('\n').split(',')
                temp2 = "".join(temp1)
                result.append(temp2)
            Node_lists=result
            return result
            # return Node_lists
        except Exception as e:
            print(e)

    @staticmethod
    def del_node(node):
        test = Node.get_nodes_list()
        test.remove(node)

    # get the number of nodes
    @staticmethod
    def get_length():
        test = Node.get_nodes_list()
        return len(test)

    def grpcNetworkStart(self):
        t = threading.Thread(target=self.__grpcNetworkStart, daemon=True)
        t.start()

    def __grpcNetworkStart(self):
        PORT = self.PORT

        global Public_key
        global Private_key
        Public_key=self.pubkey
        Private_key=self.prikey
        
        try:
            grpc_port = os.environ["GRPC_PORT"]
        except:
            grpc_port = PORT
        print("grpc listen port:" + grpc_port)
        # grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=105))
        grpc_pb2_grpc.add_DiscoveryServicer_to_server(Discovery(), server)
        # grpc_pb2_grpc.add_SynchronizationServicer_to_server(synchronization.Synchronization(), server)
        grpc_pb2_grpc.add_ConsensusServicer_to_server(blockchain.Consensus(), server)
        server.add_insecure_port("127.0.0.1:%s" % PORT)
        server.start()
        global Node_lists
        Node_lists=self.get_nodes_list()

        try:
            ROOT_TARGET = os.environ["ROOT_TARGET"]
        except:
            ROOT_TARGET = "127.0.0.1:" + PORT
        print(ROOT_TARGET)
        t = threading.Thread(target=grpcJoinNode, args=(ROOT_TARGET,self,))
        # grpcJoinNode(ROOT_TARGET)
        print("start grpc_join_node thread ......")
        t.start()
        t.join()
        print("start exchange_loop thread ......")
        threading.Thread(target=self.exchange_loop).start()
        print("exchange loop is ended")

        #获取一个与节点ip对应的公钥列表
        #global target_list


        while True:
            time.sleep(1)

    # 交換節點清單迴圈
    def exchange_loop(self):
        print("<= exchange list broadcast %s" % Node.get_nodes_list())
        print (self.get_nodes_list())
        self.broadcast(bc_enum.SERVICE * bc_enum.DISCOVERY + bc_enum.EXCHANGENODE, self.get_nodes_list())
        time.sleep(1)

    # broadcast
    def broadcast(self, task, message):
        #try:
        self_node = set()
        self_node.add(self.selfipport)
        nodes = set(Node_lists) - self_node
        
        print("print nodes in broadcast:")
        print(nodes)
        task_type, task = int(task / bc_enum.SERVICE), int(task % bc_enum.SERVICE)
        if task_type == bc_enum.DISCOVERY:
            if task == bc_enum.EXCHANGENODE:
                for i in nodes:
                    self.send(i, task, message,task_type)

            #交换梯度使用匿名网络
            if task ==bc_enum.EXCHANGEGRAD:
                #print('接下来进行梯度交换0000')    
                for i in nodes:
                    des_node = set()
                    des_node.add(i)
                    nodes_mid=list(set(nodes)-des_node)
                    if len(nodes)<4:
                        #print('接下来进行梯度交换111') 
                        route_list=[]
                        for num in range(3):
                            route_list.append('none'.encode())
                        mes_hash=hashlib.new("sha256")
                        mes_hash.update(message)
                        mes_sha256=mes_hash.hexdigest().encode()
                        channel = grpc.insecure_channel(i)
                        stub = grpc_pb2_grpc.DiscoveryStub(channel)
                        des_pk=stub.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                        des_pk=RSA.importKey(des_pk)   
                        des_pk=PKCS1_OAEP.new(des_pk)
                        mes_sha256=des_pk.encrypt(mes_sha256)
                        route_list.append(mes_sha256)
                        route_list.append(message)
                        global SELF_IP_PORT
                        route_list.append(SELF_IP_PORT.encode())
                        self.send(i, task, route_list,task_type)
                    else:
                        #print('接下来进行梯度交换222') 
                        channel = grpc.insecure_channel(i)
                        stub = grpc_pb2_grpc.DiscoveryStub(channel)
                        des_pk=stub.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                        an_index=[]
                        mes_hash=hashlib.new("sha256")
                        mes_hash.update(message)
                        mes_sha256=mes_hash.hexdigest().encode()
                        #选取三个中间节点
                        x_random=[]
                        for num_ in range(3):    
                            while True:
                                index_=random.randint(0,len(nodes_mid)-1)
                                #pk=pk_list[index_]
                                #if (pk!=self.pubkey)&(pk!=des_pk):
                                if index_ not in an_index:
                                    break
                            #pk = RSA.importKey(pk)
                            #pk=PKCS1_OAEP.new(pk)
                            #an_pk.append(pk)
                            an_index.append(index_)

                            while True:
                                x=random.randint(0,2)
                                if x not in x_random:
                                    x_random.append(x)
                                    break
                        print("该数据包建立的路径为：",SELF_IP_PORT,'->',nodes_mid[an_index[0]],'->',nodes_mid[an_index[1]],'->',nodes_mid[an_index[2]],'->',i)
                        #global target_list
                        des_pk=RSA.importKey(des_pk)   
                        des_pk=PKCS1_OAEP.new(des_pk)
                        #接下来对信息层层加密
                        mes_sha256=des_pk.encrypt(mes_sha256)
                        route_list=[]
                        for x in x_random:
                            if x+1<3:
                                channel_1 = grpc.insecure_channel(nodes_mid[an_index[x]])
                                stub_1 = grpc_pb2_grpc.DiscoveryStub(channel_1)
                                pk_1=stub_1.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                                pk_1 = RSA.importKey(pk_1)
                                pk_1=PKCS1_OAEP.new(pk_1)
                                route_list.append(pk_1.encrypt(nodes_mid[an_index[x+1]].encode()))
                            if x==2:
                                channel_1 = grpc.insecure_channel(nodes_mid[an_index[2]])
                                stub_1 = grpc_pb2_grpc.DiscoveryStub(channel_1)
                                pk_1=stub_1.tell_public_key(grpc_pb2.Message(value="hello")).value.encode()
                                pk_1 = RSA.importKey(pk_1)
                                pk_1=PKCS1_OAEP.new(pk_1)
                                route_list.append(pk_1.encrypt(i.encode()))
                        route_list.append(mes_sha256)
                        route_list.append(message)
                        #global SELF_IP_PORT
                        route_list.append(SELF_IP_PORT.encode())
                        self.send(nodes_mid[an_index[0]], task, route_list,task_type)

                        #message=an_pk[2].encrypt((i+'+').encode()+message)
                        #message=an_pk[1].encrypt((Node_lists[an_index[2]]+'+').encode()+message)
                        #message=an_pk[0].encrypt((Node_lists[an_index[1]]+'+').encode()+message)
                        #for route in route_list:
                        #    self.send(Node_lists[an_index[0]], task, route)

                        #self.send(Node_lists[an_index[0]], task, message)  #发送包裹后的信息


        #except Exception as e:
        #    print(e)

    # send
    def send(self, node, task, message,task_type):
        try:
            channel = grpc.insecure_channel(node)
            #task_type, task = int(task / bc_enum.SERVICE), int(task % bc_enum.SERVICE)
            if task_type == bc_enum.DISCOVERY:
                stub = grpc_pb2_grpc.DiscoveryStub(channel)
                if task == bc_enum.EXCHANGENODE:
                    # print("checkpoint11111")
                    response = stub.ExchangeNode(grpc_pb2.Node(number=self.get_length(), ipport=self.get_nodes_list()))
                    # print("checkpoint22222")
                    for i in response.ipport:
                        if i not in Node_lists:
                            self.add(i)
                if task ==bc_enum.EXCHANGEGRAD:
                    response=stub.ExchangeGrad(grpc_pb2.Parameter(para=message))
                    print(response.Result)

            elif task_type == bc_enum.SYNCHRONIZATION:
                stub = grpc_pb2_grpc.SynchronizationStub(channel)
                # synchronization.Task(stub, task, message)
        except Exception as e:
            print(e)
            # Node.del_node(node)
        return
    def send_epoch(self):
        self_node = set()
        self_node.add(self.selfipport)
        print(self_node)
        nodes = set(self.get_nodes_list()) - self_node
        num=0
        stubs=list()
        for i in nodes:
            channel = grpc.insecure_channel(i)
            stub= grpc_pb2_grpc.DiscoveryStub(channel)
            stubs.append(stub)
        for i in stubs:
            i.Epoch_over(grpc_pb2.Epoch(flag='1'))
        return

def send_epoch_over(node):
    channel = grpc.insecure_channel(node)
    stub = grpc_pb2_grpc.DiscoveryStub(channel)
    stub.Epoch_over(grpc_pb2.Epoch(flag='1'))

tempPort = 0

def __temp_socket(nodePort,node):
    global tempPort
    while tempPort == 0:
        port = int(PORT) + 1
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.bind(("127.0.0.1", port))
            s.listen(1)
            tempPort = port
            (conn, client_addr) = s.accept()
            tempPort = 0
            print("=> Node IP:%s" % client_addr[0])
            conn.send(client_addr[0].encode('utf-8'))
            conn.close()
            s.close()
            Node.add(node,(client_addr[0], nodePort))  # ip:port
        except Exception as e:
            print(e)


# 欲告訴對方你的 port
def talk_you_ip(node_port,node):
    global tempPort
    if tempPort == 0:
        threading.Thread(target=__temp_socket, args=(node_port,node,)).start()
        # __temp_socket(node_port)
    while tempPort == 0:
        time.sleep(1)
    return tempPort


class Discovery(grpc_pb2_grpc.DiscoveryServicer):

    def tell_public_key(self,request,context):
        global Public_key
        text=request.value
        return grpc_pb2.Message(value=Public_key.decode())

    # exchange node list
    def ExchangeNode(self, request, context):
        global Node_lists
        # print("I am here!!!!!!!!!!!!!!!!!!!!!")
        for i in request.ipport:
            if i not in Node_lists:
                Node_lists.append(i)
        return grpc_pb2.Node(number=Node.get_length(), ipport=Node_lists)

    # 告知對方他的ip,及自己的 grpc port,
    # 返回對方所開的port ->將再次連線取得自己ip
    def Hello(self, request, context):
        global PORT, SELF_IP_PORT
        selfIP = request.value[0:request.value.index(':')]
        node=Node()
        node.PORT=PORT
        node.selfipport=SELF_IP_PORT
        Node.add(node,(selfIP, PORT))
        SELF_IP_PORT = "%s:%s" % (selfIP, PORT)
        print("print in Hello:")
        print(SELF_IP_PORT)
        nodePort = request.value[request.value.index(':') + 1:len(request.value)]
        print("=> Node Port:%s" % nodePort)
        port = talk_you_ip(nodePort,node)
        return grpc_pb2.Message(value=str(port))

    def ExchangeGrad(self,request,context):
        #mes_list=[]
        #des_list=[]  #存下个转发地ipport
        global Private_key
        sk = RSA.importKey(Private_key)
        sk=PKCS1_OAEP.new(sk)
        global grad_list
        try:
            sha256_recv=sk.decrypt(request.para[3])
            h_sha256 = hashlib.new("sha256")
            h_sha256.update(request.para[4])
            sha256_real=h_sha256.hexdigest().encode()
            print("上一个中转节点ip端口为：",request.para[5].decode())
            if sha256_recv==sha256_real:
                grad_list.append(request.para[4])
                #print(request.para[4])
            return grpc_pb2.TensorReceive(Result='Grad Message Received Successfully')
        except:
            for x in range(3):
                try:
                    des=sk.decrypt(request.para[x]).decode()
                    break
                except:
                    ll=0          
            print("上一个中转节点ip端口为：",request.para[5].decode())
            channel = grpc.insecure_channel(des)
            stub = grpc_pb2_grpc.DiscoveryStub(channel)
            request.para[5]=SELF_IP_PORT.encode()
            response=stub.ExchangeGrad(grpc_pb2.Parameter(para=request.para))
            print(response.Result)
            print('下一中转节点or最终节点ip端口为：',des)            
            return grpc_pb2.TensorReceive(Result='Grad Message Received Successfully')
            


    def Epoch_over(self,request,context):
        global Epoch_overing
        Epoch_overing=True
        return grpc_pb2.Epoch(flag='1')

def grpcJoinNode(target,node):
    global PORT, GET_SELFNODE_FALG, SELF_IP_PORT
    compi = re.compile('^(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}):(\d{1,5})$')
    result = compi.match(target)
    node.add(target)
    # 判斷是否已取得自己IP
    if GET_SELFNODE_FALG:
        print("already get self ip")
        return True
    ip = result.group(1)
    print("<= grpc link to %s" % target)
    channel = grpc.insecure_channel(target)
    stub = grpc_pb2_grpc.DiscoveryStub(channel)
    time.sleep(3)
    try:
        print("hello message: %s:%s" % (ip, PORT))
        hello_response = stub.Hello(grpc_pb2.Message(value="%s:%s" % (ip, PORT)))
        print("hello_response", hello_response)
    except Exception as e:
        print(e)
        return False
    helloPort = hello_response.value
    time.sleep(1)
    # socket get my ip
    print("=> hello port:%s" % helloPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("<= connect to socket will get myIP")
    sock.connect((ip, int(helloPort)))
    myIP = sock.recv(1024).decode()
    print("=> get myIP:%s" % myIP)
    node.add((myIP, PORT))
    SELF_IP_PORT = "%s:%s" % (myIP, PORT)
    print("print in grpcJoinNode:")
    print(SELF_IP_PORT)
    GET_SELFNODE_FALG = True
    return True
