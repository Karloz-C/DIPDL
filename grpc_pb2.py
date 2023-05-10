# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngrpc.proto\"\x15\n\x05\x45poch\x12\x0c\n\x04\x66lag\x18\x01 \x01(\t\"\x19\n\tParameter\x12\x0c\n\x04para\x18\x01 \x03(\x0c\"c\n\x05\x42lock\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x11\n\ttimestamp\x18\x02 \x01(\x04\x12\x14\n\x0cprevioushash\x18\x03 \x01(\t\x12\x0f\n\x07txshash\x18\x04 \x03(\t\x12\x10\n\x08krumgrad\x18\x05 \x01(\x0c\"\x89\x01\n\rPrePrepareMsg\x12!\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x13.PrePrepareMsg.Data\x12\x11\n\tsignature\x18\x02 \x01(\t\x1a\x42\n\x04\x44\x61ta\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x15\n\x05\x62lock\x18\x02 \x01(\x0b\x32\x06.Block\x12\x12\n\nblock_hash\x18\x03 \x01(\t\"z\n\nPrepareMsg\x12\x1e\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x10.PrepareMsg.Data\x12\x11\n\tsignature\x18\x02 \x01(\t\x12\x12\n\nroute_list\x18\x03 \x03(\x0c\x1a%\n\x04\x44\x61ta\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x0c\n\x04vote\x18\x02 \x01(\t\"x\n\tCommitMsg\x12\x1d\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x0f.CommitMsg.Data\x12\x11\n\tsignature\x18\x02 \x01(\t\x12\x12\n\nroute_list\x18\x03 \x03(\x0c\x1a%\n\x04\x44\x61ta\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x0c\n\x04vote\x18\x02 \x01(\t\"\x1e\n\x0c\x43onsensusRsp\x12\x0e\n\x06Result\x18\x01 \x01(\t\"\x1f\n\rTensorReceive\x12\x0e\n\x06Result\x18\x01 \x01(\t\"=\n\x0bTransaction\x12\x10\n\x08unixtime\x18\x01 \x01(\x04\x12\x0c\n\x04\x62ody\x18\x02 \x01(\x0c\x12\x0e\n\x06txhash\x18\x03 \x03(\t\"&\n\x04Node\x12\x0e\n\x06number\x18\x01 \x01(\x05\x12\x0e\n\x06ipport\x18\x02 \x03(\t\"\x18\n\x07Message\x12\r\n\x05value\x18\x01 \x01(\t\"\x18\n\tExpertUID\x12\x0b\n\x03uid\x18\x01 \x01(\t\"%\n\nExpertInfo\x12\x17\n\x0fserialized_info\x18\x01 \x01(\x0c\"6\n\rExpertRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x18\n\x07tensors\x18\x02 \x03(\x0b\x32\x07.Tensor\"*\n\x0e\x45xpertResponse\x12\x18\n\x07tensors\x18\x02 \x03(\x0b\x32\x07.Tensor\"\x83\x01\n\x06Tensor\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\x12\x0c\n\x04size\x18\x02 \x03(\r\x12\x15\n\rrequires_grad\x18\x03 \x01(\x08\x12\r\n\x05\x64type\x18\x04 \x01(\t\x12%\n\x0b\x63ompression\x18\x05 \x01(\x0e\x32\x10.CompressionType\x12\x0e\n\x06\x63hunks\x18\x06 \x01(\x05*`\n\x0f\x43ompressionType\x12\x08\n\x04NONE\x10\x00\x12\x11\n\rMEANSTD_16BIT\x10\x01\x12\x0b\n\x07\x46LOAT16\x10\x02\x12\x11\n\rQUANTILE_8BIT\x10\x03\x12\x10\n\x0cUNIFORM_8BIT\x10\x04\x32\xb7\x01\n\tDiscovery\x12%\n\x0ftell_public_key\x12\x08.Message\x1a\x08.Message\x12\x1c\n\x0c\x45xchangeNode\x12\x05.Node\x1a\x05.Node\x12\x1b\n\x05Hello\x12\x08.Message\x1a\x08.Message\x12*\n\x0c\x45xchangeGrad\x12\n.Parameter\x1a\x0e.TensorReceive\x12\x1c\n\nEpoch_over\x12\x06.Epoch\x1a\x06.Epoch2\xab\x01\n\tConsensus\x12%\n\x0ftell_public_key\x12\x08.Message\x1a\x08.Message\x12+\n\nPrePrepare\x12\x0e.PrePrepareMsg\x1a\r.ConsensusRsp\x12%\n\x07Prepare\x12\x0b.PrepareMsg\x1a\r.ConsensusRsp\x12#\n\x06\x43ommit\x12\n.CommitMsg\x1a\r.ConsensusRsp2\xc2\x01\n\x0fSynchronization\x12\x1d\n\tBlockFrom\x12\x08.Message\x1a\x06.Block\x12\x1b\n\x07\x42lockTo\x12\x06.Block\x1a\x08.Message\x12\x1f\n\rExchangeBlock\x12\x06.Block\x1a\x06.Block\x12\'\n\rTransactionTo\x12\x0c.Transaction\x1a\x08.Message\x12)\n\x0fTransactionFrom\x12\x08.Message\x1a\x0c.Transaction2\x8d\x01\n\x11\x43onnectionHandler\x12\x1f\n\x04info\x12\n.ExpertUID\x1a\x0b.ExpertInfo\x12*\n\x07\x66orward\x12\x0e.ExpertRequest\x1a\x0f.ExpertResponse\x12+\n\x08\x62\x61\x63kward\x12\x0e.ExpertRequest\x1a\x0f.ExpertResponseb\x06proto3')

_COMPRESSIONTYPE = DESCRIPTOR.enum_types_by_name['CompressionType']
CompressionType = enum_type_wrapper.EnumTypeWrapper(_COMPRESSIONTYPE)
NONE = 0
MEANSTD_16BIT = 1
FLOAT16 = 2
QUANTILE_8BIT = 3
UNIFORM_8BIT = 4


_EPOCH = DESCRIPTOR.message_types_by_name['Epoch']
_PARAMETER = DESCRIPTOR.message_types_by_name['Parameter']
_BLOCK = DESCRIPTOR.message_types_by_name['Block']
_PREPREPAREMSG = DESCRIPTOR.message_types_by_name['PrePrepareMsg']
_PREPREPAREMSG_DATA = _PREPREPAREMSG.nested_types_by_name['Data']
_PREPAREMSG = DESCRIPTOR.message_types_by_name['PrepareMsg']
_PREPAREMSG_DATA = _PREPAREMSG.nested_types_by_name['Data']
_COMMITMSG = DESCRIPTOR.message_types_by_name['CommitMsg']
_COMMITMSG_DATA = _COMMITMSG.nested_types_by_name['Data']
_CONSENSUSRSP = DESCRIPTOR.message_types_by_name['ConsensusRsp']
_TENSORRECEIVE = DESCRIPTOR.message_types_by_name['TensorReceive']
_TRANSACTION = DESCRIPTOR.message_types_by_name['Transaction']
_NODE = DESCRIPTOR.message_types_by_name['Node']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_EXPERTUID = DESCRIPTOR.message_types_by_name['ExpertUID']
_EXPERTINFO = DESCRIPTOR.message_types_by_name['ExpertInfo']
_EXPERTREQUEST = DESCRIPTOR.message_types_by_name['ExpertRequest']
_EXPERTRESPONSE = DESCRIPTOR.message_types_by_name['ExpertResponse']
_TENSOR = DESCRIPTOR.message_types_by_name['Tensor']
Epoch = _reflection.GeneratedProtocolMessageType('Epoch', (_message.Message,), {
  'DESCRIPTOR' : _EPOCH,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Epoch)
  })
_sym_db.RegisterMessage(Epoch)

Parameter = _reflection.GeneratedProtocolMessageType('Parameter', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETER,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Parameter)
  })
_sym_db.RegisterMessage(Parameter)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Block)
  })
_sym_db.RegisterMessage(Block)

PrePrepareMsg = _reflection.GeneratedProtocolMessageType('PrePrepareMsg', (_message.Message,), {

  'Data' : _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), {
    'DESCRIPTOR' : _PREPREPAREMSG_DATA,
    '__module__' : 'grpc_pb2'
    # @@protoc_insertion_point(class_scope:PrePrepareMsg.Data)
    })
  ,
  'DESCRIPTOR' : _PREPREPAREMSG,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:PrePrepareMsg)
  })
_sym_db.RegisterMessage(PrePrepareMsg)
_sym_db.RegisterMessage(PrePrepareMsg.Data)

PrepareMsg = _reflection.GeneratedProtocolMessageType('PrepareMsg', (_message.Message,), {

  'Data' : _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), {
    'DESCRIPTOR' : _PREPAREMSG_DATA,
    '__module__' : 'grpc_pb2'
    # @@protoc_insertion_point(class_scope:PrepareMsg.Data)
    })
  ,
  'DESCRIPTOR' : _PREPAREMSG,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:PrepareMsg)
  })
_sym_db.RegisterMessage(PrepareMsg)
_sym_db.RegisterMessage(PrepareMsg.Data)

CommitMsg = _reflection.GeneratedProtocolMessageType('CommitMsg', (_message.Message,), {

  'Data' : _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), {
    'DESCRIPTOR' : _COMMITMSG_DATA,
    '__module__' : 'grpc_pb2'
    # @@protoc_insertion_point(class_scope:CommitMsg.Data)
    })
  ,
  'DESCRIPTOR' : _COMMITMSG,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:CommitMsg)
  })
_sym_db.RegisterMessage(CommitMsg)
_sym_db.RegisterMessage(CommitMsg.Data)

ConsensusRsp = _reflection.GeneratedProtocolMessageType('ConsensusRsp', (_message.Message,), {
  'DESCRIPTOR' : _CONSENSUSRSP,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:ConsensusRsp)
  })
_sym_db.RegisterMessage(ConsensusRsp)

TensorReceive = _reflection.GeneratedProtocolMessageType('TensorReceive', (_message.Message,), {
  'DESCRIPTOR' : _TENSORRECEIVE,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:TensorReceive)
  })
_sym_db.RegisterMessage(TensorReceive)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTION,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Transaction)
  })
_sym_db.RegisterMessage(Transaction)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), {
  'DESCRIPTOR' : _NODE,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Node)
  })
_sym_db.RegisterMessage(Node)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

ExpertUID = _reflection.GeneratedProtocolMessageType('ExpertUID', (_message.Message,), {
  'DESCRIPTOR' : _EXPERTUID,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:ExpertUID)
  })
_sym_db.RegisterMessage(ExpertUID)

ExpertInfo = _reflection.GeneratedProtocolMessageType('ExpertInfo', (_message.Message,), {
  'DESCRIPTOR' : _EXPERTINFO,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:ExpertInfo)
  })
_sym_db.RegisterMessage(ExpertInfo)

ExpertRequest = _reflection.GeneratedProtocolMessageType('ExpertRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXPERTREQUEST,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:ExpertRequest)
  })
_sym_db.RegisterMessage(ExpertRequest)

ExpertResponse = _reflection.GeneratedProtocolMessageType('ExpertResponse', (_message.Message,), {
  'DESCRIPTOR' : _EXPERTRESPONSE,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:ExpertResponse)
  })
_sym_db.RegisterMessage(ExpertResponse)

Tensor = _reflection.GeneratedProtocolMessageType('Tensor', (_message.Message,), {
  'DESCRIPTOR' : _TENSOR,
  '__module__' : 'grpc_pb2'
  # @@protoc_insertion_point(class_scope:Tensor)
  })
_sym_db.RegisterMessage(Tensor)

_DISCOVERY = DESCRIPTOR.services_by_name['Discovery']
_CONSENSUS = DESCRIPTOR.services_by_name['Consensus']
_SYNCHRONIZATION = DESCRIPTOR.services_by_name['Synchronization']
_CONNECTIONHANDLER = DESCRIPTOR.services_by_name['ConnectionHandler']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPRESSIONTYPE._serialized_start=1044
  _COMPRESSIONTYPE._serialized_end=1140
  _EPOCH._serialized_start=14
  _EPOCH._serialized_end=35
  _PARAMETER._serialized_start=37
  _PARAMETER._serialized_end=62
  _BLOCK._serialized_start=64
  _BLOCK._serialized_end=163
  _PREPREPAREMSG._serialized_start=166
  _PREPREPAREMSG._serialized_end=303
  _PREPREPAREMSG_DATA._serialized_start=237
  _PREPREPAREMSG_DATA._serialized_end=303
  _PREPAREMSG._serialized_start=305
  _PREPAREMSG._serialized_end=427
  _PREPAREMSG_DATA._serialized_start=390
  _PREPAREMSG_DATA._serialized_end=427
  _COMMITMSG._serialized_start=429
  _COMMITMSG._serialized_end=549
  _COMMITMSG_DATA._serialized_start=390
  _COMMITMSG_DATA._serialized_end=427
  _CONSENSUSRSP._serialized_start=551
  _CONSENSUSRSP._serialized_end=581
  _TENSORRECEIVE._serialized_start=583
  _TENSORRECEIVE._serialized_end=614
  _TRANSACTION._serialized_start=616
  _TRANSACTION._serialized_end=677
  _NODE._serialized_start=679
  _NODE._serialized_end=717
  _MESSAGE._serialized_start=719
  _MESSAGE._serialized_end=743
  _EXPERTUID._serialized_start=745
  _EXPERTUID._serialized_end=769
  _EXPERTINFO._serialized_start=771
  _EXPERTINFO._serialized_end=808
  _EXPERTREQUEST._serialized_start=810
  _EXPERTREQUEST._serialized_end=864
  _EXPERTRESPONSE._serialized_start=866
  _EXPERTRESPONSE._serialized_end=908
  _TENSOR._serialized_start=911
  _TENSOR._serialized_end=1042
  _DISCOVERY._serialized_start=1143
  _DISCOVERY._serialized_end=1326
  _CONSENSUS._serialized_start=1329
  _CONSENSUS._serialized_end=1500
  _SYNCHRONIZATION._serialized_start=1503
  _SYNCHRONIZATION._serialized_end=1697
  _CONNECTIONHANDLER._serialized_start=1700
  _CONNECTIONHANDLER._serialized_end=1841
# @@protoc_insertion_point(module_scope)
