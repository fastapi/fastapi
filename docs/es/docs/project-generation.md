# Plantilla de FastAPI Full Stack

Las plantillas, aunque típicamente vienen con una configuración específica, están diseñadas para ser flexibles y personalizables. Esto te permite modificarlas y adaptarlas a los requisitos de tu proyecto, lo que las convierte en un excelente punto de partida. 🏁

Puedes utilizar esta plantilla para comenzar, ya que incluye gran parte de la configuración inicial, seguridad, base de datos y algunos endpoints de API ya realizados.

Repositorio en GitHub: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Plantilla de FastAPI Full Stack - Tecnología y Características

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) para el backend API en Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) para las interacciones con la base de datos SQL en Python (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), utilizado por FastAPI, para la validación de datos y la gestión de configuraciones.
    - 💾 [PostgreSQL](https://www.postgresql.org) como la base de datos SQL.
- 🚀 [React](https://react.dev) para el frontend.
    - 💃 Usando TypeScript, hooks, Vite y otras partes de un stack de frontend moderno.
    - 🎨 [Chakra UI](https://chakra-ui.com) para los componentes del frontend.
    - 🤖 Un cliente frontend generado automáticamente.
    - 🧪 Playwright para pruebas End-to-End.
    - 🦇 Soporte para modo oscuro.
- 🐋 [Docker Compose](https://www.docker.com) para desarrollo y producción.
- 🔒 Hashing seguro de contraseñas por defecto.
- 🔑 Autenticación con token JWT.
- 📫 Recuperación de contraseñas basada en email.
- ✅ Tests con [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) como proxy inverso / balanceador de carga.
- 🚢 Instrucciones de despliegue utilizando Docker Compose, incluyendo cómo configurar un proxy frontend Traefik para manejar certificados HTTPS automáticos.
- 🏭 CI (integración continua) y CD (despliegue continuo) basados en GitHub Actions.
