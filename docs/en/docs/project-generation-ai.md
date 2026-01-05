# Full Stack FastAPI + Next.js Template for AI/LLM Applications

A production-ready project generator specifically designed for AI and LLM applications. It provides everything you need to build professional AI-powered products with 20+ enterprise integrations.

This template is ideal for building AI chatbots, ML applications, enterprise SaaS, or any project that needs type-safe AI agents with real-time streaming responses.

GitHub Repository: <a href="https://github.com/vstorm-co/full-stack-fastapi-nextjs-llm-template" class="external-link" target="_blank">Full Stack FastAPI + Next.js LLM Template</a>

## Why This Template

Building AI/LLM applications requires more than just an API wrapper. You need:

- **Type-safe AI agents** with tool/function calling
- **Real-time streaming** responses via WebSocket
- **Conversation persistence** and history management
- **Production infrastructure** - auth, rate limiting, observability
- **Enterprise integrations** - background tasks, webhooks, admin panels

This template gives you all of that out of the box, with **20+ configurable integrations** so you can focus on building your AI product, not boilerplate.

### Perfect For

- 🤖 **AI Chatbots & Assistants** - PydanticAI or LangChain agents with streaming responses
- 📊 **ML Applications** - Background task processing with Celery/Taskiq
- 🏢 **Enterprise SaaS** - Full auth, admin panel, webhooks, and more
- 🚀 **Startups** - Ship fast with production-ready infrastructure

### AI-Agent Friendly

Generated projects include **CLAUDE.md** and **AGENTS.md** files optimized for AI coding assistants (Claude Code, Codex, Copilot, Cursor, Zed). Following progressive disclosure best practices - concise project overview with pointers to detailed docs when needed.

## Technology Stack and Features

- **AI/LLM First**
    - 🤖 <a href="https://ai.pydantic.dev" class="external-link" target="_blank">**PydanticAI**</a> or <a href="https://python.langchain.com" class="external-link" target="_blank">**LangChain**</a> with <a href="https://langchain-ai.github.io/langgraph/" class="external-link" target="_blank">**LangGraph**</a> - Choose your preferred AI framework.
    - 🌊 **WebSocket Streaming** - Real-time responses with full event access.
    - 💬 **Conversation Persistence** - Save chat history to database.
    - 🔧 **Custom Tools** - Easily extend agent capabilities.
    - 🔌 **Multi-provider Support** - OpenAI, Anthropic, OpenRouter.
    - 📊 **Observability** - Logfire for PydanticAI, LangSmith for LangChain.
- ⚡ <a href="https://fastapi.tiangolo.com" class="external-link" target="_blank">**FastAPI**</a> for the Python backend API.
    - 🔍 <a href="https://docs.pydantic.dev" class="external-link" target="_blank">**Pydantic v2**</a> for data validation and settings management.
    - 🧰 <a href="https://sqlmodel.tiangolo.com" class="external-link" target="_blank">**SQLModel**</a> or **SQLAlchemy** for Python SQL database interactions (ORM).
    - 💾 **Multiple Databases** - PostgreSQL (async), MongoDB (async), SQLite.
    - 🔑 **Authentication** - JWT + Refresh tokens, API Keys, OAuth2 (Google).
    - ⏱️ **Background Tasks** - Celery, Taskiq, or ARQ.
    - 🛠️ **Django-style CLI** - Custom management commands with auto-discovery.
- 🚀 <a href="https://nextjs.org" class="external-link" target="_blank">**Next.js 15**</a> for the frontend.
    - 💻 **React 19** + **TypeScript** + **Tailwind CSS v4**.
    - 💭 **AI Chat Interface** - WebSocket streaming, tool call visualization.
    - 🔐 **Authentication** - HTTP-only cookies, auto-refresh.
    - 🗄️ <a href="https://zustand-demo.pmnd.rs/" class="external-link" target="_blank">**Zustand**</a> for state management.
    - 🧪 <a href="https://playwright.dev" class="external-link" target="_blank">**Playwright**</a> for End-to-End testing.
    - 🌙 **Dark Mode** + **i18n** (optional).
- 🏢 **Enterprise Integrations**
    - 📦 **Caching & State** - Redis, fastapi-cache2.
    - 🛡️ **Security** - Rate limiting, CORS, CSRF protection.
    - 📈 **Observability** - Logfire, LangSmith, Sentry, Prometheus.
    - 🖥️ **Admin** - SQLAdmin panel with auth.
    - 📡 **Events** - Webhooks, WebSockets.
    - 🐳 **DevOps** - Docker, GitHub Actions, GitLab CI, Kubernetes.

## Quick Start

### Installation

```bash
# pip
pip install fastapi-fullstack

# uv (recommended)
uv tool install fastapi-fullstack

# pipx
pipx install fastapi-fullstack
```

### Create Your Project

```bash
# Interactive wizard (recommended)
fastapi-fullstack new

# Quick mode with options
fastapi-fullstack create my_ai_app \
  --database postgresql \
  --auth jwt \
  --frontend nextjs

# Use presets for common setups
fastapi-fullstack create my_ai_app --preset production   # Full production setup
fastapi-fullstack create my_ai_app --preset ai-agent     # AI agent with streaming

# Minimal project (no extras)
fastapi-fullstack create my_ai_app --minimal
```

### Start Development

```bash
cd my_ai_app
make install        # Install dependencies
make docker-db      # Start PostgreSQL
make db-migrate     # Create migration
make db-upgrade     # Apply migrations
make create-admin   # Create admin user
make run            # Start backend

# In another terminal
cd frontend
bun install
bun dev
```

Access points:

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:8000/admin
- Frontend: http://localhost:3000

### Quick Start with Docker

```bash
make docker-up       # Start backend + database
make docker-frontend # Start frontend
```

## Architecture

The backend follows a clean **Repository + Service** pattern:

| Layer | Responsibility |
|-------|---------------|
| **Routes** | HTTP handling, validation, auth |
| **Services** | Business logic, orchestration |
| **Repositories** | Data access, queries |

## AI Agent

Choose between **PydanticAI** or **LangChain** when generating your project:

```bash
# PydanticAI with OpenAI (default)
fastapi-fullstack create my_app --ai-agent --ai-framework pydantic_ai

# PydanticAI with Anthropic
fastapi-fullstack create my_app --ai-agent --ai-framework pydantic_ai --llm-provider anthropic

# LangChain with OpenAI
fastapi-fullstack create my_app --ai-agent --ai-framework langchain
```

### Supported LLM Providers

| Framework | OpenAI | Anthropic | OpenRouter |
|-----------|:------:|:---------:|:----------:|
| **PydanticAI** | ✓ | ✓ | ✓ |
| **LangChain** | ✓ | ✓ | - |

### PydanticAI Example

Type-safe agents with full dependency injection:

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class Deps:
    user_id: str | None = None
    db: AsyncSession | None = None

agent = Agent[Deps, str](
    model="openai:gpt-4o-mini",
    system_prompt="You are a helpful assistant.",
)

@agent.tool
async def search_database(ctx: RunContext[Deps], query: str) -> list[dict]:
    """Search the database for relevant information."""
    # Access user context and database via ctx.deps
    ...
```

### LangChain with LangGraph Example

Flexible agents with LangGraph:

```python
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def search_database(query: str) -> list[dict]:
    """Search the database for relevant information."""
    ...

agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o-mini"),
    tools=[search_database],
    prompt="You are a helpful assistant.",
)
```

## Django-style CLI

Each generated project includes a CLI with built-in commands:

```bash
# Server
my_app server run --reload
my_app server routes

# Database (Alembic wrapper)
my_app db init
my_app db migrate -m "Add users"
my_app db upgrade

# Users
my_app user create --email admin@example.com --superuser
my_app user list
```

Custom commands are **automatically discovered** from `app/commands/`.

## Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| **Database** | `postgresql`, `mongodb`, `sqlite`, `none` | Async by default |
| **ORM** | `sqlalchemy`, `sqlmodel` | SQLModel for simplified syntax |
| **Auth** | `jwt`, `api_key`, `both`, `none` | JWT includes user management |
| **OAuth** | `none`, `google` | Social login |
| **AI Framework** | `pydantic_ai`, `langchain` | Choose your AI agent framework |
| **LLM Provider** | `openai`, `anthropic`, `openrouter` | OpenRouter only with PydanticAI |
| **Background Tasks** | `none`, `celery`, `taskiq`, `arq` | Distributed queues |
| **Frontend** | `none`, `nextjs` | Next.js 15 + React 19 |

### Presets

| Preset | Description |
|--------|-------------|
| `--preset production` | Full production setup with Redis, Sentry, Kubernetes, Prometheus |
| `--preset ai-agent` | AI agent with WebSocket streaming and conversation persistence |
| `--minimal` | Minimal project with no extras |

## Documentation

For detailed documentation, see the <a href="https://github.com/vstorm-co/full-stack-fastapi-nextjs-llm-template" class="external-link" target="_blank">GitHub repository</a>.

---

Created by <a href="https://github.com/vstorm-co" class="external-link" target="_blank">Vstorm</a>.
