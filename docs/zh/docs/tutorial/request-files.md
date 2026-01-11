# 请求文件 { #request-files }

你可以使用 `File` 定义要由客户端上传的文件。

/// info | 信息

要接收上传的文件，先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装它，例如：

```console
$ pip install python-multipart
```

这是因为上传的文件是以“表单数据”形式发送的。

///

## 导入 `File` { #import-file }

从 `fastapi` 导入 `File` 和 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[3] *}

## 定义 `File` 参数 { #define-file-parameters }

创建文件参数的方式与 `Body` 或 `Form` 相同：

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[9] *}

/// info | 信息

`File` 是一个直接继承自 `Form` 的类。

但请记住，当你从 `fastapi` 导入 `Query`、`Path`、`File` 等时，它们实际上是返回特殊类的函数。

///

/// tip | 提示

要声明 File 请求体，你需要使用 `File`，否则这些参数会被解释为查询参数或请求体（JSON）参数。

///

文件会以“表单数据”的形式上传。

如果你将*路径操作函数*参数的类型声明为 `bytes`，**FastAPI** 会为你读取文件，你将以 `bytes` 的形式收到其内容。

请记住，这意味着整个内容都会存储在内存中。这对小文件很有效。

但在好些情况下，你可能会从使用 `UploadFile` 中获益。

## 含 `UploadFile` 的文件参数 { #file-parameters-with-uploadfile }

定义类型为 `UploadFile` 的文件参数：

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[14] *}

使用 `UploadFile` 相比 `bytes` 有几个优势：

* 你不必在参数的默认值中使用 `File()`。
* 它使用一种“spooled”文件：
    * 文件会先存储在内存中，直到达到最大大小限制，超过该限制后会存储到磁盘。
* 这意味着它能很好地处理图像、视频、大型二进制文件等大文件，而不会消耗所有内存。
* 你可以获取上传文件的元数据。
* 它有一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> 的 `async` 接口。
* 它暴露了一个真实的 Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> 对象，你可以直接将其传递给其他期望 file-like 对象的库。

### `UploadFile` { #uploadfile }

`UploadFile` 具有以下属性：

* `filename`：一个 `str`，表示上传的原始文件名（例如 `myimage.jpg`）。
* `content_type`：一个 `str`，表示内容类型（MIME type / media type）（例如 `image/jpeg`）。
* `file`：一个 <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>（一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> 对象）。这是实际的 Python 文件对象，你可以直接把它传给其他期望“file-like”对象的函数或库。

`UploadFile` 有以下 `async` 方法。它们都会在底层调用对应的文件方法（使用内部的 `SpooledTemporaryFile`）。

* `write(data)`：把 `data`（`str` 或 `bytes`）写入文件。
* `read(size)`：读取文件的 `size`（`int`）个字节/字符。
* `seek(offset)`：跳转到文件中的字节位置 `offset`（`int`）。
    * 例如，`await myfile.seek(0)` 会跳到文件开头。
    * 如果你先运行了一次 `await myfile.read()`，之后又需要再次读取内容，这会特别有用。
* `close()`：关闭文件。

由于这些方法都是 `async` 方法，你需要对它们使用 “await”。

例如，在 `async` *路径操作函数* 中，你可以用下面的方式获取内容：

```Python
contents = await myfile.read()
```

如果你在普通的 `def` *路径操作函数* 中，你可以直接访问 `UploadFile.file`，例如：

```Python
contents = myfile.file.read()
```

/// note | `async` 技术细节

当你使用这些 `async` 方法时，**FastAPI** 会在线程池中运行文件方法并等待它们完成。

///

/// note | Starlette 技术细节

**FastAPI** 的 `UploadFile` 直接继承自 **Starlette** 的 `UploadFile`，但添加了一些必要的部分，使其与 **Pydantic** 以及 FastAPI 的其他部分兼容。

///

## 什么是“表单数据” { #what-is-form-data }

HTML 表单（`<form></form>`）向服务器发送数据的方式通常会对数据使用一种“特殊”的编码，它不同于 JSON。

**FastAPI** 会确保从正确的位置读取这些数据，而不是从 JSON 中读取。

/// note | 技术细节

不包含文件时，表单数据通常使用“媒体类型” `application/x-www-form-urlencoded` 编码。

但当表单包含文件时，会使用 `multipart/form-data` 编码。如果你使用 `File`，**FastAPI** 就会知道它必须从请求体的正确部分获取文件。

如果你想了解更多关于这些编码和表单字段的信息，请查看 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs 的 <code>POST</code></a>。

///

/// warning | 警告

你可以在一个*路径操作*中声明多个 `File` 和 `Form` 参数，但你不能同时声明你期望以 JSON 接收的 `Body` 字段，因为该请求的请求体会使用 `multipart/form-data` 而不是 `application/json` 进行编码。

这不是 **FastAPI** 的限制，这是 HTTP 协议的一部分。

///

## 可选文件上传 { #optional-file-upload }

你可以使用标准类型注解并将默认值设置为 `None` 来使文件变为可选：

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## 带有额外元数据的 `UploadFile` { #uploadfile-with-additional-metadata }

你也可以将 `File()` 与 `UploadFile` 一起使用，例如，用于设置额外的元数据：

{* ../../docs_src/request_files/tutorial001_03_an_py39.py hl[9,15] *}

## 多文件上传 { #multiple-file-uploads }

可以同时上传多个文件。

它们会关联到同一个使用“表单数据”发送的“表单字段”。

要使用它，声明一个 `bytes` 或 `UploadFile` 的列表：

{* ../../docs_src/request_files/tutorial002_an_py39.py hl[10,15] *}

你将按声明接收到一个由 `bytes` 或 `UploadFile` 组成的 `list`。

/// note | 技术细节

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 提供了与 `fastapi.responses` 相同的 `starlette.responses`，只是为了方便你（开发者）使用。但大多数可用的响应都直接来自 Starlette。

///

### 带有额外元数据的多文件上传 { #multiple-file-uploads-with-additional-metadata }

与之前相同，你可以使用 `File()` 来设置额外参数，即使对于 `UploadFile` 也是如此：

{* ../../docs_src/request_files/tutorial003_an_py39.py hl[11,18:20] *}

## 小结 { #recap }

使用 `File`、`bytes` 和 `UploadFile` 来声明要在请求中上传的文件，它们会以表单数据形式发送。
