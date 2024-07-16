import grpc
import json

from aiohttp import ClientSession, ClientResponse

from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2_grpc
from oaas_sdk_py import OaasException

from oaas_sdk_grpc.gen_grpc.oprc_offload_pb2 import ProtoOTask


async def _allocate(session: ClientSession,
                    url):
    resp = await session.get(url)
    if not resp.ok:
        raise OaasException(f"Got error when allocate keys (code:{resp.status})")
    return await resp.json()


async def _load_file(session: ClientSession,
                     url: str) -> ClientResponse:
    resp = await session.get(url)
    if not resp.ok:
        raise OaasException(f"Got error when get the data from S3 (code:{resp.status})")
    return resp


class GrpcCtx:
    main_data = None
    output_data = None

    def __init__(self, request: ProtoOTask):
        self.task = request
        self.args = request.args
        if self.main_data is None:
            self.main_data = json.loads(request.main.data)
        self.updated_main_keys = []
        self.updated_output_keys = []

    async def load_main_file(self, session: ClientSession, key: str) -> ClientResponse:
        """Load the file from the main object with the key"""
        if key not in self.task.mainGetKeys:
            raise OaasException(f"NO such key '{key}' in main object")
        return await _load_file(session, self.task.mainGetKeys[key])

    async def upload_main_byte_data(self,
                                    session: ClientSession,
                                    key: str,
                                    data: bytes) -> None:

        url = self.task.mainPutKeys[key]
        if url is None:
            raise OaasException(f"The main object not accept '{key}' as key")
        resp = await session.put(url, data=data)
        if not resp.ok:
            raise OaasException("Got error when put the data to S3")
        self.updated_main_keys.append(key)

    async def upload_byte_data(self,
                               session: ClientSession,
                               key: str,
                               data: bytes) -> None:
        url = self.task.outputKeys[key]
        if url is None:
            raise OaasException(f"The output object not accept '{key}' as key")
        resp = await session.put(url, data=data)
        if not resp.ok:
            raise OaasException("Got error when put the data to S3")
        self.updated_output_keys.append(key)


class OTaskExecutorServicer(oprc_offload_pb2_grpc.FunctionExecutorServicer):
    def __init__(self, handler):
        self.handler = handler

    async def invoke(self, request: ProtoOTask, context):
        print("Received request")
        print(request)
        ctx = GrpcCtx(request)
        if request.funcKey is not None:
            await self.handler.handle(ctx)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Handler not found')
            return oprc_offload_pb2.ProtoOTaskCompletion(id=request.id, success=False)

        main_obj = json.dumps(ctx.main_data).encode('utf-8')
        if ctx.output_data is not None:
            output_obj = json.dumps(ctx.output_data).encode('utf-8')
        else:
            output_obj = b''

        return oprc_offload_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_offload_pb2.ProtoObjectUpdate(data=main_obj,
                                                    updatedKeys=ctx.updated_main_keys),
            output=oprc_offload_pb2.ProtoObjectUpdate(data=output_obj,
                                                      updatedKeys=ctx.updated_output_keys)
        )


class OffloadGrpc:
    def __init__(self):
        self.offload = oprc_offload_pb2_grpc
