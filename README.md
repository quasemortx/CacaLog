# CaçaLog MVP

Sistema de monitoramento de inventário via WhatsApp, integrado com Evolution API e Google Sheets.

## Funcionalidades
- Monitora mensagens de um grupo específico.
- Identifica Salas (Ex: S-712) e Laboratórios (Ex: L-03).
- Extrai status via Regex (rápido e robusto).
- Persiste dados em Google Sheets (Abas Inventario e Historico).
  - Inclui sistema de _retry/backoff_ automático, tolerando falhas de rede com a API da Google de maneira transparente e segura para os logs.
- Comandos Slash (/status, /resumo, /lab).
- API REST para Painéis de visualização (Read-Only) assegurada pelo header `X-API-KEY`.

## Pré-requisitos
- Python 3.11+
- PostgreSQL (rodando localmente ou em container Docker)
- Evolution API configurada

## Instalação

1. Clone o repo.
2. Crie venv: `python -m venv .venv` e ative (No Windows: `.\.venv\Scripts\activate`).
3. Instale as dependências: `pip install -r requirements.txt`.
4. Copie `.env.example` para `.env` e ajuste `DATABASE_URL` para o seu PostgreSQL local:
   `DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/cacalog`
5. Suba seu banco de dados (ex: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=sua_senha postgres`)
6. Rode as migrations do banco de dados: `alembic upgrade head`
7. Gere os dados de teste / seed: `python -m app.db.init_db`
8. Defina um `WEBHOOK_TOKEN` e `AUTHENTICATION_API_KEY` para uso.

## Execução (Dev / Prod)

### Opção 1: Variáveis de Ambiente e Uvicorn (Recomendado)
Crie seu arquivo `.env` com segurança (sem commitá-lo) definindo como os acessos funcionarão na porta desejada:
```bash
# Terminal Mode
ENV=production
LOG_LEVEL=INFO
WEBHOOK_TOKEN=seu_super_token
API_KEY=sua_senha_para_os_dashboards_da_api
CORS_ORIGINS="*"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Opção 2: Script Windows (Desenvolvimento)
```bash
./scripts/run_dev.sh
```

## Testes

```bash
pytest
```

## Estrutura
- `app/api.py`: Roteamento da API e injeção do Banco.
- `app/config.py`: Variáveis de ambiente (`DATABASE_URL`, tokens).
- `app/db/`: Conexões com banco (`engine.py`) e script seed (`init_db.py`).
- `app/models/`: Definições SQLModel de `Local`, `Maquina`, `Historico`.
- `app/schemas/`: Esquemas de resposta da API para o frontend.
- `app/services/`: Lógica de extração e resposta que abstrai o repositório de dados.
- `app/parser.py`: Lógica Regex de extração do WhatsApp.
- `db_migrations/`: Migrations gerenciadas pelo Alembic.

## Comandos do Bot
- `/status [sala]`
- `/lab [numero]`
- `/pendentes`
- `/resumo p1`
