# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: election.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x65lection.proto\"\x07\n\x05\x45mpty\"\x19\n\x0bresponse_id\x12\n\n\x02id\x18\x01 \x01(\x05\")\n\x13response_permission\x12\x12\n\npermission\x18\x01 \x01(\x08\"\"\n\x12request_permission\x12\x0c\n\x04type\x18\x01 \x01(\t\"%\n\x10send_coordinator\x12\x11\n\tleader_id\x18\x01 \x01(\x05\"#\n\x10request_election\x12\x0f\n\x07serv_id\x18\x01 \x01(\x05\"$\n\x11response_election\x12\x0f\n\x07message\x18\x01 \x01(\t2\xdd\x01\n\x08\x45lection\x12&\n\x0cresp_serv_id\x12\x06.Empty\x1a\x0c.response_id\"\x00\x12>\n\x0fresp_permission\x12\x13.request_permission\x1a\x14.response_permission\"\x00\x12\x38\n\rresp_election\x12\x11.request_election\x1a\x12.response_election\"\x00\x12/\n\x10recv_coordinator\x12\x11.send_coordinator\x1a\x06.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'election_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=18
  _EMPTY._serialized_end=25
  _RESPONSE_ID._serialized_start=27
  _RESPONSE_ID._serialized_end=52
  _RESPONSE_PERMISSION._serialized_start=54
  _RESPONSE_PERMISSION._serialized_end=95
  _REQUEST_PERMISSION._serialized_start=97
  _REQUEST_PERMISSION._serialized_end=131
  _SEND_COORDINATOR._serialized_start=133
  _SEND_COORDINATOR._serialized_end=170
  _REQUEST_ELECTION._serialized_start=172
  _REQUEST_ELECTION._serialized_end=207
  _RESPONSE_ELECTION._serialized_start=209
  _RESPONSE_ELECTION._serialized_end=245
  _ELECTION._serialized_start=248
  _ELECTION._serialized_end=469
# @@protoc_insertion_point(module_scope)