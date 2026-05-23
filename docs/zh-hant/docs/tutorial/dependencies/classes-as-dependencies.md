# 以類別作為相依性 { #classes-as-dependencies }

在更深入了解 **相依性注入（Dependency Injection）** 系統之前，我們先把前一個範例升級一下。

## 前一個範例中的 `dict` { #a-dict-from-the-previous-example }

在前一個範例中，我們從相依項（"dependable"）回傳了一個 `dict`：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

但接著我們在路徑操作函式（*path operation function*）的參數 `commons` 中取得的是一個 `dict`。

而我們知道，編輯器對 `dict` 無法提供太多輔助（例如自動完成），因為它無法預先知道其中的鍵與值的型別。

我們可以做得更好...

## 什麼算是相依性 { #what-makes-a-dependency }

到目前為止，你看到的相依性都是宣告成函式。

但那不是宣告相依性的唯一方式（雖然那大概是最常見的）。

關鍵在於，相依性應該要是「callable」。

在 Python 中，「**callable**」指的是任何可以像函式一樣被 Python「呼叫」的東西。

因此，如果你有一個物件 `something`（它可能不是函式），而你可以像這樣「呼叫」（執行）它：

```Python
something()
```

或是

```Python
something(some_argument, some_keyword_argument="foo")
```

那它就是一個「callable」。

## 以類別作為相依性 { #classes-as-dependencies_1 }

你可能已經注意到，建立一個 Python 類別的實例時，你用的語法也是一樣的。

例如：

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在這個例子中，`fluffy` 是 `Cat` 類別的一個實例。

而要建立 `fluffy`，你其實是在「呼叫」`Cat`。

所以，Python 類別本身也是一種 **callable**。

因此，在 **FastAPI** 中，你可以將 Python 類別作為相依性。

FastAPI 其實檢查的是它是否為「callable」（函式、類別或其他），以及它所定義的參數。

如果你在 **FastAPI** 中傳入一個「callable」作為相依性，FastAPI 會分析該「callable」的參數，並以與路徑操作函式參數相同的方式來處理它們，包括子相依性。

這也適用於完全沒有參數的 callable，就和沒有參數的路徑操作函式一樣。

接著，我們可以把上面的相依項（dependable）`common_parameters` 改成類別 `CommonQueryParams`：

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

注意用來建立該類別實例的 `__init__` 方法：

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...它的參數與我們之前的 `common_parameters` 相同：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

**FastAPI** 會用這些參數來「解析」該相依性。

兩種情況下都會有：

- 一個可選的查詢參數 `q`，型別為 `str`。
- 一個查詢參數 `skip`，型別為 `int`，預設為 `0`。
- 一個查詢參數 `limit`，型別為 `int`，預設為 `100`。

兩種情況下，資料都會被轉換、驗證，並記錄到 OpenAPI schema 中等。

## 如何使用 { #use-it }

現在你可以用這個類別來宣告你的相依性。

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** 會呼叫 `CommonQueryParams` 類別。這會建立該類別的一個「實例」，而該實例會以參數 `commons` 的形式傳給你的函式。

## 型別註解與 `Depends` { #type-annotation-vs-depends }

注意上面程式碼裡我們寫了兩次 `CommonQueryParams`：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

最後面的 `CommonQueryParams`，在：

```Python
... Depends(CommonQueryParams)
```

...才是 **FastAPI** 實際用來知道相依性是什麼的依據。

FastAPI 會從這個物件中提取宣告的參數，並且實際呼叫它。

---

在這個例子中，前面的 `CommonQueryParams`，於：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams ...
```

////

...對 **FastAPI** 來說沒有任何特殊意義。FastAPI 不會用它來做資料轉換、驗證等（因為這部分由 `Depends(CommonQueryParams)` 處理）。

其實你可以只寫：

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons = Depends(CommonQueryParams)
```

////

...像是：

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

但仍建議宣告型別，這樣你的編輯器就知道會以何種型別作為參數 `commons` 傳入，進而幫助你做自動完成、型別檢查等：

<img src="/img/tutorial/dependencies/image02.png">

## 捷徑 { #shortcut }

不過你會發現這裡有些重複程式碼，我們寫了兩次 `CommonQueryParams`：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** 為這類情況提供了一個捷徑：當相依性「明確」是一個類別，且 **FastAPI** 會「呼叫」它來建立該類別的實例時。

對這些特定情況，你可以這樣做：

不要寫：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...而是改為：

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ 非 Annotated

/// tip

如有可能，優先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends()
```

////

你把相依性宣告為參數的型別，並使用不帶任何參數的 `Depends()`，而不用在 `Depends(CommonQueryParams)` 裡「再」寫一次整個類別。

整個範例就會變成：

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...而 **FastAPI** 會知道該怎麼做。

/// tip

如果你覺得這樣比幫助更令人困惑，那就忽略它吧，你並不「需要」這個技巧。

這只是個捷徑。因為 **FastAPI** 在意幫你減少重複的程式碼。

///
