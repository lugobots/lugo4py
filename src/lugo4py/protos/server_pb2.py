# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import physics_pb2 as physics__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='server.proto',
  package='lugo',
  syntax='proto3',
  serialized_options=b'Z!github.com/lugobots/lugo4go/proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cserver.proto\x12\x04lugo\x1a\rphysics.proto\"\x8e\x01\n\x0bJoinRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x18\n\x10protocol_version\x18\x02 \x01(\t\x12\"\n\tteam_side\x18\x03 \x01(\x0e\x32\x0f.lugo.Team.Side\x12\x0e\n\x06number\x18\x04 \x01(\r\x12\"\n\rinit_position\x18\x05 \x01(\x0b\x32\x0b.lugo.Point\"\xbc\x02\n\x0cGameSnapshot\x12\'\n\x05state\x18\x01 \x01(\x0e\x32\x18.lugo.GameSnapshot.State\x12\x0c\n\x04turn\x18\x02 \x01(\r\x12\x1d\n\thome_team\x18\x03 \x01(\x0b\x32\n.lugo.Team\x12\x1d\n\taway_team\x18\x04 \x01(\x0b\x32\n.lugo.Team\x12\x18\n\x04\x62\x61ll\x18\x05 \x01(\x0b\x32\n.lugo.Ball\x12\x1f\n\x17turns_ball_in_goal_zone\x18\x06 \x01(\r\x12#\n\nshot_clock\x18\x07 \x01(\x0b\x32\x0f.lugo.ShotClock\"W\n\x05State\x12\x0b\n\x07WAITING\x10\x00\x12\r\n\tGET_READY\x10\x01\x12\r\n\tLISTENING\x10\x02\x12\x0b\n\x07PLAYING\x10\x03\x12\x0c\n\x08SHIFTING\x10\x04\x12\x08\n\x04OVER\x10\x63\"}\n\x04Team\x12\x1d\n\x07players\x18\x01 \x03(\x0b\x32\x0c.lugo.Player\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05score\x18\x03 \x01(\r\x12\x1d\n\x04side\x18\x04 \x01(\x0e\x32\x0f.lugo.Team.Side\"\x1a\n\x04Side\x12\x08\n\x04HOME\x10\x00\x12\x08\n\x04\x41WAY\x10\x01\"H\n\tShotClock\x12\"\n\tteam_side\x18\x06 \x01(\x0e\x32\x0f.lugo.Team.Side\x12\x17\n\x0fremaining_turns\x18\x07 \x01(\r\"\xa1\x01\n\x06Player\x12\x0e\n\x06number\x18\x01 \x01(\r\x12\x1d\n\x08position\x18\x02 \x01(\x0b\x32\x0b.lugo.Point\x12 \n\x08velocity\x18\x03 \x01(\x0b\x32\x0e.lugo.Velocity\x12\"\n\tteam_side\x18\x04 \x01(\x0e\x32\x0f.lugo.Team.Side\x12\"\n\rinit_position\x18\x05 \x01(\x0b\x32\x0b.lugo.Point\"e\n\x04\x42\x61ll\x12\x1d\n\x08position\x18\x01 \x01(\x0b\x32\x0b.lugo.Point\x12 \n\x08velocity\x18\x02 \x01(\x0b\x32\x0e.lugo.Velocity\x12\x1c\n\x06holder\x18\x03 \x01(\x0b\x32\x0c.lugo.Player\"\xab\x01\n\rOrderResponse\x12,\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x1e.lugo.OrderResponse.StatusCode\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\"[\n\nStatusCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x12\n\x0eUNKNOWN_PLAYER\x10\x01\x12\x11\n\rNOT_LISTENING\x10\x02\x12\x0e\n\nWRONG_TURN\x10\x03\x12\t\n\x05OTHER\x10\x63\"L\n\x08OrderSet\x12\x0c\n\x04turn\x18\x01 \x01(\r\x12\x1b\n\x06orders\x18\x02 \x03(\x0b\x32\x0b.lugo.Order\x12\x15\n\rdebug_message\x18\x03 \x01(\t\"\x83\x01\n\x05Order\x12\x1a\n\x04move\x18\x01 \x01(\x0b\x32\n.lugo.MoveH\x00\x12\x1c\n\x05\x63\x61tch\x18\x02 \x01(\x0b\x32\x0b.lugo.CatchH\x00\x12\x1a\n\x04kick\x18\x03 \x01(\x0b\x32\n.lugo.KickH\x00\x12\x1a\n\x04jump\x18\x04 \x01(\x0b\x32\n.lugo.JumpH\x00\x42\x08\n\x06\x61\x63tion\"(\n\x04Move\x12 \n\x08velocity\x18\x01 \x01(\x0b\x32\x0e.lugo.Velocity\"\x07\n\x05\x43\x61tch\"(\n\x04Kick\x12 \n\x08velocity\x18\x01 \x01(\x0b\x32\x0e.lugo.Velocity\"(\n\x04Jump\x12 \n\x08velocity\x18\x01 \x01(\x0b\x32\x0e.lugo.Velocity2o\n\x04Game\x12\x34\n\tJoinATeam\x12\x11.lugo.JoinRequest\x1a\x12.lugo.GameSnapshot0\x01\x12\x31\n\nSendOrders\x12\x0e.lugo.OrderSet\x1a\x13.lugo.OrderResponseB#Z!github.com/lugobots/lugo4go/protob\x06proto3'
  ,
  dependencies=[physics__pb2.DESCRIPTOR,])



_GAMESNAPSHOT_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='lugo.GameSnapshot.State',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WAITING', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GET_READY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LISTENING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PLAYING', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SHIFTING', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OVER', index=5, number=99,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=412,
  serialized_end=499,
)
_sym_db.RegisterEnumDescriptor(_GAMESNAPSHOT_STATE)

_TEAM_SIDE = _descriptor.EnumDescriptor(
  name='Side',
  full_name='lugo.Team.Side',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HOME', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AWAY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=600,
  serialized_end=626,
)
_sym_db.RegisterEnumDescriptor(_TEAM_SIDE)

_ORDERRESPONSE_STATUSCODE = _descriptor.EnumDescriptor(
  name='StatusCode',
  full_name='lugo.OrderResponse.StatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_PLAYER', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_LISTENING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WRONG_TURN', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER', index=4, number=99,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1050,
  serialized_end=1141,
)
_sym_db.RegisterEnumDescriptor(_ORDERRESPONSE_STATUSCODE)


_JOINREQUEST = _descriptor.Descriptor(
  name='JoinRequest',
  full_name='lugo.JoinRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='lugo.JoinRequest.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol_version', full_name='lugo.JoinRequest.protocol_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='team_side', full_name='lugo.JoinRequest.team_side', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number', full_name='lugo.JoinRequest.number', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='init_position', full_name='lugo.JoinRequest.init_position', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=180,
)


_GAMESNAPSHOT = _descriptor.Descriptor(
  name='GameSnapshot',
  full_name='lugo.GameSnapshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='lugo.GameSnapshot.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='turn', full_name='lugo.GameSnapshot.turn', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='home_team', full_name='lugo.GameSnapshot.home_team', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='away_team', full_name='lugo.GameSnapshot.away_team', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ball', full_name='lugo.GameSnapshot.ball', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='turns_ball_in_goal_zone', full_name='lugo.GameSnapshot.turns_ball_in_goal_zone', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shot_clock', full_name='lugo.GameSnapshot.shot_clock', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GAMESNAPSHOT_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=183,
  serialized_end=499,
)


_TEAM = _descriptor.Descriptor(
  name='Team',
  full_name='lugo.Team',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='players', full_name='lugo.Team.players', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='lugo.Team.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='lugo.Team.score', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='side', full_name='lugo.Team.side', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TEAM_SIDE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=501,
  serialized_end=626,
)


_SHOTCLOCK = _descriptor.Descriptor(
  name='ShotClock',
  full_name='lugo.ShotClock',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_side', full_name='lugo.ShotClock.team_side', index=0,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='remaining_turns', full_name='lugo.ShotClock.remaining_turns', index=1,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=628,
  serialized_end=700,
)


_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='lugo.Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='lugo.Player.number', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position', full_name='lugo.Player.position', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='velocity', full_name='lugo.Player.velocity', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='team_side', full_name='lugo.Player.team_side', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='init_position', full_name='lugo.Player.init_position', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=703,
  serialized_end=864,
)


_BALL = _descriptor.Descriptor(
  name='Ball',
  full_name='lugo.Ball',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='lugo.Ball.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='velocity', full_name='lugo.Ball.velocity', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='holder', full_name='lugo.Ball.holder', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=866,
  serialized_end=967,
)


_ORDERRESPONSE = _descriptor.Descriptor(
  name='OrderResponse',
  full_name='lugo.OrderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='lugo.OrderResponse.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='details', full_name='lugo.OrderResponse.details', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ORDERRESPONSE_STATUSCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=970,
  serialized_end=1141,
)


_ORDERSET = _descriptor.Descriptor(
  name='OrderSet',
  full_name='lugo.OrderSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='turn', full_name='lugo.OrderSet.turn', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orders', full_name='lugo.OrderSet.orders', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='debug_message', full_name='lugo.OrderSet.debug_message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1143,
  serialized_end=1219,
)


_ORDER = _descriptor.Descriptor(
  name='Order',
  full_name='lugo.Order',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='move', full_name='lugo.Order.move', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='catch', full_name='lugo.Order.catch', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kick', full_name='lugo.Order.kick', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='jump', full_name='lugo.Order.jump', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='action', full_name='lugo.Order.action',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1222,
  serialized_end=1353,
)


_MOVE = _descriptor.Descriptor(
  name='Move',
  full_name='lugo.Move',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='velocity', full_name='lugo.Move.velocity', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1355,
  serialized_end=1395,
)


_CATCH = _descriptor.Descriptor(
  name='Catch',
  full_name='lugo.Catch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1397,
  serialized_end=1404,
)


_KICK = _descriptor.Descriptor(
  name='Kick',
  full_name='lugo.Kick',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='velocity', full_name='lugo.Kick.velocity', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1406,
  serialized_end=1446,
)


_JUMP = _descriptor.Descriptor(
  name='Jump',
  full_name='lugo.Jump',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='velocity', full_name='lugo.Jump.velocity', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1448,
  serialized_end=1488,
)

_JOINREQUEST.fields_by_name['team_side'].enum_type = _TEAM_SIDE
_JOINREQUEST.fields_by_name['init_position'].message_type = physics__pb2._POINT
_GAMESNAPSHOT.fields_by_name['state'].enum_type = _GAMESNAPSHOT_STATE
_GAMESNAPSHOT.fields_by_name['home_team'].message_type = _TEAM
_GAMESNAPSHOT.fields_by_name['away_team'].message_type = _TEAM
_GAMESNAPSHOT.fields_by_name['ball'].message_type = _BALL
_GAMESNAPSHOT.fields_by_name['shot_clock'].message_type = _SHOTCLOCK
_GAMESNAPSHOT_STATE.containing_type = _GAMESNAPSHOT
_TEAM.fields_by_name['players'].message_type = _PLAYER
_TEAM.fields_by_name['side'].enum_type = _TEAM_SIDE
_TEAM_SIDE.containing_type = _TEAM
_SHOTCLOCK.fields_by_name['team_side'].enum_type = _TEAM_SIDE
_PLAYER.fields_by_name['position'].message_type = physics__pb2._POINT
_PLAYER.fields_by_name['velocity'].message_type = physics__pb2._VELOCITY
_PLAYER.fields_by_name['team_side'].enum_type = _TEAM_SIDE
_PLAYER.fields_by_name['init_position'].message_type = physics__pb2._POINT
_BALL.fields_by_name['position'].message_type = physics__pb2._POINT
_BALL.fields_by_name['velocity'].message_type = physics__pb2._VELOCITY
_BALL.fields_by_name['holder'].message_type = _PLAYER
_ORDERRESPONSE.fields_by_name['code'].enum_type = _ORDERRESPONSE_STATUSCODE
_ORDERRESPONSE_STATUSCODE.containing_type = _ORDERRESPONSE
_ORDERSET.fields_by_name['orders'].message_type = _ORDER
_ORDER.fields_by_name['move'].message_type = _MOVE
_ORDER.fields_by_name['catch'].message_type = _CATCH
_ORDER.fields_by_name['kick'].message_type = _KICK
_ORDER.fields_by_name['jump'].message_type = _JUMP
_ORDER.oneofs_by_name['action'].fields.append(
  _ORDER.fields_by_name['move'])
_ORDER.fields_by_name['move'].containing_oneof = _ORDER.oneofs_by_name['action']
_ORDER.oneofs_by_name['action'].fields.append(
  _ORDER.fields_by_name['catch'])
_ORDER.fields_by_name['catch'].containing_oneof = _ORDER.oneofs_by_name['action']
_ORDER.oneofs_by_name['action'].fields.append(
  _ORDER.fields_by_name['kick'])
_ORDER.fields_by_name['kick'].containing_oneof = _ORDER.oneofs_by_name['action']
_ORDER.oneofs_by_name['action'].fields.append(
  _ORDER.fields_by_name['jump'])
_ORDER.fields_by_name['jump'].containing_oneof = _ORDER.oneofs_by_name['action']
_MOVE.fields_by_name['velocity'].message_type = physics__pb2._VELOCITY
_KICK.fields_by_name['velocity'].message_type = physics__pb2._VELOCITY
_JUMP.fields_by_name['velocity'].message_type = physics__pb2._VELOCITY
DESCRIPTOR.message_types_by_name['JoinRequest'] = _JOINREQUEST
DESCRIPTOR.message_types_by_name['GameSnapshot'] = _GAMESNAPSHOT
DESCRIPTOR.message_types_by_name['Team'] = _TEAM
DESCRIPTOR.message_types_by_name['ShotClock'] = _SHOTCLOCK
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['Ball'] = _BALL
DESCRIPTOR.message_types_by_name['OrderResponse'] = _ORDERRESPONSE
DESCRIPTOR.message_types_by_name['OrderSet'] = _ORDERSET
DESCRIPTOR.message_types_by_name['Order'] = _ORDER
DESCRIPTOR.message_types_by_name['Move'] = _MOVE
DESCRIPTOR.message_types_by_name['Catch'] = _CATCH
DESCRIPTOR.message_types_by_name['Kick'] = _KICK
DESCRIPTOR.message_types_by_name['Jump'] = _JUMP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JoinRequest = _reflection.GeneratedProtocolMessageType('JoinRequest', (_message.Message,), {
  'DESCRIPTOR' : _JOINREQUEST,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.JoinRequest)
  })
_sym_db.RegisterMessage(JoinRequest)

GameSnapshot = _reflection.GeneratedProtocolMessageType('GameSnapshot', (_message.Message,), {
  'DESCRIPTOR' : _GAMESNAPSHOT,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.GameSnapshot)
  })
_sym_db.RegisterMessage(GameSnapshot)

Team = _reflection.GeneratedProtocolMessageType('Team', (_message.Message,), {
  'DESCRIPTOR' : _TEAM,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Team)
  })
_sym_db.RegisterMessage(Team)

ShotClock = _reflection.GeneratedProtocolMessageType('ShotClock', (_message.Message,), {
  'DESCRIPTOR' : _SHOTCLOCK,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.ShotClock)
  })
_sym_db.RegisterMessage(ShotClock)

Player = _reflection.GeneratedProtocolMessageType('Player', (_message.Message,), {
  'DESCRIPTOR' : _PLAYER,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Player)
  })
_sym_db.RegisterMessage(Player)

Ball = _reflection.GeneratedProtocolMessageType('Ball', (_message.Message,), {
  'DESCRIPTOR' : _BALL,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Ball)
  })
_sym_db.RegisterMessage(Ball)

OrderResponse = _reflection.GeneratedProtocolMessageType('OrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _ORDERRESPONSE,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.OrderResponse)
  })
_sym_db.RegisterMessage(OrderResponse)

OrderSet = _reflection.GeneratedProtocolMessageType('OrderSet', (_message.Message,), {
  'DESCRIPTOR' : _ORDERSET,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.OrderSet)
  })
_sym_db.RegisterMessage(OrderSet)

Order = _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), {
  'DESCRIPTOR' : _ORDER,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Order)
  })
_sym_db.RegisterMessage(Order)

Move = _reflection.GeneratedProtocolMessageType('Move', (_message.Message,), {
  'DESCRIPTOR' : _MOVE,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Move)
  })
_sym_db.RegisterMessage(Move)

Catch = _reflection.GeneratedProtocolMessageType('Catch', (_message.Message,), {
  'DESCRIPTOR' : _CATCH,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Catch)
  })
_sym_db.RegisterMessage(Catch)

Kick = _reflection.GeneratedProtocolMessageType('Kick', (_message.Message,), {
  'DESCRIPTOR' : _KICK,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Kick)
  })
_sym_db.RegisterMessage(Kick)

Jump = _reflection.GeneratedProtocolMessageType('Jump', (_message.Message,), {
  'DESCRIPTOR' : _JUMP,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:lugo.Jump)
  })
_sym_db.RegisterMessage(Jump)


DESCRIPTOR._options = None

_GAME = _descriptor.ServiceDescriptor(
  name='Game',
  full_name='lugo.Game',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1490,
  serialized_end=1601,
  methods=[
  _descriptor.MethodDescriptor(
    name='JoinATeam',
    full_name='lugo.Game.JoinATeam',
    index=0,
    containing_service=None,
    input_type=_JOINREQUEST,
    output_type=_GAMESNAPSHOT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SendOrders',
    full_name='lugo.Game.SendOrders',
    index=1,
    containing_service=None,
    input_type=_ORDERSET,
    output_type=_ORDERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GAME)

DESCRIPTOR.services_by_name['Game'] = _GAME

# @@protoc_insertion_point(module_scope)
