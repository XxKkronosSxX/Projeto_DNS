"""
============================================================
  SIMULADOR DIDÁTICO DE DNS  —  PARTE DO INTEGRANTE 1
  Módulo: TABELA DNS (registros "autoritativos")
============================================================

Este módulo simula a base de dados que um servidor DNS de verdade consultaria.
Na internet real, esses registros estão espalhados por milhares de servidores
autoritativos pelo mundo. Aqui, para fins didáticos, usamos um dicionário
Python simples mapeando  DOMÍNIO -> ENDEREÇO IP.

Os IPs abaixo são apenas ILUSTRATIVOS (alguns reais, outros simulados) e servem
só para a demonstração — não consultam a internet de verdade.
"""

# Dicionário com os registros DNS. A busca é O(1) (instantânea) por ser um dict.
# DOMÍNIO (chave)  ->  IP (valor)
TABELA_DNS = {
    "google.com":        "142.250.190.78",
    "youtube.com":       "142.250.190.14",
    "facebook.com":      "157.240.12.35",
    "instagram.com":     "157.240.231.174",
    "wikipedia.org":     "208.80.154.224",
    "github.com":        "140.82.121.4",
    "stackoverflow.com": "151.101.65.69",
    "amazon.com.br":     "54.233.135.71",
    "mercadolivre.com.br":"161.35.0.10",
    "olx.com.br":        "104.18.24.50",
    "globo.com":         "186.192.90.5",
    "uol.com.br":        "200.147.118.40",
    "uff.br":            "200.20.15.10",
    "ufrj.br":           "146.164.2.10",
    "gov.br":            "161.148.164.30",
    "python.org":        "151.101.0.223",
    "openai.com":        "104.18.32.115",
    "anthropic.com":     "160.79.104.10",
}


def buscar_dominio(dominio: str):
    """
    Procura um domínio na tabela DNS.

    Retorna o IP (str) se o domínio existir, ou None se não existir.
    A busca é case-insensitive (DNS na vida real também ignora maiúsculas).
    """
    return TABELA_DNS.get(dominio.strip().lower())
