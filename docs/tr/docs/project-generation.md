# Full Stack FastAPI Şablonu { #full-stack-fastapi-template }

Şablonlar genellikle belirli bir kurulumla gelir; ancak esnek ve özelleştirilebilir olacak şekilde tasarlanır. Bu, onları projenizin gereksinimlerine göre değiştirip uyarlamanıza olanak tanır ve onları mükemmel bir başlangıç noktası yapar. 🏁

Bu şablonu başlangıç için kullanabilirsiniz; çünkü ilk kurulumun büyük bir kısmını, güvenliği, veritabanını ve bazı API endpoint'lerini sizin için zaten hazır halde içerir.

GitHub Repository: <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## Full Stack FastAPI Şablonu - Teknoloji Stack'i ve Özellikler { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ Python backend API için [**FastAPI**](https://fastapi.tiangolo.com/tr).
  - 🧰 Python SQL veritabanı etkileşimleri (ORM) için [SQLModel](https://sqlmodel.tiangolo.com).
  - 🔍 FastAPI tarafından kullanılan, veri doğrulama ve ayar yönetimi için [Pydantic](https://docs.pydantic.dev).
  - 💾 SQL veritabanı olarak [PostgreSQL](https://www.postgresql.org).
- 🚀 frontend için [React](https://react.dev).
  - 💃 TypeScript, hooks, Vite ve modern bir frontend stack'inin diğer parçaları kullanılır.
  - 🎨 frontend bileşenleri için [Tailwind CSS](https://tailwindcss.com) ve [shadcn/ui](https://ui.shadcn.com).
  - 🤖 Otomatik oluşturulan bir frontend client.
  - 🧪 End-to-End test için [Playwright](https://playwright.dev).
  - 🦇 Dark mode desteği.
- 🐋 geliştirme ve production için [Docker Compose](https://www.docker.com).
- 🔒 Varsayılan olarak güvenli parola hashing.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email tabanlı parola kurtarma.
- ✅ [Pytest](https://pytest.org) ile testler.
- 📞 reverse proxy / load balancer olarak [Traefik](https://traefik.io).
- 🚢 Docker Compose kullanarak deployment talimatları; otomatik HTTPS sertifikalarını yönetmek için bir frontend Traefik proxy'sinin nasıl kurulacağı dahil.
- 🏭 GitHub Actions tabanlı CI (continuous integration) ve CD (continuous deployment).
