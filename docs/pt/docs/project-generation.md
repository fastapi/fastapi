# Full Stack FastAPI Template { #full-stack-fastapi-template }

_Templates_, embora tipicamente venham com alguma configuração específica, são desenhados para serem flexíveis e customizáveis. Isso permite que você os modifique e adapte para as especificações do seu projeto, fazendo-os um excelente ponto de partida. 🏁

Você pode usar esse _template_ para começar, já que ele inclui várias configurações iniciais, segurança, banco de dados, e alguns _endpoints_ de API já feitos para você.

Repositório GitHub: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Template - Pilha de Tecnologias e Recursos { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/pt) para a API do backend em Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) para as interações do Python com bancos de dados SQL (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), usado pelo FastAPI, para validação de dados e gerenciamento de configurações.
    - 💾 [PostgreSQL](https://www.postgresql.org) como banco de dados SQL.
- 🚀 [React](https://react.dev) para o frontend.
    - 💃 Usando TypeScript, hooks, Vite, e outras partes de uma _stack_ frontend moderna.
    - 🎨 [Tailwind CSS](https://tailwindcss.com) e [shadcn/ui](https://ui.shadcn.com) para os componentes de frontend.
    - 🤖 Um cliente frontend automaticamente gerado.
    - 🧪 [Playwright](https://playwright.dev) para testes Ponta-a-Ponta.
    - 🦇 Suporte para modo escuro.
- 🐋 [Docker Compose](https://www.docker.com) para desenvolvimento e produção.
- 🔒 Hash seguro de senhas por padrão.
- 🔑 Autenticação JWT (JSON Web Token).
- 📫 Recuperação de senhas baseada em email.
- ✅ Testes com [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) como proxy reverso / balanceador de carga.
- 🚢 Instruções de deployment usando Docker Compose, incluindo como configurar um proxy frontend com Traefik para gerenciar automaticamente certificados HTTPS.
- 🏭 CI (Integração Contínua) e CD (_Deploy_ Contínuo) baseado em GitHub Actions.
