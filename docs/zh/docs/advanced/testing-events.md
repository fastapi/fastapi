# 测试事件：lifespan 与启动 - 关闭 { #testing-events-lifespan-and-startup-shutdown }

当你需要在测试中运行 `lifespan` 时，可以使用带有 `with` 语句的 `TestClient`：

{* ../../docs_src/app_testing/tutorial004_py39.py hl[9:15,18,27:28,30:32,41:43] *}


你可以在[官方 Starlette 文档站点中阅读更多关于“在测试中运行 lifespan”的细节。](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

对于已弃用的 `startup` 和 `shutdown` 事件，你可以按如下方式使用 `TestClient`：

{* ../../docs_src/app_testing/tutorial003_py39.py hl[9:12,20:24] *}
