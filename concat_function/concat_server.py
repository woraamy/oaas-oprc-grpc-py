import logging
import os
import time
import asyncio

import aiohttp
import json
from grpc import aio
from concurrent import futures

from oaas_sdk_grpc.model import GrpcCtx, OTaskExecutorServicer, OffloadGrpc

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
TEXT_KEY = os.getenv("TEXT_KEY", "text")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


class ConcatHandler:
    async def handle(self, ctx: GrpcCtx):
        append = ctx.args.get('APPEND', '')
        inplace = ctx.args.get('INPLACE', 'false').lower() == 'true'
        req_ts = int(ctx.args.get('reqts', '0'))

        record = json.loads(ctx.task.main.data) if ctx.task.main.data is not None and len(
            ctx.task.main.data) != 0 else {}

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
                    ctx.main_data = record
                if ctx.task.output is not None:
                    ctx.output_data = record


async def serve():
    offload_grpc = OffloadGrpc()
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
    concat_handler = ConcatHandler()
    print("Handler created")
    otask_servicer = OTaskExecutorServicer(concat_handler)
    print("Init servicer")

    offload_grpc.offload.add_FunctionExecutorServicer_to_server(otask_servicer, server)
    listen_addr = "[::]:8080"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(serve())
