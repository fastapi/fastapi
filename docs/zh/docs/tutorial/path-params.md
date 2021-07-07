# 路径参数

FastAPI 支持使用 Python 字符串格式化语法声明路径「参数」或「变量」：

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

路径参数 `item_id` 的值作为参数 `item_id` 传递给函数。

所以，运行示例并访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，获得如下响应：

```JSON
{"item_id":"foo"}
```

## 带类型的路径参数

使用 Python 标准类型注解，声明函数中路径参数的类型。

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

本例中，`item_id` 的类型声明为 `int`。

!!! check "检查"

    这将为函数提供错误检查、代码补全等编辑器支持。

## 数据<abbr title="也被称为：序列化、解析">转换</abbr>

运行示例，打开浏览器访问 <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>，获得如下响应：

```JSON
{"item_id":3}
```

!!! check "检查"

    注意，函数接收并返回的值是 `3`（ `int`），不是 `"3"`（`str`）。
    
    **FastAPI** 通过类型声明自动<abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">「解析」请求中的数据</abbr>。

## 数据校验

通过浏览器访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，会接收到 HTTP 错误信息：

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

因为路径参数 `item_id` 传入的值为 `"foo"`，不是 `int` 类型。

如果提供的是浮点数（`float`），不是整数，也会提示同样的错误，比如： <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check "检查"

    通过 Python 类型声明，**FastAPI** 实现了数据校验。
    
    注意，上面的错误同样清楚地指出了校验未通过的具体原因。
    
    开发与调试和 API 交互的代码时，这非常有用。

## 文档

通过浏览器访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，会看到自动生成的 API 交互文档：

<img src="/img/tutorial/path-params/image01.png">

!!! check "检查"

    还是通过 Python 类型声明，**FastAPI** 提供了（集成 Swagger UI 的）自动交互文档。
    
    注意，这里的路径参数类型为整数。

## 标准的好处：备选文档

由于生成的 API 概图使用 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" class="external-link" target="_blank">OpenAPI</a> 标准，所以能与很多工具兼容。

正因如此，**FastAPI** 还内置了（使用 Redoc 的）备选 API 文档：

<img src="/img/tutorial/path-params/image02.png">

同样，还有很多其他兼容工具，包括适用于多种语言的代码生成工具。

## Pydantic

所有数据校验都由 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 在后台完成，FastAPI 充分地利用了它的优势。众所周知，Pydantic 擅长的就是数据校验 。

同样，也可以为 `str`、`float`、`bool` 及其他复合数据类型使用类型声明。

下一章介绍其中的部分内容。

## 顺序很重要

有时，*路径操作*中的路径是固定不变的。

比如 `/users/me`，假设用它来获取当前用户的数据。

然后，还可以使用路径 `/users/{user_id}`，通过用户 ID 获取指定用户的数据。

由于*路径操作*是按顺序依次运行的，此时，一定要在路径 `/users/{user_id}`之前声明路径 `/users/me` ：

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

否则，`/users/{user_id}` 路径将与 `/users/me` 匹配，FastAPI 会「认为」正在接收值为 `"me"` 的 `user_id` 参数。

## 预设值

如需路径操作接收预设的*路径参数*，可以使用 Python 的 <abbr title="Enumeration">`Enum`</abbr> 类型。

### 创建 `Enum` 类

导入 `Enum` 并创建继承自 `str` 和 `Enum` 的子类。

通过从 `str` 继承，API 文档知道这些值的类型必须是 `string`，并且能正确渲染。

然后，创建包含固定值的类属性，这些固定值是可用的有效值：

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info "说明"

    Python 3.4 及之后版本支持<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">枚举（或 enums）</a>。

!!! tip "提示"

    「AlexNet」、「ResNet」、「LeNet」 是机器学习<abbr title="技术上来说是深度学习模型架构">模型</abbr>。

### 声明*路径参数*

使用定义的 Enum 类（`ModelName`）创建带有类型注解的*路径参数*：

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### 查验文档

因为已经预定义了*路径参数*的可用值，交互文档的显示效果很好：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python _枚举类型_

*路径参数*的值是*枚举的成员*。

#### 比较*枚举成员*

可以与枚举类 `ModelName` 中的*枚举项*进行比较：

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### 获取*枚举值*

`model_name.value` 或 `your_enum_member.value` 获取实际的值（本例中为 `str`）：

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip "提示"

    也可以通过 `ModelName.lenet.value` 来获取值 `"lenet"`。

#### 返回*枚举成员*

即使嵌套在 JSON 请求体（例如， `dict`）中，也可以从*路径操作*中返回*枚举成员*。

返回给客户端之前，枚举项会被转换为对应的值（本例中为字符串）：

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

客户端获取的 JSON 响应如下：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路径的路径参数

假设*路径操作*的路径为 `/files/{file_path}`。

但需要 `file_path` 中也包含*路径*，比如，`home/johndoe/myfile.txt`。

因此，该文件的 URL 是这样的：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支持

OpenAPI 不支持声明包含路径的*路径参数*，因为这可能导致测试和定义变得困难。

不过，仍可使用 Starlette 内置工具在 **FastAPI** 中实现这一功能。

而且文档也可以运行，但是不会添加有关该参数应包含路径的说明。

### 路径转换器

可以直接使用 Starlette 的选项声明包含*路径*的*路径参数*：

```
/files/{file_path:path}
```

在这种情况下，参数名为 `file_path`，结尾部分的 `:path` 说明该参数应匹配*路径*。

用法如下：

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip "提示"

    注意，包含 `/home/johndoe/myfile.txt` 的参数要以斜杠（`/`）开头。
    
    本例中的 URL 是 `/files//home/johndoe/myfile.txt`。注意，`files` 和 `home` 之间要使用双斜杠（`//`）。

## 小结

通过简短、直观的 Python 标准类型声明，**FastAPI** 可以获得：

- 编辑器支持：错误检查，代码补全等支持
- 数据「<abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">解析</abbr>」
- 数据校验
- API 标注和自动文档

只需要声明一次即可。

这可能是（除了原始性能以外） **FastAPI** 与其他框架相比的主要优势。
