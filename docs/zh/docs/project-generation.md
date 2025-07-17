# FastAPI全栈模板

模板通常带有特定的设置，而且被设计为灵活和可定制的。这允许您根据项目的需求修改和调整它们，使它们成为一个很好的起点。🏁

您可以使用此模板开始，因为它包含了许多已经为您完成的初始设置、安全性、数据库和一些API端点。

代码仓： <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## FastAPI全栈模板 - 技术栈和特性

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) 用于Python后端API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 用于Python和SQL数据库的集成（ORM）。
    - 🔍 [Pydantic](https://docs.pydantic.dev) FastAPI的依赖项之一，用于数据验证和配置管理。
    - 💾 [PostgreSQL](https://www.postgresql.org) 作为SQL数据库。
- 🚀 [React](https://react.dev) 用于前端。
    - 💃 使用了TypeScript、hooks、[Vite](https://vitejs.dev)和其他一些现代化的前端技术栈。
    - 🎨 [Chakra UI](https://chakra-ui.com) 用于前端组件。
    - 🤖 一个自动化生成的前端客户端。
    - 🧪 [Playwright](https://playwright.dev)用于端到端测试。
    - 🦇 支持暗黑主题（Dark mode）。
- 🐋 [Docker Compose](https://www.docker.com) 用于开发环境和生产环境。
- 🔒 默认使用密码哈希来保证安全。
- 🔑 JWT令牌用于权限验证。
- 📫 使用邮箱来进行密码恢复。
- ✅ 单元测试用了[Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) 用于反向代理和负载均衡。
- 🚢 部署指南（Docker Compose）包含了如何起一个Traefik前端代理来自动化HTTPS认证。
- 🏭 CI（持续集成）和 CD（持续部署）基于GitHub Actions。
