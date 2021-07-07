# 请求体

FastAPI 使用**请求体**从客户端（例如浏览器）向 API 发送数据。

**请求体**是客户端发送给 API 的数据。**响应体**是 API 发送给客户端的数据。

API 基本上总要发送**响应体**，但是客户端不一定发送**请求体**。

使用 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 模型声明**请求体**，可以充分利用它的功能和优点。

!!! info "说明"

    发送数据使用 `POST`（最常用）、`PUT`、`DELETE`、`PATCH` 等操作。
    
    规范中没有定义使用 `GET` 发送请求体的操作，但不管怎样，FastAPI 也支持这种方式，只不过仅用于非常复杂或极端的用例。
    
    我们不建议使用 `GET`，因此，在 Swagger UI 交互文档中不会显示有关 `GET` 的内容，而且代理协议也不一定支持 `GET`。

## 导入 Pydantic 的 `BaseModel`

首先，从 `pydantic` 中导入 `BaseModel`：

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## 创建数据模型

然后，把数据模型声明为继承自 `BaseModel` 的类。

使用 Python 标准类型声明所有属性：

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

包含默认值的模型属性与声明查询参数一样，不是必选的。没有默认值的模型属性是必选的。模型属性的默认值设为 `None`，则为可选。

例如，上述模型声明了如下 JSON「对象」（也是 Python 的 `dict`）：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

……由于 `description` 和 `tax` 是可选的（默认值为 `None`），下面的 JSON「对象」也有效：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 声明请求体参数

使用与声明路径和查询参数相同的方式声明请求体，就可以把请求体添加至*路径操作*：

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

……此处，请求体参数的类型为 `Item` 模型。

## 结果

仅使用 Python 类型声明，**FastAPI** 就可以：

* 以 JSON 形式读取请求体；
* （在需要时）把请求体转换为对应的类型；
* 校验数据：
    * 数据无效时返回错误信息，指出错误数据的确切位置和内容。
* 把接收的数据赋值给参数 `item`；
    * 由于已经在函数中把请求体参数声明为 `Item` 类型，还可以获得代码补全等对于所有属性及其类型的编辑器支持。
* 为模型生成 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定义，可以在项目中其他任何所需的位置使用；
* 这些概图作为 OpenAPI 概图的部件，用于自动文档 <abbr title="用户界面">UI</abbr>。

## 自动文档

模型的 JSON 概图是 OpenAPI 生产的概图部件，可显示在 API 交互文档中：

<img src="/img/tutorial/body/image01.png">

而且，还会用于 API 文档中使用了概图的*路径操作*：

<img src="/img/tutorial/body/image02.png">

## 编辑器的支持

在编辑器中，函数内部均可使用类型提示、代码补全（如果接收的不是 Pydantic 模型，而是 `dict` ，就不会出现）：

<img src="/img/tutorial/body/image03.png">

还支持对错误类型操作的错误检查：

<img src="/img/tutorial/body/image04.png">

这并非偶然，整个框架都是围绕这种操作精心设计的。

并且，在着手实现 FastAPI 之前的设计阶段，我们就已经进行了全面测试，以确保 FastAPI 可以获得所有编辑器的支持。

甚至 Pydantic 也做出了改进，以支持此功能。

虽然上面的截图取自 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>。

但 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 和大多数 Python 编辑器也支持同样的功能：

<img src="/img/tutorial/body/image05.png">

!!! tip "提示"

    使用 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 编辑器时，推荐 <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm 插件</a>。
    
    该插件用于改进 PyCharm 对 Pydantic 模型的支持，优化的功能如下：
    
    * 自动补全
    * 类型检查
    * 代码重构
    * 查找
    * 代码审查

## 使用模型

在函数内部，可以直接访问模型对象的所有属性：

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## 请求体 + 路径参数

**FastAPI** 支持同时声明路径参数和请求体。

**FastAPI** 可以识别出与路径参数匹配的，**要从路径中获取**的函数参数，以及声明为 Pydantic 模型的，**要从请求体中获取**的函数参数。

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## 请求体 + 路径参数 + 查询参数

**FastAPI** 还支持同时声明**请求体**、**路径参数**和**查询参数**。

**FastAPI** 可以正确识别出这三种参数，并从正确的位置获取数据。

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

函数参数按如下规则进行识别：

- **路径**中声明了相同参数的参数，是路径参数
- 类型是（`int`、`float`、`str`、`bool` 等）**单类型**的参数，是**查询**参数
- 类型是 **Pydantic 模型**的参数，是**请求体**

!!! note "笔记"

    因为默认值是 `=None`， FastAPI 可以识别出 `q` 是可选的。
    
    FastAPI 不使用 `Optional[str]` 中的 `Optional`， 但 `Optional` 可以让编辑器提供更好的支持，并检测错误。

## 不使用 Pydantic

即便不使用 Pydantic 模型，也可以使用 **Body** 参数。请参阅[请求体 - 多参数：请求体中的单值](body-multiple-params.md#singular-values-in-body){.internal-link target=\_blank}。
