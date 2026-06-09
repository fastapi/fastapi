# 请求体 { #request-body }

需要从客户端（比如浏览器）往 API 发送数据时，用请求体发。

请求体是客户端发给 API 的数据。响应体是 API 回给客户端的数据。

API 几乎总要发响应体。客户端不一定总要发请求体。有时只请求一个路径，加点查询参数，不带 body。

要声明请求体，用 [Pydantic](https://docs.pydantic.dev/) 的模型。功能全，还好用。

/// note | 注意

发数据应该用这些方法之一：`POST`（更常见）、`PUT`、`DELETE`、`PATCH`。

规范里，对 `GET` 携带 body 没有定义的行为。FastAPI 也支持，但只用于非常复杂/极端的场景。

因为不推荐，Swagger UI 的交互文档在 `GET` 时不会展示 body。中间的代理也可能不支持。

///

## 导入 Pydantic 的 `BaseModel` { #import-pydantics-basemodel }

先从 `pydantic` 导入 `BaseModel`：

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 创建数据模型 { #create-your-data-model }

然后写一个继承 `BaseModel` 的类，作为数据模型。

所有属性都用标准的 Python 类型：

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

跟声明查询参数一样。模型属性有默认值就不是必填。没有默认值就是必填。设成 `None` 表示可选。

比如，上面的模型对应的 JSON "`object`"（或 Python `dict`）长这样：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...因为 `description` 和 `tax` 是可选的（默认 `None`），这个 JSON "`object`" 也合法：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 把它声明成参数 { #declare-it-as-a-parameter }

要把它加到路径操作里，和声明路径参数、查询参数的方式一样：

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

把它的类型写成你创建的模型，`Item`。

## 效果 { #results }

只靠这个 Python 类型声明，FastAPI 会：

* 把请求体按 JSON 读取。
* 按需做类型转换。
* 校验数据。
    * 如果数据不合法，会返回清晰的错误。说明哪儿错了，错了什么。
* 把收到的数据放在参数 `item` 里给你。
    * 参数类型是 `Item`。编辑器会给你补全等支持，包括属性和它们的类型。
* 为你的模型生成 [JSON Schema](https://json-schema.org) 定义。你也可以在项目里其它地方复用它们。
* 这些 Schema 会进到生成的 OpenAPI 里。自动文档 <abbr title="User Interfaces - 用户界面">UIs</abbr> 会用到它们。

## 自动文档 { #automatic-docs }

模型的 JSON Schema 会包含在生成的 OpenAPI 里。会显示在交互式 API 文档里：

<img src="/img/tutorial/body/image01.png">

需要它们的每个路径操作的文档里也会用到：

<img src="/img/tutorial/body/image02.png">

## 编辑器支持 { #editor-support }

在编辑器里，函数内到处都有类型提示和补全。（如果收的是 `dict` 而不是 Pydantic 模型，就没有这些。）

还会检查错误的类型操作：

<img src="/img/tutorial/body/image04.png">

这不是巧合，整个框架就是这么设计的。

在实现前的设计阶段就充分测试过。确保能和各类编辑器配合。

为此甚至改过 Pydantic。

上面的截图用的是 [Visual Studio Code](https://code.visualstudio.com)。

用 [PyCharm](https://www.jetbrains.com/pycharm/) 和大多数 Python 编辑器也一样：

<img src="/img/tutorial/body/image05.png">

/// tip | 提示

如果用 [PyCharm](https://www.jetbrains.com/pycharm/)，可以装 [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/)。

它能增强 Pydantic 模型的编辑器支持：

* 自动补全
* 类型检查
* 重构
* 搜索
* 检查

///

## 使用模型 { #use-the-model }

在函数里可以直接访问模型对象的所有属性：

{* ../../docs_src/body/tutorial002_py310.py *}

## 请求体 + 路径参数 { #request-body-path-parameters }

可以同时声明路径参数和请求体。

FastAPI 会识别：和路径参数同名的函数参数来自路径。声明为 Pydantic 模型的函数参数来自请求体。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## 请求体 + 路径 + 查询参数 { #request-body-path-query-parameters }

也可以同时声明 body、path、query 参数。

FastAPI 会识别它们，并从对应位置取数据。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

函数参数的识别规则：

* 参数在路径里也声明了 → 当作路径参数。
* 参数是“标量类型”（如 `int`、`float`、`str`、`bool` 等）→ 当作查询参数。
* 参数类型是 Pydantic 模型 → 当作请求体。

/// note | 注意

因为默认值是 `= None`，FastAPI 知道 `q` 不是必填。

FastAPI 不靠 `str | None` 来判断是否必填。它看默认值 `= None`。

但加上类型标注，编辑器能提供更好的支持并发现错误。

///

## 不用 Pydantic { #without-pydantic }

如果不想用 Pydantic 模型，也可以用 Body 参数。看这篇文档：[Body - 多个参数：请求体里的标量值](body-multiple-params.md#singular-values-in-body)。
