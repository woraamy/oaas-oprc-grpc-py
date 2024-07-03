import asyncio
import grpc
from concurrent import futures
import time
import logging
import random
import string
import os
import oaas_sdk_py as oaas
from oaas_sdk_py import OaasInvocationCtx
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc
import json

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


def generate_text(num):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(num))


class RandomHandler(oaas.Handler):
    # Generates a random record with the specified number of entries, keys, and values.
    async def handle(self, ctx: OaasInvocationCtx):

        # Get the number of entries, keys, and values from the task arguments
        entries = int(ctx.args.get('ENTRIES', '10'))
        keys = int(ctx.args.get('KEYS', '10'))
        values = int(ctx.args.get('VALUES', '10'))
        max_keys = int(ctx.args.get('MAX', '10000'))
        inplace = ctx.args.get('INPLACE', 'true').lower() == 'true'
        req_ts = int(ctx.args.get('reqts', '0'))

        # Copy a record from the main object if it exists
        record = json.loads(ctx.task.main.data) if ctx.task.main.data is not None and len(
            ctx.task.main.data) != 0 else {}

        # Generate a random record
        for _ in range(entries):
            record[generate_text(keys)] = generate_text(values)
        count = len(record)
        if count > max_keys:
            for _ in range(count - max_keys):
                k = next(iter(record.keys()))
                record.pop(k)

        # Add a timestamp to the record
        record['ts'] = round(time.time() * 1000)
        if req_ts > 0:
            record['reqts'] = req_ts
        if inplace:
            ctx.main_data = json.dumps(record).encode('utf-8')
        if ctx.task.output is not None:
            ctx.output_data = record


class GrpcCtx:
    main_data = None
    output_data = None

    def __init__(self, request):
        self.task = request
        self.args = request.args


class OTaskExecutorServicer(oprc_offload_pb2_grpc.OTaskExecutorServicer):
    def __init__(self):
        self.random_handler = RandomHandler()
        # self.merge_handler = MergeHandler()

    async def invoke(self, request, context):
        print("Received request")
        ctx = GrpcCtx(request)
        if request.funcKey == 'example.record.random':
            await self.random_handler.handle(ctx)
        # elif request.funcKey == 'example.record.merge':
        #     await self.merge_handler.handle(ctx)

        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Handler not found')
            return oprc_offload_pb2.ProtoOTaskCompletion(id=request.id, success=False)

        # Serialize the main and output objects to be bytes
        main_obj = json.dumps(ctx.main_data).encode('utf-8')
        if ctx.output_data is not None:
            output_obj = json.dumps(ctx.output_data).encode('utf-8')
        else:
            output_obj = b''

        # Return the completion message and the main and output objects
        return oprc_offload_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_offload_pb2.ProtoObjectUpdate(data=main_obj),
            output=oprc_offload_pb2.ProtoObjectUpdate(data=output_obj)
        )

    # def Invoke(self, request, context):
    #     loop = asyncio.get_event_loop()
    #     return loop.run_until_complete(self.invoke(request, context))


async def serve():
    server = grpc.aio.server()
    oprc_offload_pb2_grpc.add_OTaskExecutorServicer_to_server(OTaskExecutorServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
