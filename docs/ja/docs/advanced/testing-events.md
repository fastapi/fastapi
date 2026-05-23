# イベントのテスト: lifespan と startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

テストで `lifespan` を実行する必要がある場合は、`with` 文と併用して `TestClient` を使用できます:

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}

より詳しい内容は、[公式 Starlette ドキュメントの「テストでの lifespan の実行」](https://www.starlette.dev/lifespan/#running-lifespan-in-tests) を参照してください。

非推奨の `startup` および `shutdown` イベントについては、次のように `TestClient` を使用できます:

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
