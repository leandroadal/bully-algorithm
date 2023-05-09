from concurrent import futures

import grpc
import election_pb2_grpc
import node


def run_server(id, port, peers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    election = node.Election(id)
    election_pb2_grpc.add_ElectionServicer_to_server(election, server)
    server.add_insecure_port(f'[::]:{str(port)}')
    server.start()
    print(f'Servidor: {id}, iniciado na porta: {port}\n')

    try:
        while True:
            choice = input('[1] - Criar canal com os outros nó\n'
                           '[2] - Encontrar os ids do servidores\n'
                           '[3] - Solicitar permissão ao coordenador\n'
                           '[4] - ID do Líder atual\n'
                           '[5] - Solicitar eleições\n'
                           '[6] - Tornar este nó coordenador\n'
                           'Digite o número correspondente a requisição: ')
            print(' ')

            if choice == '1':
                election.stubs = []
                for peer in peers:
                    if peer != port:
                        channel = grpc.insecure_channel(f'localhost:{str(peer)}')
                        stub = election_pb2_grpc.ElectionStub(channel)
                        election.stubs.append(stub)
                print('Sucesso!\n')
            elif choice == '2':
                print('=== Solicitando ids ===')
                election.req_serv_id()
                print('\n')
            elif choice == '3':
                if election.req_permission('CREATE') is False:
                    print('Coordenador não está respondendo!')
                    print('Elegendo um novo coordenador...')
                    print(f'O novo coordenador será: {election.req_election()}')
                print(election.req_permission('CREATE'))
            elif choice == '4':
                print(f'O líder atual é: {election.leader_id}')
            elif choice == '5':
                res = election.req_election()
                if res == 'OK':
                    print(f'Desistindo da eleição pois nó com id mais alto respondeu')
                else:
                    print(f'O novo líder é: {res}')
            elif choice == '6':
                print(election.send_coordinator())
    except KeyboardInterrupt:
        print('\n')
        print('Encerando o Servidor!')


if __name__ == '__main__':
    id = int(input('Digite o ID do servidor: '))
    port = int(input('Digite a porta do servidor: '))

    qt = int(input('Digite a quantidade de peers: '))
    peers = []
    for i in range(qt):
        p = int(input(f'{i + 1} peer: '))
        peers.append(p)
    run_server(id, port, peers)

    # id=1, port=50051, peers=[50052, 50053]
    # id=2, port=50052, peers=[50051, 50053]
    # id=3, port=50053, peers=[50052, 50051]
