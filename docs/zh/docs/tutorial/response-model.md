# 响应模型 - 返回类型 { #response-model-return-type }

你可以通过为*路径操作函数*的 **返回类型** 添加注解，来声明用于响应的类型。

你可以像在函数**参数**中用于输入数据那样使用**类型注解**，可以使用 Pydantic 模型、列表、字典、整数、布尔值等标量类型。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI 将使用该返回类型来：

* **校验**返回的数据。
    * 如果数据无效（例如缺少字段），这意味着是*你的*应用代码有问题，没有返回它应该返回的内容，它将返回服务器错误，而不是返回不正确的数据。通过这种方式，你和你的客户端可以确信将收到预期的数据以及预期的数据结构。
* 在 OpenAPI 的*路径操作*中为响应添加一个 **JSON Schema**。
    * 这将被**自动化文档**使用。
    * 它也会被自动客户端代码生成工具使用。

但最重要的是：

* 它会将输出数据**限制并过滤**为返回类型中定义的内容。
    * 这对**安全性**尤其重要，下面我们会看到更多相关内容。

## `response_model` 参数 { #response-model-parameter }

在某些情况下，你需要或想要返回一些与类型声明并不完全一致的数据。

例如，你可能想要**返回一个字典**或数据库对象，但**将其声明为 Pydantic 模型**。这样，Pydantic 模型就可以为你返回的对象（例如字典或数据库对象）完成所有的数据文档、校验等工作。

如果你添加了返回类型注解，工具和编辑器会提示（正确的）错误，告诉你函数返回的类型（例如 dict）与声明的类型（例如 Pydantic 模型）不同。

在这些情况下，你可以使用*路径操作装饰器*的参数 `response_model` 来替代返回类型。

你可以在任意的*路径操作*中使用 `response_model` 参数：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等等。

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | 注意

注意，`response_model`是「装饰器」方法（`get`，`post` 等）的一个参数。不像之前的所有参数和请求体，它不属于*路径操作函数*。

///

`response_model` 接收的类型与你将为 Pydantic 模型字段所声明的类型相同，因此它可以是一个 Pydantic 模型，但也可以是例如由 Pydantic 模型组成的 `list`，比如 `List[Item]`。

FastAPI 将使用此 `response_model` 来完成所有的数据文档、校验等工作，并且还会将输出数据**转换并过滤**为其类型声明。

/// tip | 提示

如果你在编辑器、mypy 等中启用了严格类型检查，你可以将函数返回类型声明为 `Any`。

这样你就是在告诉编辑器你是有意返回任意内容的。但 FastAPI 仍然会使用 `response_model` 来进行数据文档、校验、过滤等工作。

///

### `response_model` 优先级 { #response-model-priority }

如果你同时声明了返回类型和 `response_model`，FastAPI 会优先使用 `response_model`。

这样，即使你返回的类型与响应模型不同，你仍然可以为函数添加正确的类型注解，供编辑器和 mypy 等工具使用。同时你仍然可以让 FastAPI 使用 `response_model` 来进行数据校验、文档等。

你也可以使用 `response_model=None` 来禁用该*路径操作*的响应模型创建；如果你要为一些不是有效 Pydantic 字段的内容添加类型注解，你可能会需要这样做，你会在下面某个章节看到示例。

## 返回与输入相同的数据 { #return-the-same-input-data }

现在我们声明一个 `UserIn` 模型，它将包含一个明文密码：

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | 信息

要使用 `EmailStr`，请先安装 <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装，例如：

```console
$ pip install email-validator
```

或使用：

```console
$ pip install "pydantic[email]"
```

///

我们正在使用此模型声明输入数据，并使用同一模型声明输出数据：

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

现在，每当浏览器使用一个密码创建用户时，API 都会在响应中返回相同的密码。

在这个案例中，这可能不算是问题，因为用户自己正在发送密码。

但是，如果我们在其他的*路径操作*中使用相同的模型，则可能会将用户的密码发送给每个客户端。

/// danger | 危险

永远不要存储用户的明文密码，也不要像这样在响应中发送密码，除非你了解所有注意事项并且你清楚自己在做什么。

///

## 添加输出模型 { #add-an-output-model }

相反，我们可以创建一个有明文密码的输入模型和一个没有明文密码的输出模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

这样，即便我们的*路径操作函数*将会返回包含密码的相同输入用户：

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...我们已经将 `response_model` 声明为了不包含密码的 `UserOut` 模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

因此，**FastAPI** 将会负责过滤掉未在输出模型中声明的所有数据（使用 Pydantic）。

### `response_model` 还是返回类型 { #response-model-or-return-type }

在这种情况下，因为两个模型不同，如果我们将函数返回类型注解为 `UserOut`，编辑器和工具会抱怨我们返回了无效类型，因为它们是不同的类。

这就是为什么在这个例子中我们必须在 `response_model` 参数中声明它。

...但请继续往下读，看看如何解决这个问题。

## 返回类型与数据过滤 { #return-type-and-data-filtering }

让我们继续上面的例子。我们想要**用一种类型来注解函数**，但我们希望能够从函数中返回实际上包含**更多数据**的内容。

我们希望 FastAPI 继续使用响应模型来**过滤**数据。这样即便函数返回了更多数据，响应也只会包含响应模型中声明的字段。

在前面的例子中，因为类不同，我们不得不使用 `response_model` 参数。但这也意味着我们无法获得编辑器和工具对函数返回类型的检查支持。

但在大多数我们需要这样做的情况下，我们只是想让模型像这个例子一样**过滤/移除**部分数据。

而在这些情况下，我们可以通过类与继承来利用函数的**类型注解**，在编辑器和工具中获得更好的支持，同时仍然获得 FastAPI 的**数据过滤**。

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

这样一来，我们既能获得编辑器和 mypy 等工具的支持（因为这段代码从类型角度看是正确的），也能获得 FastAPI 的数据过滤。

这怎么做到的？我们来看看。🤓

### 类型注解与工具支持 { #type-annotations-and-tooling }

首先我们看看编辑器、mypy 和其他工具会如何看待它。

`BaseUser` 有基础字段。然后 `UserIn` 继承自 `BaseUser` 并添加 `password` 字段，因此它会包含两个模型的全部字段。

我们把函数返回类型注解为 `BaseUser`，但实际上返回的是一个 `UserIn` 实例。

编辑器、mypy 以及其他工具不会对此抱怨，因为从类型角度来说，`UserIn` 是 `BaseUser` 的子类，这意味着当期望的是任何 `BaseUser` 时，`UserIn` 是一个*有效*类型。

### FastAPI 数据过滤 { #fastapi-data-filtering }

现在，对于 FastAPI，它会查看返回类型，并确保你返回的内容**仅**包含该类型中声明的字段。

FastAPI 内部会使用 Pydantic 做几件事，以确保用于返回数据过滤时不会应用相同的类继承规则，否则你可能会返回比预期多得多的数据。

通过这种方式，你就可以两者兼得：带有**工具支持**的类型注解，以及**数据过滤**。

## 在文档中查看 { #see-it-in-the-docs }

当你查看自动化文档时，你可以检查输入模型和输出模型是否都具有自己的 JSON Schema：

<img src="/img/tutorial/response-model/image01.png">

并且两种模型都将在交互式 API 文档中使用：

<img src="/img/tutorial/response-model/image02.png">

## 其他返回类型注解 { #other-return-type-annotations }

在某些情况下，你会返回一些不是有效 Pydantic 字段的东西，并在函数中对其进行注解，仅仅是为了获得工具（编辑器、mypy 等）提供的支持。

### 直接返回 Response { #return-a-response-directly }

最常见的情况是[像高级文档后面解释的那样直接返回 Response](../advanced/response-directly.md){.internal-link target=_blank}。

{* ../../docs_src/response_model/tutorial003_02_py39.py hl[8,10:11] *}

FastAPI 会自动处理这个简单情况，因为返回类型注解是 `Response` 类（或其子类）。

并且工具也会满意，因为 `RedirectResponse` 和 `JSONResponse` 都是 `Response` 的子类，所以类型注解是正确的。

### 注解 Response 的子类 { #annotate-a-response-subclass }

你也可以在类型注解中使用 `Response` 的子类：

{* ../../docs_src/response_model/tutorial003_03_py39.py hl[8:9] *}

这同样可行，因为 `RedirectResponse` 是 `Response` 的子类，并且 FastAPI 会自动处理这个简单情况。

### 无效的返回类型注解 { #invalid-return-type-annotations }

但是，当你返回另一个不是有效 Pydantic 类型的任意对象（例如数据库对象），并在函数中这样进行注解时，FastAPI 会尝试从该类型注解创建一个 Pydantic 响应模型，并且会失败。

如果你使用了类似于在不同类型之间做 <abbr title='多种类型之间的 union 表示“这些类型中的任意一种”。'>union</abbr> 的注解，其中一个或多个不是有效 Pydantic 类型，也会发生同样的情况，例如下面这样会失败 💥：

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...这是因为该类型注解不是 Pydantic 类型，也不仅仅是单个 `Response` 类或子类，它是一个 union（两者任意一个）：`Response` 与 `dict`。

### 禁用响应模型 { #disable-response-model }

延续上面的例子，你可能不想要 FastAPI 执行默认的数据校验、文档、过滤等功能。

但你可能仍想保留函数中的返回类型注解，以获得编辑器和类型检查器（例如 mypy）等工具的支持。

在这种情况下，你可以通过设置 `response_model=None` 来禁用响应模型生成：

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

这会让 FastAPI 跳过响应模型生成，这样你就可以使用任何你需要的返回类型注解，而不会影响你的 FastAPI 应用。🤓

## 响应模型编码参数 { #response-model-encoding-parameters }

你的响应模型可以具有默认值，例如：

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None`（或在 Python 3.10 中使用 `str | None = None`）的默认值是 `None`。
* `tax: float = 10.5` 的默认值是 `10.5`。
* `tags: List[str] = []` 的默认值是一个空列表：`[]`。

但如果它们并没有存储实际的值，你可能想从结果中忽略它们的默认值。

举个例子，当你在 NoSQL 数据库中保存了具有许多可选属性的模型，但你又不想发送充满默认值的很长的 JSON 响应。

### 使用 `response_model_exclude_unset` 参数 { #use-the-response-model-exclude-unset-parameter }

你可以设置*路径操作装饰器*的 `response_model_exclude_unset=True` 参数：

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

然后响应中将不会包含那些默认值，而是仅有实际设置的值。

因此，如果你向*路径操作*发送 ID 为 `foo` 的商品的请求，则响应（不包括默认值）将为：

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | 信息

你还可以使用：

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

参考 <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">Pydantic 文档</a> 中对 `exclude_defaults` 和 `exclude_none` 的描述。

///

#### 默认值字段有实际值的数据 { #data-with-values-for-fields-with-defaults }

但是，如果你的数据在具有默认值的模型字段中有实际的值，例如 ID 为 `bar` 的项：

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

这些值将包含在响应中。

#### 具有与默认值相同值的数据 { #data-with-the-same-values-as-the-defaults }

如果数据具有与默认值相同的值，例如 ID 为 `baz` 的项：

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI 足够聪明（实际上是 Pydantic 足够聪明）去认识到这一点：即使 `description`、`tax` 和 `tags` 具有与默认值相同的值，它们也是被显式设定的（而不是取自默认值）。

因此，它们将包含在 JSON 响应中。

/// tip | 提示

请注意默认值可以是任何值，而不仅是 `None`。

它们可以是一个列表（`[]`）、一个值为 `10.5` 的 `float`，等等。

///

### `response_model_include` 和 `response_model_exclude` { #response-model-include-and-response-model-exclude }

你还可以使用*路径操作装饰器*的 `response_model_include` 和 `response_model_exclude` 参数。

它们接收一个由属性名称 `str` 组成的 `set` 来包含（忽略其余的）或排除（保留其余的）这些属性。

如果你只有一个 Pydantic 模型，并且想要从输出中移除一些数据，则可以使用这种快捷方法。

/// tip | 提示

但是依然建议你使用上面提到的思路，使用多个类，而不是这些参数。

这是因为即使使用 `response_model_include` 或 `response_model_exclude` 来省略某些属性，在应用程序的 OpenAPI 定义（和文档）中生成的 JSON Schema 仍将是完整模型的那个。

这也适用于作用类似的 `response_model_by_alias`。

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | 提示

`{"name", "description"}` 语法创建一个具有这两个值的 `set`。

等同于 `set(["name", "description"])`。

///

#### 使用 `list` 而不是 `set` { #using-lists-instead-of-sets }

如果你忘记使用 `set` 而是使用 `list` 或 `tuple`，FastAPI 仍会将其转换为 `set` 并且正常工作：

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## 总结 { #recap }

使用*路径操作装饰器*的 `response_model` 参数来定义响应模型，特别是确保私有数据被过滤掉。

使用 `response_model_exclude_unset` 来仅返回显式设定的值。
