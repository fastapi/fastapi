# Frontend { #frontend }

Puedes servir apps frontend estáticas con `app.frontend()` (o `router.frontend()`).

Esto es útil para herramientas de frontend que generan archivos estáticos, como React con Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid y otras.

Con estas herramientas, normalmente tienes un paso que construye el frontend, con un comando como:

```bash
npm run build
```

Eso generaría un directorio como `./dist/` con tus archivos frontend.

Puedes usar `app.frontend()` para servir ese directorio siguiendo las convenciones que necesitan estos frameworks frontend.

**FastAPI** revisa primero las *path operations*. Los archivos frontend se revisan solo si ninguna ruta normal coincide, así que tu API no se verá afectada.

## Sirve un Frontend { #serve-a-frontend }

Después de construir tu frontend, por ejemplo con `npm run build`, pon los archivos generados en un directorio, por ejemplo, `dist`.

La estructura de tu proyecto podría verse así:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

Luego sírvelo con `app.frontend()`:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

Con esto, un request a `/assets/app.js` puede servir `dist/assets/app.js`.

Si también tienes una *path operation* de **FastAPI**, la *path operation* gana.

## Routing del lado del cliente { #client-side-routing }

Muchas apps frontend, incluidas las **single-page apps** (SPAs), usan routing del lado del cliente. Un path como `/dashboard/settings` podría no ser un archivo real, pero el framework se encargaría de manejarlo.

Entonces, si se accede a esa URL directamente (en lugar de navegar por la app), el backend debería servir la app frontend desde `index.html`, para que el framework frontend pueda manejar el routing del lado del cliente.

Para eso, usa `fallback="index.html"`:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** usa este fallback solo para requests `GET` y `HEAD` que parecen navegación del navegador. Los archivos faltantes como JavaScript, CSS e imágenes siguen devolviendo `404`.

Los requests con otros métodos, como `POST` o `PUT`, a paths que solo coinciden con el fallback del frontend también devuelven `404`. Las *path operations* normales de **FastAPI** siguen teniendo mayor prioridad que las rutas frontend.

/// tip | Consejo

Por defecto, `fallback` tiene un valor de `fallback="auto"`. En la mayoría de los casos no necesitarás especificar `fallback`. Lee más abajo para los detalles.

///

Esto es lo que querrías con muchas apps frontend que usan routing del lado del cliente, por ejemplo, React con TanStack Router, Vue, Angular, SvelteKit o Solid.

## Página 404 personalizada { #custom-404-page }

También puedes servir una página estática `404.html` para paths frontend faltantes:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Esa response mantiene un código de estado `404`.

En este caso, **FastAPI** no servirá `index.html` para paths frontend faltantes. En su lugar, devolverá el archivo `404.html`.

/// tip | Consejo

Por defecto, `fallback` tiene un valor de `fallback="auto"`. Con esto, si se encuentra un archivo `404.html`, se usará automáticamente como fallback.

Así que normalmente puedes omitir el argumento `fallback`.

///

Esto es útil con herramientas de frontend que generan archivos HTML estáticos para cada página, como Astro.

## Fallback automático { #fallback-auto }

Por defecto, `app.frontend()` usa `fallback="auto"`.

Si hay un archivo `404.html` en el directorio frontend, los paths frontend faltantes sirven ese archivo con código de estado `404`.

De lo contrario, si hay un archivo `index.html`, los paths faltantes de navegación del navegador sirven `index.html`, que es lo que muchas apps frontend con routing del lado del cliente esperan.

Así que, en la mayoría de los casos, puedes usar `app.frontend("/", directory="dist")` sin especificar el argumento `fallback`.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Desactiva el fallback { #disable-fallback }

Si no quieres servir un archivo fallback para paths frontend faltantes, usa `fallback=None`:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Entonces los paths frontend faltantes devuelven el `404` normal.

## Revisa el directorio { #check-directory }

Por defecto, `app.frontend()` revisa que el directorio exista cuando se crea la app.

Esto ayuda a detectar errores de configuración temprano. Por ejemplo, si falta el directorio de salida del build del frontend, **FastAPI** lanzará un error al iniciar.

Si tus archivos frontend se crean más tarde, por ejemplo mediante un paso de build separado después de crear el objeto app, configura `check_dir=False`:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

Con `check_dir=False`, **FastAPI** no revisará el directorio cuando se cree la app. Si el directorio configurado todavía falta cuando se maneja un request, **FastAPI** lanzará un error en ese momento.

## Úsalo con `APIRouter` { #use-it-with-apirouter }

También puedes agregar archivos frontend a un `APIRouter` e incluirlo con un prefijo:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

En este ejemplo, los paths frontend se sirven bajo `/app`.

Cualquier *path operation* regular en la app seguirá teniendo prioridad, incluso en otros routers.

## Dependencias y Middleware { #dependencies-and-middleware }

Las responses frontend se ejecutan dentro de la aplicación **FastAPI** normal, así que el middleware HTTP se aplica a ellas.

Las dependencias de la app, de un `APIRouter` y de `include_router()` también se aplican a las responses frontend. Esto puede ser útil para proteger un frontend con autenticación por cookie o similar.

## Solo salida estática del build { #static-build-output-only }

`app.frontend()` sirve archivos ya generados por tu build del frontend.

No ejecuta renderizado del lado del servidor. Es para frameworks frontend que generan archivos estáticos, no para frameworks que necesitan renderizado dinámico en el servidor para cada request.
