# 请求表单与文件 { #request-forms-and-files }

FastAPI 支持同时使用 `File` 和 `Form` 定义文件和表单字段。

/// info | 信息

接收上传文件和/或表单数据，要先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装它，例如：

```console
$ pip install python-multipart
```

///

## 导入 `File` 与 `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## 定义 `File` 与 `Form` 参数 { #define-file-and-form-parameters }

创建文件和表单参数的方式与 `Body` 或 `Query` 一样：

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

文件和表单字段会作为表单数据上传，你将接收到这些文件和表单字段。

并且你可以将其中一些文件声明为 `bytes`，另一些声明为 `UploadFile`。

/// warning | 警告

可在一个*路径操作*中声明多个 `File` 与 `Form` 参数，但不能同时声明你期望以 JSON 形式接收的 `Body` 字段，因为该请求会使用 `multipart/form-data` 对请求体编码，而不是 `application/json`。

这不是 **FastAPI** 的限制，这是 HTTP 协议的一部分。

///

## 小结 { #recap }

在同一个请求中接收数据和文件时，应同时使用 `File` 和 `Form`。
