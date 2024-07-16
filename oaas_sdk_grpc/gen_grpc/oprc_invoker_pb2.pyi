import oaas_sdk_grpc.gen_grpc.oprc_object_pb2 as _oprc_object_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoInvocationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROTO_INVOCATION_STATUS_UNSPECIFIED: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_QUEUE: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_DOING: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_SUCCEEDED: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_FAILED: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_DEPENDENCY_FAILED: _ClassVar[ProtoInvocationStatus]
    PROTO_INVOCATION_STATUS_READY: _ClassVar[ProtoInvocationStatus]
PROTO_INVOCATION_STATUS_UNSPECIFIED: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_QUEUE: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_DOING: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_SUCCEEDED: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_FAILED: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_DEPENDENCY_FAILED: ProtoInvocationStatus
PROTO_INVOCATION_STATUS_READY: ProtoInvocationStatus

class ProtoInvocationRequest(_message.Message):
    __slots__ = ("invId", "main", "cls", "fb", "args", "immutable", "outId", "body", "chains")
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INVID_FIELD_NUMBER: _ClassVar[int]
    MAIN_FIELD_NUMBER: _ClassVar[int]
    CLS_FIELD_NUMBER: _ClassVar[int]
    FB_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    IMMUTABLE_FIELD_NUMBER: _ClassVar[int]
    OUTID_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CHAINS_FIELD_NUMBER: _ClassVar[int]
    invId: str
    main: str
    cls: str
    fb: str
    args: _containers.ScalarMap[str, str]
    immutable: bool
    outId: str
    body: bytes
    chains: _containers.RepeatedCompositeFieldContainer[ProtoInvocationChain]
    def __init__(self, invId: _Optional[str] = ..., main: _Optional[str] = ..., cls: _Optional[str] = ..., fb: _Optional[str] = ..., args: _Optional[_Mapping[str, str]] = ..., immutable: bool = ..., outId: _Optional[str] = ..., body: _Optional[bytes] = ..., chains: _Optional[_Iterable[_Union[ProtoInvocationChain, _Mapping]]] = ...) -> None: ...

class ProtoInvocationChain(_message.Message):
    __slots__ = ("invId", "main", "cls", "fb", "args", "outId", "body", "immutable", "chains")
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INVID_FIELD_NUMBER: _ClassVar[int]
    MAIN_FIELD_NUMBER: _ClassVar[int]
    CLS_FIELD_NUMBER: _ClassVar[int]
    FB_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    OUTID_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    IMMUTABLE_FIELD_NUMBER: _ClassVar[int]
    CHAINS_FIELD_NUMBER: _ClassVar[int]
    invId: str
    main: str
    cls: str
    fb: str
    args: _containers.ScalarMap[str, str]
    outId: str
    body: bytes
    immutable: bool
    chains: _containers.RepeatedCompositeFieldContainer[ProtoInvocationChain]
    def __init__(self, invId: _Optional[str] = ..., main: _Optional[str] = ..., cls: _Optional[str] = ..., fb: _Optional[str] = ..., args: _Optional[_Mapping[str, str]] = ..., outId: _Optional[str] = ..., body: _Optional[bytes] = ..., immutable: bool = ..., chains: _Optional[_Iterable[_Union[ProtoInvocationChain, _Mapping]]] = ...) -> None: ...

class ProtoInvocationResponse(_message.Message):
    __slots__ = ("main", "output", "invId", "fb", "macroIds", "status", "stats", "body", "macroInvIds")
    class MacroIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MAIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    INVID_FIELD_NUMBER: _ClassVar[int]
    FB_FIELD_NUMBER: _ClassVar[int]
    MACROIDS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    MACROINVIDS_FIELD_NUMBER: _ClassVar[int]
    main: _oprc_object_pb2.ProtoPOObject
    output: _oprc_object_pb2.ProtoPOObject
    invId: str
    fb: str
    macroIds: _containers.ScalarMap[str, str]
    status: ProtoInvocationStatus
    stats: ProtoInvocationStats
    body: bytes
    macroInvIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, main: _Optional[_Union[_oprc_object_pb2.ProtoPOObject, _Mapping]] = ..., output: _Optional[_Union[_oprc_object_pb2.ProtoPOObject, _Mapping]] = ..., invId: _Optional[str] = ..., fb: _Optional[str] = ..., macroIds: _Optional[_Mapping[str, str]] = ..., status: _Optional[_Union[ProtoInvocationStatus, str]] = ..., stats: _Optional[_Union[ProtoInvocationStats, _Mapping]] = ..., body: _Optional[bytes] = ..., macroInvIds: _Optional[_Iterable[str]] = ..., **kwargs) -> None: ...

class ProtoInvocationStats(_message.Message):
    __slots__ = ("queTs", "smtTs", "cptTs")
    QUETS_FIELD_NUMBER: _ClassVar[int]
    SMTTS_FIELD_NUMBER: _ClassVar[int]
    CPTTS_FIELD_NUMBER: _ClassVar[int]
    queTs: int
    smtTs: int
    cptTs: int
    def __init__(self, queTs: _Optional[int] = ..., smtTs: _Optional[int] = ..., cptTs: _Optional[int] = ...) -> None: ...
