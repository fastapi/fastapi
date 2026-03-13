# 请求文件 { #request-files }

你可以使用 `File` 定义由客户端上传的文件。

/// info | 信息

要接收上传的文件，请先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}、激活它，然后安装，例如：

```console
$ pip install python-multipart
```

这是因为上传文件是以「表单数据」发送的。

///

## 导入 `File` { #import-file }

从 `fastapi` 导入 `File` 和 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## 定义 `File` 参数 { #define-file-parameters }

像为 `Body` 或 `Form` 一样创建文件参数：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info | 信息

`File` 是直接继承自 `Form` 的类。

但要注意，从 `fastapi` 导入的 `Query`、`Path`、`File` 等项，实际上是返回特定类的函数。

///

/// tip | 提示

声明文件体必须使用 `File`，否则，这些参数会被当作查询参数或请求体（JSON）参数。

///

文件将作为「表单数据」上传。

如果把*路径操作函数*参数的类型声明为 `bytes`，**FastAPI** 会为你读取文件，并以 `bytes` 的形式接收其内容。

请注意，这意味着整个内容会存储在内存中，适用于小型文件。

不过，在很多情况下，使用 `UploadFile` 会更有优势。

## 含 `UploadFile` 的文件参数 { #file-parameters-with-uploadfile }

将文件参数的类型声明为 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

与 `bytes` 相比，使用 `UploadFile` 有多项优势：

* 无需在参数的默认值中使用 `File()`。
* 它使用“spooled”文件：
    * 文件会先存储在内存中，直到达到最大上限，超过该上限后会写入磁盘。
* 因此，非常适合处理图像、视频、大型二进制等大文件，而不会占用所有内存。
* 你可以获取上传文件的元数据。
* 它提供 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> 的 `async` 接口。
* 它暴露了一个实际的 Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> 对象，你可以直接传给期望「file-like」对象的其他库。

### `UploadFile` { #uploadfile }

`UploadFile` 的属性如下：

* `filename`：上传的原始文件名字符串（`str`），例如 `myimage.jpg`。
* `content_type`：内容类型（MIME 类型 / 媒体类型）的字符串（`str`），例如 `image/jpeg`。
* `file`：<a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>（一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> 对象）。这是实际的 Python 文件对象，你可以直接传递给其他期望「file-like」对象的函数或库。

`UploadFile` 具有以下 `async` 方法。它们都会在底层调用对应的文件方法（使用内部的 `SpooledTemporaryFile`）。

* `write(data)`：将 `data` (`str` 或 `bytes`) 写入文件。
* `read(size)`：读取文件中 `size` (`int`) 个字节/字符。
* `seek(offset)`：移动到文件中字节位置 `offset` (`int`)。
    * 例如，`await myfile.seek(0)` 会移动到文件开头。
    * 如果你先运行过 `await myfile.read()`，然后需要再次读取内容时，这尤其有用。
* `close()`：关闭文件。

由于这些方法都是 `async` 方法，你需要对它们使用 await。

例如，在 `async` *路径操作函数* 内，你可以这样获取内容：

```Python
contents = await myfile.read()
```

如果是在普通 `def` *路径操作函数* 内，你可以直接访问 `UploadFile.file`，例如：

```Python
contents = myfile.file.read()
```

/// note | 注意

当你使用这些 `async` 方法时，**FastAPI** 会在线程池中运行相应的文件方法并等待其完成。

///

/// note | 注意

**FastAPI** 的 `UploadFile` 直接继承自 **Starlette** 的 `UploadFile`，但添加了一些必要的部分，使其与 **Pydantic** 以及 FastAPI 的其他部分兼容。

///

## 什么是「表单数据」 { #what-is-form-data }

HTML 表单（`<form></form>`）向服务器发送数据的方式通常会对数据使用一种「特殊」的编码，这与 JSON 不同。

**FastAPI** 会确保从正确的位置读取这些数据，而不是从 JSON 中读取。

/// note | 注意

当不包含文件时，来自表单的数据通常使用「媒体类型」`application/x-www-form-urlencoded` 编码。

但当表单包含文件时，会编码为 `multipart/form-data`。如果你使用 `File`，**FastAPI** 会知道需要从请求体的正确位置获取文件。

如果你想进一步了解这些编码和表单字段，请参阅 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 开发者网络">MDN</abbr> 关于 <code>POST</code> 的 Web 文档</a>。

///

/// warning | 警告

你可以在一个*路径操作*中声明多个 `File` 和 `Form` 参数，但不能同时声明希望以 JSON 接收的 `Body` 字段，因为此时请求体会使用 `multipart/form-data` 编码，而不是 `application/json`。

这不是 **FastAPI** 的限制，而是 HTTP 协议的一部分。

///

## 可选文件上传 { #optional-file-upload }

您可以通过使用标准类型注解并将 `None` 作为默认值的方式将一个文件参数设为可选:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## 带有额外元数据的 `UploadFile` { #uploadfile-with-additional-metadata }

您也可以将 `File()` 与 `UploadFile` 一起使用，例如，设置额外的元数据:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## 多文件上传 { #multiple-file-uploads }

FastAPI 支持同时上传多个文件。

它们会被关联到同一个通过「表单数据」发送的「表单字段」。

要实现这一点，声明一个由 `bytes` 或 `UploadFile` 组成的列表（`List`）：

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

接收的也是含 `bytes` 或 `UploadFile` 的列表（`list`）。

/// note | 注意

也可以使用 `from starlette.responses import HTMLResponse`。

`fastapi.responses` 其实与 `starlette.responses` 相同，只是为了方便开发者调用。实际上，大多数 **FastAPI** 的响应都直接从 Starlette 调用。

///

### 带有额外元数据的多文件上传 { #multiple-file-uploads-with-additional-metadata }

和之前的方式一样，你可以为 `File()` 设置额外参数，即使是 `UploadFile`：

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## 小结 { #recap }

使用 `File`、`bytes` 和 `UploadFile` 来声明在请求中上传的文件，它们以表单数据发送。
