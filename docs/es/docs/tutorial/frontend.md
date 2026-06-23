# Frontend { #frontend }

Puedes servir aplicaciones de frontend estáticas con `app.frontend()` (o `router.frontend()`).

Esto es útil para herramientas de frontend que generan archivos estáticos, como React con Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid y otras.

Con estas herramientas normalmente tienes un paso que construye el frontend, con un comando como:

```bash
npm run build
```

Eso generaría un directorio como `./dist/` con los archivos de tu frontend.

Puedes usar `app.frontend()` para servir ese directorio siguiendo las convenciones que necesitan estos frameworks de frontend.

**FastAPI** comprueba primero las *path operations*. Los archivos del frontend solo se comprueban si ninguna ruta normal coincidió, así que tu API no se verá afectada.

## Servir un frontend { #serve-a-frontend }

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

Con esto, una petición a `/assets/app.js` puede servir `dist/assets/app.js`.

Si también tienes una *path operation* de **FastAPI**, la *path operation* gana.

## Enrutamiento en el cliente { #client-side-routing }

Muchas apps de frontend, incluidas las **single-page apps** (SPAs), usan enrutamiento en el cliente. Una ruta como `/dashboard/settings` podría no ser un archivo real, pero el framework se encargaría de gestionarla.

Así que, al acceder directamente a esa URL (en lugar de navegar por la app), el backend debería servir la app de frontend desde `index.html`, para que el framework de frontend pueda gestionar entonces el enrutamiento en el cliente.

Para eso, usa `fallback="index.html"`:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** usa este fallback solo para las peticiones que parecen navegación de un navegador. Los archivos que falten, como JavaScript, CSS e imágenes, siguen devolviendo `404`.

/// tip | Consejo

Por defecto, `fallback` tiene el valor `fallback="auto"`. En la mayoría de los casos no necesitarás especificar `fallback`. Lee más abajo para los detalles.

///

Esto es lo que querrías con muchas apps de frontend que usan enrutamiento en el cliente, por ejemplo, React con TanStack Router, Vue, Angular, SvelteKit o Solid.

## Página 404 personalizada { #custom-404-page }

También puedes servir una página estática `404.html` para las rutas de frontend que falten:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Esa respuesta mantiene un código de estado `404`.

En este caso, **FastAPI** no servirá `index.html` para las rutas de frontend que falten. Servirá el archivo `404.html` en su lugar.

/// tip | Consejo

Por defecto, `fallback` tiene el valor `fallback="auto"`. Con esto, si se encuentra un archivo `404.html`, se usará como fallback automáticamente.

Así que normalmente puedes omitir el argumento `fallback`.

///

Esto es útil con herramientas de frontend que generan archivos HTML estáticos para cada página, como Astro.

## Fallback automático { #fallback-auto }

Por defecto, `app.frontend()` usa `fallback="auto"`.

Si hay un archivo `404.html` en el directorio del frontend, las rutas de frontend que falten sirven ese archivo con un código de estado `404`.

En caso contrario, si hay un archivo `index.html`, las rutas de navegación del navegador que falten sirven `index.html`, que es lo que esperan muchas apps de frontend con enrutamiento en el cliente.

Así que, en la mayoría de los casos puedes usar `app.frontend("/", directory="dist")` sin especificar el argumento `fallback`.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Desactivar el fallback { #disable-fallback }

Si no quieres servir un archivo de fallback para las rutas de frontend que falten, usa `fallback=None`:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Entonces las rutas de frontend que falten devuelven el `404` normal.

## Comprobar el directorio { #check-directory }

Por defecto, `app.frontend()` comprueba que el directorio existe cuando se crea la app.

Esto ayuda a detectar errores de configuración pronto. Por ejemplo, si falta el directorio de salida del build del frontend, **FastAPI** lanzará un error al arrancar.

Si tus archivos de frontend se crean más tarde, por ejemplo con un paso de build separado después de crear el objeto de la app, pon `check_dir=False`:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

Con `check_dir=False`, **FastAPI** no comprobará el directorio cuando se cree la app. Si el directorio configurado sigue faltando cuando se gestiona una petición, **FastAPI** lanzará un error en ese momento.

## Úsalo con `APIRouter` { #use-it-with-apirouter }

También puedes añadir archivos de frontend a un `APIRouter` e incluirlo con un prefijo:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

En este ejemplo, las rutas de frontend se sirven bajo `/app`.

Cualquier *path operation* normal de la app seguirá teniendo prioridad, incluso en otros routers.

## Solo archivos estáticos del build { #static-build-output-only }

`app.frontend()` sirve archivos ya generados por el build de tu frontend.

No ejecuta renderizado en el servidor. Es para frameworks de frontend que generan archivos estáticos, no para frameworks que necesitan renderizado dinámico en el servidor en cada petición.
