# 请求体 { #request-body }

当你需要从客户端（比如浏览器）向你的 API 发送数据时，会把它作为**请求体**发送。

**请求体**是客户端发送给你的 API 的数据。**响应体**是你的 API 发送给客户端的数据。

你的 API 几乎总是需要发送**响应体**。但客户端不一定总是要发送**请求体**，有时它们只请求某个路径，可能带一些查询参数，但不会发送请求体。

使用 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 模型来声明**请求体**，能充分利用它的功能和优点。

/// info | 信息

发送数据应使用以下之一：`POST`（最常见）、`PUT`、`DELETE` 或 `PATCH`。

规范中没有定义用 `GET` 请求发送请求体的行为，但 FastAPI 仍支持这种方式，只用于非常复杂/极端的用例。

由于不推荐，在使用 `GET` 时，Swagger UI 的交互式文档不会显示请求体的文档，而且中间的代理可能也不支持它。

///

## 导入 Pydantic 的 `BaseModel` { #import-pydantics-basemodel }

从 `pydantic` 中导入 `BaseModel`：

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 创建数据模型 { #create-your-data-model }

把数据模型声明为继承 `BaseModel` 的类。

使用 Python 标准类型声明所有属性：

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。把默认值设为 `None` 可使其变为可选。

例如，上述模型声明如下 JSON "object"（即 Python `dict`）：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...由于 `description` 和 `tax` 是可选的（默认值为 `None`），下面的 JSON "object" 也有效：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 声明为参数 { #declare-it-as-a-parameter }

使用与声明路径和查询参数相同的方式，把它添加至*路径操作*：

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...并把其类型声明为你创建的模型 `Item`。

## 结果 { #results }

仅使用这些 Python 类型声明，**FastAPI** 就可以：

* 以 JSON 形式读取请求体。
* （在必要时）把请求体转换为对应的类型。
* 校验数据。
    * 数据无效时返回清晰的错误信息，并指出错误数据的确切位置和内容。
* 把接收的数据赋值给参数 `item`。
    * 因为你把函数中的参数类型声明为 `Item`，所以还能获得所有属性及其类型的编辑器支持（补全等）。
* 为你的模型生成 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定义，如果对你的项目有意义，还可以在其他地方使用它们。
* 这些 schema 会成为生成的 OpenAPI Schema 的一部分，并被自动文档的 <abbr title="User Interfaces - 用户界面">UIs</abbr> 使用。

## 自动文档 { #automatic-docs }

你的模型的 JSON Schema 会成为生成的 OpenAPI Schema 的一部分，并显示在交互式 API 文档中：

<img src="/img/tutorial/body/image01.png">

并且，还会用于需要它们的每个*路径操作*的 API 文档中：

<img src="/img/tutorial/body/image02.png">

## 编辑器支持 { #editor-support }

在编辑器中，函数内部你会在各处得到类型提示与补全（如果接收的不是 Pydantic 模型，而是 `dict`，就不会有这样的支持）：

<img src="/img/tutorial/body/image03.png">

还支持检查错误的类型操作：

<img src="/img/tutorial/body/image04.png">

这并非偶然，整个框架都是围绕这种设计构建的。

并且在设计阶段、实现之前就进行了全面测试，以确保它能在所有编辑器中正常工作。

我们甚至对 Pydantic 本身做了一些改动以支持这些功能。

上面的截图来自 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>。

但使用 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 和大多数其他 Python 编辑器，你也会获得相同的编辑器支持：

<img src="/img/tutorial/body/image05.png">

/// tip | 提示

如果你使用 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 作为编辑器，可以使用 <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm 插件</a>。

它能改进对 Pydantic 模型的编辑器支持，包括：

* 自动补全
* 类型检查
* 代码重构
* 查找
* 代码审查

///

## 使用模型 { #use-the-model }

在*路径操作*函数内部直接访问模型对象的所有属性：

{* ../../docs_src/body/tutorial002_py310.py *}

## 请求体 + 路径参数 { #request-body-path-parameters }

可以同时声明路径参数和请求体。

**FastAPI** 能识别与**路径参数**匹配的函数参数应该**从路径中获取**，而声明为 Pydantic 模型的函数参数应该**从请求体中获取**。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## 请求体 + 路径 + 查询参数 { #request-body-path-query-parameters }

也可以同时声明**请求体**、**路径**和**查询**参数。

**FastAPI** 会分别识别它们，并从正确的位置获取数据。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

函数参数按如下规则进行识别：

* 如果该参数也在**路径**中声明了，它就是路径参数。
* 如果该参数是（`int`、`float`、`str`、`bool` 等）**单一类型**，它会被当作**查询**参数。
* 如果该参数的类型声明为 **Pydantic 模型**，它会被当作请求**体**。

/// note | 注意

FastAPI 会根据默认值 `= None` 知道 `q` 的值不是必填的。

`str | None` 并不是 FastAPI 用来判断是否必填的依据；是否必填由是否有默认值 `= None` 决定。

但添加这些类型注解可以让你的编辑器提供更好的支持并检测错误。

///

## 不使用 Pydantic { #without-pydantic }

即便不使用 Pydantic 模型也能使用 **Body** 参数。详见[请求体 - 多参数：请求体中的单值](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}。
