# Full Stack FastAPI Template { #full-stack-fastapi-template }

_Templates_, embora tipicamente venham com alguma configuração específica, são desenhados para serem flexíveis e customizáveis. Isso permite que você os modifique e adapte para as especificações do seu projeto, fazendo-os um excelente ponto de partida. 🏁

Você pode usar esse _template_ para começar, já que ele inclui várias configurações iniciais, segurança, banco de dados, e alguns _endpoints_ de API já feitos para você.

Repositório GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## Full Stack FastAPI Template - Pilha de Tecnologias e Recursos { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/pt) para a API do backend em Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) para as interações do Python com bancos de dados SQL (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), usado pelo FastAPI, para validação de dados e gerenciamento de configurações.
    - 💾 [PostgreSQL](https://www.postgresql.org) como banco de dados SQL.
- 🚀 [React](https://react.dev) para o frontend.
    - 💃 Usando TypeScript, hooks, [Vite](https://vitejs.dev), e outras partes de uma _stack_ frontend moderna.
    - 🎨 [Chakra UI](https://chakra-ui.com) para os componentes de frontend.
    - 🤖 Um cliente frontend automaticamente gerado.
    - 🧪 [Playwright](https://playwright.dev) para testes Ponta-a-Ponta.
    - 🦇 Suporte para modo escuro.
- 🐋 [Docker Compose](https://www.docker.com) para desenvolvimento e produção.
- 🔒 _Hash_ seguro de senhas por padrão.
- 🔑 Autenticação por token JWT.
- 📫 Recuperação de senhas baseada em email.
- ✅ Testes com [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) como proxy reverso / balanceador de carga.
- 🚢 Instruções de _deployment_ usando Docker Compose, incluindo como configurar um proxy frontend com Traefik para gerenciar automaticamente certificados HTTPS.
- 🏭 CI (Integração Contínua) e CD (_Deploy_ Contínuo) baseado em GitHub Actions.
