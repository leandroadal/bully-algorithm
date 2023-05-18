from concurrent import futures

import grpc
import election_pb2_grpc
import node


def conf_server():
    while True:
        standard = input('Deseja usar uma configuração pre-definida '
                         'para a porta do servidor e seus pares? S / N: ')
        if standard == 'S' or 's':
            id = int(input('Digite o ID (de 1 a 3) do servidor: '))
            servers = {
                1: {'port': 50051, 'peers': [50052, 50053]},
                2: {'port': 50052, 'peers': [50051, 50053]},
                3: {'port': 50053, 'peers': [50052, 50051]},
            }
            if 0 < id < 4:
                port = servers[id]['port']
                peers = servers[id]['peers']
                return id, port, peers
            else:
                print('Erro! Digite um ID entre 1 e 3')
        elif standard == 'N' or 'n':
            id = int(input('Digite o ID do servidor: '))
            port = int(input('Digite a porta do servidor: '))
            qt = int(input('Digite a quantidade de peers: '))

            peers = []
            for i in range(qt):
                p = int(input(f'{i + 1} peer: '))
                peers.append(p)
            return id, port, peers
        else:
            print('Erro! Digite S para usar uma configuração padrão e N pada definir uma própria')


def run_server(id, port, peers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    election = node.Election(id)
    election_pb2_grpc.add_ElectionServicer_to_server(election, server)
    server.add_insecure_port(f'[::]:{str(port)}')
    server.start()
    print(f'Servidor: {id}, iniciado na porta: {port}\n')
    menu_server(election, port, peers)


def menu_server(election, port, peers):
    while True:
        choice = input('[1] - Criar canal com os outros nó\n'
                       '[2] - Encontrar os ids do servidores\n'
                       '[3] - Solicitar permissão ao coordenador\n'
                       '[4] - ID do coordenador atual (debug)\n'
                       '[5] - Solicitar eleições (debug)\n'
                       '[6] - Tornar este nó coordenador (debug)\n'
                       'Digite o número correspondente a requisição: ')
        print(' ')
        if choice == '1':
            stubs(election, port, peers)
        elif choice == '2':
            print('=== Solicitando ids ===')
            res = election.req_serv_id()
            if res and election.leader_id is None:
                print('Solicitando ser eleito...')
                res_election = election.req_election()  # Realiza a eleição do coordenador
                if res_election != 'OK':  # caso receba um OK ao alguém com id maior disponível
                    print(f'O coordenador é o Nó: '
                          f'{"Atual" if election.leader_id == election.id else election.leader_id}')
                else:
                    print('Desistindo da eleição')
            elif res:
                print(f'O coordenador é o Nó: '
                      f'{"Atual" if election.leader_id == election.id else election.leader_id}')
            elif res is False:
                print('Falha ao obter algum id')
            print('\n')
        elif choice == '3':
            if election.id != election.leader_id and election.req_permission('CREATE') is None:
                print('Coordenador não está respondendo!')
                print('Elegendo um novo coordenador...')
                print(f'O novo coordenador será: {election.leader_id}')
            elif election.id != election.leader_id:
                print(election.req_permission('CREATE'))
            else:
                print('Não foi possível efetuar a requisição. O nó atual é o coordenador')
        elif choice == '4':
            print(f'O coordenador atual é: nó {election.leader_id}')
        elif choice == '5':
            res = election.req_election()
            if res == 'OK':
                print(f'Desistindo da eleição pois nó com id mais alto respondeu')
                print(f'O coordenador eleito é: nó {election.leader_id}')
        elif choice == '6':
            print(election.req_leader())


def stubs(election, port, peers):
    election.stubs = []
    for peer in peers:
        if peer != port:
            channel = grpc.insecure_channel(f'localhost:{str(peer)}')
            stub = election_pb2_grpc.ElectionStub(channel)
            election.stubs.append(stub)
    print('Sucesso!\n')


if __name__ == '__main__':
    try:
        serv_id, serv_port, serv_peers = conf_server()
        run_server(serv_id, serv_port, serv_peers)
    except KeyboardInterrupt:
        print('\n')
        print('Encerando o Servidor!')
