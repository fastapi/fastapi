# Modèle Full Stack FastAPI { #full-stack-fastapi-template }

Les modèles, bien qu'ils soient généralement livrés avec une configuration spécifique, sont conçus pour être flexibles et personnalisables. Cela vous permet de les modifier et de les adapter aux exigences de votre projet, ce qui en fait un excellent point de départ. 🏁

Vous pouvez utiliser ce modèle pour démarrer, car il inclut une grande partie de la configuration initiale, la sécurité, la base de données et quelques endpoints d'API déjà prêts pour vous.

Dépôt GitHub : <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Modèle Full Stack FastAPI</a>

## Modèle Full Stack FastAPI - Pile technologique et fonctionnalités { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/fr) pour l'API backend Python.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) pour les interactions avec la base de données SQL en Python (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), utilisé par FastAPI, pour la validation des données et la gestion des paramètres.
  - 💾 [PostgreSQL](https://www.postgresql.org) comme base de données SQL.
- 🚀 [React](https://react.dev) pour le frontend.
  - 💃 Utilisation de TypeScript, des hooks, de Vite et d'autres éléments d'un stack frontend moderne.
  - 🎨 [Tailwind CSS](https://tailwindcss.com) et [shadcn/ui](https://ui.shadcn.com) pour les composants frontend.
  - 🤖 Un client frontend généré automatiquement.
  - 🧪 [Playwright](https://playwright.dev) pour les tests de bout en bout.
  - 🦇 Prise en charge du mode sombre.
- 🐋 [Docker Compose](https://www.docker.com) pour le développement et la production.
- 🔒 Hachage sécurisé des mots de passe par défaut.
- 🔑 Authentification JWT (JSON Web Token).
- 📫 Récupération de mot de passe par e-mail.
- ✅ Tests avec [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) comme proxy inverse / répartiteur de charge.
- 🚢 Instructions de déploiement avec Docker Compose, y compris la configuration d'un proxy Traefik frontal pour gérer les certificats HTTPS automatiques.
- 🏭 CI (intégration continue) et CD (déploiement continu) basés sur GitHub Actions.
