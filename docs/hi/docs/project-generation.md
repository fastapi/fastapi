# Full Stack FastAPI Template { #full-stack-fastapi-template }

Templates आम तौर पर एक विशिष्ट setup के साथ आते हैं, लेकिन उन्हें flexible और customizable होने के लिए डिज़ाइन किया जाता है। इससे आप उन्हें अपने project की आवश्यकताओं के अनुसार modify और adapt कर सकते हैं, जिससे वे एक बेहतरीन starting point बन जाते हैं। 🏁

आप शुरू करने के लिए इस template का उपयोग कर सकते हैं, क्योंकि इसमें आपके लिए बहुत सा initial setup, security, database और कुछ API endpoints पहले से तैयार हैं।

GitHub Repository: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Template - Technology Stack और Features { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ Python backend API के लिए [**FastAPI**](https://fastapi.tiangolo.com/hi)।
  - 🧰 Python SQL database interactions (ORM) के लिए [SQLModel](https://sqlmodel.tiangolo.com)।
  - 🔍 data validation और settings management के लिए [Pydantic](https://docs.pydantic.dev), जिसका उपयोग FastAPI करता है।
  - 💾 SQL database के रूप में [PostgreSQL](https://www.postgresql.org)।
- 🚀 frontend के लिए [React](https://react.dev)।
  - 💃 TypeScript, hooks, Vite, और modern frontend stack के अन्य parts का उपयोग।
  - 🎨 frontend components के लिए [Tailwind CSS](https://tailwindcss.com) और [shadcn/ui](https://ui.shadcn.com)।
  - 🤖 एक automatically generated frontend client।
  - 🧪 End-to-End testing के लिए [Playwright](https://playwright.dev)।
  - 🦇 Dark mode support।
- 🐋 development और production के लिए [Docker Compose](https://www.docker.com)।
- 🔒 default रूप से secure password hashing।
- 🔑 JWT (JSON Web Token) authentication।
- 📫 Email आधारित password recovery।
- ✅ [Pytest](https://pytest.org) के साथ tests।
- 📞 reverse proxy / load balancer के रूप में [Traefik](https://traefik.io)।
- 🚢 Docker Compose का उपयोग करके deployment instructions, जिसमें automatic HTTPS certificates handle करने के लिए frontend Traefik proxy setup करना शामिल है।
- 🏭 GitHub Actions पर आधारित CI (continuous integration) और CD (continuous deployment)।
