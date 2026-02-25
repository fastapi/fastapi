# 測試事件：lifespan 與 startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

當你需要在測試中執行 lifespan（生命週期）時，你可以使用 TestClient 並搭配 with 陳述式：

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}

你可以閱讀更多細節：[在測試中執行 lifespan](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)（Starlette 官方文件）。

對於已棄用的 `startup` 和 `shutdown` 事件，你可以這樣使用 TestClient：

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
