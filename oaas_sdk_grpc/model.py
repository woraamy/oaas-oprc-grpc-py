import asyncio
import grpc
import logging
import os
import json

from gen_grpc import oprc_offload_pb2_grpc, oprc_offload_pb2


class GrpcCtx:
    main_data = None
    output_data = None

    def __init__(self, request):
        self.task = request
        self.args = request.args
        if self.main_data is None:
            self.main_data = json.loads(request.main.data)


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