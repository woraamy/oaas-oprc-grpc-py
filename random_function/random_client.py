import json

import grpc
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2, oprc_object_pb2
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2_grpc
import asyncio
import logging


async def run():
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = oprc_offload_pb2_grpc.FunctionExecutorStub(channel)
        data = {"": ""}
        request = oprc_offload_pb2.ProtoOTask(
            funcKey='example.record.random',
            main=oprc_object_pb2.ProtoPOObject(data=json.dumps(data).encode('utf-8'))
        )
        response = await stub.invoke(request)
        print(response)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
