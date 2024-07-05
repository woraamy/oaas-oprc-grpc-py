import logging
import os
import time
import asyncio

import aiohttp
import grpc
from grpc import aio
from concurrent import futures

from oaas_sdk_grpc.model import GrpcCtx, OTaskExecutorServicer
from gen_grpc import oprc_offload_pb2_grpc

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
TEXT_KEY = os.getenv("TEXT_KEY", "text")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


class ConcatHandler:
    async def handle(self, ctx: GrpcCtx):
        append = ctx.args.get('APPEND', '')
        inplace = ctx.task.output_obj is None or ctx.task.output_obj.id is None
        req_ts = int(ctx.args.get('reqts', '0'))

        record = ctx.task.main_obj.data.copy() if ctx.task.main_obj.data is not None else {}

        if req_ts != 0:
            record['reqts'] = req_ts

        start_ts = time.time()
        async with aiohttp.ClientSession() as session:
            async with await ctx.load_main_file(session, TEXT_KEY) as resp:
                old_text = await resp.read()
                loading_time = time.time() - start_ts
                logging.debug(f"load data in {loading_time} s")

                text = old_text.decode("utf-8") + append
                b_text = bytes(text, 'utf-8')
                start_ts = time.time()
                if inplace:
                    await ctx.upload_main_byte_data(session, TEXT_KEY, b_text)
                else:
                    start_ts = time.time()
                    await ctx.upload_byte_data(session, TEXT_KEY, b_text)
                uploading_time = time.time() - start_ts
                logging.debug(f"upload data in {uploading_time} s")
                record['ts'] = round(time.time() * 1000)
                record['load'] = round(loading_time * 1000)
                record['upload'] = round(uploading_time * 1000)
                if inplace:
                    ctx.task.main_obj.data = record
                else:
                    ctx.task.output_obj.data = record


async def serve():
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
    concat_handler = ConcatHandler()
    otask_servicer = OTaskExecutorServicer(concat_handler)

    oprc_offload_pb2_grpc.add_FunctionExecutorServicer_to_server(otask_servicer, server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(serve())
