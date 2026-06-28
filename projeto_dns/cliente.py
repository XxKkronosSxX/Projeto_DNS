"""
============================================================
  SIMULADOR DIDÁTICO DE DNS — CLIENTE
  Com integração da PARTE 3: Interface Visual e Logs
============================================================

Este arquivo mantém a lógica do cliente DNS didático e usa o módulo
visual_logs.py para exibir a consulta de forma organizada.
"""

import socket
import time

from visual_logs import (
    cabecalho,
    exibir_resultado_cliente,
    mostrar_fluxo_cliente,
    separador,
    timestamp_completo,
)

# ------------------------------------------------------------
# CONFIGURAÇÃO DA CONEXÃO
# ------------------------------------------------------------
HOST = "127.0.0.1"
PORTA = 5353
TIMEOUT = 5.0
ENCODING = "utf-8"
BUFFER = 1024


def consultar_dominio(dominio: str) -> dict:
    """Consulta um domínio no servidor e retorna os dados para exibição."""
    resultado = {
        "dominio": dominio,
        "status": None,
        "ip": None,
        "resposta_bruta": "",
        "tempo_ms": None,
        "ip_servidor": None,
        "porta_servidor": None,
        "ip_local": None,
        "porta_local": None,
        "horario": timestamp_completo(),
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(TIMEOUT)

            inicio = time.perf_counter()
            cliente.connect((HOST, PORTA))

            resultado["ip_servidor"], resultado["porta_servidor"] = cliente.getpeername()
            resultado["ip_local"], resultado["porta_local"] = cliente.getsockname()

            cliente.sendall(dominio.encode(ENCODING))
            dados = cliente.recv(BUFFER)
            resposta = dados.decode(ENCODING).strip()

            fim = time.perf_counter()
            resultado["tempo_ms"] = (fim - inicio) * 1000
            resultado["resposta_bruta"] = resposta

            if resposta.startswith("OK"):
                partes = resposta.split(maxsplit=1)
                resultado["status"] = "SUCESSO"
                resultado["ip"] = partes[1] if len(partes) > 1 else "(sem IP)"
            elif resposta.startswith("ERRO"):
                resultado["status"] = "NAO_ENCONTRADO"
            else:
                resultado["status"] = "NAO_ENCONTRADO"

    except ConnectionRefusedError:
        resultado["status"] = "FALHA_CONEXAO"
    except socket.timeout:
        resultado["status"] = "TIMEOUT"
    except socket.gaierror:
        resultado["status"] = "FALHA_CONEXAO"

    return resultado


def main() -> None:
    """Laço principal do cliente DNS didático."""
    cabecalho("CLIENTE DNS — SIMULADOR DIDÁTICO", "Visualização da consulta")
    print(f"  Servidor configurado : {HOST}:{PORTA}")
    print("  Digite um domínio para consultar. Exemplos:")
    print("    - google.com")
    print("    - python.org")
    print("    - dominioinexistente.com")
    print("  Digite 'sair' para encerrar.")
    separador("=")

    while True:
        try:
            dominio = input("\n  Domínio> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Encerrando o cliente. Até logo!\n")
            break

        if dominio.lower() in ("sair", "exit", "quit", "q"):
            print("\n  Encerrando o cliente. Até logo!\n")
            break

        if not dominio:
            print("  (digite um domínio ou 'sair')")
            continue

        # Parte 3: mostrar o fluxo de forma didática antes do envio.
        mostrar_fluxo_cliente(dominio, HOST, PORTA)

        resultado = consultar_dominio(dominio)

        # Parte 3: exibir resultado com mensagens, tempo, IP e porta.
        exibir_resultado_cliente(resultado, HOST, PORTA, TIMEOUT)


if __name__ == "__main__":
    main()
