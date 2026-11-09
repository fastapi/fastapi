# Full Stack FastAPI Template { #full-stack-fastapi-template }

Templates সাধারণত একটি নির্দিষ্ট setup-সহ আসলেও, flexible আর customizable হওয়ার জন্যই design করা। এতে আপনার project-এর দরকার অনুযায়ী এগুলো বদলে নিতে পারেন, তাই শুরু করার জন্য এগুলো দারুণ। 🏁

শুরু করার জন্য এই template ব্যবহার করতে পারেন, কারণ এতে শুরুর অনেক setup, security, database আর কিছু API endpoints আগে থেকেই করা আছে।

GitHub Repository: [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)

## Full Stack FastAPI Template - Technology Stack আর Features { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ Python backend API-এর জন্য [**FastAPI**](https://fastapi.tiangolo.com/bn)।
  - 🧰 Python SQL database interactions (ORM)-এর জন্য [SQLModel](https://sqlmodel.tiangolo.com)।
  - 🔍 data validation আর settings management-এর জন্য [Pydantic](https://pydantic.dev/docs/), যেটা FastAPI ব্যবহার করে।
  - 💾 SQL database হিসেবে [PostgreSQL](https://www.postgresql.org)।
- 🚀 frontend-এর জন্য [React](https://react.dev)।
  - 💃 TypeScript, hooks, Vite আর একটি আধুনিক frontend stack-এর অন্যান্য অংশ ব্যবহার করে।
  - 🎨 frontend components-এর জন্য [Tailwind CSS](https://tailwindcss.com) আর [shadcn/ui](https://ui.shadcn.com)।
  - 🤖 নিজে থেকে generate হওয়া একটি frontend client।
  - 🧪 End-to-End testing-এর জন্য [Playwright](https://playwright.dev)।
  - 🦇 Dark mode support।
- 🐋 development আর production-এর জন্য [Docker Compose](https://www.docker.com)।
- 🔒 default-ভাবেই secure password hashing।
- 🔑 JWT (JSON Web Token) authentication।
- 📫 Email-ভিত্তিক password recovery।
- ✅ [Pytest](https://pytest.org) দিয়ে tests।
- 📞 reverse proxy / load balancer হিসেবে [Traefik](https://traefik.io)।
- 🚢 Docker Compose দিয়ে deployment instructions, automatic HTTPS certificates handle করার জন্য একটি frontend Traefik proxy কীভাবে set up করতে হয়, সেটা সহ।
- 🏭 GitHub Actions-ভিত্তিক CI (continuous integration) আর CD (continuous deployment)।
