"""
============================================================
  SIMULADOR DIDÁTICO DE DNS — SERVIDOR
  Com integração da PARTE 3: Interface Visual e Logs
============================================================

Este arquivo mantém a lógica do servidor DNS didático e usa o módulo
visual_logs.py para mostrar e registrar as consultas de forma organizada.
"""

import socket
import threading
import time

from dns_table import buscar_dominio
from visual_logs import (
    cabecalho,
    imprimir_evento_servidor,
    registrar_consulta,
    separador,
    timestamp_completo,
)

# ------------------------------------------------------------
# CONFIGURAÇÃO DO SERVIDOR
# ------------------------------------------------------------
HOST = "127.0.0.1"
PORTA = 5353
ENCODING = "utf-8"
BUFFER = 1024
ARQUIVO_LOG_TXT = "dns_log.txt"
ARQUIVO_LOG_CSV = "dns_log.csv"
ATRASO_BUSCA = 0.15

# ------------------------------------------------------------
# CACHE DNS
# ------------------------------------------------------------
cache_dns = {}
trava_cache = threading.Lock()
trava_saida = threading.Lock()


def resolver(dominio: str):
    """Resolve um domínio usando cache e tabela DNS."""
    chave = dominio.strip().lower()

    with trava_cache:
        if chave in cache_dns:
            return cache_dns[chave], True

    time.sleep(ATRASO_BUSCA)
    ip = buscar_dominio(chave)

    if ip is not None:
        with trava_cache:
            cache_dns[chave] = ip

    return ip, False


def atender_cliente(conexao: socket.socket, endereco) -> None:
    """Atende um cliente conectado ao servidor."""
    ip_cliente, porta_cliente = endereco

    with conexao:
        try:
            dados = conexao.recv(BUFFER)
            if not dados:
                return

            dominio = dados.decode(ENCODING).strip()
            ip, veio_do_cache = resolver(dominio)

            if ip is not None:
                resposta = f"OK {ip}"
                status = "ENCONTRADO"
            else:
                resposta = "ERRO dominio nao encontrado"
                status = "NAO ENCONTRADO"

            conexao.sendall(resposta.encode(ENCODING))

            evento = {
                "horario": timestamp_completo(),
                "ip_cliente": ip_cliente,
                "porta_cliente": porta_cliente,
                "dominio": dominio,
                "status": status,
                "origem": "CACHE" if veio_do_cache else "TABELA",
                "resposta": resposta,
            }

            # Parte 3: registrar em log e mostrar no terminal do servidor.
            with trava_saida:
                registrar_consulta(evento, ARQUIVO_LOG_TXT, ARQUIVO_LOG_CSV)
                imprimir_evento_servidor(evento)

        except ConnectionResetError:
            with trava_saida:
                print(f"  Cliente {ip_cliente}:{porta_cliente} desconectou inesperadamente.")
                separador()
        except UnicodeDecodeError:
            with trava_saida:
                print(f"  Cliente {ip_cliente}:{porta_cliente} enviou dados fora do padrão UTF-8.")
                separador()


def iniciar_servidor() -> None:
    """Inicializa o socket TCP e fica aguardando consultas."""
    cabecalho("SERVIDOR DNS — SIMULADOR DIDÁTICO", "Monitoramento em tempo real")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()

        print(f"  Protocolo          : TCP")
        print(f"  Escutando em       : {HOST}:{PORTA}")
        print(f"  Log TXT            : {ARQUIVO_LOG_TXT}")
        print(f"  Log CSV            : {ARQUIVO_LOG_CSV}")
        print("  Status             : aguardando consultas")
        separador("=")
        print()

        try:
            while True:
                conexao, endereco = servidor.accept()
                thread = threading.Thread(
                    target=atender_cliente,
                    args=(conexao, endereco),
                    daemon=True,
                )
                thread.start()
        except KeyboardInterrupt:
            print("\n\n  Servidor encerrado pelo usuário. Até logo!\n")


if __name__ == "__main__":
    iniciar_servidor()
