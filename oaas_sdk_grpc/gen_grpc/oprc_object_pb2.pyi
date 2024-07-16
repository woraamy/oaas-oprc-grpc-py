from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoOObject(_message.Message):
    __slots__ = ("id", "revision", "cls", "state", "refs", "data", "lastOffset", "lastInv")
    class RefsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CLS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LASTOFFSET_FIELD_NUMBER: _ClassVar[int]
    LASTINV_FIELD_NUMBER: _ClassVar[int]
    id: str
    revision: int
    cls: str
    state: OOState
    refs: _containers.ScalarMap[str, str]
    data: bytes
    lastOffset: int
    lastInv: str
    def __init__(self, id: _Optional[str] = ..., revision: _Optional[int] = ..., cls: _Optional[str] = ..., state: _Optional[_Union[OOState, _Mapping]] = ..., refs: _Optional[_Mapping[str, str]] = ..., data: _Optional[bytes] = ..., lastOffset: _Optional[int] = ..., lastInv: _Optional[str] = ...) -> None: ...

class ProtoPOObject(_message.Message):
    __slots__ = ("meta", "data")
    META_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    meta: ProtoOMeta
    data: bytes
    def __init__(self, meta: _Optional[_Union[ProtoOMeta, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class ProtoOMeta(_message.Message):
    __slots__ = ("id", "revision", "cls", "verIds", "refs", "lastOffset")
    class VerIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class RefsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CLS_FIELD_NUMBER: _ClassVar[int]
    VERIDS_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    LASTOFFSET_FIELD_NUMBER: _ClassVar[int]
    id: str
    revision: int
    cls: str
    verIds: _containers.ScalarMap[str, str]
    refs: _containers.ScalarMap[str, str]
    lastOffset: int
    def __init__(self, id: _Optional[str] = ..., revision: _Optional[int] = ..., cls: _Optional[str] = ..., verIds: _Optional[_Mapping[str, str]] = ..., refs: _Optional[_Mapping[str, str]] = ..., lastOffset: _Optional[int] = ...) -> None: ...

class OOState(_message.Message):
    __slots__ = ("overrideUrls", "verIds")
    class OverrideUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class VerIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OVERRIDEURLS_FIELD_NUMBER: _ClassVar[int]
    VERIDS_FIELD_NUMBER: _ClassVar[int]
    overrideUrls: _containers.ScalarMap[str, str]
    verIds: _containers.ScalarMap[str, str]
    def __init__(self, overrideUrls: _Optional[_Mapping[str, str]] = ..., verIds: _Optional[_Mapping[str, str]] = ...) -> None: ...
