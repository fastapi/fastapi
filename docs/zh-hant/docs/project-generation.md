# 全端 FastAPI 範本 { #full-stack-fastapi-template }

範本通常附帶特定的設定，但設計上具有彈性且可自訂。這讓你可以依專案需求調整與擴充，因此非常適合作為起點。🏁

你可以使用此範本快速起步，裡面已替你完成大量初始設定、安全性、資料庫，以及部分 API 端點。

GitHub 儲存庫：<a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">全端 FastAPI 範本</a>

## 全端 FastAPI 範本 - 技術堆疊與功能 { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/zh-hant) 作為 Python 後端 API。
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) 作為 Python 與 SQL 資料庫互動（ORM）。
  - 🔍 [Pydantic](https://docs.pydantic.dev)（由 FastAPI 使用）用於資料驗證與設定管理。
  - 💾 [PostgreSQL](https://www.postgresql.org) 作為 SQL 資料庫。
- 🚀 [React](https://react.dev) 作為前端。
  - 💃 使用 TypeScript、hooks、Vite，以及現代前端技術堆疊的其他組件。
  - 🎨 [Tailwind CSS](https://tailwindcss.com) 與 [shadcn/ui](https://ui.shadcn.com) 作為前端元件。
  - 🤖 自動產生的前端用戶端。
  - 🧪 [Playwright](https://playwright.dev) 用於端到端測試。
  - 🦇 支援深色模式。
- 🐋 [Docker Compose](https://www.docker.com) 用於開發與正式環境。
- 🔒 預設即採用安全的密碼雜湊。
- 🔑 JWT（JSON Web Token）驗證。
- 📫 以 Email 為基礎的密碼重設。
- ✅ 使用 [Pytest](https://pytest.org) 的測試。
- 📞 [Traefik](https://traefik.io) 作為反向代理／負載平衡器。
- 🚢 使用 Docker Compose 的部署指引，包含如何設定前端 Traefik 代理以自動處理 HTTPS 憑證。
- 🏭 基於 GitHub Actions 的 CI（持續整合）與 CD（持續部署）。
