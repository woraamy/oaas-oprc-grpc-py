import grpc
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc, oprc_object_pb2
import asyncio
import logging
import json


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = oprc_offload_pb2_grpc.OTaskExecutorStub(channel)
        data = {'PRIME': 0}
        request = oprc_offload_pb2.ProtoOTask(
            funcKey='example.prime.generate',
            main=oprc_object_pb2.ProtoOObject(data=json.dumps(data).encode('utf-8'))
        )
        response = await stub.invoke(request)
        print(response.main.data.decode('utf-8'))


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
