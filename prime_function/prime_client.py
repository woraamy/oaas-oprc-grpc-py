import grpc
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc
import asyncio
import logging

async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = oprc_offload_pb2_grpc.OTaskExecutorStub(channel)
        request = oprc_offload_pb2.ProtoOTask(
            funcKey='example.prime.generate',
            args={'COUNT': '10'}
        )
        response = await stub.invoke(request)
        print(response.main.data.decode('utf-8'))
        print(response.output.data.decode('utf-8'))


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
