import json

import grpc
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2, oprc_object_pb2
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2_grpc
import asyncio
import logging


async def run():
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = oprc_offload_pb2_grpc.FunctionExecutorStub(channel)
        data = {"helllooo": "world"}
        request = oprc_offload_pb2.ProtoOTask(
            funcKey='example.text.concat',
            main=oprc_object_pb2.ProtoPOObject(data=json.dumps(data).encode('utf-8'))
        )
        response = await stub.invoke(request)
        print(response)
        print(response.main.data.decode('utf-8'))
        print(response.output.data.decode('utf-8'))


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())