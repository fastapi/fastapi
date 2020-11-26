# 请求表单和文件

你可以使用 `File` 和 `Form`同时定义文件和表单字段。

!!! info
    要接收上传的文件或表单数据，首先需要安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    如 `pip install python-multipart`.

## 导入 `File` 和 `Form`

```Python hl_lines="1"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

## 定义 `File` 和 `Form` 参数

使用和`Body` 或 `Query`类似的方法创建文件和表单参数：

```Python hl_lines="8"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

文件和表单字段将作为表单数据上传，您将收到文件和表单字段。

你可以声明一些文件为 `bytes` 一些文件为`UploadFile`。

!!! warning
    你可以在 *路径操作*  中定义多个 `File` 和 `Form` 参数，但你不能同时定义 `Body` 字段并期望以JSON的格式获得数据， 因为请求体将会使用 `multipart/form-data` 编码，而不是`application/json`。

    这不是**FastAPI**的限制，它是HTTP协议的一部分。

## 回顾

当你需要在同一个请求中接收数据和文件时，请同时使用 `File` 和 `Form` 。
