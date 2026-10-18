# 路径参数 { #path-parameters }

你可以使用与 Python 字符串格式化相同的语法声明路径“参数”或“变量”：

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

路径参数 `item_id` 的值会作为参数 `item_id` 传递给你的函数。

运行示例并访问 [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)，可获得如下响应：

```JSON
{"item_id":"foo"}
```

## 声明路径参数的类型 { #path-parameters-with-types }

使用 Python 标准类型注解，声明路径操作函数中路径参数的类型：

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

本例把 `item_id` 的类型声明为 `int`。

/// tip | 提示

类型声明将为函数提供错误检查、代码补全等编辑器支持。

///

## 数据<dfn title="也称为：序列化、解析、编组">转换</dfn> { #data-conversion }

运行示例并访问 [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3)，返回的响应如下：

```JSON
{"item_id":3}
```

/// tip | 提示

注意，函数接收并返回的值是 `3`（ `int`），不是 `"3"`（`str`）。

**FastAPI** 通过类型声明自动进行请求的<dfn title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">“解析”</dfn>。

///

## 数据校验 { #data-validation }

通过浏览器访问 [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)，接收如下 HTTP 错误信息：

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

这是因为路径参数 `item_id` 的值（`"foo"`）的类型不是 `int`。

值的类型不是 `int` 而是浮点数（`float`）时也会显示同样的错误，比如： [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// tip | 提示

**FastAPI** 使用同样的 Python 类型声明实现了数据校验。

注意，上面的错误清晰地指出了未通过校验的具体位置。

这在开发调试与 API 交互的代码时非常有用。

///

## 文档 { #documentation }

访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)，查看自动生成的交互式 API 文档：

<img src="/img/tutorial/path-params/image01.png">

/// tip | 提示

还是使用 Python 类型声明，**FastAPI** 提供了（集成 Swagger UI 的）自动交互式文档。

注意，路径参数的类型是整数。

///

## 基于标准的好处，备选文档 { #standards-based-benefits-alternative-documentation }

**FastAPI** 使用 [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md) 生成概图，所以能兼容很多工具。

因此，**FastAPI** 还内置了 ReDoc 生成的备选 API 文档，可在此查看 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)：

<img src="/img/tutorial/path-params/image02.png">

同样，还有很多兼容工具，包括多种语言的代码生成工具。

## Pydantic { #pydantic }

所有数据校验都由 [Pydantic](https://pydantic.dev/docs/) 在幕后完成，因此你能从中获得所有好处。而且你可以放心。

同样，`str`、`float`、`bool` 以及很多复合数据类型都可以使用类型声明。

接下来的章节会介绍其中的好几种。

## 顺序很重要 { #order-matters }

有时，*路径操作*中的路径是写死的。

比如要使用 `/users/me` 获取当前用户的数据。

然后还要使用 `/users/{user_id}`，通过用户 ID 获取指定用户的数据。

由于*路径操作*是按顺序依次运行的，因此，一定要在 `/users/{user_id}` 之前声明 `/users/me` ：

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

否则，`/users/{user_id}` 将匹配 `/users/me`，FastAPI 会**认为**正在接收值为 `"me"` 的 `user_id` 参数。

同样，你不能重复定义一个路径操作：

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

由于路径首先匹配，始终会使用第一个定义的。

## 预设值 { #predefined-values }

如果你的*路径操作*接收一个*路径参数*，但你希望可能有效的*路径参数*值是预设的，可以使用标准 Python <abbr title="Enumeration - 枚举">`Enum`</abbr>。

### 创建 `Enum` 类 { #create-an-enum-class }

导入 `Enum` 并创建继承自 `str` 和 `Enum` 的子类。

通过从 `str` 继承，API 文档就能把值的类型定义为**字符串**，并且能正确渲染。

然后，创建包含固定值的类属性，这些固定值是可用的有效值：

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | 提示

如果你好奇，"AlexNet"、"ResNet" 和 "LeNet" 只是机器学习<dfn title="技术上来说是深度学习模型架构">模型</dfn>的名字。

///

### 声明*路径参数* { #declare-a-path-parameter }

使用你创建的枚举类（`ModelName`）创建带有类型注解的*路径参数*：

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### 查看文档 { #check-the-docs }

由于*路径参数*的可用值是预定义的，交互式文档可以很好地显示它们：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python *枚举* { #working-with-python-enumerations }

*路径参数*的值是一个*枚举成员*。

#### 比较*枚举成员* { #compare-enumeration-members }

可以将其与你创建的枚举 `ModelName` 中的*枚举成员*进行比较：

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### 获取*枚举值* { #get-the-enumeration-value }

使用 `model_name.value` 或通用的 `your_enum_member.value` 获取实际的值（本例中为 `str`）：

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | 提示

使用 `ModelName.lenet.value` 也能获取值 `"lenet"`。

///

#### 返回*枚举成员* { #return-enumeration-members }

即使嵌套在 JSON 请求体里（例如，`dict`），也可以从你的*路径操作*返回*枚举成员*。

返回给客户端之前，会把它们转换为对应的值（本例中为字符串）：

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

客户端中的 JSON 响应如下：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路径的路径参数 { #path-parameters-containing-paths }

假设你有一个路径为 `/files/{file_path}` 的*路径操作*。

但需要 `file_path` 本身也包含*路径*，比如，`home/johndoe/myfile.txt`。

因此，该文件的 URL 可能是这样的：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支持 { #openapi-support }

OpenAPI 不支持声明内部包含*路径*的*路径参数*，因为这会导致测试和定义更加困难。

不过，仍可使用 Starlette 内部工具之一在 **FastAPI** 中实现这一功能。

而且不影响文档正常运行，但是不会添加该参数应包含路径的说明。

### 路径转换器 { #path-convertor }

直接使用 Starlette 的选项，就可以用如下 URL 声明包含*路径*的*路径参数*：

```
/files/{file_path:path}
```

本例中，参数名为 `file_path`，结尾部分的 `:path` 说明该参数应匹配任意*路径*。

用法如下：

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | 提示

注意，包含 `/home/johndoe/myfile.txt` 的路径参数要以斜杠（`/`）开头。

本例中的 URL 是 `/files//home/johndoe/myfile.txt`。注意，`files` 和 `home` 之间要使用双斜杠（`//`）。

///

## 小结 { #recap }

通过简短、直观的 Python 标准类型声明，**FastAPI** 可以获得：

* 编辑器支持：错误检查，代码自动补全等
* 数据 "<dfn title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">解析</dfn>"
* 数据校验
* API 注解和自动文档

只需要声明一次即可。

这可能是除了性能以外，**FastAPI** 与其它框架相比的主要优势。
