# 路径参数

FastAPI 支持使用 Python 字符串格式化语法声明**路径参数**（**变量**）：

{* ../../docs_src/path_params/tutorial001.py hl[6:7] *}

这段代码把路径参数 `item_id` 的值传递给路径函数的参数 `item_id`。

运行示例并访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，可获得如下响应：

```JSON
{"item_id":"foo"}
```

## 声明路径参数的类型

使用 Python 标准类型注解，声明路径操作函数中路径参数的类型。

{* ../../docs_src/path_params/tutorial002.py hl[7] *}

本例把 `item_id` 的类型声明为 `int`。

/// check | 检查

类型声明将为函数提供错误检查、代码补全等编辑器支持。

///

## 数据<abbr title="也称为：序列化、解析">转换</abbr>

运行示例并访问 <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>，返回的响应如下：

```JSON
{"item_id":3}
```

/// check | 检查

注意，函数接收并返回的值是 `3`（ `int`），不是 `"3"`（`str`）。

**FastAPI** 通过类型声明自动<abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">**解析**请求中的数据</abbr>。

///

## 数据校验

通过浏览器访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，接收如下 HTTP 错误信息：

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

这是因为路径参数 `item_id` 的值 （`"foo"`）的类型不是 `int`。

值的类型不是 `int ` 而是浮点数（`float`）时也会显示同样的错误，比如： <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2。</a>

/// check | 检查

**FastAPI** 使用 Python 类型声明实现了数据校验。

注意，上面的错误清晰地指出了未通过校验的具体原因。

这在开发调试与 API 交互的代码时非常有用。

///

## 查看文档

访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，查看自动生成的 API 文档：

<img src="/img/tutorial/path-params/image01.png">

/// check | 检查

还是使用 Python 类型声明，**FastAPI** 提供了（集成 Swagger UI 的）API 文档。

注意，路径参数的类型是整数。

///

## 基于标准的好处，备选文档

**FastAPI** 使用 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" class="external-link" target="_blank">OpenAPI</a> 生成概图，所以能兼容很多工具。

因此，**FastAPI** 还内置了 ReDoc 生成的备选 API 文档，可在此查看 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>：

<img src="/img/tutorial/path-params/image02.png">

同样，还有很多兼容工具，包括多种语言的代码生成工具。

## Pydantic

FastAPI 充分地利用了 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 的优势，用它在后台校验数据。众所周知，Pydantic 擅长的就是数据校验。

同样，`str`、`float`、`bool` 以及很多复合数据类型都可以使用类型声明。

下一章介绍详细内容。

## 顺序很重要

有时，*路径操作*中的路径是写死的。

比如要使用 `/users/me` 获取当前用户的数据。

然后还要使用 `/users/{user_id}`，通过用户 ID 获取指定用户的数据。

由于*路径操作*是按顺序依次运行的，因此，一定要在 `/users/{user_id}` 之前声明 `/users/me` ：

{* ../../docs_src/path_params/tutorial003.py hl[6,11] *}

否则，`/users/{user_id}` 将匹配 `/users/me`，FastAPI 会**认为**正在接收值为 `"me"` 的 `user_id` 参数。

## 预设值

路径操作使用 Python 的 <abbr title="Enumeration">`Enum`</abbr> 类型接收预设的*路径参数*。

### 创建 `Enum` 类

导入 `Enum` 并创建继承自 `str` 和 `Enum` 的子类。

通过从 `str` 继承，API 文档就能把值的类型定义为**字符串**，并且能正确渲染。

然后，创建包含固定值的类属性，这些固定值是可用的有效值：

{* ../../docs_src/path_params/tutorial005.py hl[1,6:9] *}

/// info | 说明

Python 3.4 及之后版本支持<a href="https://docs.python.org/zh-cn/3/library/enum.html" class="external-link" target="_blank">枚举（即 enums）</a>。

///

/// tip | 提示

**AlexNet**、**ResNet**、**LeNet** 是机器学习<abbr title="技术上来说是深度学习模型架构">模型</abbr>。

///

### 声明*路径参数*

使用 Enum 类（`ModelName`）创建使用类型注解的*路径参数*：

{* ../../docs_src/path_params/tutorial005.py hl[16] *}

### 查看文档

 API 文档会显示预定义*路径参数*的可用值：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python _枚举类型_

*路径参数*的值是枚举的元素。

#### 比较*枚举元素*

枚举类 `ModelName` 中的*枚举元素*支持比较操作：

{* ../../docs_src/path_params/tutorial005.py hl[17] *}

#### 获取*枚举值*

使用 `model_name.value` 或 `your_enum_member.value` 获取实际的值（本例中为**字符串**）：

{* ../../docs_src/path_params/tutorial005.py hl[20] *}

/// tip | 提示

使用 `ModelName.lenet.value` 也能获取值 `"lenet"`。

///

#### 返回*枚举元素*

即使嵌套在 JSON 请求体里（例如， `dict`），也可以从*路径操作*返回*枚举元素*。

返回给客户端之前，要把枚举元素转换为对应的值（本例中为字符串）：

{* ../../docs_src/path_params/tutorial005.py hl[18,21,23] *}

客户端中的 JSON 响应如下：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路径的路径参数

假设*路径操作*的路径为 `/files/{file_path}`。

但需要 `file_path` 中也包含*路径*，比如，`home/johndoe/myfile.txt`。

此时，该文件的 URL 是这样的：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支持

OpenAPI 不支持声明包含路径的*路径参数*，因为这会导致测试和定义更加困难。

不过，仍可使用 Starlette 内置工具在 **FastAPI** 中实现这一功能。

而且不影响文档正常运行，但是不会添加该参数包含路径的说明。

### 路径转换器

直接使用 Starlette 的选项声明包含*路径*的*路径参数*：

```
/files/{file_path:path}
```

本例中，参数名为 `file_path`，结尾部分的 `:path` 说明该参数应匹配*路径*。

用法如下：

{* ../../docs_src/path_params/tutorial004.py hl[6] *}

/// tip | 提示

注意，包含 `/home/johndoe/myfile.txt` 的路径参数要以斜杠（`/`）开头。

本例中的 URL 是 `/files//home/johndoe/myfile.txt`。注意，`files` 和 `home` 之间要使用**双斜杠**（`//`）。

///

## 小结

通过简短、直观的 Python 标准类型声明，**FastAPI** 可以获得：

- 编辑器支持：错误检查，代码自动补全等
- 数据**<abbr title="把来自 HTTP 请求中的字符串转换为 Python 数据类型">解析</abbr>**
- 数据校验
- API 注解和 API 文档

只需要声明一次即可。

这可能是除了性能以外，**FastAPI** 与其它框架相比的主要优势。
