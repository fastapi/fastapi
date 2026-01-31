# Full Stack FastAPI Template { #full-stack-fastapi-template }

模板虽然通常带有特定的设置，但其设计目标是灵活且可定制的。这使你可以根据项目需求对它们进行修改和调整，让它们成为一个极好的起点。🏁

你可以使用此模板开始，因为它包含了许多已经为你完成的初始设置、安全性、数据库和一些 API 端点。

GitHub 代码仓： <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## Full Stack FastAPI Template - 技术栈和特性 { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/zh) 用于 Python 后端 API。
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 用于 Python 与 SQL 数据库交互（ORM）。
  - 🔍 [Pydantic](https://docs.pydantic.dev)，被 FastAPI 使用，用于数据验证和配置管理。
  - 💾 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- 🚀 [React](https://react.dev) 用于前端。
  - 💃 使用 TypeScript、hooks、Vite，以及现代前端技术栈的其他部分。
  - 🎨 [Tailwind CSS](https://tailwindcss.com) 和 [shadcn/ui](https://ui.shadcn.com) 用于前端组件。
  - 🤖 自动生成的前端客户端。
  - 🧪 [Playwright](https://playwright.dev) 用于端到端测试。
  - 🦇 支持暗黑主题（Dark mode）。
- 🐋 [Docker Compose](https://www.docker.com) 用于开发环境和生产环境。
- 🔒 默认使用安全的密码哈希。
- 🔑 JWT（JSON Web Token）认证。
- 📫 基于邮箱的密码恢复。
- ✅ 使用 [Pytest](https://pytest.org) 进行测试。
- 📞 [Traefik](https://traefik.io) 作为反向代理 / 负载均衡器。
- 🚢 使用 Docker Compose 的部署说明，包括如何设置一个前端 Traefik 代理来处理自动 HTTPS 证书。
- 🏭 基于 GitHub Actions 的 CI（持续集成）和 CD（持续部署）。
