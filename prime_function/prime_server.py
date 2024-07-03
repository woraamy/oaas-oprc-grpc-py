import asyncio
import grpc
import logging
import os
import json
from gen_grpc import oprc_offload_pb2, oprc_offload_pb2_grpc

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)


def is_prime(n):
    # Check if a number is prime
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def next_prime(p):
    # Return the next prime number after the given prime p
    if not is_prime(p):
        raise ValueError(f"The input is not a prime number")

    next_candidate = p + 1
    while not is_prime(next_candidate):
        next_candidate += 1
    return next_candidate


class PrimeNumber:
    def __init__(self):
        self.prime = None

    def update(self, prime):
        self.prime = prime


class GrpcCtx:
    main_data = None

    def __init__(self, request):
        self.task = request
        self.args = request.args
        if self.main_data is None:
            self.main_data = request.main.data


class PrimeHandler:
    # User's handler to generate prime numbers
    async def handle(self, ctx: GrpcCtx, number: PrimeNumber):
        prev_prime = number.prime
        prime = next_prime(prev_prime)
        number.update(prime)
        new_data = {'PRIME': prime}
        ctx.main_data = json.dumps(new_data).encode('utf-8')


class OTaskExecutorServicer(oprc_offload_pb2_grpc.OTaskExecutorServicer):
    def __init__(self, handler: PrimeHandler(), number: PrimeNumber()):
        self.prime_handler = handler
        self.prime_number = number

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

        return oprc_offload_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_offload_pb2.ProtoObjectUpdate(data=main_obj)
        )


async def serve():
    server = grpc.aio.server()
    prime_handler = PrimeHandler()
    prime_number = PrimeNumber()
    oprc_offload_pb2_grpc.add_OTaskExecutorServicer_to_server(OTaskExecutorServicer(handler=prime_handler,
                                                                                    number=prime_number), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
