# 中繼資料與文件 URL { #metadata-and-docs-urls }

你可以在你的 FastAPI 應用程式中自訂多項中繼資料設定。

## API 的中繼資料 { #metadata-for-api }

你可以設定下列欄位，這些欄位會用在 OpenAPI 規格與自動產生的 API 文件介面中：

| 參數 | 型別 | 說明 |
|------------|------|-------------|
| `title` | `str` | API 的標題。 |
| `summary` | `str` | API 的簡短摘要。<small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small> |
| `description` | `str` | API 的簡短說明。可使用 Markdown。 |
| `version` | `string` | API 的版本號。這是你自己的應用程式版本，不是 OpenAPI 的版本，例如 `2.5.0`。 |
| `terms_of_service` | `str` | 指向 API 服務條款的 URL。若提供，必須是 URL。 |
| `contact` | `dict` | 對外公開的 API 聯絡資訊。可包含多個欄位。<details><summary><code>contact</code> 欄位</summary><table><thead><tr><th>參數</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>聯絡人／組織的識別名稱。</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>指向聯絡資訊的 URL。必須是 URL 格式。</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>聯絡人／組織的電子郵件地址。必須是電子郵件格式。</td></tr></tbody></table></details> |
| `license_info` | `dict` | 對外公開的 API 授權資訊。可包含多個欄位。<details><summary><code>license_info</code> 欄位</summary><table><thead><tr><th>參數</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>必填</strong>（若有設定 <code>license_info</code>）。API 使用的授權名稱。</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API 的 <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> 授權表示式。<code>identifier</code> 欄位與 <code>url</code> 欄位互斥。<small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>API 所採用授權的 URL。必須是 URL 格式。</td></tr></tbody></table></details> |

你可以這樣設定它們：

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | 提示

你可以在 `description` 欄位中撰寫 Markdown，輸出時會被正確渲染。

///

使用這些設定後，自動產生的 API 文件會像這樣：

<img src="/img/tutorial/metadata/image01.png">

## 授權識別碼 { #license-identifier }

自 OpenAPI 3.1.0 與 FastAPI 0.99.0 起，你也可以在 `license_info` 中使用 `identifier` 來取代 `url`。

例如：

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## 標籤的中繼資料 { #metadata-for-tags }

你也可以透過 `openapi_tags` 參數，為用來分組你的路徑操作（path operation）的各個標籤加入額外中繼資料。

它接收一個 list，其中每個標籤對應一個 dictionary。

每個 dictionary 可包含：

* `name`（**必填**）：一個 `str`，其值需與你在路徑操作與 `APIRouter`s 的 `tags` 參數中使用的標籤名稱相同。
* `description`：一個 `str`，為該標籤的簡短描述。可使用 Markdown，並會顯示在文件介面中。
* `externalDocs`：一個 `dict`，描述外部文件，包含：
    * `description`：一個 `str`，外部文件的簡短描述。
    * `url`（**必填**）：一個 `str`，外部文件的 URL。

### 建立標籤的中繼資料 { #create-metadata-for-tags }

我們用 `users` 與 `items` 兩個標籤來示範。

先為你的標籤建立中繼資料，然後將它傳給 `openapi_tags` 參數：

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

注意你可以在描述中使用 Markdown，例如「login」會以粗體（**login**）顯示，而「fancy」會以斜體（_fancy_）顯示。

/// tip | 提示

你不必為你使用到的每個標籤都加入中繼資料。

///

### 使用你的標籤 { #use-your-tags }

在你的路徑操作（以及 `APIRouter`s）上使用 `tags` 參數，將它們歸類到不同標籤下：

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// info | 資訊

在［路徑操作設定］中閱讀更多關於標籤的內容：[Path Operation Configuration](path-operation-configuration.md#tags){.internal-link target=_blank}。

///

### 檢視文件 { #check-the-docs }

現在檢視文件時，會看到所有額外的中繼資料：

<img src="/img/tutorial/metadata/image02.png">

### 標籤順序 { #order-of-tags }

每個標籤中繼資料 dictionary 在清單中的順序，也會決定它們在文件介面中的顯示順序。

例如，雖然按字母排序時 `users` 會排在 `items` 之後，但因為我們在清單中將它的中繼資料放在第一個，所以它會先顯示。

## OpenAPI URL { #openapi-url }

預設情況下，OpenAPI 綱要（schema）會提供在 `/openapi.json`。

但你可以用 `openapi_url` 參數來調整。

例如，將它設定為提供在 `/api/v1/openapi.json`：

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

如果你想完全停用 OpenAPI 綱要，可以設定 `openapi_url=None`，同時也會停用依賴它的文件使用者介面。

## 文件 URL { #docs-urls }

你可以設定內建的兩個文件使用者介面：

* Swagger UI：提供於 `/docs`。
    * 可用 `docs_url` 參數設定其 URL。
    * 設定 `docs_url=None` 可停用。
* ReDoc：提供於 `/redoc`。
    * 可用 `redoc_url` 參數設定其 URL。
    * 設定 `redoc_url=None` 可停用。

例如，將 Swagger UI 提供於 `/documentation`，並停用 ReDoc：

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
