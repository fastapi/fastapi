# 响应模型 - 返回类型 { #response-model-return-type }

你可以通过为*路径操作函数*的**返回类型**添加注解来声明用于响应的类型。

和为输入数据在函数**参数**里做类型注解的方式相同，你可以使用 Pydantic 模型、`list`、`dict`、以及整数、布尔值等标量类型。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI 会使用这个返回类型来：

* 对返回数据进行**校验**。
    * 如果数据无效（例如缺少某个字段），这意味着你的应用代码有问题，没有返回应有的数据，FastAPI 将返回服务器错误而不是返回错误的数据。这样你和你的客户端都可以确定会收到期望的数据及其结构。
* 在 OpenAPI 的*路径操作*中为响应添加**JSON Schema**。
    * 它会被**自动文档**使用。
    * 它也会被自动客户端代码生成工具使用。

但更重要的是：

* 它会将输出数据**限制并过滤**为返回类型中定义的内容。
    * 这对**安全性**尤为重要，下面会进一步介绍。

## `response_model` 参数 { #response-model-parameter }

在一些情况下，你需要或希望返回的数据与声明的类型不完全一致。

例如，你可能希望**返回一个字典**或数据库对象，但**将其声明为一个 Pydantic 模型**。这样 Pydantic 模型就会为你返回的对象（例如字典或数据库对象）完成文档、校验等工作。

如果你添加了返回类型注解，工具和编辑器会（正确地）报错，提示你的函数返回的类型（例如 `dict`）与声明的类型（例如一个 Pydantic 模型）不同。

在这些情况下，你可以使用*路径操作装饰器*参数 `response_model`，而不是返回类型。

你可以在任意*路径操作*中使用 `response_model` 参数：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等等。

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | 注意

注意，`response_model` 是「装饰器」方法（`get`、`post` 等）的一个参数。不是你的*路径操作函数*的参数，不像所有查询参数和请求体那样。

///

`response_model` 接收的类型与为 Pydantic 模型字段声明的类型相同，因此它可以是一个 Pydantic 模型，也可以是一个由 Pydantic 模型组成的 `list`，例如 `List[Item]`。

FastAPI 会使用这个 `response_model` 来完成数据文档、校验等，并且还会将输出数据**转换并过滤**为其类型声明。

/// tip | 提示

如果你的编辑器、mypy 等进行严格类型检查，你可以将函数返回类型声明为 `Any`。

这样你告诉编辑器你是有意返回任意类型。但 FastAPI 仍会使用 `response_model` 做数据文档、校验、过滤等工作。

///

### `response_model` 的优先级 { #response-model-priority }

如果你同时声明了返回类型和 `response_model`，`response_model` 会具有优先级并由 FastAPI 使用。

这样，即使你返回的类型与响应模型不同，你也可以为函数添加正确的类型注解，供编辑器和 mypy 等工具使用。同时你仍然可以让 FastAPI 使用 `response_model` 进行数据校验、文档等。

你也可以使用 `response_model=None` 来禁用该*路径操作*的响应模型生成；当你为一些不是有效 Pydantic 字段的东西添加类型注解时，可能需要这样做，下面的章节会有示例。

## 返回与输入相同的数据 { #return-the-same-input-data }

这里我们声明一个 `UserIn` 模型，它包含一个明文密码：

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | 信息

要使用 `EmailStr`，首先安装 <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>。

请先创建并激活一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，然后安装，例如：

```console
$ pip install email-validator
```

或者：

```console
$ pip install "pydantic[email]"
```

///

我们使用这个模型来声明输入，同时也用相同的模型来声明输出：

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

现在，每当浏览器使用密码创建用户时，API 会在响应中返回相同的密码。

在这个场景下，这可能不算问题，因为发送密码的是同一个用户。

但如果我们在其他*路径操作*中使用相同的模型，就可能会把用户的密码发送给每个客户端。

/// danger | 危险

除非你非常清楚所有注意事项并确实知道自己在做什么，否则永远不要存储用户的明文密码，也不要像这样在响应中发送它。

///

## 添加输出模型 { #add-an-output-model }

相反，我们可以创建一个包含明文密码的输入模型和一个不包含它的输出模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

这里，即使我们的*路径操作函数*返回的是包含密码的同一个输入用户：

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

……我们仍将 `response_model` 声明为不包含密码的 `UserOut` 模型：

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

因此，**FastAPI** 会负责过滤掉输出模型中未声明的所有数据（使用 Pydantic）。

### `response_model` 还是返回类型 { #response-model-or-return-type }

在这个例子中，因为两个模型不同，如果我们将函数返回类型注解为 `UserOut`，编辑器和工具会抱怨我们返回了无效类型，因为它们是不同的类。

这就是为什么在这个例子里我们必须在 `response_model` 参数中声明它。

……但继续往下读，看看如何更好地处理这种情况。

## 返回类型与数据过滤 { #return-type-and-data-filtering }

延续上一个例子。我们希望**用一种类型来注解函数**，但希望从函数返回的内容实际上可以**包含更多数据**。

我们希望 FastAPI 继续使用响应模型来**过滤**数据。这样即使函数返回了更多数据，响应也只会包含响应模型中声明的字段。

在上一个例子中，因为类不同，我们不得不使用 `response_model` 参数。但这也意味着我们无法从编辑器和工具处获得对函数返回类型的检查支持。

不过在大多数需要这样做的场景里，我们只是希望模型像这个例子中那样**过滤/移除**一部分数据。

在这些场景里，我们可以使用类和继承，既利用函数的**类型注解**获取更好的编辑器和工具支持，又能获得 FastAPI 的**数据过滤**。

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

这样一来，我们既能从编辑器和 mypy 获得工具支持（这段代码在类型上是正确的），也能从 FastAPI 获得数据过滤。

这是如何做到的？我们来看看。🤓

### 类型注解与工具链 { #type-annotations-and-tooling }

先看看编辑器、mypy 和其他工具会如何看待它。

`BaseUser` 有基础字段。然后 `UserIn` 继承自 `BaseUser` 并新增了 `password` 字段，因此它包含了两个模型的全部字段。

我们把函数返回类型注解为 `BaseUser`，但实际上返回的是一个 `UserIn` 实例。

编辑器、mypy 和其他工具不会对此抱怨，因为在类型系统里，`UserIn` 是 `BaseUser` 的子类，这意味着当期望 `BaseUser` 时，返回 `UserIn` 是*合法*的。

### FastAPI 的数据过滤 { #fastapi-data-filtering }

对于 FastAPI，它会查看返回类型并确保你返回的内容**只**包含该类型中声明的字段。

FastAPI 在内部配合 Pydantic 做了多项处理，确保不会把类继承的这些规则用于返回数据的过滤，否则你可能会返回比预期多得多的数据。

这样，你就能兼得两方面的优势：带有**工具支持**的类型注解和**数据过滤**。

## 在文档中查看 { #see-it-in-the-docs }

当你查看自动文档时，你会看到输入模型和输出模型都会有各自的 JSON Schema：

<img src="/img/tutorial/response-model/image01.png">

并且两个模型都会用于交互式 API 文档：

<img src="/img/tutorial/response-model/image02.png">

## 其他返回类型注解 { #other-return-type-annotations }

有些情况下你会返回一些不是有效 Pydantic 字段的内容，并在函数上做了相应注解，只是为了获得工具链（编辑器、mypy 等）的支持。

### 直接返回 Response { #return-a-response-directly }

最常见的情况是[直接返回 Response，详见进阶文档](../advanced/response-directly.md){.internal-link target=_blank}。

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

这个简单场景 FastAPI 会自动处理，因为返回类型注解是 `Response`（或其子类）。

工具也会满意，因为 `RedirectResponse` 和 `JSONResponse` 都是 `Response` 的子类，所以类型注解是正确的。

### 注解 Response 的子类 { #annotate-a-response-subclass }

你也可以在类型注解中使用 `Response` 的子类：

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

这同样可行，因为 `RedirectResponse` 是 `Response` 的子类，FastAPI 会自动处理这个简单场景。

### 无效的返回类型注解 { #invalid-return-type-annotations }

但当你返回其他任意对象（如数据库对象）而它不是有效的 Pydantic 类型，并在函数中按此进行了注解时，FastAPI 会尝试基于该类型注解创建一个 Pydantic 响应模型，但会失败。

如果你有一个在多个类型之间的<dfn title="多个类型的联合表示“这些类型中的任意一个”。">联合类型</dfn>，其中一个或多个不是有效的 Pydantic 类型，也会发生同样的情况，例如这个会失败 💥：

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

……它失败是因为该类型注解不是 Pydantic 类型，也不只是单个 `Response` 类或其子类，而是 `Response` 与 `dict` 的联合类型（任意其一）。

### 禁用响应模型 { #disable-response-model }

延续上面的例子，你可能不想要 FastAPI 执行默认的数据校验、文档、过滤等。

但你可能仍然想在函数上保留返回类型注解，以获得编辑器和类型检查器（如 mypy）的支持。

在这种情况下，你可以通过设置 `response_model=None` 来禁用响应模型生成：

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

这会让 FastAPI 跳过响应模型的生成，这样你就可以按需使用任意返回类型注解，而不会影响你的 FastAPI 应用。🤓

## 响应模型的编码参数 { #response-model-encoding-parameters }

你的响应模型可以具有默认值，例如：

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None`（或在 Python 3.10 中的 `str | None = None`）默认值为 `None`。
* `tax: float = 10.5` 默认值为 `10.5`。
* `tags: List[str] = []` 默认值为一个空列表：`[]`。

但如果它们并没有被实际存储，你可能希望在结果中省略这些默认值。

例如，当你在 NoSQL 数据库中保存了具有许多可选属性的模型，但又不想发送充满默认值的冗长 JSON 响应。

### 使用 `response_model_exclude_unset` 参数 { #use-the-response-model-exclude-unset-parameter }

你可以设置*路径操作装饰器*参数 `response_model_exclude_unset=True`：

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

这样响应中将不会包含那些默认值，而只包含实际设置的值。

因此，如果你向该*路径操作*请求 ID 为 `foo` 的商品，响应（不包括默认值）将为：

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

详见 <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">Pydantic 文档</a>中对 `exclude_defaults` 和 `exclude_none` 的说明。

///

#### 默认字段有实际值的数据 { #data-with-values-for-fields-with-defaults }

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

FastAPI 足够聪明（实际上是 Pydantic 足够聪明）去认识到，即使 `description`、`tax` 和 `tags` 的值与默认值相同，它们也是被显式设置的（而不是取自默认值）。

因此，它们将包含在 JSON 响应中。

/// tip | 提示

请注意默认值可以是任何值，而不仅是 `None`。

它们可以是一个列表（`[]`）、值为 `10.5` 的 `float`，等等。

///

### `response_model_include` 和 `response_model_exclude` { #response-model-include-and-response-model-exclude }

你还可以使用*路径操作装饰器*的 `response_model_include` 和 `response_model_exclude` 参数。

它们接收一个由属性名 `str` 组成的 `set`，用于包含（忽略其他）或排除（包含其他）这些属性。

当你只有一个 Pydantic 模型，并且想要从输出中移除一些数据时，这可以作为一种快捷方式。

/// tip | 提示

但仍然推荐使用上面的思路，使用多个类，而不是这些参数。

因为即使你使用 `response_model_include` 或 `response_model_exclude` 省略了一些属性，你的应用在 OpenAPI（和文档）中生成的 JSON Schema 仍然会是完整模型。

这同样适用于类似的 `response_model_by_alias`。

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | 提示

`{"name", "description"}` 语法创建一个包含这两个值的 `set`。

等同于 `set(["name", "description"])`。

///

#### 使用 `list` 而不是 `set` { #using-lists-instead-of-sets }

如果你忘记使用 `set` 而是使用了 `list` 或 `tuple`，FastAPI 仍会将其转换为 `set` 并正常工作：

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## 总结 { #recap }

使用*路径操作装饰器*的 `response_model` 参数来定义响应模型，尤其是确保私有数据被过滤掉。

使用 `response_model_exclude_unset` 来仅返回显式设置的值。
