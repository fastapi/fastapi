# 测试 WebSockets { #testing-websockets }

你可以使用同一个 `TestClient` 来测试 WebSockets。

为此，你需要在 `with` 语句中使用 `TestClient`，连接到 WebSocket：

{* ../../docs_src/app_testing/tutorial002_py39.py hl[27:31] *}

/// note | 注意

更多细节请查看 Starlette 关于 <a href="https://www.starlette.dev/testclient/#testing-websocket-sessions" class="external-link" target="_blank">测试 WebSockets</a> 的文档。

///
