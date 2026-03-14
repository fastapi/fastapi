# Full Stack FastAPI Template { #full-stack-fastapi-template }

Templates عام طور پر ایک مخصوص setup کے ساتھ آتے ہیں، لیکن یہ لچکدار اور حسب ضرورت بنانے کے قابل ہونے کے لیے ڈیزائن کیے گئے ہیں۔ اس سے آپ انہیں اپنے project کی ضروریات کے مطابق تبدیل اور ڈھال سکتے ہیں، جو انہیں ایک بہترین نقطہ آغاز بناتا ہے۔ 🏁

آپ شروع کرنے کے لیے یہ template استعمال کر سکتے ہیں، کیونکہ اس میں ابتدائی setup، security، database اور کچھ API endpoints پہلے سے آپ کے لیے بنے ہوئے ہیں۔

GitHub Repository: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Template - Technology Stack اور Features { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) Python backend API کے لیے۔
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) Python SQL database interactions (ORM) کے لیے۔
  - 🔍 [Pydantic](https://docs.pydantic.dev)، FastAPI کے ذریعے استعمال شدہ، data validation اور settings management کے لیے۔
  - 💾 [PostgreSQL](https://www.postgresql.org) بطور SQL database۔
- 🚀 [React](https://react.dev) frontend کے لیے۔
  - 💃 TypeScript، hooks، Vite، اور جدید frontend stack کے دوسرے حصے استعمال کرتے ہوئے۔
  - 🎨 [Tailwind CSS](https://tailwindcss.com) اور [shadcn/ui](https://ui.shadcn.com) frontend components کے لیے۔
  - 🤖 خودکار طور پر generate شدہ frontend client۔
  - 🧪 [Playwright](https://playwright.dev) End-to-End testing کے لیے۔
  - 🦇 Dark mode support۔
- 🐋 [Docker Compose](https://www.docker.com) development اور production کے لیے۔
- 🔒 بطور default محفوظ password hashing۔
- 🔑 JWT (JSON Web Token) authentication۔
- 📫 Email پر مبنی password recovery۔
- ✅ [Pytest](https://pytest.org) کے ساتھ Tests۔
- 📞 [Traefik](https://traefik.io) بطور reverse proxy / load balancer۔
- 🚢 Docker Compose استعمال کرتے ہوئے deployment ہدایات، بشمول خودکار HTTPS certificates سنبھالنے کے لیے frontend Traefik proxy سیٹ اپ کرنے کا طریقہ۔
- 🏭 GitHub Actions پر مبنی CI (continuous integration) اور CD (continuous deployment)۔
