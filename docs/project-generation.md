There is a project generator that you can use to get started, with a lot of the initial set up, security, database and first API endpoints already done for you.

## Full-Stack-FastAPI-Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

### Features

* Full **Docker** integration (Docker based).
* Docker Swarm Mode deployment.
* **Docker Compose** integration and optimization for local development.
* **Production ready** Python web server using Uvicorn and Gunicorn.
* Python **FastAPI** backend with all its features.
* **Celery** worker that can import and use code from the rest of the backend selectively (you don't have to install the complete app in each worker).
* **NoSQL Couchbase** database that supports direct synchronization via Couchbase Sync Gateway for offline-first applications.
* **Full Text Search** integrated, using Couchbase.
* REST backend tests based on Pytest, integrated with Docker, so you can test the full API interaction, independent on the database. As it runs in Docker, it can build a new data store from scratch each time (so you can use ElasticSearch, MongoDB, or whatever you want, and just test that the API works).
* Easy Python integration with **Jupyter** Kernels for remote or in-Docker development with extensions like Atom Hydrogen or Visual Studio Code Jupyter.
* **Email notifications** for account creation and password recovery, compatible with:
    * Mailgun
    * SparkPost
    * SendGrid
    * ...any other provider that can generate standard SMTP credentials.
* **Vue** frontend:
    * Generated with Vue CLI.
    * **JWT Authentication** handling.
    * Login view.
    * After login, main dashboard view.
    * Main dashboard with user creation and edition.
    * Self user edition.
    * **Vuex**.
    * **Vue-router**.
    * **Vuetify** for beautiful material design components.
    * **TypeScript**.
    * Docker server based on **Nginx** (configured to play nicely with Vue-router).
    * Docker multi-stage building, so you don't need to save or commit compiled code.
    * Frontend tests ran at build time (can be disabled too).
    * Made as modular as possible, so it works out of the box, but you can re-generate with Vue CLI or create it as you need, and re-use what you want.
* Flower for Celery jobs monitoring.
* Load balancing between frontend and backend with **Traefik**, so you can have both under the same domain, separated by path, but served by different containers.
* Traefik integration, including Let's Encrypt **HTTPS** certificates automatic generation.
* GitLab **CI** (continuous integration), including frontend and backend testing.
