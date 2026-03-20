# 額外的模型 { #extra-models }

延續前一個範例，通常會有不只一個彼此相關的模型。

對使用者模型尤其如此，因為：

* 「輸入模型」需要能包含密碼。
* 「輸出模型」不應包含密碼。
* 「資料庫模型」通常需要儲存雜湊後的密碼。

/// danger

切勿儲存使用者的明文密碼。務必只儲存可供驗證的「安全雜湊」。

若你還不清楚，稍後會在[安全性章節](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}學到什麼是「密碼雜湊」。

///

## 多個模型 { #multiple-models }

以下是模型大致長相、與其密碼欄位以及它們被使用的位置：

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### 關於 `**user_in.model_dump()` { #about-user-in-model-dump }

#### Pydantic 的 `.model_dump()` { #pydantics-model-dump }

`user_in` 是一個 `UserIn` 類別的 Pydantic 模型。

Pydantic 模型有 `.model_dump()` 方法，會回傳包含該模型資料的 `dict`。

因此，若我們建立一個 Pydantic 物件 `user_in` 如：

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

接著呼叫：

```Python
user_dict = user_in.model_dump()
```

此時變數 `user_dict` 會是一個承載資料的 `dict`（也就是 `dict`，而非 Pydantic 模型物件）。

若再呼叫：

```Python
print(user_dict)
```

我們會得到一個 Python `dict`：

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 解包 `dict` { #unpacking-a-dict }

若將像 `user_dict` 這樣的 `dict` 以 `**user_dict` 傳給函式（或類別），Python 會將其「解包」，把 `user_dict` 的鍵和值直接當作具名引數傳入。

因此，延續上面的 `user_dict`，寫成：

```Python
UserInDB(**user_dict)
```

效果等同於：

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

更精確地說，直接使用 `user_dict`（未來內容可能有所不同）則等同於：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 由另一個模型內容建立 Pydantic 模型 { #a-pydantic-model-from-the-contents-of-another }

如上例我們從 `user_in.model_dump()` 得到 `user_dict`，以下程式碼：

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

等同於：

```Python
UserInDB(**user_in.model_dump())
```

...因為 `user_in.model_dump()` 回傳的是 `dict`，接著在傳給 `UserInDB` 時以 `**` 前綴讓 Python 進行解包。

因此，我們可以用一個 Pydantic 模型的資料建立另一個 Pydantic 模型。

#### 解包 `dict` 並加入額外參數 { #unpacking-a-dict-and-extra-keywords }

接著加入額外的具名引數 `hashed_password=hashed_password`，如下：

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...結果等同於：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning

輔助函式 `fake_password_hasher` 與 `fake_save_user` 只是用來示範資料流程，並不提供任何實際的安全性。

///

## 減少重複 { #reduce-duplication }

減少程式碼重複是 FastAPI 的核心理念之一。

因為重複的程式碼會提高發生錯誤、安全性問題、程式不同步（某處更新但其他處未更新）等風險。

而這些模型共享大量資料，重複了屬性名稱與型別。

我們可以做得更好。

我們可以宣告一個作為基底的 `UserBase` 模型，其他模型繼承它成為子類別，沿用其屬性（型別宣告、驗證等）。

所有資料轉換、驗證、文件產生等仍可正常運作。

如此一來，我們只需要宣告模型之間的差異（含明文 `password`、含 `hashed_password`、或不含密碼）：

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 或 `anyOf` { #union-or-anyof }

你可以將回應宣告為多個型別的 `Union`，表示回應可能是其中任一型別。

在 OpenAPI 中會以 `anyOf` 定義。

要達成這點，使用標準的 Python 型別提示 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>：

/// note

在定義 <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> 時，請先放置「更具體」的型別，再放「較不具體」的型別。以下範例中，較具體的 `PlaneItem` 置於 `CarItem` 之前：`Union[PlaneItem, CarItem]`。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 中的 `Union` { #union-in-python-3-10 }

此範例中，我們將 `Union[PlaneItem, CarItem]` 作為引數 `response_model` 的值。

由於這裡是把它當作引數的「值」傳入，而非用於型別註記，因此即使在 Python 3.10 也必須使用 `Union`。

若用於型別註記，則可以使用直線（|），如下：

```Python
some_variable: PlaneItem | CarItem
```

但若寫成指定值 `response_model=PlaneItem | CarItem` 會發生錯誤，因為 Python 會嘗試在 `PlaneItem` 與 `CarItem` 之間執行「無效運算」，而非將其視為型別註記。

## 模型的清單 { #list-of-models }

同樣地，你可以將回應宣告為物件的 `list`。

為此，使用標準的 Python `list`：

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## 以任意 `dict` 作為回應 { #response-with-arbitrary-dict }

你也可以用一般的任意 `dict` 宣告回應，只需指定鍵和值的型別，而不必使用 Pydantic 模型。

當你事先不知道可用的欄位／屬性名稱（定義 Pydantic 模型所需）時，這很實用。

此時可使用 `dict`：

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## 重點回顧 { #recap }

依情境使用多個 Pydantic 模型並靈活繼承。

當一個實體需要呈現不同「狀態」時，不必侷限於一個資料模型。例如使用者這個實體，可能有包含 `password`、包含 `password_hash`，或不含密碼等不同狀態。
