import asyncio
import grpc
from concurrent import futures
import time
import logging
import random
import string
import os
import gen_grpc.oprc_offload_pb2 as oprc_offload_pb2
import gen_grpc.oprc_offload_pb2_grpc as oprc_offload_pb2_grpc
import oaas_sdk_py as oaas
from oaas_sdk_py import OaasInvocationCtx

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)

def generate_text(num):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(num))

class RandomHandler(oaas.Handler):
    async def handle(self, ctx: OaasInvocationCtx):

        entries = int(ctx.args.get('ENTRIES', '10'))
        keys = int(ctx.args.get('KEYS', '10'))
        values = int(ctx.args.get('VALUES', '10'))
        max_keys = int(ctx.args.get('MAX', '10000'))
        inplace = ctx.args.get('INPLACE', 'true').lower() == 'true'
        req_ts = int(ctx.args.get('reqts', '0'))

        record = ctx.task.main_obj.data.copy() if ctx.task.main_obj.data is not None else {}

        for _ in range(entries):
            record[generate_text(keys)] = generate_text(values)
        count = len(record)
        if count > max_keys:
            for _ in range(count - max_keys):
                k = next(iter(record.keys()))
                record.pop(k)

        record['ts'] = round(time.time() * 1000)
        if req_ts > 0:
            record['reqts'] = req_ts
        if inplace:
            ctx.task.main_obj.data = record
        if ctx.task.output_obj is not None:
            ctx.task.output_obj.data = record


class MergeHandler(oaas.Handler):
    async def handle(self, ctx: OaasInvocationCtx):
        inplace = ctx.args.get('INPLACE', 'false').lower() == 'true'
        record = ctx.task.main_obj.data.copy() if ctx.task.main_obj.data is not None else {}

        for input_obj in ctx.task.inputs:
            other_record = input_obj.data.copy() if input_obj.data is not None else {}
            record = record | other_record

        if inplace:
            ctx.task.main_obj.data = record
        if ctx.task.output_obj is not None:
            ctx.task.output_obj.data = record

class OTaskExecutorServicer(oprc_offload_pb2_grpc.OTaskExecutorServicer):
    def __init__(self):
        self.random_handler = RandomHandler()
        self.merge_handler = MergeHandler()

    async def invoke(self, request, context):
        if request.funcKey == 'example.record.random':
            result = await self.random_handler.handle(request)
        elif request.funcKey == 'example.record.merge':
            result = await self.merge_handler.handle(request)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Handler not found')
            return oprc_offload_pb2.ProtoOTaskCompletion(id=request.id, success=False)

        return oprc_offload_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_offload_pb2.ProtoObjectUpdate(data=result),
            output=oprc_offload_pb2.ProtoObjectUpdate(data=result)
        )

    def Invoke(self, request, context):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.invoke(request, context))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    oprc_offload_pb2_grpc.add_OTaskExecutorServicer_to_server(OTaskExecutorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
