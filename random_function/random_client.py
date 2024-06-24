import grpc
import gen_grpc.oprc_offload_pb2 as oprc_offload_pb2
import gen_grpc.oprc_offload_pb2_grpc as oprc_offload_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = oprc_offload_pb2_grpc.OTaskExecutorStub(channel)
        response = stub.invoke(oprc_offload_pb2.ProtoOTask(funcKey='example.record.random'))
        print("Task completed:", response)

if __name__ == '__main__':
    run()
