# Plantilla Full Stack FastAPI { #full-stack-fastapi-template }

Las plantillas, aunque normalmente vienen con una configuración específica, están diseñadas para ser flexibles y personalizables. Esto te permite modificarlas y adaptarlas a los requisitos de tu proyecto, haciéndolas un excelente punto de partida. 🏁

Puedes usar esta plantilla para comenzar, ya que incluye gran parte de la configuración inicial, seguridad, base de datos y algunos endpoints de API ya hechos para ti.

Repositorio de GitHub: [Plantilla Full Stack FastAPI](https://github.com/tiangolo/full-stack-fastapi-template)

## Plantilla Full Stack FastAPI - Stack de tecnología y funcionalidades { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/es) para la API del backend en Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) para las interacciones con bases de datos SQL en Python (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), utilizado por FastAPI, para la validación de datos y gestión de configuraciones.
    - 💾 [PostgreSQL](https://www.postgresql.org) como base de datos SQL.
- 🚀 [React](https://react.dev) para el frontend.
    - 💃 Usando TypeScript, hooks, Vite, y otras partes de una stack moderna de frontend.
    - 🎨 [Tailwind CSS](https://tailwindcss.com) y [shadcn/ui](https://ui.shadcn.com) para los componentes del frontend.
    - 🤖 Un cliente de frontend generado automáticamente.
    - 🧪 [Playwright](https://playwright.dev) para escribir pruebas End-to-End.
    - 🦇 Soporte para modo oscuro.
- 🐋 [Docker Compose](https://www.docker.com) para desarrollo y producción.
- 🔒 Hashing seguro de contraseñas por defecto.
- 🔑 Autenticación con tokens JWT.
- 📫 Recuperación de contraseñas basada en email.
- ✅ Pruebas con [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) como proxy inverso / load balancer.
- 🚢 Instrucciones de despliegue usando Docker Compose, incluyendo cómo configurar un proxy Traefik frontend para manejar certificados HTTPS automáticos.
- 🏭 CI (integración continua) y CD (despliegue continuo) basados en GitHub Actions.
