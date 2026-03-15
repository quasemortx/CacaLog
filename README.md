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
   `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cacalog`
5. Suba seu conteiner com banco de dados criado (usando POSTGRES_DB=cacalog):
   `docker run -d --name cacalog-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=cacalog postgres:15-alpine`
6. Rode as migrations do banco de dados: `alembic upgrade head`
7. Gere os dados de teste / seed: `python -m app.db.init_db`
8. Suba o servidor backend: `uvicorn app.main:app --reload`
9. (Opcional) Defina um `WEBHOOK_TOKEN` e `AUTHENTICATION_API_KEY` para uso em chamadas externas.

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
- `app/api.py`: Roteamento da API (agora com CRUD completo de locais/máquinas).
- `app/config.py`: Variáveis de ambiente (`DATABASE_URL`, tokens).
- `app/db/`: Conexões com banco (`engine.py`) e script seed (`init_db.py`).
- `app/models/`: Definições SQLModel de `Local`, `Maquina`, `Historico`.
- `app/repositories/`: Camada de acesso a dados.
- `app/schemas/`: Esquemas de resposta da API e validação Pydantic.
- `app/services/`: Lógica de negócio e coordenação de histórico.
- `app/parser.py`: Lógica Regex de extração do WhatsApp.
- `db_migrations/`: Migrations gerenciadas pelo Alembic.

## API CRUD (Painel Administrativo)

### Locais
- `POST /api/locais`: Cria novo local.
- `GET /api/locais/{local_id}`: Retorna dados do local e suas máquinas.
- `PUT /api/locais/{local_id}`: Atualiza campos do local.

Exemplo Payload (POST /api/locais):
```json
{
  "local_id": "L-05",
  "tipo_local": "LAB",
  "predio": 1,
  "status": "OK"
}
```

### Máquinas
- `POST /api/locais/{local_id}/maquinas`: Adiciona modelo de máquina ao local.
- `PUT /api/maquinas/{maquina_id}`: Atualiza dados da máquina.
- `DELETE /api/maquinas/{maquina_id}`: Remove a máquina.

Exemplo Payload (POST /api/locais/L-05/maquinas):
```json
{
  "modelo": "Dell Optiplex 3040",
  "quantidade": 20,
  "propriedade": "PROPRIO"
}
```


## Comandos do Bot
- `/status [sala]`
- `/lab [numero]`
- `/pendentes`
- `/resumo p1`
