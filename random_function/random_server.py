import asyncio
import grpc
import time
import logging
import random
import string
import os
import oaas_sdk_py as oaas
from oaas_sdk_py import OaasInvocationCtx
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc
import json
from oaas_sdk_grpc.model import GrpcCtx, OffloadGrpc
from oaas_sdk_grpc.model import OTaskExecutorServicer

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


def generate_text(num):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(num))


class RandomHandler(oaas.Handler):
    # Generates a random record with the specified number of entries, keys, and values.
    async def handle(self, ctx: GrpcCtx):

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
            ctx.main_data = record
        if ctx.task.output is not None:
            ctx.output_data = record


async def serve():
    offload_grpc = OffloadGrpc()
    server = grpc.aio.server()
    random_handler = RandomHandler()
    otask_servicer = OTaskExecutorServicer(random_handler)

    offload_grpc.offload.add_FunctionExecutorServicer_to_server(
        otask_servicer, server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())