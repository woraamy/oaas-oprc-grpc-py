import grpc
from concurrent import futures
import time
import logging
import random
import string
import os
import gen_grpc.oprc_offload_pb2 as oprc_offload_pb2
import gen_grpc.oprc_offload_pb2_grpc as oprc_offload_pb2_grpc

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
level = logging.getLevelName(LOG_LEVEL)
logging.basicConfig(level=level)

def generate_text(num):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(num))

class RandomHandler:
    async def handle(self, task):
        entries = int(task.args.get('ENTRIES', '10'))
        keys = int(task.args.get('KEYS', '10'))
        values = int(task.args.get('VALUES', '10'))
        max_keys = int(task.args.get('MAX', '10000'))
        inplace = task.args.get('INPLACE', 'true').lower() == 'true'
        req_ts = int(task.args.get('reqts', '0'))

        record = {}  # Placeholder for the actual data handling

        for _ in range(entries):
            record[generate_text(keys)] = generate_text(values)
        count = len(record)
        if count > max_keys:
            for _ in range(count - max_keys):
                k = next(iter(record.keys()))
                record.pop(k)

        record['ts'] = round(time.time() * 1000)
        if req_ts > 0:
            record['reqts'] = req_ts

        # Update the task's main object data or output object data
        task.main.data = record if inplace else None
        task.output.data = record if not inplace else None

        return record

class MergeHandler:
    async def handle(self, task):
        inplace = task.args.get('INPLACE', 'false').lower() == 'true'
        record = {}  # Placeholder for the actual data handling

        for input_obj in task.inputs:
            other_record = {}  # Placeholder for actual input object data handling
            record.update(other_record)

        task.main.data = record if inplace else None
        task.output.data = record if not inplace else None

        return record

class OTaskExecutorServicer(oprc__offload_pb2_grpc.OTaskExecutorServicer):
    def __init__(self):
        self.random_handler = RandomHandler()
        self.merge_handler = MergeHandler()

    async def invoke(self, request, context):
        if request.funcKey == 'example.record.random':
            result = await self.random_handler.handle(request)
        elif request.funcKey == 'example.record.merge':
            result = await self.merge_handler.handle(request)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Handler not found')
            return oprc_offload_pb2.ProtoOTaskCompletion(id=request.id, success=False)

        return oprc_pb2.ProtoOTaskCompletion(
            id=request.id,
            success=True,
            main=oprc_pb2.ProtoObjectUpdate(data=result),
            output=oprc_pb2.ProtoObjectUpdate(data=result)
        )

    def Invoke(self, request, context):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.invoke(request, context))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    oprc_offload_pb2_grpc.add_OTaskExecutorServicer_to_server(OTaskExecutorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
