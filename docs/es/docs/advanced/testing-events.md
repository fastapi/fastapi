# Testing Events: startup - shutdown

Cuando necesitas que tus manejadores de eventos (`startup` y `shutdown`) se ejecuten en tus tests, puedes usar el `TestClient` con un statement `with`:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
