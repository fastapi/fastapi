# Тестування подій: `lifespan` і `startup` - `shutdown` { #testing-events-lifespan-and-startup-shutdown }

Коли вам потрібно, щоб `lifespan` виконувався у ваших тестах, ви можете використати `TestClient` з оператором `with`:

{* ../../docs_src/app_testing/tutorial004_py39.py hl[9:15,18,27:28,30:32,41:43] *}


Ви можете прочитати більше деталей про [«Running lifespan in tests in the official Starlette documentation site.»](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

Для застарілих подій `startup` і `shutdown` ви можете використати `TestClient` так:

{* ../../docs_src/app_testing/tutorial003_py39.py hl[9:12,20:24] *}
