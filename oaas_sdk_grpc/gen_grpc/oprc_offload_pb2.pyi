import oprc_object_pb2 as _oprc_object_pb2
import oprc_invoker_pb2 as _oprc_invoker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoOTask(_message.Message):
    __slots__ = ("id", "partKey", "main", "output", "funcKey", "allocMainUrl", "allocOutputUrl", "mainGetKeys", "mainPutKeys", "outputKeys", "args", "reqBody", "fbName", "immutable", "ts")
    class MainGetKeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class MainPutKeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class OutputKeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    PARTKEY_FIELD_NUMBER: _ClassVar[int]
    MAIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    FUNCKEY_FIELD_NUMBER: _ClassVar[int]
    ALLOCMAINURL_FIELD_NUMBER: _ClassVar[int]
    ALLOCOUTPUTURL_FIELD_NUMBER: _ClassVar[int]
    MAINGETKEYS_FIELD_NUMBER: _ClassVar[int]
    MAINPUTKEYS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTKEYS_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    REQBODY_FIELD_NUMBER: _ClassVar[int]
    FBNAME_FIELD_NUMBER: _ClassVar[int]
    IMMUTABLE_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    id: str
    partKey: str
    main: _oprc_object_pb2.ProtoPOObject
    output: _oprc_object_pb2.ProtoPOObject
    funcKey: str
    allocMainUrl: str
    allocOutputUrl: str
    mainGetKeys: _containers.ScalarMap[str, str]
    mainPutKeys: _containers.ScalarMap[str, str]
    outputKeys: _containers.ScalarMap[str, str]
    args: _containers.ScalarMap[str, str]
    reqBody: bytes
    fbName: str
    immutable: bool
    ts: int
    def __init__(self, id: _Optional[str] = ..., partKey: _Optional[str] = ..., main: _Optional[_Union[_oprc_object_pb2.ProtoPOObject, _Mapping]] = ..., output: _Optional[_Union[_oprc_object_pb2.ProtoPOObject, _Mapping]] = ..., funcKey: _Optional[str] = ..., allocMainUrl: _Optional[str] = ..., allocOutputUrl: _Optional[str] = ..., mainGetKeys: _Optional[_Mapping[str, str]] = ..., mainPutKeys: _Optional[_Mapping[str, str]] = ..., outputKeys: _Optional[_Mapping[str, str]] = ..., args: _Optional[_Mapping[str, str]] = ..., reqBody: _Optional[bytes] = ..., fbName: _Optional[str] = ..., immutable: bool = ..., ts: _Optional[int] = ...) -> None: ...

class ProtoOTaskCompletion(_message.Message):
    __slots__ = ("id", "success", "errorMsg", "ext", "main", "output", "body", "invokes")
    class ExtEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    EXT_FIELD_NUMBER: _ClassVar[int]
    MAIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    INVOKES_FIELD_NUMBER: _ClassVar[int]
    id: str
    success: bool
    errorMsg: str
    ext: _containers.ScalarMap[str, str]
    main: ProtoObjectUpdate
    output: ProtoObjectUpdate
    body: bytes
    invokes: _containers.RepeatedCompositeFieldContainer[_oprc_invoker_pb2.ProtoInvocationRequest]
    def __init__(self, id: _Optional[str] = ..., success: bool = ..., errorMsg: _Optional[str] = ..., ext: _Optional[_Mapping[str, str]] = ..., main: _Optional[_Union[ProtoObjectUpdate, _Mapping]] = ..., output: _Optional[_Union[ProtoObjectUpdate, _Mapping]] = ..., body: _Optional[bytes] = ..., invokes: _Optional[_Iterable[_Union[_oprc_invoker_pb2.ProtoInvocationRequest, _Mapping]]] = ...) -> None: ...

class ProtoObjectUpdate(_message.Message):
    __slots__ = ("data", "refs", "updatedKeys")
    class RefsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    UPDATEDKEYS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    refs: _containers.ScalarMap[str, str]
    updatedKeys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, data: _Optional[bytes] = ..., refs: _Optional[_Mapping[str, str]] = ..., updatedKeys: _Optional[_Iterable[str]] = ...) -> None: ...
