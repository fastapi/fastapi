# Шаблон Full Stack FastAPI { #full-stack-fastapi-template }

Шаблони, хоча зазвичай постачаються з певним налаштуванням, спроєктовані бути гнучкими та налаштовуваними. Це дає змогу змінювати їх і адаптувати до вимог вашого проєкту, що робить їх чудовою відправною точкою. 🏁

Ви можете використати цей шаблон для старту, адже в ньому вже виконано значну частину початкового налаштування, безпеки, роботи з базою даних і деяких кінцевих точок API.

Репозиторій GitHub: [Шаблон Full Stack FastAPI](https://github.com/tiangolo/full-stack-fastapi-template)

## Шаблон Full Stack FastAPI - стек технологій і можливості { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/uk) для бекенд API на Python.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) для взаємодії з SQL-базою даних у Python (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), який використовується FastAPI, для перевірки даних і керування налаштуваннями.
  - 💾 [PostgreSQL](https://www.postgresql.org) як SQL-база даних.
- 🚀 [React](https://react.dev) для фронтенду.
  - 💃 Використання TypeScript, хуків, Vite та інших частин сучасного фронтенд-стеку.
  - 🎨 [Tailwind CSS](https://tailwindcss.com) і [shadcn/ui](https://ui.shadcn.com) для фронтенд-компонентів.
  - 🤖 Автоматично згенерований фронтенд-клієнт.
  - 🧪 [Playwright](https://playwright.dev) для End-to-End тестування.
  - 🦇 Підтримка темного режиму.
- 🐋 [Docker Compose](https://www.docker.com) для розробки та продакшену.
- 🔒 Безпечне хешування паролів за замовчуванням.
- 🔑 Автентифікація JWT (JSON Web Token).
- 📫 Відновлення пароля на основі електронної пошти.
- ✅ Тести з [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) як зворотний представник / балансувальник навантаження.
- 🚢 Інструкції з розгортання з Docker Compose, включно з налаштуванням фронтенд-представника Traefik для автоматичних HTTPS-сертифікатів.
- 🏭 CI (безперервна інтеграція) і CD (безперервне розгортання) на базі GitHub Actions.
