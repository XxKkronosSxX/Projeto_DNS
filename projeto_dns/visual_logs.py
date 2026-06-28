"""
============================================================
  SIMULADOR DIDÁTICO DE DNS — PARTE 3
  Módulo: INTERFACE VISUAL, TIMESTAMPS E LOGS
============================================================

Este arquivo concentra a contribuição do Integrante 3:
  - organização visual dos terminais;
  - mensagens didáticas;
  - timestamps;
  - logs das consultas;
  - exibição de IP e porta;
  - mensagens de erro e sucesso;
  - monitoramento das consultas no terminal do servidor.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime
from typing import Any

LARGURA = 64
ENCODING = "utf-8"


def timestamp_curto() -> str:
    """Retorna hora:minuto:segundo para exibir no terminal."""
    return datetime.now().strftime("%H:%M:%S")


def timestamp_completo() -> str:
    """Retorna data e hora para salvar nos logs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def cabecalho(titulo: str, subtitulo: str | None = None) -> None:
    """Imprime cabeçalho visual padronizado."""
    print()
    print("=" * LARGURA)
    print(titulo.center(LARGURA))
    if subtitulo:
        print(subtitulo.center(LARGURA))
    print("=" * LARGURA)


def separador(caractere: str = "─") -> None:
    """Imprime uma linha separadora para organizar o terminal."""
    print("  " + caractere * (LARGURA - 4))


def formatar_endpoint(ip: Any, porta: Any) -> str:
    """Formata IP:porta de forma segura."""
    if ip is None or porta is None:
        return "não disponível"
    return f"{ip}:{porta}"


def formatar_tempo_ms(valor: float | None) -> str:
    """Formata tempo de resposta em milissegundos."""
    if valor is None:
        return "não medido"
    return f"{valor:.2f} ms"


# ============================================================
# VISUAL DO CLIENTE
# ============================================================
def mostrar_fluxo_cliente(dominio: str, host: str, porta: int) -> None:
    """Mostra o caminho da consulta antes de ela ser enviada."""
    print()
    separador()
    print(f"  [{timestamp_curto()}] FLUXO DA CONSULTA")
    print(f"  1) Cliente conecta no servidor DNS em {host}:{porta}")
    print(f"  2) Cliente envia o domínio: {dominio}")
    print("  3) Servidor responde: OK <ip> ou ERRO <mensagem>")
    print("  4) Cliente interpreta e exibe o resultado")
    separador()


def exibir_resultado_cliente(resultado: dict, host: str, porta: int, timeout: float) -> None:
    """Exibe o resultado da consulta de forma didática."""
    status = resultado.get("status")

    print()
    separador()

    if status == "SUCESSO":
        print("  ✓ DOMÍNIO ENCONTRADO")
        separador()
        print(f"  Domínio consultado : {resultado.get('dominio')}")
        print(f"  Endereço IP        : {resultado.get('ip')}")
        print(f"  Horário            : {resultado.get('horario')}")
        print(f"  Tempo de resposta  : {formatar_tempo_ms(resultado.get('tempo_ms'))}")
        print()
        print("  Endpoints da conexão TCP:")
        print(f"  Servidor DNS       : {formatar_endpoint(resultado.get('ip_servidor'), resultado.get('porta_servidor'))}")
        print(f"  Cliente            : {formatar_endpoint(resultado.get('ip_local'), resultado.get('porta_local'))}")
        print()
        print("  Explicação         : o servidor encontrou o domínio e respondeu OK <ip>.")

    elif status == "NAO_ENCONTRADO":
        print("  ✗ DOMÍNIO NÃO ENCONTRADO")
        separador()
        print(f"  Domínio consultado : {resultado.get('dominio')}")
        print(f"  Horário            : {resultado.get('horario')}")
        print(f"  Tempo de resposta  : {formatar_tempo_ms(resultado.get('tempo_ms'))}")
        print(f"  Resposta recebida  : {resultado.get('resposta_bruta')}")
        print()
        print("  Explicação         : esse domínio não está cadastrado na tabela DNS.")

    elif status == "FALHA_CONEXAO":
        print("  ⚠ FALHA DE CONEXÃO")
        separador()
        print(f"  Tentativa          : {host}:{porta}")
        print("  Possível causa     : servidor desligado, IP errado ou porta errada.")
        print("  Como resolver      : rode primeiro o servidor com 'python servidor.py'.")

    elif status == "TIMEOUT":
        print("  ⚠ TEMPO ESGOTADO (TIMEOUT)")
        separador()
        print(f"  Domínio consultado : {resultado.get('dominio')}")
        print(f"  Limite configurado : {timeout:.0f} segundos")
        print("  Explicação         : o cliente esperou, mas não recebeu resposta a tempo.")

    else:
        print("  ⚠ STATUS DESCONHECIDO")
        separador()
        print(f"  Resultado bruto    : {resultado}")

    separador()
    print()


# ============================================================
# LOGS E MONITORAMENTO DO SERVIDOR
# ============================================================
def montar_linha_log(evento: dict) -> str:
    """Monta uma linha legível para o arquivo dns_log.txt."""
    return (
        f"[{evento['horario']}] "
        f"cliente={evento['ip_cliente']}:{evento['porta_cliente']} "
        f"dominio='{evento['dominio']}' "
        f"status={evento['status']} "
        f"origem={evento['origem']} "
        f"resposta='{evento['resposta']}'"
    )


def registrar_consulta(evento: dict, arquivo_txt: str = "dns_log.txt", arquivo_csv: str = "dns_log.csv") -> None:
    """
    Registra a consulta em dois formatos:
      - TXT: bom para mostrar rapidamente no terminal;
      - CSV: bom para abrir como tabela.
    """
    with open(arquivo_txt, "a", encoding=ENCODING) as arquivo:
        arquivo.write(montar_linha_log(evento) + "\n")

    campos = [
        "horario",
        "ip_cliente",
        "porta_cliente",
        "dominio",
        "status",
        "origem",
        "resposta",
    ]

    precisa_cabecalho = not os.path.exists(arquivo_csv) or os.path.getsize(arquivo_csv) == 0

    with open(arquivo_csv, "a", encoding=ENCODING, newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if precisa_cabecalho:
            escritor.writeheader()
        escritor.writerow({campo: evento.get(campo, "") for campo in campos})


def imprimir_evento_servidor(evento: dict) -> None:
    """Mostra no terminal do servidor a consulta recebida em tempo real."""
    hora_terminal = evento["horario"].split()[-1]
    simbolo = "✓" if evento["status"] == "ENCONTRADO" else "✗"

    print(f"  [{hora_terminal}] {simbolo} CONSULTA RECEBIDA")
    print(f"      Cliente : {evento['ip_cliente']}:{evento['porta_cliente']}")
    print(f"      Domínio : {evento['dominio']}")
    print(f"      Status  : {evento['status']}")
    print(f"      Origem  : {evento['origem']}")
    print(f"      Resposta: {evento['resposta']}")
    separador()
    print(flush=True)
