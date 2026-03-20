# OAuth2 範圍（scopes） { #oauth2-scopes }

你可以直接在 FastAPI 中使用 OAuth2 的 scopes，已整合可無縫運作。

這能讓你在 OpenAPI 應用（以及 API 文件）中，依照 OAuth2 標準，實作更細粒度的權限系統。

帶有 scopes 的 OAuth2 是許多大型身分驗證提供者（如 Facebook、Google、GitHub、Microsoft、X（Twitter）等）所使用的機制。他們用它來為使用者與應用程式提供特定權限。

每次你「使用」Facebook、Google、GitHub、Microsoft、X（Twitter）「登入」時，那個應用就是在使用帶有 scopes 的 OAuth2。

在本節中，你將看到如何在你的 FastAPI 應用中，用同樣的帶有 scopes 的 OAuth2 管理驗證與授權。

/// warning

這一節算是進階內容。如果你剛開始，可以先跳過。

你不一定需要 OAuth2 scopes，你可以用任何你想要的方式處理驗證與授權。

但帶有 scopes 的 OAuth2 可以很漂亮地整合進你的 API（透過 OpenAPI）與 API 文件。

無論如何，你仍然會在程式碼中，依你的需求，強制檢查那些 scopes，或其他任何安全性／授權需求。

在許多情況下，帶有 scopes 的 OAuth2 可能有點大材小用。

但如果你確定需要，或是好奇，請繼續閱讀。

///

## OAuth2 scopes 與 OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 規格將「scopes」定義為以空白分隔的一串字串列表。

每個字串的內容可以有任意格式，但不應包含空白。

這些 scopes 代表「權限」。

在 OpenAPI（例如 API 文件）中，你可以定義「security schemes」。

當某個 security scheme 使用 OAuth2 時，你也可以宣告並使用 scopes。

每個「scope」就是一個（不含空白的）字串。

它們通常用來宣告特定的安全性權限，例如：

- `users:read` 或 `users:write` 是常見的例子。
- `instagram_basic` 是 Facebook / Instagram 使用的。
- `https://www.googleapis.com/auth/drive` 是 Google 使用的。

/// info

在 OAuth2 中，「scope」只是宣告所需特定權限的一個字串。

是否包含像 `:` 這樣的字元，或是否是一個 URL，都沒差。

那些細節取決於實作。

對 OAuth2 而言，它們就是字串。

///

## 全局概觀 { #global-view }

先快速看看相對於主教學「使用密碼（與雜湊）、Bearer 與 JWT token 的 OAuth2」的差異（[OAuth2 with Password (and hashing), Bearer with JWT tokens](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank}）。現在加入了 OAuth2 scopes：

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

接著我們一步一步檢視這些變更。

## OAuth2 安全性方案 { #oauth2-security-scheme }

第一個變更是：我們現在宣告了帶有兩個可用 scope 的 OAuth2 安全性方案，`me` 與 `items`。

參數 `scopes` 接收一個 `dict`，以各 scope 為鍵、其描述為值：

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

由於現在宣告了這些 scopes，當你登入／授權時，它們會出現在 API 文件中。

你可以選擇要授予哪些 scopes 存取權：`me` 與 `items`。

這與你使用 Facebook、Google、GitHub 等登入時所授與權限的機制相同：

<img src="/img/tutorial/security/image11.png">

## 內含 scopes 的 JWT token { #jwt-token-with-scopes }

現在，修改 token 的路徑操作以回傳所請求的 scopes。

我們仍然使用相同的 `OAuth2PasswordRequestForm`。它包含屬性 `scopes`，其為 `list` 的 `str`，列出請求中收到的每個 scope。

並且我們將這些 scopes 作為 JWT token 的一部分回傳。

/// danger

為了簡化，這裡我們只是直接把接收到的 scopes 加進 token。

但在你的應用中，為了安全性，你應確保只加入該使用者實際可擁有或你預先定義的 scopes。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## 在路徑操作與相依性中宣告 scopes { #declare-scopes-in-path-operations-and-dependencies }

現在我們宣告 `/users/me/items/` 這個路徑操作需要 `items` 這個 scope。

為此，我們從 `fastapi` 匯入並使用 `Security`。

你可以使用 `Security` 來宣告相依性（就像 `Depends`），但 `Security` 也能接收參數 `scopes`，其為 scopes（字串）的列表。

在這裡，我們將相依函式 `get_current_active_user` 傳給 `Security`（就像使用 `Depends` 一樣）。

但同時也傳入一個 `list` 的 scopes，這裡只有一個 scope：`items`（當然也可以有更多）。

而相依函式 `get_current_active_user` 也能宣告子相依性，不只用 `Depends`，也能用 `Security`。它宣告了自己的子相依函式（`get_current_user`），並加入更多 scope 要求。

在這個例子中，它要求 `me` 這個 scope（也可以要求多個）。

/// note

你不一定需要在不同地方加上不同的 scopes。

我們在這裡這樣做，是為了示範 FastAPI 如何處理在不同層級宣告的 scopes。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | 技術細節

`Security` 其實是 `Depends` 的子類別，僅多了一個我們稍後會看到的參數。

改用 `Security` 而不是 `Depends`，能讓 FastAPI 知道可以宣告安全性 scopes、在內部使用它們，並用 OpenAPI 文件化 API。

另外，當你從 `fastapi` 匯入 `Query`、`Path`、`Depends`、`Security` 等時，實際上它們是回傳特殊類別的函式。

///

## 使用 `SecurityScopes` { #use-securityscopes }

現在更新相依性 `get_current_user`。

上面的相依性就是使用它。

這裡我們使用先前建立的相同 OAuth2 scheme，並將其宣告為相依性：`oauth2_scheme`。

因為此相依函式本身沒有任何 scope 要求，所以我們可以用 `Depends` 搭配 `oauth2_scheme`，當不需要指定安全性 scopes 時就不必用 `Security`。

我們也宣告了一個型別為 `SecurityScopes` 的特殊參數，從 `fastapi.security` 匯入。

這個 `SecurityScopes` 類似於 `Request`（`Request` 用來直接取得請求物件）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## 使用這些 `scopes` { #use-the-scopes }

參數 `security_scopes` 的型別是 `SecurityScopes`。

它會有屬性 `scopes`，包含一個列表，內含此函式本身與所有使用它為子相依性的相依性所要求的所有 scopes。也就是所有「相依者（dependants）」... 這聽起來可能有點混亂，下面會再解釋。

`security_scopes` 物件（類別 `SecurityScopes`）也提供 `scope_str` 屬性，為一個字串，包含那些以空白分隔的 scopes（我們會用到）。

我們建立一個可在多處重複丟出（`raise`）的 `HTTPException`。

在這個例外中，我們把所需的 scopes（若有）以空白分隔的字串形式（透過 `scope_str`）加入，並將該包含 scopes 的字串放在 `WWW-Authenticate` 標頭中（這是規格的一部分）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## 驗證 `username` 與資料結構 { #verify-the-username-and-data-shape }

我們先確認取得了 `username`，並取出 scopes。

接著用 Pydantic 模型驗證這些資料（捕捉 `ValidationError` 例外），若在讀取 JWT token 或用 Pydantic 驗證資料時出錯，就丟出先前建立的 `HTTPException`。

為此，我們更新了 Pydantic 模型 `TokenData`，加入新屬性 `scopes`。

透過 Pydantic 驗證資料，我們可以確保，例如，scopes 正好是 `list` 的 `str`，而 `username` 是 `str`。

否則若是 `dict` 或其他型別，可能在後續某處使應用壞掉，造成安全風險。

我們也會確認該 `username` 對應的使用者是否存在，否則同樣丟出之前建立的例外。

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## 驗證 `scopes` { #verify-the-scopes }

我們現在要驗證，此相依性與所有相依者（包含路徑操作）所要求的所有 scopes，是否都包含在收到的 token 內所提供的 scopes 中；否則就丟出 `HTTPException`。

為此，我們使用 `security_scopes.scopes`，其中包含一個 `list`，列出所有這些 `str` 形式的 scopes。

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 相依性樹與 scopes { #dependency-tree-and-scopes }

我們再回顧一次這個相依性樹與 scopes。

由於 `get_current_active_user` 相依於 `get_current_user`，因此在 `get_current_active_user` 宣告的 `"me"` 這個 scope 會包含在傳給 `get_current_user` 的 `security_scopes.scopes` 的必須 scopes 清單中。

路徑操作本身也宣告了 `"items"` 這個 scope，因此它也會包含在傳給 `get_current_user` 的 `security_scopes.scopes` 中。

以下是相依性與 scopes 的階層關係：

- 路徑操作 `read_own_items` 具有：
  - 需要的 scopes `["items"]`，並有相依性：
  - `get_current_active_user`：
    - 相依函式 `get_current_active_user` 具有：
      - 需要的 scopes `["me"]`，並有相依性：
      - `get_current_user`：
        - 相依函式 `get_current_user` 具有：
          - 自身沒有需要的 scopes。
          - 一個使用 `oauth2_scheme` 的相依性。
          - 一個型別為 `SecurityScopes` 的 `security_scopes` 參數：
            - 這個 `security_scopes` 參數有屬性 `scopes`，其為一個 `list`，包含了上面宣告的所有 scopes，因此：
              - 對於路徑操作 `read_own_items`，`security_scopes.scopes` 會包含 `["me", "items"]`。
              - 對於路徑操作 `read_users_me`，因為它在相依性 `get_current_active_user` 中被宣告，`security_scopes.scopes` 會包含 `["me"]`。
              - 對於路徑操作 `read_system_status`，因為它沒有宣告任何帶 `scopes` 的 `Security`，且其相依性 `get_current_user` 也未宣告任何 `scopes`，所以 `security_scopes.scopes` 會包含 `[]`（空）。

/// tip

這裡重要且「神奇」的是：`get_current_user` 在每個路徑操作中，會有不同的 `scopes` 清單需要檢查。

這完全取決於該路徑操作與其相依性樹中每個相依性所宣告的 `scopes`。

///

## 更多關於 `SecurityScopes` 的細節 { #more-details-about-securityscopes }

你可以在任意位置、多個地方使用 `SecurityScopes`，它不需要位於「根」相依性。

它會永遠帶有對於「該特定」路徑操作與「該特定」相依性樹中，目前 `Security` 相依性所宣告的安全性 scopes（以及所有相依者）：

因為 `SecurityScopes` 會擁有由相依者宣告的所有 scopes，你可以在一個集中式相依函式中用它來驗證 token 是否具有所需 scopes，然後在不同路徑操作中宣告不同的 scope 要求。

它們會在每個路徑操作被各自獨立檢查。

## 試用看看 { #check-it }

如果你打開 API 文件，你可以先驗證並指定你要授權的 scopes。

<img src="/img/tutorial/security/image11.png">

如果你沒有選任何 scope，你仍會「通過驗證」，但當你嘗試存取 `/users/me/` 或 `/users/me/items/` 時，會收到沒有足夠權限的錯誤。你仍能存取 `/status/`。

若你只選了 `me` 而未選 `items`，你能存取 `/users/me/`，但無法存取 `/users/me/items/`。

這就是第三方應用在取得使用者提供的 token 後，嘗試存取上述路徑操作時，會依使用者授與該應用的權限多寡而有不同結果。

## 關於第三方整合 { #about-third-party-integrations }

在這個範例中，我們使用 OAuth2 的「password」流程。

當我們登入自己的應用（可能也有自己的前端）時，這是合適的。

因為我們可以信任它接收 `username` 與 `password`，因為我們掌控它。

但如果你要打造一個讓他人連接的 OAuth2 應用（也就是你要建立一個相當於 Facebook、Google、GitHub 等的身分驗證提供者），你應該使用其他流程之一。

最常見的是 Implicit Flow（隱式流程）。

最安全的是 Authorization Code Flow（授權碼流程），但它需要更多步驟、實作也更複雜。因為較複雜，許多提供者最後會建議使用隱式流程。

/// note

很常見的是，每個身分驗證提供者會用不同的方式命名他們的流程，讓它成為品牌的一部分。

但最終，他們實作的都是相同的 OAuth2 標準。

///

FastAPI 在 `fastapi.security.oauth2` 中提供了所有這些 OAuth2 驗證流程的工具。

## 在裝飾器 `dependencies` 中使用 `Security` { #security-in-decorator-dependencies }

就像你可以在裝飾器的 `dependencies` 參數中定義一個 `Depends` 的 `list` 一樣（詳見[路徑操作裝飾器中的相依性](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}），你也可以在那裡使用帶有 `scopes` 的 `Security`。
