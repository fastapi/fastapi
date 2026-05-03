# Full Stack FastAPI Template { #full-stack-fastapi-template }

Vorlagen, die normalerweise mit einem bestimmten Setup geliefert werden, sind so konzipiert, dass sie flexibel und anpassbar sind. Dies ermöglicht es Ihnen, sie zu ändern und an die Anforderungen Ihres Projekts anzupassen und sie somit zu einem hervorragenden Ausgangspunkt zu machen. 🏁

Sie können diese Vorlage verwenden, um loszulegen, da sie bereits vieles der anfänglichen Einrichtung, Sicherheit, Datenbank und einige API-Endpunkte für Sie eingerichtet hat.

GitHub-Repository: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Template – Technologiestack und Funktionen { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/de) für die Python-Backend-API.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) für die Interaktion mit der Python-SQL-Datenbank (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), verwendet von FastAPI, für die Datenvalidierung und das Einstellungsmanagement.
  - 💾 [PostgreSQL](https://www.postgresql.org) als SQL-Datenbank.
- 🚀 [React](https://react.dev) für das Frontend.
  - 💃 Verwendung von TypeScript, Hooks, Vite und anderen Teilen eines modernen Frontend-Stacks.
  - 🎨 [Tailwind CSS](https://tailwindcss.com) und [shadcn/ui](https://ui.shadcn.com) für die Frontend-Komponenten.
  - 🤖 Ein automatisch generierter Frontend-Client.
  - 🧪 [Playwright](https://playwright.dev) für End-to-End-Tests.
  - 🦇 „Dark-Mode“-Unterstützung.
- 🐋 [Docker Compose](https://www.docker.com) für Entwicklung und Produktion.
- 🔒 Sicheres Passwort-Hashing standardmäßig.
- 🔑 JWT (JSON Web Token)-Authentifizierung.
- 📫 E-Mail-basierte Passwortwiederherstellung.
- ✅ Tests mit [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) als Reverse-Proxy / Load Balancer.
- 🚢 Deployment-Anleitungen unter Verwendung von Docker Compose, einschließlich der Einrichtung eines Frontend-Traefik-Proxys zur Handhabung automatischer HTTPS-Zertifikate.
- 🏭 CI (kontinuierliche Integration) und CD (kontinuierliches Deployment) basierend auf GitHub Actions.
