# Full Stack FastAPI टेम्पलेट { #full-stack-fastapi-template }

टेम्पलेट आमतौर पर एक विशिष्ट सेटअप के साथ आते हैं, लेकिन इन्हें लचीला और कस्टमाइज़ करने योग्य बनाया जाता है। इससे आप उन्हें अपने प्रोजेक्ट की आवश्यकताओं के अनुसार बदल और अनुकूलित कर सकते हैं, जिससे वे एक बेहतरीन शुरुआती बिंदु बन जाते हैं। 🏁

आप इस टेम्पलेट का उपयोग शुरुआत करने के लिए कर सकते हैं, क्योंकि इसमें शुरुआती सेटअप, सुरक्षा, डेटाबेस और कुछ API endpoints पहले से ही आपके लिए तैयार हैं।

GitHub Repository: [Full Stack FastAPI टेम्पलेट](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI टेम्पलेट - Technology Stack और Features { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ Python backend API के लिए [**FastAPI**](https://fastapi.tiangolo.com/hi)।
  - 🧰 Python SQL database interactions (ORM) के लिए [SQLModel](https://sqlmodel.tiangolo.com)।
  - 🔍 data validation और settings management के लिए [Pydantic](https://docs.pydantic.dev), जिसका उपयोग FastAPI करता है।
  - 💾 SQL database के रूप में [PostgreSQL](https://www.postgresql.org)।
- 🚀 frontend के लिए [React](https://react.dev)।
  - 💃 TypeScript, hooks, Vite, और modern frontend stack के अन्य हिस्सों का उपयोग।
  - 🎨 frontend components के लिए [Tailwind CSS](https://tailwindcss.com) और [shadcn/ui](https://ui.shadcn.com)।
  - 🤖 अपने-आप generate किया गया frontend client।
  - 🧪 End-to-End testing के लिए [Playwright](https://playwright.dev)।
  - 🦇 Dark mode support।
- 🐋 development और production के लिए [Docker Compose](https://www.docker.com)।
- 🔒 default रूप से secure password hashing।
- 🔑 JWT (JSON Web Token) authentication।
- 📫 Email based password recovery।
- ✅ [Pytest](https://pytest.org) के साथ tests।
- 📞 reverse proxy / load balancer के रूप में [Traefik](https://traefik.io)।
- 🚢 Docker Compose का उपयोग करके deployment instructions, जिसमें automatic HTTPS certificates संभालने के लिए frontend Traefik proxy सेट अप करने का तरीका शामिल है।
- 🏭 GitHub Actions पर आधारित CI (continuous integration) और CD (continuous deployment)।
