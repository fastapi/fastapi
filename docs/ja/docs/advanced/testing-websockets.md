# WebSocket のテスト { #testing-websockets }

WebSocket をテストするのにも同じ `TestClient` を使用できます。

そのために、`with` 文の中で `TestClient` を使用し、WebSocket に接続します:

{* ../../docs_src/app_testing/tutorial002_py310.py hl[27:31] *}

/// note | 備考

詳細については、Starlette のドキュメント「<a href="https://www.starlette.dev/testclient/#testing-websocket-sessions" class="external-link" target="_blank">WebSocket のテスト</a>」を参照してください。

///
