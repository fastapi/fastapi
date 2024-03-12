<p align="center">
<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/full-stack-fastapi-postgresql/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/full-stack-fastapi-postgresql" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/full-stack-fastapi-postgresql.svg" alt="Coverage">
</p>

# FastAPI Project Template

## 🚨 Warning: in (re) construction 😎 🏗️

This project is currently being restructured, don't use it right now, hold for a bit.

In the next couple of weeks it will be ready. 😎 🚀

Some of the future new features and changes:

- [x] Upgrade to the latest FastAPI.
- [x] Migration from SQLAlchemy to SQLModel.
- [x] Upgrade to Pydantic v2.
- [ ] Refactor and simplification of most of the code, a lot of the complexity won't be necessary anymore.
- [x] Automatic TypeScript frontend client generated from the FastAPI API (OpenAPI).
- [ ] Migrate from Vue.js 2 to React with hooks and TypeScript.
- [x] Make the project work as is, allowing to clone and use (not requiring to generate a project with Cookiecutter or Copier)
- [x] Migrate from Cookiecutter to Copier
- [ ] Move from Docker Swarm Model to Docker Compose for a simple deployment.
- [x] GitHub Actions for CI.

---

### Interactive API documentation

[![API docs](img/docs.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### Dashboard Login

[![API docs](img/login.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### Dashboard - Admin

[![API docs](img/dashboard.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### Dashboard - Create User

[![API docs](img/dashboard-create.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### Dashboard - Items

[![API docs](img/dashboard-items.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### Dashboard - User Settings

[![API docs](img/dashboard-user-settings.png)](https://github.com/tiangolo/full-stack-fastapi-postgresql)

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
    - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
    - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
    - 🤖 An automatically generated frontend client.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- 📫 Email based password recovery.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

## How to use it

You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

### Configure

You can then update configs in the `.env` files to customize your configurations.

Make sure you at least change the value for `SECRET_KEY` in the main `.env` file before deploying to production.

### Generate secret keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

## How to use it - alternative with Copier

This project template also supports generating a new project using [Copier](https://copier.readthedocs.io).

It will copy all the files, ask you configuration questions, and update the `.env` files with your answers.

### Install Copier

You can install Copier with:

```bash
pip install copier
```

Or better, if you have [`pipx`](https://pipx.pypa.io/), you can run it with:

```bash
pipx install copier
```

**Note**: If you have `pipx`, installing copier is optional, you could run it directly.

### Generate a Project with Copier

Decide a name for your new project's directory, you will use it below. For example, `my-awesome-project`.

Go to the directory that will be the parent of your project, and run the command with your project's name:

```bash
copier copy https://github.com/tiangolo/full-stack-fastapi-postgresql my-awesome-project --trust
```

If you have `pipx` and you didn't install `copier`, you can run it directly:

```bash
pipx run copier copy https://github.com/tiangolo/full-stack-fastapi-postgresql my-awesome-project --trust
```

**Note** the `--trust` option is necessary to be able to execute a [post-creation script](https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/.copier/update_dotenv.py) that updates your `.env` files.

### Input variables

Copier will ask you for some data, you might want to have at hand before generating the project.

But don't worry, you can just update any of that in the `.env` files afterwards.

The input variables, with their default values (some auto generated) are:

- `project_name`: (default: `"FastAPI Project"`) The name of the project, shown to API users (in .env).
- `stack_name`: (default: `"fastapi-project"`) The name of the stack used for Docker Compose labels (no spaces) (in .env).
- `secret_key`: (default: `"changethis"`) The secret key for the project, used for security, stored in .env, you can generate one with the method above.
- `first_superuser`: (default: `"admin@example.com"`) The email of the first superuser (in .env).
- `first_superuser_password`: (default: `"changethis"`) The password of the first superuser (in .env).
- `smtp_host`: (default: "") The SMTP server host to send emails, you can set it later in .env.
- `smtp_user`: (default: "") The SMTP server user to send emails, you can set it later in .env.
- `smtp_password`: (default: "") The SMTP server password to send emails, you can set it later in .env.
- `emails_from_email`: (default: `"info@example.com"`) The email account to send emails from, you can set it later in .env.
- `postgres_password`: (default: `"changethis"`) The password for the PostgreSQL database, stored in .env, you can generate one with the method above.
- `pgadmin_default_user`: (default: `"admin"`) The default user for pgAdmin, you can set it later in .env.
- `pgadmin_default_password`: (default: `"changethis"`) The default user password for pgAdmin, stored in .env.
- `sentry_dsn`: (default: "") The DSN for Sentry, if you are using it, you can set it later in .env.
- `flower_basic_auth`: (default: `"admin:changethis"`) The basic auth for Flower, you can set it later in .env.

## Release Notes

Check the file [release-notes.md](./release-notes.md).

## License

The FastAPI Project Template is licensed under the terms of the MIT license.

---

The documentation below is for **your own project**, not the Project Template. 👇

## Backend Development

See more instructions specific to backend development in [backend/README.md](./backend/README.md).

## Frontend Development

See more instructions specific to frontend development in [frontend/README.md](./frontend/README.md).

## Deployment

See more instructions specific to deployment in [deployment.md](./deployment.md).

## Development

See general development instructions in [development.md](./development.md).

This includes using Docker Compose, custom local domains, `.env` configurations, etc.
