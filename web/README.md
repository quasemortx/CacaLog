# CaçaLog Web Panel (MVP)

Este é o **frontend oficial de gerenciamento** do CaçaLog, construído sobre um stack moderno e altamente escalável contendo _Vite, React, TypeScript, Tailwind CSS e Shadcn/UI_.

O propósito do *Web Panel* está em apresentar os dados do Inventário e o Histórico de atividades do Robô num dashboard fluido para os gerentes que desejam inspecionar os logs do seu inventário de forma visual e analítica fora do WhatsApp.

## Funcionalidades (PR1 - MVP Frontend Placeholder)
- Estrutura completa de Layout Web com React Router.
- AppShell Base (Sidebar e PageHeaders responsivos) utilizando Shadcn/UI conventions.
- Placeholders do **Dashboard**, **Inventário** e **Histórico**, prontas para a integração com a `/api` passiva do backend.
- Dark mode preparado globalmente no CSS Root.

---

## 🚀 Como Rodar Localmente

Certifique-se de ter o NodeJS instalado na sua máquina. A partir do diretório `/web` do projeto CaçaLog:

1. **Configurar as Variáveis de Ambiente:**
   Copie o arquivo amigável:
   ```bash
   cp .env.example .env
   ```
   > Certifique-se de preencher `VITE_API_KEY` com o valor de `API_KEY` rodando no seu servidor Backend.

2. **Instale as dependências:**
   ```bash
   npm install
   ```

3. **Suba o Servidor de Desenvolvimento:**
   ```bash
   npm run dev
   ```

   > **NOTA:** O painel consumirá a porta 8000. Para que as telas funcionem e não exibam `ErrorState`, o backend FastAPI (`uvicorn app.main:...`) deve estar estar simultâneamente sendo executado!

O painel ficará disponível interativamente, geralmente em `http://localhost:5173`. 

> O projeto foi validado garantindo TypeScript rigoroso e Tailwind formatado. A próxima PR unirá os endpoints à tabela!
