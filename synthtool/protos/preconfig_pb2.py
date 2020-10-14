# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: preconfig.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="preconfig.proto",
    package="yoshi.synth.preconfig",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x0fpreconfig.proto\x12\x15yoshi.synth.preconfig"\x91\x01\n\tPreconfig\x12M\n\x0fprecloned_repos\x18\x01 \x03(\x0b\x32\x34.yoshi.synth.preconfig.Preconfig.PreclonedReposEntry\x1a\x35\n\x13PreclonedReposEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3',
)


_PRECONFIG_PRECLONEDREPOSENTRY = _descriptor.Descriptor(
    name="PreclonedReposEntry",
    full_name="yoshi.synth.preconfig.Preconfig.PreclonedReposEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="yoshi.synth.preconfig.Preconfig.PreclonedReposEntry.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="yoshi.synth.preconfig.Preconfig.PreclonedReposEntry.value",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=b"8\001",
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=135,
    serialized_end=188,
)

_PRECONFIG = _descriptor.Descriptor(
    name="Preconfig",
    full_name="yoshi.synth.preconfig.Preconfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="precloned_repos",
            full_name="yoshi.synth.preconfig.Preconfig.precloned_repos",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[
        _PRECONFIG_PRECLONEDREPOSENTRY,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=43,
    serialized_end=188,
)

_PRECONFIG_PRECLONEDREPOSENTRY.containing_type = _PRECONFIG
_PRECONFIG.fields_by_name[
    "precloned_repos"
].message_type = _PRECONFIG_PRECLONEDREPOSENTRY
DESCRIPTOR.message_types_by_name["Preconfig"] = _PRECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Preconfig = _reflection.GeneratedProtocolMessageType(
    "Preconfig",
    (_message.Message,),
    {
        "PreclonedReposEntry": _reflection.GeneratedProtocolMessageType(
            "PreclonedReposEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _PRECONFIG_PRECLONEDREPOSENTRY,
                "__module__": "preconfig_pb2"
                # @@protoc_insertion_point(class_scope:yoshi.synth.preconfig.Preconfig.PreclonedReposEntry)
            },
        ),
        "DESCRIPTOR": _PRECONFIG,
        "__module__": "preconfig_pb2"
        # @@protoc_insertion_point(class_scope:yoshi.synth.preconfig.Preconfig)
    },
)
_sym_db.RegisterMessage(Preconfig)
_sym_db.RegisterMessage(Preconfig.PreclonedReposEntry)


_PRECONFIG_PRECLONEDREPOSENTRY._options = None
# @@protoc_insertion_point(module_scope)
