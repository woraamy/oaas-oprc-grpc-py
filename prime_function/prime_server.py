import asyncio
import grpc
import logging
import os
import json
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while (i * i) <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

class PrimeHandler:
    async def handle(self, ctx):
        count = int(ctx.args.get('COUNT', '10'))
        primes = generate_primes(count)
        ctx.main_data = primes
        ctx.output_data = primes

class GrpcCtx:
    main_data = None
    output_data = None

    def __init__(self, request):
        self.task = request
        self.args = request.args

class OTaskExecutorServicer(oprc_offload_pb2_grpc.OTaskExecutorServicer):
    def __init__(self):
        self.prime_handler = PrimeHandler()

    async def invoke(self, request, context):
        print("Received request")
        ctx = GrpcCtx(request)
        if request.funcKey == 'example.prime.generate':
            await self.prime_handler.handle(ctx)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Handler not found')
            return oprc_offload_pb2.ProtoOTaskCompletion(id=request.id, success=False)
        
        main_obj = json.dumps(ctx.main_data).encode('utf-8')
        if ctx.output_data is not None:
            output_obj = json.dumps(ctx.output_data).encode('utf-8')
        else:
            output_obj = b''

        return oprc_offload_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_offload_pb2.ProtoObjectUpdate(data=main_obj),
            output=oprc_offload_pb2.ProtoObjectUpdate(data=output_obj)
        )

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
