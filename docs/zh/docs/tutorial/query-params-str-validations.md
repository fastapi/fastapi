# 查询参数和字符串校验 { #query-parameters-and-string-validations }

**FastAPI** 允许你为参数声明额外的信息和校验。

让我们以下面的应用为例：

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

查询参数 `q` 的类型为 `str | None`，这意味着它是 `str` 类型，但也可以是 `None`。其默认值确实为 `None`，所以 FastAPI 会知道它不是必填的。

/// note | 注意

FastAPI 会因为默认值 `= None` 而知道 `q` 的值不是必填的。

将类型标注为 `str | None` 能让你的编辑器提供更好的辅助和错误检测。

///

## 额外校验 { #additional-validation }

我们打算添加约束：即使 `q` 是可选的，但只要提供了该参数，**其长度不能超过 50 个字符**。

### 导入 `Query` 和 `Annotated` { #import-query-and-annotated }

为此，先导入：

- 从 `fastapi` 导入 `Query`
- 从 `typing` 导入 `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | 信息

FastAPI 在 0.95.0 版本中添加了对 `Annotated` 的支持（并开始推荐使用）。

如果你的版本更旧，使用 `Annotated` 会报错。

在使用 `Annotated` 之前，请确保先[升级 FastAPI 版本](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}到至少 0.95.1。

///

## 在 `q` 参数的类型中使用 `Annotated` { #use-annotated-in-the-type-for-the-q-parameter }

还记得我之前在[Python 类型简介](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}中说过可以用 `Annotated` 给参数添加元数据吗？

现在正是与 FastAPI 搭配使用它的时候。🚀

我们之前的类型标注是：

```Python
q: str | None = None
```

我们要做的是用 `Annotated` 把它包起来，变成：

```Python
q: Annotated[str | None] = None
```

这两种写法含义相同，`q` 是一个可以是 `str` 或 `None` 的参数，默认是 `None`。

现在进入更有趣的部分。🎉

## 在 `q` 的 `Annotated` 中添加 `Query` { #add-query-to-annotated-in-the-q-parameter }

有了 `Annotated` 之后，我们就可以放入更多信息（本例中是额外的校验）。在 `Annotated` 中添加 `Query`，并把参数 `max_length` 设为 `50`：

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

注意默认值依然是 `None`，所以该参数仍是可选的。

但现在把 `Query(max_length=50)` 放到 `Annotated` 里，我们就在告诉 FastAPI，这个值需要**额外校验**，最大长度为 50 个字符。😎

/// tip | 提示

这里用的是 `Query()`，因为这是一个**查询参数**。稍后我们还会看到 `Path()`、`Body()`、`Header()` 和 `Cookie()`，它们也接受与 `Query()` 相同的参数。

///

FastAPI 现在会：

- 对数据进行**校验**，确保最大长度为 50 个字符
- 当数据无效时向客户端展示**清晰的错误**
- 在 OpenAPI 模式的*路径操作*中**记录**该参数（因此会出现在**自动文档 UI** 中）

## 另一种（旧的）方式：把 `Query` 作为默认值 { #alternative-old-query-as-the-default-value }

早期版本的 FastAPI（<dfn title="早于 2023-03">0.95.0</dfn> 之前）要求你把 `Query` 作为参数的默认值，而不是放在 `Annotated` 里。你很可能会在别处看到这种写法，所以我也给你解释一下。

/// tip | 提示

对于新代码以及在可能的情况下，请按上文所述使用 `Annotated`。它有多项优势（如下所述），没有劣势。🍰

///

像这样把 `Query()` 作为函数参数的默认值，并把参数 `max_length` 设为 50：

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

由于这种情况下（不使用 `Annotated`）我们必须把函数中的默认值 `None` 替换为 `Query()`，因此需要通过参数 `Query(default=None)` 来设置默认值，它起到同样的作用（至少对 FastAPI 来说）。

所以：

```Python
q: str | None = Query(default=None)
```

……会让参数变成可选，默认值为 `None`，等同于：

```Python
q: str | None = None
```

但使用 `Query` 的版本会显式把它声明为一个查询参数。

然后，我们可以向 `Query` 传入更多参数。本例中是适用于字符串的 `max_length` 参数：

```Python
q: str | None = Query(default=None, max_length=50)
```

这会校验数据、在数据无效时展示清晰的错误，并在 OpenAPI 模式的*路径操作*中记录该参数。

### 在默认值中使用 `Query` 或在 `Annotated` 中使用 `Query` { #query-as-the-default-value-or-in-annotated }

注意，当你在 `Annotated` 中使用 `Query` 时，不能再给 `Query` 传 `default` 参数。

相反，应使用函数参数本身的实际默认值。否则会不一致。

例如，下面这样是不允许的：

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

……因为不清楚默认值应该是 `"rick"` 还是 `"morty"`。

因此，你应该这样用（推荐）：

```Python
q: Annotated[str, Query()] = "rick"
```

……或者在旧代码库中你会见到：

```Python
q: str = Query(default="rick")
```

### `Annotated` 的优势 { #advantages-of-annotated }

**推荐使用 `Annotated`**，而不是把 `Query` 放在函数参数的默认值里，这样做在多方面都**更好**。🤓

函数参数的**默认值**就是**真正的默认值**，这与 Python 的直觉更一致。😌

你可以在**其他地方**不通过 FastAPI **直接调用**这个函数，而且它会**按预期工作**。如果有**必填**参数（没有默认值），你的**编辑器**会报错提示；如果在运行时没有传入必填参数，**Python** 也会报错。

当你不使用 `Annotated` 而是使用**（旧的）默认值风格**时，如果你在**其他地方**不通过 FastAPI 调用该函数，你必须**记得**给函数传参，否则得到的值会和预期不同（例如得到 `QueryInfo` 之类的对象而不是 `str`）。而你的编辑器不会报错，Python 也不会在调用时报错，只有在函数内部的操作出错时才会暴露问题。

由于 `Annotated` 可以包含多个元数据标注，你甚至可以用同一个函数与其他工具配合，例如 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>。🚀

## 添加更多校验 { #add-more-validations }

你还可以添加 `min_length` 参数：

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 添加正则表达式 { #add-regular-expressions }

你可以定义一个参数必须匹配的 <dfn title="正则表达式（regex 或 regexp）是用于定义字符串搜索模式的字符序列。">正则表达式</dfn> `pattern`：

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

这个特定的正则表达式通过以下规则检查接收到的参数值：

- `^`：必须以接下来的字符开头，前面没有其他字符。
- `fixedquery`：值必须精确等于 `fixedquery`。
- `$`：到此结束，在 `fixedquery` 之后没有更多字符。

如果你对这些**「正则表达式」**概念感到迷茫，不必担心。对很多人来说这都是个难点。你仍然可以在不使用正则表达式的情况下做很多事情。

现在你知道了，一旦需要时，你可以在 **FastAPI** 中直接使用它们。

## 默认值 { #default-values }

当然，你也可以使用 `None` 以外的默认值。

假设你想要声明查询参数 `q` 的 `min_length` 为 `3`，并且默认值为 `"fixedquery"`：

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | 注意

任何类型的默认值（包括 `None`）都会让该参数变为可选（非必填）。

///

## 必填参数 { #required-parameters }

当我们不需要声明更多校验或元数据时，只需不声明默认值就可以让查询参数 `q` 成为必填参数，例如：

```Python
q: str
```

而不是：

```Python
q: str | None = None
```

但现在我们用 `Query` 来声明它，例如：

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

因此，在使用 `Query` 的同时需要把某个值声明为必填时，只需不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### 必填，但可以为 `None` { #required-can-be-none }

你可以声明一个参数可以接收 `None`，但它仍然是必填的。这将强制客户端必须发送一个值，即使该值是 `None`。

为此，你可以声明 `None` 是有效类型，但不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## 查询参数列表 / 多个值 { #query-parameter-list-multiple-values }

当你用 `Query` 显式地定义查询参数时，你还可以声明它接收一个值列表，换句话说，接收多个值。

例如，要声明一个可在 URL 中出现多次的查询参数 `q`，你可以这样写：

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

然后，访问如下 URL：

```
http://localhost:8000/items/?q=foo&q=bar
```

你会在*路径操作函数*的*函数参数* `q` 中以一个 Python `list` 的形式接收到多个 `q` *查询参数* 的值（`foo` 和 `bar`）。

因此，该 URL 的响应将会是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | 提示

要声明类型为 `list` 的查询参数（如上例），你需要显式地使用 `Query`，否则它会被解释为请求体。

///

交互式 API 文档会相应更新，以支持多个值：

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 具有默认值的查询参数列表 / 多个值 { #query-parameter-list-multiple-values-with-defaults }

你还可以定义在没有给定值时的默认 `list`：

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

如果你访问：

```
http://localhost:8000/items/
```

`q` 的默认值将为：`["foo", "bar"]`，你的响应会是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### 只使用 `list` { #using-just-list }

你也可以直接使用 `list`，而不是 `list[str]`：

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | 注意

请记住，在这种情况下 FastAPI 不会检查列表的内容。

例如，`list[int]` 会检查（并记录到文档）列表的内容必须是整数。但仅用 `list` 不会。

///

## 声明更多元数据 { #declare-more-metadata }

你可以添加更多有关该参数的信息。

这些信息会包含在生成的 OpenAPI 中，并被文档用户界面和外部工具使用。

/// note | 注意

请记住，不同的工具对 OpenAPI 的支持程度可能不同。

其中一些可能还不会展示所有已声明的额外信息，尽管在大多数情况下，缺失的功能已经在计划开发中。

///

你可以添加 `title`：

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

以及 `description`：

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## 别名参数 { #alias-parameters }

假设你想要参数名为 `item-query`。

像这样：

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

但 `item-query` 不是有效的 Python 变量名。

最接近的有效名称是 `item_query`。

但你仍然需要它在 URL 中就是 `item-query`……

这时可以用 `alias` 参数声明一个别名，FastAPI 会用该别名在 URL 中查找参数值：

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## 弃用参数 { #deprecating-parameters }

现在假设你不再喜欢这个参数了。

由于还有客户端在使用它，你不得不保留一段时间，但你希望文档清楚地将其展示为<dfn title="已过时，不推荐使用">已弃用</dfn>。

那么将参数 `deprecated=True` 传给 `Query`：

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

文档将会像下面这样展示它：

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 从 OpenAPI 中排除参数 { #exclude-parameters-from-openapi }

要把某个查询参数从生成的 OpenAPI 模式中排除（从而也不会出现在自动文档系统中），将 `Query` 的参数 `include_in_schema` 设为 `False`：

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## 自定义校验 { #custom-validation }

有些情况下你需要做一些无法通过上述参数完成的**自定义校验**。

在这些情况下，你可以使用**自定义校验函数**，该函数会在正常校验之后应用（例如，在先校验值是 `str` 之后）。

你可以在 `Annotated` 中使用 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic 的 `AfterValidator`</a> 来实现。

/// tip | 提示

Pydantic 还有 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> 等。🤓

///

例如，这个自定义校验器会检查条目 ID 是否以 `isbn-`（用于 <abbr title="International Standard Book Number - 国际标准书号">ISBN</abbr> 书号）或 `imdb-`（用于 <abbr title="Internet Movie Database - 互联网电影数据库: 一个包含电影信息的网站">IMDB</abbr> 电影 URL 的 ID）开头：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | 信息

这在 Pydantic 2 或更高版本中可用。😎

///

/// tip | 提示

如果你需要进行任何需要与**外部组件**通信的校验，例如数据库或其他 API，你应该改用 **FastAPI 依赖项**，稍后你会学到它们。

这些自定义校验器用于只需检查请求中**同一份数据**即可完成的事情。

///

### 理解这段代码 { #understand-that-code }

关键点仅仅是：在 `Annotated` 中使用带函数的 **`AfterValidator`**。不感兴趣可以跳过这一节。🤸

---

但如果你对这个具体示例好奇，并且还愿意继续看，这里有一些额外细节。

#### 字符串与 `value.startswith()` { #string-with-value-startswith }

注意到了吗？字符串的 `value.startswith()` 可以接收一个元组，它会检查元组中的每个值：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### 一个随机条目 { #a-random-item }

使用 `data.items()` 我们会得到一个包含每个字典项键和值的元组的 <dfn title="可以用 for 循环迭代的对象，例如 list、set 等">可迭代对象</dfn>。

我们用 `list(data.items())` 把这个可迭代对象转换成一个真正的 `list`。

然后用 `random.choice()` 可以从该列表中获取一个**随机值**，也就是一个 `(id, name)` 的元组。它可能像 `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` 这样。

接着我们把这个元组的**两个值**分别赋给变量 `id` 和 `name`。

所以，即使用户没有提供条目 ID，他们仍然会收到一个随机推荐。

……而我们把这些都放在**一行简单的代码**里完成。🤯 你不爱 Python 吗？🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## 总结 { #recap }

你可以为参数声明额外的校验和元数据。

通用的校验和元数据：

- `alias`
- `title`
- `description`
- `deprecated`

字符串特有的校验：

- `min_length`
- `max_length`
- `pattern`

也可以使用 `AfterValidator` 进行自定义校验。

在这些示例中，你看到了如何为 `str` 值声明校验。

参阅下一章节，了解如何为其他类型（例如数值）声明校验。
