# Eventos de testing: lifespan y startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

Cuando necesitas que `lifespan` se ejecute en tus tests, puedes usar el `TestClient` con un statement `with`:

{* ../../docs_src/app_testing/tutorial004_py39.py hl[9:15,18,27:28,30:32,41:43] *}


Puedes leer más detalles sobre ["Ejecutar lifespan en tests en el sitio oficial de documentación de Starlette."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

Para los eventos obsoletos `startup` y `shutdown`, puedes usar el `TestClient` así:

{* ../../docs_src/app_testing/tutorial003_py39.py hl[9:12,20:24] *}
