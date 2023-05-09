import grpc
import random
import election_pb2
import election_pb2_grpc


class Election(election_pb2_grpc.ElectionServicer):
    def __init__(self, id):
        self.id = id
        self.leader_id = None
        self.stubs = []
        self.nodes_id = {}

    def req_serv_id(self):
        for stub in self.stubs:
            try:
                response = stub.resp_serv_id(election_pb2.Empty())
                print(response.id)
                self.nodes_id[response.id] = stub
            except grpc.RpcError:
                continue

    def resp_serv_id(self, request, context):
        return election_pb2.response_id(id=self.id)

    def req_permission(self, type):
        if self.leader_id is None:
            self.req_election()
            return None
        else:
            try:
                # Pede permissão ao coordenador
                stub = self.nodes_id[self.leader_id]
                response = stub.resp_permission((election_pb2.request_permission(type=type)), timeout=5.0)
                return response.permission
            except grpc.RpcError:
                return False

    def resp_permission(self, request, context):
        """Quando eleito, o nó coordenador gerenciara os processos"""
        ran = random.randint(1, 1000)
        if ran >= 500:
            return election_pb2.response_permission(permission=True)
        else:
            return election_pb2.response_permission(permission=False)

    def req_election(self):
        for ids, stub in self.nodes_id.items():
            if ids > self.id:
                try:
                    response = stub.resp_election(election_pb2.request_election(serv_id=self.id))
                    if response.message == 'OK':  # Se houver receber um OK esse servidor desiste
                        return response.message
                except grpc.RpcError:
                    continue
        return self.send_coordinator()  # Nenhum servidor respondeu com OK

    def resp_election(self, request, context):
        if request.serv_id < self.id:
            return election_pb2.response_election(message='OK')
        return election_pb2.response_election(message='IGNORE')

    def send_coordinator(self):
        for stub in self.stubs:
            try:
                stub.recv_coordinator(election_pb2.send_coordinator(leader_id=self.id))
                self.leader_id = self.id
            except grpc.RpcError:
                continue
        return f'O novo coordenador é: {self.leader_id}'

    def recv_coordinator(self, request, context):
        self.leader_id = request.leader_id
        return election_pb2.Empty()
