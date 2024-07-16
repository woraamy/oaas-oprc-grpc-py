import asyncio
import logging
import os

import grpc

from oaas_sdk_grpc.model import GrpcCtx
from oaas_sdk_grpc.model import OTaskExecutorServicer
from oaas_sdk_grpc.gen_grpc import oprc_offload_pb2_grpc


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


class PrimeHandler:
    # User's handler to generate prime numbers
    async def handle(self, ctx: GrpcCtx):
        prev_prime = int(ctx.main_data['PRIME'])
        prime = next_prime(prev_prime)
        new_data = {'PRIME': prime}
        ctx.main_data = new_data
        ctx.output_data = new_data


async def serve():

    server = grpc.aio.server()
    prime_handler = PrimeHandler()
    otask_servicer = OTaskExecutorServicer(prime_handler)

    oprc_offload_pb2_grpc.add_FunctionExecutorServicer_to_server(otask_servicer, server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(serve())
