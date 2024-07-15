import asyncio
import grpc
import logging
import os
import json

from aiohttp import ClientSession, ClientResponse

from gen_grpc import oprc_offload_pb2_grpc, oprc_offload_pb2
from oaas_sdk_py import OaasException

from gen_grpc.oprc_object_pb2 import ProtoPOObject
from gen_grpc.oprc_offload_pb2 import ProtoOTask


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

    # allocate_url_dict = None
    # allocate_main_url_dict = None

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
        # if self.allocate_main_url_dict is None:
        #     await self.allocate_main_file(session)
        #     url = self.allocate_main_url_dict[key]
        # else:
        #     url = self.allocate_url_dict[key]
        #
        # url = self.url_dict[key]
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
        # if key in self.task.outputKeys:
        url = self.task.outputKeys[key]
        # elif self.allocate_url_dict is None:
        #     await self.allocate_file(session)
        #     url = self.allocate_url_dict[key]
        # else:
        #     url = self.allocate_url_dict[key]
        if url is None:
            raise OaasException(f"The output object not accept '{key}' as key")
        resp = await session.put(url, data=data)
        if not resp.ok:
            raise OaasException("Got error when put the data to S3")
        self.updated_output_keys.append(key)

    # async def allocate_file(self,
    #                         session: ClientSession) -> dict:
    #     logging.debug(f"allocate_file for '{self.task.output.id}'")
    #     resp_dict = await _allocate(session, self.task.allocOutputUrl)
    #     if self.allocate_url_dict is None:
    #         self.allocate_url_dict = resp_dict
    #     else:
    #         self.allocate_url_dict = self.allocate_url_dict | resp_dict
    #     return self.allocate_url_dict
    #
    # async def allocate_main_file(self,
    #                              session: ClientSession) -> dict:
    #     logging.debug(f"allocate_file for '{self.task.main.meta.id}'")
    #     resp_dict = await _allocate(session, self.task.allocMainUrl)
    #     if self.allocate_main_url_dict is None:
    #         self.allocate_main_url_dict = resp_dict
    #     else:
    #         self.allocate_main_url_dict = self.allocate_main_url_dict | resp_dict
    #     return self.allocate_main_url_dict


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
