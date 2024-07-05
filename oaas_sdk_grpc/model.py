import asyncio
import grpc
import logging
import os
import json

from aiohttp import ClientSession, ClientResponse

from gen_grpc import oprc_offload_pb2_grpc, oprc_offload_pb2
from oaas_sdk_py import OaasException


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
    allocate_url_dict = None
    allocate_main_url_dict = None

    def __init__(self, request):
        self.task = request
        self.args = request.args
        if self.main_data is None:
            self.main_data = json.loads(request.main.data)

    async def load_main_file(self, session: ClientSession, key: str) -> ClientResponse:
        """Load the file from the main object with the key"""
        if key not in self.task.main_keys:
            raise OaasException(f"NO such key '{key}' in main object")
        return await _load_file(session, self.task.main_keys[key])

    async def upload_main_byte_data(self,
                                    session: ClientSession,
                                    key: str,
                                    data: bytes) -> None:
        if self.allocate_main_url_dict is None:
            await self.allocate_main_file(session)
            url = self.allocate_main_url_dict[key]
        else:
            url = self.allocate_url_dict[key]
        if url is None:
            raise OaasException(f"The main object not accept '{key}' as key")
        resp = await session.put(url, data=data)
        if not resp.ok:
            raise OaasException("Got error when put the data to S3")
        self.task.main_obj.updated_keys.append(key)

    async def upload_byte_data(self,
                               session: ClientSession,
                               key: str,
                               data: bytes) -> None:
        if key in self.task.output_keys:
            url = self.task.output_keys[key]
        elif self.allocate_url_dict is None:
            await self.allocate_file(session)
            url = self.allocate_url_dict[key]
        else:
            url = self.allocate_url_dict[key]
        if url is None:
            raise OaasException(f"The output object not accept '{key}' as key")
        resp = await session.put(url, data=data)
        if not resp.ok:
            raise OaasException("Got error when put the data to S3")
        self.task.output_obj.updated_keys.append(key)

    async def allocate_file(self,
                            session: ClientSession) -> dict:
        logging.debug(f"allocate_file for '{self.task.output_obj.id}'")
        resp_dict = await _allocate(session, self.task.alloc_url)
        if self.allocate_url_dict is None:
            self.allocate_url_dict = resp_dict
        else:
            self.allocate_url_dict = self.allocate_url_dict | resp_dict
        return self.allocate_url_dict

    async def allocate_main_file(self,
                                 session: ClientSession) -> dict:
        logging.debug(f"allocate_file for '{self.task.main_obj.id}'")
        resp_dict = await _allocate(session, self.task.alloc_main_url)
        if self.allocate_main_url_dict is None:
            self.allocate_main_url_dict = resp_dict
        else:
            self.allocate_main_url_dict = self.allocate_main_url_dict | resp_dict
        return self.allocate_main_url_dict


class OTaskExecutorServicer(oprc_offload_pb2_grpc.FunctionExecutorServicer):
    def __init__(self, handler):
        self.handler = handler

    async def invoke(self, request, context):
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
            main=oprc_offload_pb2.ProtoObjectUpdate(data=main_obj),
            output=oprc_offload_pb2.ProtoObjectUpdate(data=output_obj)
        )