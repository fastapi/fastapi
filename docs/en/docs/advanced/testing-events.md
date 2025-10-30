# Testing Events: lifespan and startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

When you need `lifespan` to run in your tests, you can use the `TestClient` with a `with` statement:

{* ../../docs_src/app_testing/tutorial004.py hl[9:15,18,27:28,30:32,41:43] *}


You can read more details about the ["Running lifespan in tests in the official Starlette documentation site."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

For the deprecated `startup` and `shutdown` events, you can use the `TestClient` as follows:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
