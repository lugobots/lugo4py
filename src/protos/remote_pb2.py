# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: remote.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import physics_pb2 as physics__pb2
import server_pb2 as server__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cremote.proto\x12\x04lugo\x1a\rphysics.proto\x1a\x0cserver.proto\"\x14\n\x12PauseResumeRequest\"\x11\n\x0fNextTurnRequest\"\x12\n\x10NextOrderRequest\"o\n\x0e\x42\x61llProperties\x12\x1d\n\x08position\x18\x01 \x01(\x0b\x32\x0b.lugo.Point\x12 \n\x08velocity\x18\x02 \x01(\x0b\x32\x0e.lugo.Velocity\x12\x1c\n\x06holder\x18\x03 \x01(\x0b\x32\x0c.lugo.Player\"\x82\x01\n\x10PlayerProperties\x12\x1d\n\x04side\x18\x01 \x01(\x0e\x32\x0f.lugo.Team.Side\x12\x0e\n\x06number\x18\x02 \x01(\r\x12\x1d\n\x08position\x18\x03 \x01(\x0b\x32\x0b.lugo.Point\x12 \n\x08velocity\x18\x04 \x01(\x0b\x32\x0e.lugo.Velocity\"\x83\x01\n\x0eGameProperties\x12\x0c\n\x04turn\x18\x01 \x01(\r\x12\x12\n\nhome_score\x18\x02 \x01(\r\x12\x12\n\naway_score\x18\x03 \x01(\r\x12\x16\n\x0e\x66rame_interval\x18\x04 \x01(\x03\x12#\n\nshot_clock\x18\x05 \x01(\x0b\x32\x0f.lugo.ShotClock\"\xcd\x01\n\x0f\x43ommandResponse\x12.\n\x04\x63ode\x18\x01 \x01(\x0e\x32 .lugo.CommandResponse.StatusCode\x12)\n\rgame_snapshot\x18\x02 \x01(\x0b\x32\x12.lugo.GameSnapshot\x12\x0f\n\x07\x64\x65tails\x18\x03 \x01(\t\"N\n\nStatusCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x11\n\rINVALID_VALUE\x10\x01\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x02\x12\t\n\x05OTHER\x10\x63\"\x18\n\x16ResumeListeningRequest\"\x19\n\x17ResumeListeningResponse2\xdf\x03\n\x06Remote\x12@\n\rPauseOrResume\x12\x18.lugo.PauseResumeRequest\x1a\x15.lugo.CommandResponse\x12\x38\n\x08NextTurn\x12\x15.lugo.NextTurnRequest\x1a\x15.lugo.CommandResponse\x12:\n\tNextOrder\x12\x16.lugo.NextOrderRequest\x1a\x15.lugo.CommandResponse\x12@\n\x11SetBallProperties\x12\x14.lugo.BallProperties\x1a\x15.lugo.CommandResponse\x12\x44\n\x13SetPlayerProperties\x12\x16.lugo.PlayerProperties\x1a\x15.lugo.CommandResponse\x12@\n\x11SetGameProperties\x12\x14.lugo.GameProperties\x1a\x15.lugo.CommandResponse\x12S\n\x14ResumeListeningPhase\x12\x1c.lugo.ResumeListeningRequest\x1a\x1d.lugo.ResumeListeningResponseB#Z!github.com/lugobots/lugo4go/protob\x06proto3')



_PAUSERESUMEREQUEST = DESCRIPTOR.message_types_by_name['PauseResumeRequest']
_NEXTTURNREQUEST = DESCRIPTOR.message_types_by_name['NextTurnRequest']
_NEXTORDERREQUEST = DESCRIPTOR.message_types_by_name['NextOrderRequest']
_BALLPROPERTIES = DESCRIPTOR.message_types_by_name['BallProperties']
_PLAYERPROPERTIES = DESCRIPTOR.message_types_by_name['PlayerProperties']
_GAMEPROPERTIES = DESCRIPTOR.message_types_by_name['GameProperties']
_COMMANDRESPONSE = DESCRIPTOR.message_types_by_name['CommandResponse']
_RESUMELISTENINGREQUEST = DESCRIPTOR.message_types_by_name['ResumeListeningRequest']
_RESUMELISTENINGRESPONSE = DESCRIPTOR.message_types_by_name['ResumeListeningResponse']
_COMMANDRESPONSE_STATUSCODE = _COMMANDRESPONSE.enum_types_by_name['StatusCode']
PauseResumeRequest = _reflection.GeneratedProtocolMessageType('PauseResumeRequest', (_message.Message,), {
  'DESCRIPTOR' : _PAUSERESUMEREQUEST,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.PauseResumeRequest)
  })
_sym_db.RegisterMessage(PauseResumeRequest)

NextTurnRequest = _reflection.GeneratedProtocolMessageType('NextTurnRequest', (_message.Message,), {
  'DESCRIPTOR' : _NEXTTURNREQUEST,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.NextTurnRequest)
  })
_sym_db.RegisterMessage(NextTurnRequest)

NextOrderRequest = _reflection.GeneratedProtocolMessageType('NextOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _NEXTORDERREQUEST,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.NextOrderRequest)
  })
_sym_db.RegisterMessage(NextOrderRequest)

BallProperties = _reflection.GeneratedProtocolMessageType('BallProperties', (_message.Message,), {
  'DESCRIPTOR' : _BALLPROPERTIES,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.BallProperties)
  })
_sym_db.RegisterMessage(BallProperties)

PlayerProperties = _reflection.GeneratedProtocolMessageType('PlayerProperties', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERPROPERTIES,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.PlayerProperties)
  })
_sym_db.RegisterMessage(PlayerProperties)

GameProperties = _reflection.GeneratedProtocolMessageType('GameProperties', (_message.Message,), {
  'DESCRIPTOR' : _GAMEPROPERTIES,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.GameProperties)
  })
_sym_db.RegisterMessage(GameProperties)

CommandResponse = _reflection.GeneratedProtocolMessageType('CommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDRESPONSE,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.CommandResponse)
  })
_sym_db.RegisterMessage(CommandResponse)

ResumeListeningRequest = _reflection.GeneratedProtocolMessageType('ResumeListeningRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESUMELISTENINGREQUEST,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.ResumeListeningRequest)
  })
_sym_db.RegisterMessage(ResumeListeningRequest)

ResumeListeningResponse = _reflection.GeneratedProtocolMessageType('ResumeListeningResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESUMELISTENINGRESPONSE,
  '__module__' : 'remote_pb2'
  # @@protoc_insertion_point(class_scope:lugo.ResumeListeningResponse)
  })
_sym_db.RegisterMessage(ResumeListeningResponse)

_REMOTE = DESCRIPTOR.services_by_name['Remote']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z!github.com/lugobots/lugo4go/proto'
  _PAUSERESUMEREQUEST._serialized_start=51
  _PAUSERESUMEREQUEST._serialized_end=71
  _NEXTTURNREQUEST._serialized_start=73
  _NEXTTURNREQUEST._serialized_end=90
  _NEXTORDERREQUEST._serialized_start=92
  _NEXTORDERREQUEST._serialized_end=110
  _BALLPROPERTIES._serialized_start=112
  _BALLPROPERTIES._serialized_end=223
  _PLAYERPROPERTIES._serialized_start=226
  _PLAYERPROPERTIES._serialized_end=356
  _GAMEPROPERTIES._serialized_start=359
  _GAMEPROPERTIES._serialized_end=490
  _COMMANDRESPONSE._serialized_start=493
  _COMMANDRESPONSE._serialized_end=698
  _COMMANDRESPONSE_STATUSCODE._serialized_start=620
  _COMMANDRESPONSE_STATUSCODE._serialized_end=698
  _RESUMELISTENINGREQUEST._serialized_start=700
  _RESUMELISTENINGREQUEST._serialized_end=724
  _RESUMELISTENINGRESPONSE._serialized_start=726
  _RESUMELISTENINGRESPONSE._serialized_end=751
  _REMOTE._serialized_start=754
  _REMOTE._serialized_end=1233
# @@protoc_insertion_point(module_scope)
