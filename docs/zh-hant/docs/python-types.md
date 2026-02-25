# Python 型別入門 { #python-types-intro }

Python 支援可選用的「型別提示」（也稱為「型別註記」）。

這些「型別提示」或註記是一種特殊語法，用來宣告變數的<dfn title="例如：str、int、float、bool">型別</dfn>。

為你的變數宣告型別後，編輯器與工具就能提供更好的支援。

這裡只是關於 Python 型別提示的快速教學／複習。它只涵蓋使用在 **FastAPI** 時所需的最低限度...其實非常少。

**FastAPI** 完全是以這些型別提示為基礎，並因此帶來許多優勢與好處。

但就算你從不使用 **FastAPI**，學一點型別提示也會有幫助。

/// note | 注意

如果你是 Python 專家，而且已經完全了解型別提示，可以直接跳到下一章。

///

## 動機 { #motivation }

先從一個簡單的例子開始：

{* ../../docs_src/python_types/tutorial001_py310.py *}

執行這個程式會輸出：

```
John Doe
```

這個函式會做以下事情：

* 接收 `first_name` 與 `last_name`。
* 用 `title()` 把每個字的第一個字母轉成大寫。
* 用一個空白把它們<dfn title="把它們合在一起，成為一個。將其中一個的內容接在另一個後面。">串接</dfn>起來。

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### 編輯它 { #edit-it }

這是一個非常簡單的程式。

但現在想像你正從零開始寫它。

在某個時間點你會開始定義函式，參數都準備好了...

接著你需要呼叫「那個把第一個字母轉大寫的方法」。

是 `upper`？還是 `uppercase`？`first_uppercase`？`capitalize`？

然後你試著用老牌程式設計師的好朋友——編輯器自動完成。

你輸入函式的第一個參數 `first_name`，接著打一個點（`.`），然後按下 `Ctrl+Space` 觸發自動完成。

但很遺憾，你什麼有用的也沒得到：

<img src="/img/python-types/image01.png">

### 加上型別 { #add-types }

我們來修改前一版中的一行。

我們只要把函式參數這一段，從：

```Python
    first_name, last_name
```

改成：

```Python
    first_name: str, last_name: str
```

就這樣。

那些就是「型別提示」：

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

這和宣告預設值不同，例如：

```Python
    first_name="john", last_name="doe"
```

這是不同的東西。

我們使用的是冒號（`:`），不是等號（`=`）。

而且加上型別提示通常不會改變執行結果，和不加時是一樣的。

不過現在，想像你又在撰寫那個函式，但這次有型別提示。

在同樣的地方，你按 `Ctrl+Space` 嘗試自動完成，然後你會看到：

<img src="/img/python-types/image02.png">

有了這些，你可以往下捲動查看選項，直到找到一個「看起來眼熟」的：

<img src="/img/python-types/image03.png">

## 更多動機 { #more-motivation }

看這個函式，它已經有型別提示了：

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

因為編輯器知道變數的型別，你不只會得到自動完成，還會得到錯誤檢查：

<img src="/img/python-types/image04.png">

現在你知道要修正它，把 `age` 用 `str(age)` 轉成字串：

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## 宣告型別 { #declaring-types }

你剛剛看到宣告型別提示的主要位置：函式參數。

這也是你在 **FastAPI** 中最常使用它們的地方。

### 簡單型別 { #simple-types }

你可以宣告所有標準的 Python 型別，不只 `str`。

例如你可以用：

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` 模組 { #typing-module }

在一些其他情境中，你可能需要從標準程式庫的 `typing` 模組匯入一些東西，比如當你想宣告某個東西可以是「任何型別」時，可以用 `typing` 裡的 `Any`：

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### 泛型（Generic types） { #generic-types }

有些型別可以在方括號中接收「型別參數」，以定義其內部元素的型別，例如「字串的 list」可以宣告為 `list[str]`。

這些能接收型別參數的型別稱為「泛型（Generic types）」或「Generics」。

你可以將相同的內建型別用作泛型（使用方括號並在裡面放型別）：

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

例如，讓我們定義一個變數是 `str` 的 `list`。

宣告變數，使用相同的冒號（`:`）語法。

型別填 `list`。

由於 list 是一種包含內部型別的型別，你要把內部型別放在方括號中：

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | 資訊

方括號裡的那些內部型別稱為「型別參數」。

在這個例子中，`str` 是傳給 `list` 的型別參數。

///

這表示：「變數 `items` 是一個 `list`，而這個清單中的每個元素都是 `str`」。

這麼做之後，你的編輯器甚至在處理清單裡的項目時也能提供支援：

<img src="/img/python-types/image05.png">

沒有型別時，幾乎不可能做到這點。

請注意，變數 `item` 是清單 `items` 中的一個元素。

即便如此，編輯器仍然知道它是 `str`，並提供相應的支援。

#### Tuple 與 Set { #tuple-and-set }

你也可以用相同方式來宣告 `tuple` 與 `set`：

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

這代表：

* 變數 `items_t` 是一個有 3 個項目的 `tuple`，分別是 `int`、`int` 和 `str`。
* 變數 `items_s` 是一個 `set`，而其中每個項目都是 `bytes` 型別。

#### Dict { #dict }

定義 `dict` 時，你需要傳入 2 個以逗號分隔的型別參數。

第一個型別參數是 `dict` 的鍵（key）。

第二個型別參數是 `dict` 的值（value）：

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

這代表：

* 變數 `prices` 是個 `dict`：
    * 這個 `dict` 的鍵是 `str`（例如每個項目的名稱）。
    * 這個 `dict` 的值是 `float`（例如每個項目的價格）。

#### Union { #union }

你可以宣告一個變數可以是「多種型別」中的任一種，例如 `int` 或 `str`。

要這麼定義，你使用<dfn title='也稱為「位元或運算子」，但在這裡與該含義無關'>豎線（`|`）</dfn>來分隔兩種型別。

這稱為「union」，因為變數可以是這兩種型別集合的聯集中的任一種。

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

這表示 `item` 可以是 `int` 或 `str`。

#### 可能為 `None` { #possibly-none }

你可以宣告某個值可以是某個型別（例如 `str`），但它也可能是 `None`。

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

使用 `str | None` 而不是單純的 `str`，可以讓編輯器幫你偵測錯誤，例如你以為某個值一定是 `str`，但它其實也可能是 `None`。

### 類別作為型別 { #classes-as-types }

你也可以用類別來宣告變數的型別。

假設你有一個 `Person` 類別，帶有名稱：

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

接著你可以宣告一個變數為 `Person` 型別：

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

然後，你一樣會得到完整的編輯器支援：

<img src="/img/python-types/image06.png">

請注意，這表示「`one_person` 是類別 `Person` 的『實例（instance）』」。

並不是「`one_person` 就是名為 `Person` 的『類別（class）』」。

## Pydantic 模型 { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 是一個用來做資料驗證的 Python 程式庫。

你以帶有屬性的類別來宣告資料的「形狀」。

而每個屬性都有其型別。

接著你用一些值建立這個類別的實例，它會驗證這些值、在需要時把它們轉換成適當的型別，然後回給你一個包含所有資料的物件。

你也會對這個產生的物件得到完整的編輯器支援。

以下是來自 Pydantic 官方文件的例子：

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | 資訊

想了解更多 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic，請查看它的文件</a>。

///

**FastAPI** 完全是以 Pydantic 為基礎。

你會在[教學 - 使用者指南](tutorial/index.md){.internal-link target=_blank}中看到更多實際範例。

## 含中繼資料的型別提示 { #type-hints-with-metadata-annotations }

Python 也有一個功能，允許使用 `Annotated` 在這些型別提示中放入額外的<dfn title="關於資料的資料；在此情境下，是關於型別的資訊，例如描述。">中繼資料</dfn>。

你可以從 `typing` 匯入 `Annotated`。

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python 本身不會對這個 `Annotated` 做任何事。對編輯器與其他工具而言，該型別仍然是 `str`。

但你可以利用 `Annotated` 這個空間，來提供 **FastAPI** 額外的中繼資料，告訴它你希望應用程式如何運作。

重要的是要記住，傳給 `Annotated` 的「第一個型別參數」才是「真正的型別」。其餘的，都是給其他工具用的中繼資料。

目前你只需要知道 `Annotated` 的存在，而且它是標準的 Python。😎

之後你會看到它有多「強大」。

/// tip | 提示

因為這是「標準 Python」，所以你在編輯器、分析與重構程式碼的工具等方面，仍然能獲得「最佳的開發體驗」。✨

而且你的程式碼也會與許多其他 Python 工具與程式庫非常相容。🚀

///

## 在 **FastAPI** 中的型別提示 { #type-hints-in-fastapi }

**FastAPI** 善用這些型別提示來完成多項工作。

在 **FastAPI** 中，你用型別提示來宣告參數，然後你會得到：

* 編輯器支援
* 型別檢查

...而 **FastAPI** 也會用同樣的宣告來：

* 定義需求：來自請求的路徑參數、查詢參數、標頭、主體（body）、相依性等
* 轉換資料：把請求中的資料轉成所需型別
* 驗證資料：來自每個請求的資料：
    * 當資料無效時，自動產生錯誤並回傳給用戶端
* 使用 OpenAPI 書寫 API 文件：
    * 之後會由自動的互動式文件介面所使用

這些現在聽起來可能有點抽象。別擔心。你會在[教學 - 使用者指南](tutorial/index.md){.internal-link target=_blank}中看到它們的實際運作。

重點是，透過在單一位置使用標準的 Python 型別（而不是新增更多類別、裝飾器等），**FastAPI** 會幫你完成很多工作。

/// info | 資訊

如果你已經完整讀完整個教學，並回來想多看一些關於型別的內容，一個不錯的資源是 <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy` 的「小抄」</a>。

///
