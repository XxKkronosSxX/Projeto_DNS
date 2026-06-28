# Projeto DNS Didático em Python

## 📌 Descrição

Este projeto é uma simulação didática de um sistema DNS usando **sockets TCP em Python**. A aplicação possui um **servidor DNS**, um **cliente DNS**, uma **tabela DNS simulada**, cache simples e logs das consultas.

A ideia principal é demonstrar como acontece uma comunicação cliente-servidor: o cliente envia um domínio, o servidor procura esse domínio em uma tabela/cache e responde com um IP ou com uma mensagem de erro.

---

## 👥 Divisão do trabalho

### Integrante 1 — Servidor DNS
Responsável pelo servidor TCP, recebimento das consultas, busca na tabela DNS, resposta ao cliente, tratamento de domínio inexistente e cache simples.

### Integrante 2 — Cliente DNS
Responsável pelo cliente TCP, conexão com o servidor, envio do domínio digitado, recebimento da resposta, cálculo do tempo de resposta e exibição dos dados da consulta.

### Integrante 3 — Interface Visual e Logs
Responsável pela organização visual dos terminais, mensagens didáticas, timestamps, exibição de IP/porta, logs das consultas e monitoramento das consultas no servidor.

### Integrante 4 — Testes, GitHub e Documentação
Responsável pela organização do repositório, README, testes com domínios válidos/inválidos, documentação e links finais de entrega.

---

## 🗂️ Estrutura do projeto

```text
projeto_dns_final_apresentacao/
├── servidor.py                    # Servidor DNS usando socket TCP
├── cliente.py                     # Cliente DNS usando socket TCP
├── dns_table.py                   # Tabela DNS simulada
├── visual_logs.py                 # Interface visual e logs da Parte 3
├── README.md                      # Documentação principal
├── PROTOCOLO_E_APRESENTACAO.md    # Protocolo combinado cliente-servidor
├── ROTEIRO_APRESENTACAO.md        # Organização dos slides e fala
├── PASSO_A_PASSO_DEMO.md          # Passo a passo para demonstração prática
├── COLA_EXPLICACAO.md             # Cola para explicar o projeto
├── PARTE4_COMPLEMENTADA.md        # Complemento da Parte 4
├── LINKS_ENTREGA.md               # Espaço para GitHub e vídeo
├── requirements.txt               # Dependências do projeto
└── .gitignore                     # Arquivos ignorados pelo Git
```

---

## 🚀 Como executar

### 1. Abrir a pasta do projeto

```bash
cd projeto_dns_final_apresentacao
```

### 2. Rodar o servidor

Em um terminal:

```bash
python servidor.py
```

O servidor ficará aguardando consultas na porta `5353`.

### 3. Rodar o cliente

Em outro terminal:

```bash
python cliente.py
```

Depois, digite um domínio para consultar.

---

## 🧪 Testes sugeridos

### Domínios válidos

Use domínios que existem em `dns_table.py`:

- `google.com`
- `youtube.com`
- `github.com`
- `python.org`

### Domínios inválidos

Use domínios que **não** existem na tabela:

- `teste.com`
- `dominioinexistente.com`
- `sitequalquer.com`

> Observação importante: `facebook.com` está cadastrado na tabela DNS do projeto, então ele deve ser tratado como **domínio válido**, não como inválido.

---

## 🔁 Teste do cache

Para demonstrar o cache DNS, consulte o mesmo domínio duas vezes:

```text
google.com
google.com
```

Na primeira consulta, o servidor deve indicar origem `TABELA`. Na segunda, deve indicar origem `CACHE`.

---

## 📜 Logs

Durante a execução, o servidor gera arquivos de log:

- `dns_log.txt`: histórico legível das consultas;
- `dns_log.csv`: histórico em formato de tabela.

Exemplo de linha de log:

```text
[2026-06-28 15:30:10] cliente=127.0.0.1:54321 dominio='google.com' status=ENCONTRADO origem=TABELA resposta='OK 142.250.190.78'
```

---

## 📡 Protocolo de comunicação

O cliente envia apenas o domínio em texto puro:

```text
google.com
```

O servidor responde de uma destas formas:

```text
OK 142.250.190.78
```

ou:

```text
ERRO dominio nao encontrado
```

---

## 📡 Conceitos de redes envolvidos

- Sockets TCP;
- comunicação cliente-servidor;
- DNS simulado;
- endereçamento IP;
- portas TCP;
- tempo de resposta/RTT;
- cache DNS;
- logs e monitoramento;
- tratamento de erros.

---

## 🛠️ Tecnologias

- Python 3;
- biblioteca padrão do Python: `socket`, `threading`, `time`, `datetime`, `csv`, `os`.
