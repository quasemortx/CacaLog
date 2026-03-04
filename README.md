# CaçaLog MVP

Sistema de monitoramento de inventário via WhatsApp, integrado com Evolution API e Google Sheets.

## Funcionalidades
- Monitora mensagens de um grupo específico.
- Identifica Salas (Ex: S-712) e Laboratórios (Ex: L-03).
- Extrai status via Regex (rápido e robusto).
- Persiste dados em Google Sheets (Abas Inventario e Historico).
- Comandos Slash (/status, /resumo, /lab).

## Pré-requisitos
- Python 3.11+
- Evolution API configurada
- Conta de Serviço Google (JSON) com acesso à planilha

## Instalação

1. Clone o repo.
2. Crie venv: `python -m venv venv` e ative.
3. Instale deps: `pip install -r requirements.txt`.
4. Copie `.env.example` para `.env` e preencha.
5. Defina um `WEBHOOK_TOKEN` nas suas variáveis de ambiente ou no `.env`.
   O endpoint `POST /webhook` exige esse token no header `X-CACALOG-TOKEN`. Sem isso, retornará `401 Unauthorized`.

## Execução

```bash
# Windows
./scripts/run_dev.sh
# ou
python -m uvicorn app.main:app --reload
```

## Testes

```bash
pytest
```

## Estrutura
- `app/`: Código fonte.
- `tests/`: Testes unitários.
- `app/parser.py`: Lógica principal de extração.
- `app/sheets.py`: Integração GSpread.

## Comandos do Bot
- `/status [sala]`
- `/lab [numero]`
- `/pendentes`
- `/resumo p1`
