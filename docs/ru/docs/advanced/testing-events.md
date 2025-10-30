# Тестирование событий: lifespan и startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

Если вам нужно, чтобы `lifespan` выполнялся в ваших тестах, вы можете использовать `TestClient` вместе с оператором `with`:

{* ../../docs_src/app_testing/tutorial004.py hl[9:15,18,27:28,30:32,41:43] *}


Вы можете узнать больше подробностей в статье [Запуск lifespan в тестах на официальном сайте документации Starlette.](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

Для устаревших событий `startup` и `shutdown` вы можете использовать `TestClient` следующим образом:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
