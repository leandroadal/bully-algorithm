# Bully Algorithm

# Description:
- Projeto da disciplina de Sistemas Distribuídos que tem por objetivo mostra o funcionamento do algoritmo do Valentão usando o `gRPC` como forma de comunicação.

- Em `main` o servidor é "ligado" e mostra os menus
  
- `node` representa um nó no sistema e possui a classe `Election` herda do service do gRPC sendo responsável por implementar a lógica da eleição do coordenador.
  
- Cada servidor deve se associar a portas diferentes para se comunicar entre si na rede.
  

## Rodando o projeto

Para o roda o projeto é simples:

- 1 - Executar o arquivo Main em ao menos dois terminais

- 2 - Digitar as informações do servidor como `id`, `porta` e `peer` (ou seja, os servidores que devem se conectar).
  
- 3 - Realizar as requisições desejadas