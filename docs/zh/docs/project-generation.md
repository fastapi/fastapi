# FastAPI全栈模板 { #full-stack-fastapi-template }

模板通常带有特定的设置，但它们被设计为灵活且可定制。这样你可以根据项目需求进行修改和调整，使其成为很好的起点。🏁

你可以使用此模板开始，它已经为你完成了大量的初始设置、安全性、数据库以及一些 API 端点。

GitHub 仓库： <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## FastAPI全栈模板 - 技术栈和特性 { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/zh) 用于 Python 后端 API。
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 用于 Python 与 SQL 数据库的交互（ORM）。
  - 🔍 [Pydantic](https://docs.pydantic.dev)，FastAPI 使用，用于数据验证与配置管理。
  - 💾 [PostgreSQL](https://www.postgresql.org) 作为 SQL 数据库。
- 🚀 [React](https://react.dev) 用于前端。
  - 💃 使用 TypeScript、hooks、Vite 以及现代前端技术栈的其他部分。
  - 🎨 [Tailwind CSS](https://tailwindcss.com) 与 [shadcn/ui](https://ui.shadcn.com) 用于前端组件。
  - 🤖 自动生成的前端客户端。
  - 🧪 [Playwright](https://playwright.dev) 用于端到端测试。
  - 🦇 支持暗黑模式。
- 🐋 [Docker Compose](https://www.docker.com) 用于开发与生产。
- 🔒 默认启用安全的密码哈希。
- 🔑 JWT（JSON Web Token）认证。
- 📫 基于邮箱的密码找回。
- ✅ 使用 [Pytest](https://pytest.org) 进行测试。
- 📞 [Traefik](https://traefik.io) 用作反向代理/负载均衡。
- 🚢 使用 Docker Compose 的部署指南，包括如何设置前端 Traefik 代理以自动处理 HTTPS 证书。
- 🏭 基于 GitHub Actions 的 CI（持续集成）与 CD（持续部署）。
