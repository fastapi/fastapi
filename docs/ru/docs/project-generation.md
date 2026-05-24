# Шаблон Full Stack FastAPI { #full-stack-fastapi-template }

Шаблоны, хотя обычно поставляются с определённой конфигурацией, спроектированы так, чтобы быть гибкими и настраиваемыми. Это позволяет вам изменять их и адаптировать под требования вашего проекта, что делает их отличной отправной точкой. 🏁

Вы можете использовать этот шаблон для старта: в нём уже сделана значительная часть начальной настройки, безопасность, база данных и несколько эндпоинтов API.

Репозиторий GitHub: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Шаблон Full Stack FastAPI — Технологический стек и возможности { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/ru) для бэкенд‑API на Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) для взаимодействия с SQL‑базой данных на Python (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), используется FastAPI, для валидации данных и управления настройками.
    - 💾 [PostgreSQL](https://www.postgresql.org) в качестве SQL‑базы данных.
- 🚀 [React](https://react.dev) для фронтенда.
    - 💃 Используются TypeScript, хуки, Vite и другие части современного фронтенд‑стека.
    - 🎨 [Tailwind CSS](https://tailwindcss.com) и [shadcn/ui](https://ui.shadcn.com) для компонентов фронтенда.
    - 🤖 Автоматически сгенерированный фронтенд‑клиент.
    - 🧪 [Playwright](https://playwright.dev) для End‑to‑End тестирования.
    - 🦇 Поддержка тёмной темы.
- 🐋 [Docker Compose](https://www.docker.com) для разработки и продакшн.
- 🔒 Безопасное хэширование паролей по умолчанию.
- 🔑 Аутентификация по JWT‑токенам.
- 📫 Восстановление пароля по электронной почте.
- ✅ Тесты с [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) в роли обратного прокси / балансировщика нагрузки.
- 🚢 Инструкции по развёртыванию с использованием Docker Compose, включая настройку фронтенд‑прокси Traefik для автоматического получения сертификатов HTTPS.
- 🏭 CI (continuous integration) и CD (continuous deployment) на основе GitHub Actions.
