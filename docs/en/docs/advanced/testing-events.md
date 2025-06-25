# Testing Events: startup - shutdown

When you need your event handlers (`lifespan`, `startup` and `shutdown`) to run in your tests, you can use the `TestClient` with a `with` statement:

You can read more details about the ["Running lifespan in tests in the official Starlette documentation site."](https://www.starlette.io/lifespan/#running-lifespan-in-tests)

{* ../../docs_src/app_testing/tutorial003.py hl[9:15,32:37] *}
