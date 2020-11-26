# 请求文件

您可以使用 `File` 定义客户端上传的文件。

!!! info
    要接收上传的文件，首先需要安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    如： `pip install python-multipart`.

    这是因为上传的文件是作为 "form data" 发送的。

## 导入 `File`

从 `fastapi` 导入 `File` 和 `UploadFile`:

```Python hl_lines="1"
{!../../../docs_src/request_files/tutorial001.py!}
```

## 定义 `File` 参数

创建文件参数的方法和`Body` 或 `Form` 时相同:

```Python hl_lines="7"
{!../../../docs_src/request_files/tutorial001.py!}
```

!!! info
    `File` 是直接继承 `Form` 的一个子类就

    但是要记住，当你从 `fastapi` 导入 `Query`, `Path`, `File` 和其他类似项目时, 实际上导入的是返回特定类型的工厂函数。

!!! tip
    要声明文件请求体，需要使用 `File`, 否则参数将被解释为查询参数或请求体(JSON)参数。

这些文件将以 "表单数据" 的形式上传。

如果您在 *路径操作函数* 中将参数类型声明为 `bytes`，**FastAPI** 将会为您读取文件，您将以 `bytes` 的形式接收文件的内容。

请记住，这意味着整个内容将存储在内存中。这对小文件很有效。

但是在一些情况下，使用 `UploadFile` 将可能会更加有益。

## `File` 参数使用 `UploadFile` 类型

使用 `UploadFile` 类型定义一个 `File` 参数

```Python hl_lines="12"
{!../../../docs_src/request_files/tutorial001.py!}
```

使用 `UploadFile` 相较 `bytes` 有许多优势：

* 它使用一个 "假脱机" 文件:
    * 在内存中存储的文件的具有最大大小限制，在超过这个限制后，它将被存储在磁盘上。
* 这意味着它可以很好地处理大文件，如图像，视频，大型二进制文件等，而不消耗所有的内存。
* 你可以从上传的文件中获取元数据。
* 它是一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">类文件</a> `async` 接口。
* 它公开了一个实际的Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> 对象，您可以直接传递给其他期望一个类文件对象的库。

### `UploadFile`

`UploadFile` 具有如下的属性：

* `filename`: 一个上传的原始文件名的 `str` (如 `myimage.jpg`)。
* `content_type`: 一个内容类型的 `str` (MIME type / media type) (如 `image/jpeg`)。
* `file`: 一个 <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">类文件</a> 对象)。 这是实际的Python文件，您可以直接传递给其他需要 "类文件" 对象的函数或库。

`UploadFile` 具有如下的 `async` 方法。它们都在内部调用相应的文件方法(使用内部 `SpooledTemporaryFile` )。

* `write(data)`: 写 `data` (`str` 或 `bytes`) 到文件。
* `read(size)`: 读 `size` (`int`) 大小的文件 字节/字符。
* `seek(offset)`: 移动文件中的字节位置到 `offset` (`int`)。
    * 如, `await myfile.seek(0)` 将会移动到文件开头。
    * 如果你运行过 `await myfile.read()` 之后，想再次读取这些内容，这将十分有用。
* `close()`: 关闭文件.

所有这些方法都是 `async` 方法，你需要 "await" 他们。

比如，在一个 `async` *路径操作函数* 之内你可以这样获取内容:

```Python
contents = await myfile.read()
```

如果你在一个普通的 `def` *路径操作函数* 内部，你可以直接访问`UploadFile.file`，比如：

```Python
contents = myfile.file.read()
```

!!! note "`async` 技术细节"
    当你使用 `async` 方法, **FastAPI** 在线程池中运行文件方法并等待它们

!!! note "Starlette 技术细节"
    **FastAPI** 的 `UploadFile` 直接继承自**Starlette** 的 `UploadFile`，但是增加了一些必要的部分来保证其与 **Pydantic** 和 FastAPI 的其它部分兼容。

## 什么是 "表单数据"

HTML表单 (`<form></form>`) 向服务器发送数据的方式通常使用该数据的 "特殊" 编码，这与JSON不同。

**FastAPI** 将确保从正确的位置读取数据，而不是JSON。

!!! note "技术细节"
    当不包括文件时，来自表单的数据通常使用 "媒体类型" `application/x-www-form-urlencoded` 。

    但是当表单包含文件时，它被编码为 `multipart/form-data`。如果你使用 `File`, **FastAPI** 将知道它必须从请求体的正确部分获取文件。
    
    如果你想了解更多关于这些编码和表单字段的信息，请访问<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> 网站，查看 <code>POST</code></a>的文档。

!!! warning
    你可以在一个 *路径操作* 中声明多个 `File` 和 `Form` 参数，但你不能同时声明 `Body` 字段，以希望收到内容是JSON格式，因为请求体将使用 `multipart/form-data` 编码而不是 `application/json`。

    这不是 **FastAPI** 的限制，而是HTTP协议的一部分.

## 多个文件上传

可以同时上传几个文件。

它们将与使用 "表单数据" 发送的相同 "表单字段" 相关联。

要使用它，声明一个 `bytes` 或 `UploadFile` 的 `List`：

```Python hl_lines="10  15"
{!../../../docs_src/request_files/tutorial002.py!}
```

您将会和所声明的一样，接收一个 `bytes` 或 `UploadFile` 的 `list`。

!!! note
    注意，直到 2019-04-14, Swagger UI 不支持在同一个表单字段中上传多个文件。如需更多信息，请查看<a href="https://github.com/swagger-api/swagger-ui/issues/4276" class="external-link" target="_blank">#4276</a> 和 <a href="https://github.com/swagger-api/swagger-ui/issues/3641" class="external-link" target="_blank">#3641</a>.

    不过，**FastAPI** 已经与它兼容，使用的是标准的OpenAPI。
    
    所以，只要Swagger UI支持多文件上传，或者任何其他支持OpenAPI的工具，它们都将与**FastAPI**兼容。

!!! note "技术细节"
    你也可以使用 `from starlette.responses import HTMLResponse`.

    **FastAPI** 提供了 `fastapi.responses`，但实际上和 `starlette.responses` 是相同的。只是为了方便开发者。但大多数可用的响应都直接来自Starlette。

## 回顾

使用 `File` 将上传的文件声明为输入参数(作为表单数据)。
