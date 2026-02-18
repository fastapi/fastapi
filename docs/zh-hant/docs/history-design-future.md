# 歷史、設計與未來 { #history-design-and-future }

不久之前，<a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">一位 **FastAPI** 使用者提問</a>：

> 這個專案的歷史是什麼？看起來它在短短幾週內從默默無名變得非常厲害 [...]

以下是其中一小段歷史。

## 替代方案 { #alternatives }

多年來我一直在打造具有複雜需求的 API（機器學習、分散式系統、非同步工作、NoSQL 資料庫等），並帶領多個開發團隊。

在此過程中，我需要調查、測試並使用許多替代方案。

**FastAPI** 的歷史，在很大程度上也是其前身工具的歷史。

如在[替代方案](alternatives.md){.internal-link target=_blank}章節所述：

<blockquote markdown="1">

若沒有他人的前期成果，就不會有 **FastAPI**。

先前已有許多工具啟發了它的誕生。

我曾經多年避免再去打造一個新框架。起初我嘗試用各種不同的框架、外掛與工具，來滿足 **FastAPI** 涵蓋的所有功能。

但在某個時刻，別無選擇，只能打造一個同時提供所有這些功能的東西，取過去工具之長，並以可能的最佳方式加以結合，還運用了以往甚至不存在的語言功能（Python 3.6+ 的型別提示）。

</blockquote>

## 調研 { #investigation }

透過實際使用這些替代方案，我得以向它們學習、汲取想法，並以我能為自己與合作開發團隊找到的最佳方式加以整合。

例如，很清楚理想上應以標準的 Python 型別提示為基礎。

同時，最佳做法就是採用現有標準。

因此，在開始撰寫 **FastAPI** 之前，我花了好幾個月研究 OpenAPI、JSON Schema、OAuth2 等規範，了解它們之間的關係、重疊與差異。

## 設計 { #design }

接著，我花時間設計作為使用者（作為使用 FastAPI 的開發者）時希望擁有的開發者「API」。

我在最受歡迎的 Python 編輯器中測試了多個想法：PyCharm、VS Code、基於 Jedi 的編輯器。

根據最新的 <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python 開發者調查</a>，這些工具涵蓋約 80% 的使用者。

這表示 **FastAPI** 已針對 80% 的 Python 開發者所使用的編輯器進行過專門測試。而由於其他多數編輯器的行為也類似，這些優點幾乎在所有編輯器上都能生效。

藉此我找到了盡可能減少程式碼重複、在各處提供自動補全、型別與錯誤檢查等的最佳方式。

一切都是為了讓所有開發者都能擁有最佳的開發體驗。

## 需求 { #requirements }

在測試多種替代方案後，我決定採用 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a>，因為它的優勢。

隨後我也對它做出貢獻，使其完全符合 JSON Schema、支援以不同方式定義約束，並依據在多款編輯器中的測試結果改進編輯器支援（型別檢查、自動補全）。

在開發過程中，我也對 <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a>（另一個關鍵依賴）做出貢獻。

## 開發 { #development }

當我開始著手實作 **FastAPI** 本身時，多數拼圖已經就緒，設計已定，需求與工具已備齊，對各項標準與規範的理解也清晰且新鮮。

## 未來 { #future }

到目前為止，**FastAPI** 及其理念已經對許多人有幫助。

相較先前的替代方案，它更適合許多使用情境，因而被選用。

許多開發者與團隊（包括我和我的團隊）已經在他們的專案中依賴 **FastAPI**。

但仍有許多改進與功能即將到來。

**FastAPI** 的前景非常光明。

也非常感謝[你的幫助](help-fastapi.md){.internal-link target=_blank}。
