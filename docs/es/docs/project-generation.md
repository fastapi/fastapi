# Project Generation - Plantilla

Para comenzar puedes utilizar un project generator, pues incluye una configuración inicial bastante amplia, seguridad, bases de datos y los primeros API endpoints ya están hechos por ti.

Siempre habra un extenso debate en que debe de llevar la configuración de un project generator, por lo cual la debes de actualizar y adaptar de acuerdo a tus necesidades, sin embargo puede ser un buen punto de partida para tu proyecto.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Características

* Completa integración con **Docker** (Docker based).
* Docker Swarm Mode deployment.
* **Docker Compose** integración y optimización para desarrollo local.
* **Production ready** Servidor web de Python usando Uvicorn y Gunicorn.
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend:
    * **Rápido**: Muy alto rendimiento, a la par de **NodeJS** y **Go** (debido a Starlette y Pydantic).
    * **Intuitivo**: Buen soporte de editores. <abbr title="también conocido como auto-complete, autocompletion, IntelliSense">Completación</abbr> dondequiera. Menos tiempo resolviendo errores.
    * **Fácil**: Diseñado para ser fácil de usar y aprender. Menos tiempo leyendo documentación.
    * **Corto**: Reduce el código duplicado. Multiples características de cada parámetro declarado.
    * **Robusto**: Consigue código listo para producción. Con documentación interactiva automática.
    * **Basado en estándares**: Basado en (y totalmente compatible con) los open standards para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> y <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**Muchas otras características**</a> incluyendo validación automática, serialización, autenticación con OAuth2 JWT tokens, etc.
* **Contraseñas seguras** hashing por defecto.
* **JWT token** autenticación.
* **SQLAlchemy** modelos (independientes de las extensiones de Flask, para que puedan ser usadas con Celery workers directamente).
* Modelos básicos para usuarios (modifica y elimina conforme vayas necesitando).
* **Alembic** migraciones.
* **CORS** (Cross Origin Resource Sharing).
* **Celery** importa, usa modelos, y programa desde el resto del backend selectivamente.
* Pruebas de backends REST basadas en **Pytest**, integradas con Docker, para puedas probar la interacción completa de la API, independientemente de la base de datos. Mientras corre en Docker, puede construir un nuevo almacenamiento desde 0 cada vez (así, puedes usar ElasticSearch, MongoDB, CouchDB, o cualquiera que quieras, y solamente probar que la API funciona).
* Integración sencilla de Python con **Jupyter Kernels** para desarrollo remoto o en Docker con extensiones como Atom Hydrogen o Visual Studio Code Jupyter.
* Frontend en **Vue**:
    * Generado con el CLI de Vue.
    * Manejo de **JWT Authentication**.
    * Vista de Login.
    * Después de login, vista del dashboard principal.
    * Dashboard principal con creación y edición de usurarios.
    * Edición del mismo usuario.
    * **Vuex**.
    * **Vue-router**.
    * **Vuetify** para hermosos componentes de material design.
    * **TypeScript**.
    * Servidor de Docker basado en **Nginx** (configurado para hacer buen juego con Vue-router).
    * Docker multi-stage building, para que no necesites guardar o hacer commit a código compilado.
    * Pruebas del Frontend corren en tiempo de construcción (también pueden desactivarse).
    * Hecho lo mas modular posible, para que funcione recién sacado del horno, pero puedes regenerarlo con el CLI de Vue o crearlo mientras lo necesitas, y reusar lo que quieras.
* **PGAdmin** para una base de datos de PostgreSQL, puedes modificarla fácilmente usando PHPMyAdmin y MySQL.
* **Flower** para monitoreo de tareas de Celery.
* Balanceo de carga entre el frontend y el backend con **Traefik**, para que así puedas tener ambos bajo el mismo dominio, separados por un path, pero provenientes de diferentes contenedores.
* Integración de Traefik, incluyendo generado automático de certificados Let's Encrypt **HTTPS**.
* **CI** (integración continua) de GitLab, incluyendo pruebas de frontend y backend.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **Advertencia** ⚠️

Si estas comenzando un proyecto desde 0, revisa las alternativas aquí.

Por ejemplo, el project generator, <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a>, puede ser una mejor alternativa, puesto que se encuentra activo y en uso. Y incluye todas las novedades y mejoras.

Eres libre de seguir usando el Couchbase-based generator si tu quieres, debería de continuar funcionando correctamente, y si ya tienes un proyecto generado con este, también esta bien (y es probable que ya lo hayas adecuado a tus necesidades)

Puedes leer más acerca de él en la documentación del repositorio.

## Full Stack FastAPI MongoDB

...vendrá después, dependiendo en mi tiempo disponible y otros factores. 😅 🎉

## Modelos de Machine Learning con spaCy y FastAPI

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### Modelos de Machine Learning con spaCy y FastAPI - Características

* **spaCy** Integración de modelo NER.
* **Azure Cognitive Search** formato de <abbr title="peticiones">request</abbr> incorporadas.
* **Listo para producción** Servidor web de Python usando Uvicorn y Gunicorn.
* **Azure DevOps** Desplegado incorporado de Kubernetes (AKS) CI/CD.
* **Multi-lenguaje** Fácilmente escoge entre uno de los lenguajes incorporados en spaCy's durante la configuración del proyecto.
* **Fácilmente extendible** a otros frameworks de modelado (Pytorch, Tensorflow), no solo spaCy.
