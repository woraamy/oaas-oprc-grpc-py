import grpc
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc 
import asyncio
import logging

async def run():
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = oprc_offload_pb2_grpc.OTaskExecutorStub(channel)
        response = await stub.invoke(oprc_offload_pb2.ProtoOTask(funcKey='example.record.random'))
        print(response)

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
