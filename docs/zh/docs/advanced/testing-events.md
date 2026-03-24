# 测试事件：lifespan 和 startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

当你需要在测试中运行 `lifespan` 时，可以将 `TestClient` 与 `with` 语句一起使用：

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}

你可以在[官方 Starlette 文档站点的“在测试中运行 lifespan”](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)阅读更多细节。

对于已弃用的 `startup` 和 `shutdown` 事件，可以按如下方式使用 `TestClient`：

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
