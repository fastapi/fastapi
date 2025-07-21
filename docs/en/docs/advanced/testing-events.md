# Testing Events: startup - shutdown

When you need your event handlers (`startup` and `shutdown`) to run in your tests, you can use the `TestClient` with a `with` statement:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
