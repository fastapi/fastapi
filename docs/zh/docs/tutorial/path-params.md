# 路径参数 { #path-parameters }

FastAPI 支持使用与 Python 格式化字符串相同的语法声明路径“参数”或“变量”：

{* ../../docs_src/path_params/tutorial001_py39.py hl[6:7] *}

路径参数 `item_id` 的值会作为参数 `item_id` 传递给你的函数。

所以，如果你运行这个示例并访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，你将看到如下响应：

```JSON
{"item_id":"foo"}
```

## 带类型的路径参数 { #path-parameters-with-types }

你可以在函数中使用标准 Python 类型注解来声明路径参数的类型：

{* ../../docs_src/path_params/tutorial002_py39.py hl[7] *}

在这个例子中，`item_id` 被声明为 `int`。

/// check

这会在你的函数内部提供编辑器支持，例如错误检查、代码补全等。

///

## 数据<abbr title="also known as: serialization, parsing, marshalling - 也称为：序列化、解析、编组">转换</abbr> { #data-conversion }

如果你运行这个示例并在浏览器中打开 <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>，你将看到如下响应：

```JSON
{"item_id":3}
```

/// check

注意，你的函数接收（并返回）的值是 `3`，作为 Python 的 `int`，而不是字符串 `"3"`。

因此，有了这个类型声明，**FastAPI** 就会为你自动进行请求 <abbr title="converting the string that comes from an HTTP request into Python data - 将来自 HTTP 请求的字符串转换为 Python 数据">“parsing”</abbr>。

///

## 数据校验 { #data-validation }

但是，如果你在浏览器中访问 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，你将看到一个很友好的 HTTP 错误：

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

这是因为路径参数 `item_id` 的值是 `"foo"`，它不是 `int`。

如果你提供的是 `float` 而不是 `int`，也会出现同样的错误，例如：<a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check

所以，同样通过 Python 类型声明，**FastAPI** 会为你提供数据校验。

注意，错误也清晰地指出了校验未通过的具体位置。

这在开发和调试与 API 交互的代码时非常有用。

///

## 文档 { #documentation }

当你在浏览器中打开 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> 时，你将看到自动生成的、可交互的 API 文档，例如：

<img src="/img/tutorial/path-params/image01.png">

/// check

同样，只通过这个 Python 类型声明，**FastAPI** 就会为你提供自动的、可交互的文档（集成 Swagger UI）。

注意，路径参数被声明为整数。

///

## 基于标准的好处，备选文档 { #standards-based-benefits-alternative-documentation }

并且因为生成的 schema 来自 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> 标准，所以有很多兼容工具。

因此，**FastAPI** 本身也提供了一个备选的 API 文档（使用 ReDoc），你可以在 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> 访问：

<img src="/img/tutorial/path-params/image02.png">

同样，有很多兼容工具，包括适用于多种语言的代码生成工具。

## Pydantic { #pydantic }

所有的数据校验都由 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 在底层完成，因此你能获得它的所有好处。你也可以放心交给它处理。

你可以用同样的类型声明来声明 `str`、`float`、`bool` 以及许多其他复杂数据类型。

教程接下来的章节会介绍其中的若干内容。

## 顺序很重要 { #order-matters }

在创建*路径操作*时，你可能会遇到有固定路径的情况。

比如 `/users/me`，假设它用于获取当前用户的数据。

然后你还可以有一个路径 `/users/{user_id}`，用于通过某个用户 ID 获取特定用户的数据。

因为*路径操作*会按顺序依次进行匹配，你需要确保 `/users/me` 的路径声明在 `/users/{user_id}` 之前：

{* ../../docs_src/path_params/tutorial003_py39.py hl[6,11] *}

否则，`/users/{user_id}` 的路径也会匹配 `/users/me`，“认为”它接收到了一个值为 `"me"` 的 `user_id` 参数。

同样地，你不能重定义一个路径操作：

{* ../../docs_src/path_params/tutorial003b_py39.py hl[6,11] *}

第一个将始终被使用，因为它会先匹配到该路径。

## 预定义值 { #predefined-values }

如果你有一个接收*路径参数*的*路径操作*，但你希望可用的有效*路径参数*值是预先定义好的，你可以使用标准 Python 的 <abbr title="Enumeration">`Enum`</abbr>。

### 创建 `Enum` 类 { #create-an-enum-class }

导入 `Enum` 并创建一个同时继承 `str` 和 `Enum` 的子类。

通过继承 `str`，API 文档就能知道这些值必须是 `string` 类型，并能正确渲染。

然后创建具有固定值的类属性，这些固定值就是可用的有效值：

{* ../../docs_src/path_params/tutorial005_py39.py hl[1,6:9] *}

/// tip

如果你在想，“AlexNet”、“ResNet” 和 “LeNet” 只是机器学习<abbr title="Technically, Deep Learning model architectures - 技术上来说是深度学习模型架构">models</abbr>的名字。

///

### 声明*路径参数* { #declare-a-path-parameter }

然后使用你创建的枚举类（`ModelName`）来创建一个带类型注解的*路径参数*：

{* ../../docs_src/path_params/tutorial005_py39.py hl[16] *}

### 查看文档 { #check-the-docs }

因为*路径参数*的可用值是预定义的，可交互文档可以很好地展示它们：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python *枚举* { #working-with-python-enumerations }

*路径参数*的值将是一个*枚举成员*。

#### 比较*枚举成员* { #compare-enumeration-members }

你可以将它与创建的枚举 `ModelName` 中的*枚举成员*进行比较：

{* ../../docs_src/path_params/tutorial005_py39.py hl[17] *}

#### 获取*枚举值* { #get-the-enumeration-value }

你可以使用 `model_name.value` 获取实际的值（本例中为 `str`），或者一般来说，使用 `your_enum_member.value`：

{* ../../docs_src/path_params/tutorial005_py39.py hl[20] *}

/// tip

你也可以用 `ModelName.lenet.value` 访问值 `"lenet"`。

///

#### 返回*枚举成员* { #return-enumeration-members }

你可以从你的*路径操作*返回*枚举成员*，即使它们嵌套在 JSON body（例如 `dict`）中。

在返回给客户端之前，它们会被转换成对应的值（本例中为字符串）：

{* ../../docs_src/path_params/tutorial005_py39.py hl[18,21,23] *}

客户端将得到类似如下的 JSON 响应：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路径的路径参数 { #path-parameters-containing-paths }

假设你有一个*路径操作*，路径是 `/files/{file_path}`。

但你需要 `file_path` 本身包含一个*路径*，例如 `home/johndoe/myfile.txt`。

那么这个文件的 URL 会是类似：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支持 { #openapi-support }

OpenAPI 不支持声明一个*路径参数*来在内部包含*路径*，因为那可能会导致难以测试和定义的场景。

尽管如此，你仍然可以在 **FastAPI** 中使用 Starlette 的内部工具来实现它。

并且文档仍然可用，尽管不会添加说明该参数应该包含路径的文档。

### 路径转换器 { #path-convertor }

使用 Starlette 的一个选项，你可以用如下 URL 声明一个包含*路径*的*路径参数*：

```
/files/{file_path:path}
```

此时，参数名为 `file_path`，最后一部分 `:path` 表示该参数应匹配任意*路径*。

所以，你可以这样使用：

{* ../../docs_src/path_params/tutorial004_py39.py hl[6] *}

/// tip

你可能需要参数包含 `/home/johndoe/myfile.txt`，并以斜杠（`/`）开头。

这种情况下，URL 会是：`/files//home/johndoe/myfile.txt`，在 `files` 和 `home` 之间有一个双斜杠（`//`）。

///

## 小结 { #recap }

在 **FastAPI** 中，通过使用简短、直观、标准的 Python 类型声明，你将获得：

* 编辑器支持：错误检查、自动补全等
* 数据“<abbr title="converting the string that comes from an HTTP request into Python data - 将来自 HTTP 请求的字符串转换为 Python 数据">parsing</abbr>”
* 数据校验
* API 注解与自动文档

并且你只需要声明一次。

这大概是 **FastAPI** 相比其他框架最主要的可见优势（除了原始性能之外）。
