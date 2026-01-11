# 查询参数和字符串校验 { #query-parameters-and-string-validations }

**FastAPI** 允许你为参数声明额外的信息和校验。

让我们以下面的应用程序为例：

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

查询参数 `q` 的类型为 `str | None`，这意味着它的类型是 `str` 但也可以是 `None`，并且默认值确实是 `None`，所以 FastAPI 会知道它不是必需的。

/// note | 注意

FastAPI 会因为默认值 `= None` 而知道 `q` 的值不是必需的。

使用 `str | None` 会让你的编辑器给你更好的支持并检测错误。

///

## 额外的校验 { #additional-validation }

我们打算添加约束条件：即使 `q` 是可选的，但只要提供了该参数，则**它的长度不能超过 50 个字符**。

### 导入 `Query` 和 `Annotated` { #import-query-and-annotated }

为此，首先导入：

* 从 `fastapi` 导入 `Query`
* 从 `typing` 导入 `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | 信息

FastAPI 在 0.95.0 版本中增加了对 `Annotated` 的支持（并开始推荐使用它）。

如果你使用的是更旧的版本，在尝试使用 `Annotated` 时会报错。

在使用 `Annotated` 之前，请确保[升级 FastAPI 版本](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}到至少 0.95.1。

///

## 在 `q` 参数的类型中使用 `Annotated` { #use-annotated-in-the-type-for-the-q-parameter }

还记得我之前在 [Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} 中说过，`Annotated` 可以用来为参数添加元数据吗？

现在就是在 FastAPI 中使用它的时候了。🚀

我们之前有这样的类型注解：

//// tab | Python 3.10+

```Python
q: str | None = None
```

////

//// tab | Python 3.9+

```Python
q: Union[str, None] = None
```

////

我们要做的是用 `Annotated` 包裹它，变成：

//// tab | Python 3.10+

```Python
q: Annotated[str | None] = None
```

////

//// tab | Python 3.9+

```Python
q: Annotated[Union[str, None]] = None
```

////

这两个版本表达的是同一件事：`q` 是一个可以是 `str` 或 `None` 的参数，并且默认情况下它是 `None`。

现在我们开始进入有趣的部分。🎉

## 在 `q` 参数的 `Annotated` 中添加 `Query` { #add-query-to-annotated-in-the-q-parameter }

现在我们有了这个 `Annotated`，可以在其中放入更多信息（在这里是一些额外校验），把 `Query` 放到 `Annotated` 里，并把参数 `max_length` 设置为 `50`：

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

注意默认值仍然是 `None`，所以该参数依然是可选的。

但现在，因为在 `Annotated` 里有了 `Query(max_length=50)`，我们是在告诉 FastAPI：我们希望它对这个值进行**额外校验**，它的最大长度是 50 个字符。😎

/// tip | 提示

这里我们使用 `Query()` 是因为这是一个**查询参数**。之后我们还会看到 `Path()`、`Body()`、`Header()` 和 `Cookie()` 等，它们也接受与 `Query()` 相同的参数。

///

FastAPI 现在将会：

* **校验**数据，确保最大长度为 50 个字符
* 当数据无效时向客户端展示**清晰的错误**
* 在 OpenAPI schema 的*路径操作*中**记录**该参数（因此会出现在**自动文档 UI** 中）

## 替代方案（旧）：使用 `Query` 作为默认值 { #alternative-old-query-as-the-default-value }

FastAPI 的早期版本（<abbr title="before 2023-03">0.95.0</abbr> 之前）要求你把 `Query` 作为参数的默认值来使用，而不是放在 `Annotated` 中。你很可能会在某些代码里看到这种写法，所以我会为你解释它。

/// tip | 提示

对于新代码，并且在可行的情况下，请按上面说明使用 `Annotated`。它有多个优点（下面会解释）且没有缺点。🍰

///

下面是将 `Query()` 用作函数参数默认值，并把参数 `max_length` 设置为 50 的写法：

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

在这种情况下（不使用 `Annotated`），我们必须用 `Query()` 替换函数中的默认值 `None`，因此现在需要使用参数 `Query(default=None)` 来设置默认值，它的作用与定义默认值相同（至少对 FastAPI 来说）。

所以：

```Python
q: str | None = Query(default=None)
```

...会让参数变成可选，默认值为 `None`，等同于：

```Python
q: str | None = None
```

但是 `Query` 版本会显式地将其声明为查询参数。

然后，我们可以向 `Query` 传递更多参数。本例中，适用于字符串的 `max_length` 参数：

```Python
q: str | None = Query(default=None, max_length=50)
```

这将会校验数据，在数据无效时展示清晰的错误信息，并在 OpenAPI schema 的*路径操作*中记录该参数。

### `Query` 作为默认值或放在 `Annotated` 中 { #query-as-the-default-value-or-in-annotated }

请记住，当在 `Annotated` 内使用 `Query` 时，你不能为 `Query` 使用 `default` 参数。

相反，应使用函数参数的实际默认值。否则会不一致。

例如，这样是不允许的：

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...因为不清楚默认值应该是 `"rick"` 还是 `"morty"`。

所以，你应该（最好）这样写：

```Python
q: Annotated[str, Query()] = "rick"
```

...或者在较旧的代码库中你会看到：

```Python
q: str = Query(default="rick")
```

### `Annotated` 的优点 { #advantages-of-annotated }

**推荐使用 `Annotated`**，而不是在函数参数中使用默认值的写法，它在多个方面都**更好**。🤓

**函数参数**的**默认值**就是**实际默认值**，这在整体上更符合 Python 的直觉。😌

你可以在没有 FastAPI 的情况下在**其它地方**直接**调用**同一个函数，并且它会**按预期工作**。如果有一个**必需**参数（没有默认值），你的**编辑器**会用错误提示你，**Python** 在运行时也会在你没有传入必需参数时提示错误。

当你不使用 `Annotated` 而是使用**（旧）默认值风格**时，如果你在没有 FastAPI 的情况下在**其它地方**调用该函数，你必须**记得**给函数传入参数它才能正确工作，否则这些值会与你预期不同（例如变成 `QueryInfo` 或类似对象，而不是 `str`）。并且你的编辑器不会抱怨，Python 运行该函数也不会抱怨，只会在内部操作出错时才会报错。

因为 `Annotated` 可以有多个元数据注解，你甚至可以把同一个函数用在其他工具上，比如 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>。🚀

## 添加更多校验 { #add-more-validations }

你还可以添加 `min_length` 参数：

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 添加正则表达式 { #add-regular-expressions }

你可以定义一个参数值必须匹配的<abbr title="正则表达式、regex 或 regexp 是定义字符串搜索模式的字符序列。">正则表达式</abbr> `pattern`：

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

这个指定的正则表达式 pattern 通过以下规则检查接收到的参数值：

* `^`：以后面的字符开头，前面没有字符。
* `fixedquery`: 值精确地等于 `fixedquery`。
* `$`: 到此结束，在 `fixedquery` 之后没有更多字符。

如果你对这些**“正则表达式”**概念感到迷茫，请不要担心。对于许多人来说这都是一个困难的主题。你仍然可以在无需正则表达式的情况下做很多事情。

现在你知道了，一旦你需要它们，你就可以在 **FastAPI** 中使用它们。

## 默认值 { #default-values }

你当然也可以使用 `None` 以外的默认值。

假设你想要声明查询参数 `q` 使其 `min_length` 为 `3`，并且默认值为 `"fixedquery"`：

{* ../../docs_src/query_params_str_validations/tutorial005_an_py39.py hl[9] *}

/// note | 注意

任何类型的默认值（包括 `None`）都会使参数变为可选（非必需）。

///

## 必需参数 { #required-parameters }

当我们不需要声明更多校验或元数据时，只要不声明默认值，就可以让 `q` 查询参数成为必需参数，例如：

```Python
q: str
```

代替：

```Python
q: str | None = None
```

但现在我们正使用 `Query` 来声明它，例如：

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

因此，当你在使用 `Query` 且需要声明一个值为必需时，只需不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006_an_py39.py hl[9] *}

### 必需，但可以是 `None` { #required-can-be-none }

你可以声明一个参数可以接收 `None`，但它仍然是必需的。这将强制客户端发送一个值，即使该值是 `None`。

为此，你可以声明 `None` 是一个有效类型，但只需不声明默认值：

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## 查询参数列表 / 多个值 { #query-parameter-list-multiple-values }

当你使用 `Query` 显式地定义查询参数时，你还可以声明它接收一组值，或者换句话说，接收多个值。

例如，要声明一个可在 URL 中出现多次的查询参数 `q`，你可以这样写：

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

然后，使用如下 URL：

```
http://localhost:8000/items/?q=foo&q=bar
```

你会在*路径操作函数*的*函数参数* `q` 中，以一个 Python `list` 的形式接收到多个 `q` *查询参数*值（`foo` 和 `bar`）。

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

要声明类型为 `list` 的查询参数（如上例所示），你需要显式地使用 `Query`，否则它会被解释为请求体。

///

交互式 API 文档将会相应地进行更新，以允许使用多个值：

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 带默认值的查询参数列表 / 多个值 { #query-parameter-list-multiple-values-with-defaults }

你还可以在没有提供任何值时定义一个默认的 `list` 值：

{* ../../docs_src/query_params_str_validations/tutorial012_an_py39.py hl[9] *}

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

你也可以直接使用 `list` 代替 `list[str]`：

{* ../../docs_src/query_params_str_validations/tutorial013_an_py39.py hl[9] *}

/// note | 注意

请记住，在这种情况下 FastAPI 不会检查列表的内容。

例如，`list[int]` 会检查（并记录到文档）列表的内容必须是整数。但仅 `list` 不会。

///

## 声明更多元数据 { #declare-more-metadata }

你可以添加更多有关该参数的信息。

这些信息将包含在生成的 OpenAPI 中，并由文档用户界面和外部工具使用。

/// note | 注意

请记住，不同工具对 OpenAPI 的支持程度可能不同。

其中一些可能还不会展示所有已声明的额外信息，尽管在大多数情况下，缺少的功能已经计划进行开发。

///

你可以添加 `title`：

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

以及 `description`：

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## 别名参数 { #alias-parameters }

想象一下，你希望参数名为 `item-query`。

例如：

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

但是 `item-query` 不是有效的 Python 变量名。

最接近的是 `item_query`。

但你仍然需要它在 URL 中必须是 `item-query`...

这时你可以声明一个 `alias`，这个别名将用于查找参数值：

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## 弃用参数 { #deprecating-parameters }

现在假设你不再喜欢这个参数了。

你必须保留它一段时间，因为有客户端在使用它，但你希望文档清楚地将它展示为 <abbr title="obsolete, recommended not to use it - 已过时，建议不要使用它">deprecated</abbr>。

那么将参数 `deprecated=True` 传入 `Query`：

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

文档将会像下面这样展示它：

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 从 OpenAPI 中排除参数 { #exclude-parameters-from-openapi }

要从生成的 OpenAPI schema 中排除某个查询参数（因此也会从自动文档系统中排除），将 `Query` 的参数 `include_in_schema` 设置为 `False`：

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## 自定义校验 { #custom-validation }

在某些情况下，你可能需要进行一些**自定义校验**，这些无法通过上面展示的参数来实现。

在这些情况下，你可以使用一个**自定义校验器函数**，它会在常规校验之后应用（例如在校验值是 `str` 之后）。

你可以通过在 `Annotated` 中使用 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic 的 `AfterValidator`</a> 来实现。

/// tip | 提示

Pydantic 还有 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> 等其他功能。🤓

///

例如，这个自定义校验器会检查 item ID 对于 <abbr title="ISBN means International Standard Book Number - ISBN 表示国际标准书号">ISBN</abbr> 图书编号是否以 `isbn-` 开头，或对于 <abbr title="IMDB (Internet Movie Database) is a website with information about movies - IMDB（Internet Movie Database）是一个提供电影信息的网站">IMDB</abbr> 电影 URL ID 是否以 `imdb-` 开头：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | 信息

这在 Pydantic 版本 2 或以上可用。😎

///

/// tip | 提示

如果你需要进行任何需要与**外部组件**通信的校验，例如数据库或另一个 API，那么你应该改用 **FastAPI 依赖项**，你会在后面学到它们。

这些自定义校验器用于只用请求中提供的**同一份数据**就能检查的情况。

///

### 理解那段代码 { #understand-that-code }

关键点只是：在 `Annotated` 里使用**带函数的 `AfterValidator`**。你可以随意跳过这一部分。🤸

---

但如果你对这个特定的代码示例感到好奇，并且你还愿意继续看，这里有一些额外细节。

#### 使用 `value.startswith()` 的字符串 { #string-with-value-startswith }

你注意到了吗？使用 `value.startswith()` 时，可以传入一个 tuple，它会检查 tuple 中的每个值：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### 一个随机条目 { #a-random-item }

使用 `data.items()` 我们会得到一个<abbr title="Something we can iterate on with a for loop, like a list, set, etc. - 可以用 for 循环迭代的对象，比如 list、set 等">iterable object</abbr>，它会生成包含每个字典条目 key 和 value 的 tuple。

我们用 `list(data.items())` 将这个可迭代对象转换成一个真正的 `list`。

然后用 `random.choice()` 从 list 中取得一个**随机值**，因此得到一个 `(id, name)` 的 tuple。它会像 `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` 这样。

然后我们把这个 tuple 的**两个值**赋给变量 `id` 和 `name`。

所以，如果用户没有提供 item ID，他们仍然会收到一个随机建议。

...我们把这一切都写在了**一行简单代码**里。🤯 你不爱 Python 吗？🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## 总结 { #recap }

你可以为参数声明额外的校验和元数据。

通用校验和元数据：

* `alias`
* `title`
* `description`
* `deprecated`

字符串特有的校验：

* `min_length`
* `max_length`
* `pattern`

使用 `AfterValidator` 的自定义校验。

在这些示例中，你了解了如何声明对 `str` 值的校验。

请参阅下一章节，以了解如何声明对其他类型（例如数值）的校验。
