# Header 參數 { #header-parameters }

你可以用與定義 `Query`、`Path`、`Cookie` 參數相同的方式來定義 Header 參數。

## 匯入 `Header` { #import-header }

先匯入 `Header`：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## 宣告 `Header` 參數 { #declare-header-parameters }

接著使用與 `Path`、`Query`、`Cookie` 相同的結構來宣告標頭參數。

你可以設定預設值，以及所有額外的驗證或註解參數：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | 注意

`Header` 與 `Path`、`Query`、`Cookie` 是「姊妹」類別，同樣繼承自共同的 `Param` 類別。

但請記得，當你從 `fastapi` 匯入 `Query`、`Path`、`Header` 等時，它們其實是會回傳特殊類別的函式。

///

/// info | 說明

要宣告標頭，必須使用 `Header`，否則參數會被解讀為查詢參數。

///

## 自動轉換 { #automatic-conversion }

在 `Path`、`Query`、`Cookie` 提供的功能之上，`Header` 還有一些額外的小功能。

大多數標準標頭的單字以連字號（減號，`-`）分隔。

但像 `user-agent` 這樣的變數名稱在 Python 中是無效的。

因此，`Header` 會在預設情況下把參數名稱中的底線（`_`）轉換為連字號（`-`），以便讀取並在文件中顯示該標頭。

此外，HTTP 標頭不區分大小寫，所以你可以使用標準的 Python 命名風格（snake_case）來宣告。

因此，你可以像在 Python 程式中一樣使用 `user_agent`，不需要把首字母大寫成 `User_Agent` 或類似寫法。

若因某些原因需要停用底線自動轉連字號的行為，將 `Header` 的 `convert_underscores` 參數設為 `False`：

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | 警告

在將 `convert_underscores` 設為 `False` 之前，請注意有些 HTTP 代理與伺服器不允許使用帶有底線的標頭。

///

## 重複的標頭 { #duplicate-headers }

有時可能會收到重複的標頭，也就是同一個標頭會有多個值。

可以在型別宣告中使用 list 來定義這種情況。

你會以 Python 的 `list` 形式收到該重複標頭的所有值。

例如，要宣告可以出現多次的 `X-Token` 標頭，可以這樣寫：

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

如果你在與該*路徑操作 (path operation)* 溝通時送出兩個 HTTP 標頭如下：

```
X-Token: foo
X-Token: bar
```

回應會像這樣：

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## 小結 { #recap }

使用 `Header` 宣告標頭，套用與 `Query`、`Path`、`Cookie` 相同的通用模式。

而且別擔心變數名稱中的底線，**FastAPI** 會自動幫你轉換。
