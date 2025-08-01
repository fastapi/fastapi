# Тестирование событий: startup - shutdown

Когда вам нужно, чтобы ваши обработчики событий (`startup` и `shutdown`) запускались в ваших тестах, вы можете использовать `TestClient` с оператором `with`:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
