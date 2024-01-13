# Generación de proyectos - Plantilla

Puedes utilizar un generador de proyectos para comenzar, ya que incluye gran parte de la configuración inicial, la seguridad, la base de datos y algunos endpoints de la API listos para ti.

Un generador de proyectos siempre tendrá una configuración muy dogmática que deberás actualizar y adaptar a tus propias necesidades, pero podría ser un buen punto de partida para tu proyecto.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Características

* Integración completa con **Docker** (basado en Docker).
* Despliegue del modo Docker Swarm.
* Integración y optimización con **Docker Compose** para el desarrollo local.
* **Listo para producción** Servidor web Python usando Uvicorn y Gunicorn.
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend:
    * **Rápido**: Muy alto rendimiento, a la par de **NodeJS** y **Go** (gracias a Starlette y Pydantic).
    * **Intuitivo**: Excelente compatibilidad con el editor. <abbr title="también conocido como en inglés como: auto-complete, autocompletion, IntelliSense">Autocompletado</abbr> en todas partes. Menos tiempo de depuración.
    * **Fácil**: Diseñado para ser fácil de usar y aprender. Menos tiempo leyendo documentación.
    * **Breve**: Minimiza la duplicación de código. Múltiples características de cada declaración de parámetro.
    * **Robusto**: Obtenga código listo para producción. Con documentación interactiva automática.
    * **Basado en estándares**: Basado en (y totalmente compatible con) los estándares abiertos para API:<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> y <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**Muchas otras características**</a> incluyendo validación automática, serialización, interactive documentación interactiva, autenticación con tokens OAuth2 JWT, etc..
* **Seguridad de contraseñas** hashing por defecto.
* Autenticación vía **JWT token**.
* Modelos **SQLAlchemy** (independiente de las extensiones Flask, por lo que se pueden usar directamente con los workers de Celery).
* Modelos iniciales básicos para usuarios (modificarlos y eliminarlos según sea necesario).
* Migraciones **Alembic**.
* **CORS** (Cross Origin Resource Sharing).
* **Celery** worker que puede importar y utilizar modelos y códigos del resto del backend de forma selectiva.
* Pruebas de backend REST basadas en **Pytest**, integradas con Docker, para que puedas probar la interacción API completa, independientemente de la base de datos. Al ejecutarse en Docker, puede crear un nuevo almacén de datos desde cero cada vez (por lo que puedes usar ElasticSearch, MongoDB, CouchDB o los que quiera y simplemente probar que la API funciona).
* Fácil integración de Python con **Jupyter Kernels** para desarrollo remoto o en Docker con extensiones como Atom Hydrogen o Visual Studio Code Jupyter.
* **Vue** frontend:
    * Generado con Vue CLI.
    * Manejo de **JWT Authentication**.
    * Vista de inicio de sesión.
    * Después de iniciar sesión, vista del Panel Principal.
    * Panel Principal con creación y edición de usuario.
    * Auto-edición de usuario
    * **Vuex**.
    * **Vue-router**.
    * **Vuetify** para hermosos componentes de material design.
    * **TypeScript**.
    * Servidor Docker basado en **Nginx** (configurado para funcionar bien con Vue-router).
    * Construcción de Docker multi-stage, por lo que no es necesario guardar ni confirmar el código compilado.
    * Las pruebas de Frontend se ejecutan en el momento de la compilación (también se pueden deshabilitar).
    * Hecha tan modular como es posible, por lo que funciona de inmediato, pero puedes volver a generarlo con Vue CLI o crearlo según lo necesites y reutilizar lo que desees.
* **PGAdmin** para la base de datos de PostgreSQL, puedes modificarlo para usar PHPMyAdmin y MySQL fácilmente.
* **Flower** para el monitoreo de los jobs de Celery.
* Balanceo de carga entre frontend y backend con **Traefik**, para que puedas tener ambos bajo el mismo dominio, separados por ruta, pero atendidos por diferentes contenedores.
* Integración de Traefik, incluida la generación automática de certificados Let's Encrypt **HTTPS**.
* GitLab **CI** (integración continua), incluidas pruebas de frontend y backend.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **ALERTA** ⚠️

Si estás iniciando un nuevo proyecto desde cero, consulta las alternativas aquí.

Por ejemplo, el generador de proyectos <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a> podría ser una mejor alternativa, ya que se mantiene activamente y se utiliza. Además incluye todas las nuevas funciones y mejoras.

Aún eres libre de usar el generador basado en Couchbase si lo deseas, probablemente aún debería funcionar bien, y si ya tienes un proyecto generado con él, también está bien (y probablemente ya lo hayas actualizado para satisfacer tus necesidades).

Puede leer más al respecto en la documentación del repositorio.

## Full Stack FastAPI MongoDB

...podría venir más tarde, dependiendo de mi disponibilidad de tiempo y otros factores. 😅 🎉

## Modelos de Machine Learning con spaCy y FastAPI

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### Modelos de Machine Learning con spaCy y FastAPI - Características

* **spaCy** Integración del modelo NER.
* Formato de solicitud de **Azure Cognitive Search** integrado.
* **Listo para producción** Servidor web Python usando Uvicorn y Gunicorn.
* **Azure DevOps** Implementación de CI/CD de Kubernetes (AKS) integrada.
* **Multilingüe** Elija fácilmente uno de los idiomas integrados de spaCy durante la configuración del proyecto.
* **Fácilmente extensible** a otros frameworks (Pytorch, Tensorflow), no solo a spaCy.
