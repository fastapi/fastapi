# 路徑參數與數值驗證 { #path-parameters-and-numeric-validations }

就像使用 `Query` 為查詢參數宣告更多驗證與中繼資料一樣，你也可以用 `Path` 為路徑參數宣告相同類型的驗證與中繼資料。

## 匯入 `Path` { #import-path }

首先，從 `fastapi` 匯入 `Path`，並匯入 `Annotated`：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info

FastAPI 在 0.95.0 版加入並開始推薦使用 `Annotated`。

如果你使用更舊的版本，嘗試使用 `Annotated` 會出錯。

請確保在使用 `Annotated` 前，先[升級 FastAPI 版本](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}到至少 0.95.1。

///

## 宣告中繼資料 { #declare-metadata }

你可以宣告與 `Query` 相同的所有參數。

例如，若要為路徑參數 `item_id` 宣告 `title` 中繼資料，可以這樣寫：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note

路徑參數一定是必填，因為它必須是路徑的一部分。即使你將其宣告為 `None` 或設定預設值，也不會有任何影響，它仍然是必填。

///

## 依需求調整參數順序 { #order-the-parameters-as-you-need }

/// tip

如果你使用 `Annotated`，這點大概沒那麼重要或必要。

///

假設你想把查詢參數 `q` 宣告為必要的 `str`。

而你不需要為該參數宣告其他內容，所以其實不需要用 `Query`。

但你仍需要為路徑參數 `item_id` 使用 `Path`，而且基於某些理由你不想用 `Annotated`。

如果你把有「預設值」的參數放在沒有「預設值」的參數之前，Python 會抱怨。

但你可以調整它們的順序，先放沒有預設值（查詢參數 `q`）的參數。

對 **FastAPI** 來說沒差。它會依參數名稱、型別與預設宣告（`Query`、`Path` 等）來辨識參數，並不在意順序。

因此，你可以這樣宣告你的函式：

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

但請記住，若使用 `Annotated`，你就不會有這個問題，因為你不是用函式參數預設值來放 `Query()` 或 `Path()`。

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## 依需求調整參數順序的技巧 { #order-the-parameters-as-you-need-tricks }

/// tip

如果你使用 `Annotated`，這點大概沒那麼重要或必要。

///

這裡有個小技巧偶爾很好用，不過你大概不常需要。

如果你想要：

* 不用 `Query`、也不給預設值就宣告查詢參數 `q`
* 使用 `Path` 宣告路徑參數 `item_id`
* 讓它們的順序不同
* 不使用 `Annotated`

…Python 有個小語法可以做到。

在函式的參數列表最前面放一個 `*`。

Python 不會對這個 `*` 做任何事，但它會知道後續的所有參數都必須以關鍵字引數（key-value pairs）方式呼叫，也就是所謂的 <abbr title="源自：K-ey W-ord Arg-uments - 關鍵字參數"><code>kwargs</code></abbr>。即便它們沒有預設值也一樣。

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### 使用 `Annotated` 更好 { #better-with-annotated }

記住，如果你使用 `Annotated`，因為不是用函式參數預設值，所以你不會遇到這個問題，也可能不需要使用 `*`。

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## 數值驗證：大於或等於 { #number-validations-greater-than-or-equal }

使用 `Query` 和 `Path`（以及你之後會看到的其他類別）可以宣告數值限制。

這裡用 `ge=1`，代表 `item_id` 必須是「大於（`g`reater）或等於（`e`qual）」`1` 的整數。

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## 數值驗證：大於與小於或等於 { #number-validations-greater-than-and-less-than-or-equal }

同樣也適用於：

* `gt`：大於（`g`reater `t`han）
* `le`：小於或等於（`l`ess than or `e`qual）

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## 數值驗證：浮點數、大於與小於 { #number-validations-floats-greater-than-and-less-than }

數值驗證也適用於 `float`。

這時就能看出能宣告 <abbr title="greater than - 大於"><code>gt</code></abbr>（不只是 <abbr title="greater than or equal - 大於或等於"><code>ge</code></abbr>）的重要性。因為你可以要求數值必須大於 `0`，即便它小於 `1`。

所以，`0.5` 是有效的值，但 `0.0` 或 `0` 則無效。

<abbr title="less than - 小於"><code>lt</code></abbr> 也是同樣的道理。

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## 小結 { #recap }

使用 `Query`、`Path`（以及你尚未看到的其他類別）時，你可以像在[查詢參數與字串驗證](query-params-str-validations.md){.internal-link target=_blank}中一樣，宣告中繼資料與字串驗證。

你也可以宣告數值驗證：

* `gt`：大於（`g`reater `t`han）
* `ge`：大於或等於（`g`reater than or `e`qual）
* `lt`：小於（`l`ess `t`han）
* `le`：小於或等於（`l`ess than or `e`qual）

/// info

你之後會看到的 `Query`、`Path` 與其他類別，都是共同父類別 `Param` 的子類別。

它們共享你已經看到的那些用於額外驗證與中繼資料的參數。

///

/// note | 技術細節

當你從 `fastapi` 匯入 `Query`、`Path` 等時，它們其實是函式。

呼叫它們時，會回傳同名類別的實例。

也就是說，你匯入的是名為 `Query` 的函式，而當你呼叫它時，它會回傳同名的 `Query` 類別實例。

這些函式之所以存在（而不是直接使用類別），是為了避免編輯器標記它們的型別錯誤。

如此一來，你就能使用一般的編輯器與開發工具，而不需要額外設定來忽略那些錯誤。

///
