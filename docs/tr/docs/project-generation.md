# Full Stack FastAPI Şablonu { #full-stack-fastapi-template }

Şablonlar genellikle belirli bir kurulumla gelir, ancak esnek ve özelleştirilebilir olacak şekilde tasarlanırlar. Bu sayede şablonu projenizin gereksinimlerine göre değiştirip uyarlayabilir, çok iyi bir başlangıç noktası olarak kullanabilirsiniz. 🏁

Bu şablonu başlangıç için kullanabilirsiniz; çünkü ilk kurulumun, güvenliğin, veritabanının ve bazı API endpoint'lerinin önemli bir kısmı sizin için zaten hazırlanmıştır.

GitHub Repository: [Full Stack FastAPI Şablonu](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Şablonu - Teknoloji Yığını ve Özellikler { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ Python backend API için [**FastAPI**](https://fastapi.tiangolo.com/tr).
  - 🧰 Python SQL veritabanı etkileşimleri (ORM) için [SQLModel](https://sqlmodel.tiangolo.com).
  - 🔍 FastAPI'nin kullandığı; veri doğrulama ve ayarlar yönetimi için [Pydantic](https://docs.pydantic.dev).
  - 💾 SQL veritabanı olarak [PostgreSQL](https://www.postgresql.org).
- 🚀 frontend için [React](https://react.dev).
  - 💃 TypeScript, hooks, Vite ve modern bir frontend stack'inin diğer parçalarını kullanır.
  - 🎨 frontend component'leri için [Tailwind CSS](https://tailwindcss.com) ve [shadcn/ui](https://ui.shadcn.com).
  - 🤖 Otomatik üretilen bir frontend client.
  - 🧪 End-to-End testleri için [Playwright](https://playwright.dev).
  - 🦇 Dark mode desteği.
- 🐋 Geliştirme ve production için [Docker Compose](https://www.docker.com).
- 🔒 Varsayılan olarak güvenli password hashing.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 E-posta tabanlı şifre kurtarma.
- ✅ [Pytest](https://pytest.org) ile testler.
- 📞 Reverse proxy / load balancer olarak [Traefik](https://traefik.io).
- 🚢 Docker Compose kullanarak deployment talimatları; otomatik HTTPS sertifikalarını yönetmek için bir frontend Traefik proxy'sini nasıl kuracağınız dahil.
- 🏭 GitHub Actions tabanlı CI (continuous integration) ve CD (continuous deployment).
