# LLM 測試檔案 { #llm-test-file }

本文件用來測試用於翻譯文件的 <abbr title="Large Language Model - 大型語言模型">LLM</abbr> 是否理解 `scripts/translate.py` 中的 `general_prompt`，以及 `docs/{language code}/llm-prompt.md` 中的語言特定提示。語言特定提示會附加在 `general_prompt` 後面。

此處新增的測試會提供給所有語言特定提示的設計者參考。

使用方式：

* 準備語言特定提示 - `docs/{language code}/llm-prompt.md`。
* 針對本文件做一次全新的翻譯為你想要的目標語言（例如使用 `translate.py` 的 `translate-page` 指令）。這會在 `docs/{language code}/docs/_llm-test.md` 產生翻譯檔。
* 檢查翻譯是否正確。
* 如有需要，改進你的語言特定提示、通用提示，或英文原文。
* 然後手動修正翻譯中剩下的問題，讓它成為一個好的譯文。
* 重新翻譯，並保留這份好的譯文。理想結果是 LLM 不再對該譯文做任何變更。這代表通用提示與你的語言特定提示已經盡可能完善（有時它仍可能做出幾個看似隨機的變更，原因是<a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs 並非決定性演算法</a>）。

測試：

## 程式碼片段 { #code-snippets }

//// tab | 測試

這是一個程式碼片段：`foo`。這是另一個程式碼片段：`bar`。還有一個：`baz quux`。

////

//// tab | 資訊

程式碼片段內的內容應保持原樣。

請見 `scripts/translate.py` 中通用提示的 `### Content of code snippets` 小節。

////

## 引號 { #quotes }

//// tab | 測試

Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".

/// note | 注意

LLM 很可能會把這段翻譯錯。重點只在於重新翻譯時是否能保留已修正的翻譯。

///

////

//// tab | 資訊

提示設計者可以選擇是否將中性引號轉換為排印引號。保留原樣也可以。

例如請見 `docs/de/llm-prompt.md` 中的 `### Quotes` 小節。

////

## 程式碼片段中的引號 { #quotes-in-code-snippets }

//// tab | 測試

`pip install "foo[bar]"`

程式碼片段中字串常值的例子："this"、'that'。

較難的程式碼片段中字串常值例子：`f"I like {'oranges' if orange else "apples"}"`

進階：`Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | 資訊

... 不過，程式碼片段中的引號必須保持原樣。

////

## 程式碼區塊 { #code-blocks }

//// tab | 測試

一個 Bash 程式碼範例...

```bash
# 向宇宙輸出問候
echo "Hello universe"
```

...以及一個主控台範例...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...以及另一個主控台範例...

```console
// 建立目錄 "code"
$ mkdir code
// 切換到該目錄
$ cd code
```

...以及一個 Python 程式碼範例...

```Python
wont_work()  # 這不會運作 😱
works(foo="bar")  # 這可以運作 🎉
```

...就是這樣。

////

//// tab | 資訊

程式碼區塊中的程式碼不應修改，註解除外。

請見 `scripts/translate.py` 中通用提示的 `### Content of code blocks` 小節。

////

## 分頁與色塊 { #tabs-and-colored-boxes }

//// tab | 測試

/// info | 資訊
Some text
///

/// note | 注意
Some text
///

/// note | 技術細節
Some text
///

/// check | 檢查
Some text
///

/// tip | 提示
Some text
///

/// warning | 警告
Some text
///

/// danger | 危險
Some text
///

////

//// tab | 資訊

分頁與 `Info`/`Note`/`Warning`/等區塊，應在直線（`|`）後加入其標題的翻譯。

請見 `scripts/translate.py` 中通用提示的 `### Special blocks` 與 `### Tab blocks` 小節。

////

## 網頁與內部連結 { #web-and-internal-links }

//// tab | 測試

連結文字應被翻譯，連結位址應保持不變：

* [連結到上方標題](#code-snippets)
* [內部連結](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">外部連結</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">連結到樣式</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">連結到腳本</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">連結到圖片</a>

連結文字應被翻譯，連結位址應指向對應的翻譯版本：

* <a href="https://fastapi.tiangolo.com/zh-hant/" class="external-link" target="_blank">FastAPI 連結</a>

////

//// tab | 資訊

連結應翻譯其文字，但位址需保持不變。例外是指向 FastAPI 文件網站的絕對連結，該情況下位址應指向對應的翻譯版本。

請見 `scripts/translate.py` 中通用提示的 `### Links` 小節。

////

## HTML「abbr」元素 { #html-abbr-elements }

//// tab | 測試

以下是一些包在 HTML「abbr」元素中的內容（部分為杜撰）：

### abbr 提供完整詞組 { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - 搞定工作法">GTD</abbr>
* <abbr title="less than - 小於"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML 網路權杖">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - 平行伺服器閘道介面">PSGI</abbr>

### abbr 提供完整詞組與說明 { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla 開發者網路: 給開發者的文件，由 Firefox 團隊撰寫">MDN</abbr>
* <abbr title="Input/Output - 輸入/輸出: 磁碟讀寫，網路通訊。">I/O</abbr>.

////

//// tab | 資訊

「abbr」元素的「title」屬性需依特定規則翻譯。

翻譯可以自行新增「abbr」元素（例如為解釋英文單字），LLM 不應移除它們。

請見 `scripts/translate.py` 中通用提示的 `### HTML abbr elements` 小節。

////

## HTML「dfn」元素 { #html-dfn-elements }

* <dfn title="被設定為連接並以某種方式一起工作的機器群組。">叢集</dfn>
* <dfn title="一種機器學習方法，使用具備多個隱藏層的人工神經網路，在輸入與輸出層之間建立完整的內部結構">深度學習</dfn>

## 標題 { #headings }

//// tab | 測試

### 開發網頁應用程式 - 教學 { #develop-a-webapp-a-tutorial }

Hello.

### 型別提示與註解 { #type-hints-and-annotations }

Hello again.

### 超類與子類別 { #super-and-subclasses }

Hello again.

////

//// tab | 資訊

標題唯一的硬性規則是保留花括號中的雜湊片段不變，以確保連結不會失效。

請見 `scripts/translate.py` 中通用提示的 `### Headings` 小節。

關於語言特定的說明，參見例如 `docs/de/llm-prompt.md` 中的 `### Headings` 小節。

////

## 文件中使用的術語 { #terms-used-in-the-docs }

//// tab | 測試

* you
* your

* e.g.
* etc.

* `foo` as an `int`
* `bar` as a `str`
* `baz` as a `list`

* 教學 - 使用者指南
* 進階使用者指南
* SQLModel 文件
* API 文件
* 自動文件

* 資料科學
* 深度學習
* 機器學習
* 相依性注入
* HTTP 基本驗證
* HTTP 摘要驗證
* ISO 格式
* JSON Schema 標準
* JSON 結構描述
* 結構描述定義
* 密碼流程
* 行動裝置

* 已棄用
* 設計的
* 無效
* 即時
* 標準
* 預設
* 區分大小寫
* 不區分大小寫

* 提供應用程式服務
* 提供頁面服務

* 應用程式
* 應用程式

* 請求
* 回應
* 錯誤回應

* 路徑操作
* 路徑操作裝飾器
* 路徑操作函式

* 主體
* 請求主體
* 回應主體
* JSON 主體
* 表單主體
* 檔案主體
* 函式主體

* 參數
* 主體參數
* 路徑參數
* 查詢參數
* Cookie 參數
* 標頭參數
* 表單參數
* 函式參數

* 事件
* 啟動事件
* 伺服器的啟動
* 關閉事件
* 生命週期事件

* 處理器
* 事件處理器
* 例外處理器
* 處理

* 模型
* Pydantic 模型
* 資料模型
* 資料庫模型
* 表單模型
* 模型物件

* 類別
* 基底類別
* 父類別
* 子類別
* 子類別
* 同級類別
* 類別方法

* 標頭
* 標頭
* 授權標頭
* `Authorization` 標頭
* 轉送標頭

* 相依性注入系統
* 相依項
* 可相依對象
* 相依者

* I/O 受限
* CPU 受限
* 並發
* 平行處理
* 多處理程序

* 環境變數
* 環境變數
* `PATH`
* `PATH` 變數

* 驗證
* 驗證提供者
* 授權
* 授權表單
* 授權提供者
* 使用者進行驗證
* 系統驗證使用者

* CLI
* 命令列介面

* 伺服器
* 用戶端

* 雲端提供者
* 雲端服務

* 開發
* 開發階段

* dict
* 字典
* 列舉
* enum
* 列舉成員

* 編碼器
* 解碼器
* 編碼
* 解碼

* 例外
* 拋出

* 運算式
* 陳述式

* 前端
* 後端

* GitHub 討論
* GitHub 議題

* 效能
* 效能優化

* 回傳型別
* 回傳值

* 安全性
* 安全性機制

* 任務
* 背景任務
* 任務函式

* 樣板
* 樣板引擎

* 型別註解
* 型別提示

* 伺服器工作進程
* Uvicorn 工作進程
* Gunicorn 工作進程
* 工作進程
* worker 類別
* 工作負載

* 部署
* 部署

* SDK
* 軟體開發工具組

* `APIRouter`
* `requirements.txt`
* Bearer Token
* 相容性破壞變更
* 錯誤
* 按鈕
* 可呼叫對象
* 程式碼
* 提交
* 情境管理器
* 協程
* 資料庫工作階段
* 磁碟
* 網域
* 引擎
* 假的 X
* HTTP GET 方法
* 項目
* 函式庫
* 生命週期
* 鎖
* 中介軟體
* 行動應用程式
* 模組
* 掛載
* 網路
* 來源
* 覆寫
* 有效負載
* 處理器
* 屬性
* 代理
* pull request
* 查詢
* RAM
* 遠端機器
* 狀態碼
* 字串
* 標籤
* Web 框架
* 萬用字元
* 回傳
* 驗證

////

//// tab | 資訊

這是一份不完整且非規範性的（多為）技術術語清單，來源為文件內容。它可能有助於提示設計者判斷哪些術語需要 LLM 的特別協助。例如當 LLM 反覆把好的翻譯改回成較差的版本，或在你的語言中對某詞的詞形變化處理有困難時。

請見例如 `docs/de/llm-prompt.md` 中的 `### List of English terms and their preferred German translations` 小節。

////
