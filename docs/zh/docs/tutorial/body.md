# 请求体 { #request-body }

当你需要从客户端（比如浏览器）向 API 发送数据时，可以把数据作为**请求体**发送。

**请求**体是客户端发送给 API 的数据。**响应**体是你的 API 发送给客户端的数据。

你的 API 几乎总是要发送**响应体**。但客户端不一定总是需要发送**请求体**，有时它们只请求一个路径，可能带一些查询参数，但不发送请求体。

要声明**请求**体，你可以使用 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 模型，并利用它的全部能力和优势。

/// info | 信息

要发送数据，你应该使用以下之一：`POST`（更常见）、`PUT`、`DELETE` 或 `PATCH`。

在规范中，用 `GET` 请求发送请求体属于未定义行为；不过 FastAPI 仍然支持它，但仅用于非常复杂/极端的用例。

由于不推荐这样做，使用 Swagger UI 的交互式文档在使用 `GET` 时不会显示请求体的文档，而且中间的代理也可能不支持它。

///

## 导入 Pydantic 的 `BaseModel` { #import-pydantics-basemodel }

首先，你需要从 `pydantic` 中导入 `BaseModel`：

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 创建数据模型 { #create-your-data-model }

然后，把数据模型声明为继承 `BaseModel` 的类。

为所有属性使用标准的 Python 类型：

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


与声明查询参数时相同，当模型属性有默认值时，它不是必需的；否则就是必需的。使用 `None` 可以让它变成可选。

例如，上面的这个模型会声明如下 JSON "`object`"（或 Python `dict`）：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...由于 `description` 和 `tax` 是可选的（默认值为 `None`），下面这个 JSON "`object`" 也同样有效：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 声明为参数 { #declare-it-as-a-parameter }

要把它添加到你的*路径操作*中，按你声明路径参数和查询参数的同样方式来声明它：

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...并把它的类型声明为你创建的模型 `Item`。

## 结果 { #results }

只需要这份 Python 类型声明，**FastAPI** 就会：

* 将请求体按 JSON 读取。
* 转换为对应的类型（如有需要）。
* 校验数据。
    * 如果数据无效，它会返回清晰友好的错误信息，准确指出哪里、哪部分数据不正确。
* 通过参数 `item` 给你接收到的数据。
    * 因为你在函数中把它声明为 `Item` 类型，你也会获得编辑器对所有属性及其类型的支持（补全等）。
* 为你的模型生成 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定义；如果对你的项目有意义，你也可以在任何其它地方使用它们。
* 这些 Schema 将成为生成的 OpenAPI Schema 的一部分，并被自动文档 <abbr title="User Interfaces - 用户界面">UIs</abbr> 使用。

## 自动文档 { #automatic-docs }

你的模型的 JSON Schema 将成为 OpenAPI 生成的 Schema 的一部分，并显示在交互式 API 文档中：

<img src="/img/tutorial/body/image01.png">

并且也会在每个需要它们的*路径操作*的 API 文档中使用：

<img src="/img/tutorial/body/image02.png">

## 编辑器支持 { #editor-support }

在编辑器中，在函数内部你会在各处获得类型提示和补全（如果你接收的是 `dict` 而不是 Pydantic 模型，就不会发生这种情况）：

<img src="/img/tutorial/body/image03.png">

你也会得到对错误类型操作的检查：

<img src="/img/tutorial/body/image04.png">

这并非偶然，整个框架都是围绕这种设计构建的。

并且在设计阶段、任何实现之前，就进行了彻底测试，以确保它能与所有编辑器配合工作。

甚至还对 Pydantic 本身做了一些改动来支持这一点。

之前的截图是用 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> 截取的。

但在 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 以及大多数其它 Python 编辑器中，你也会得到同样的编辑器支持：

<img src="/img/tutorial/body/image05.png">

/// tip | 提示

如果你使用 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 作为编辑器，你可以使用 <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>。

它会改进编辑器对 Pydantic 模型的支持，包括：

* auto-completion
* type checks
* refactoring
* searching
* inspections

///

## 使用模型 { #use-the-model }

在函数内部，你可以直接访问模型对象的所有属性：

{* ../../docs_src/body/tutorial002_py310.py *}

## 请求体 + 路径参数 { #request-body-path-parameters }

你可以同时声明路径参数和请求体。

**FastAPI** 会识别与路径参数匹配的函数参数应该**从路径中获取**，并且把声明为 Pydantic 模型的函数参数**从请求体中获取**。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## 请求体 + 路径参数 + 查询参数 { #request-body-path-query-parameters }

你也可以同时声明 **body**、**path** 和 **query** 参数。

**FastAPI** 会识别每一种参数，并从正确的位置获取数据。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

函数参数将按如下方式识别：

* 如果参数也在**路径**中声明了，它会被用作路径参数。
* 如果参数是**单类型**（如 `int`、`float`、`str`、`bool` 等），它会被解释为**查询**参数。
* 如果参数被声明为**Pydantic 模型**类型，它会被解释为请求**体**。

/// note | 注意

FastAPI 会因为默认值 `= None` 而知道 `q` 的值不是必需的。

FastAPI 不会使用 `str | None`（Python 3.10+）或 `Union[str, None]`（Python 3.9+）中的 `Union` 来判断该值不是必需的；它会因为默认值是 `= None` 而知道它不是必需的。

但添加这些类型注解会让你的编辑器提供更好的支持并检测错误。

///

## 不使用 Pydantic { #without-pydantic }

如果你不想使用 Pydantic 模型，你也可以使用 **Body** 参数。详见 [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}。
