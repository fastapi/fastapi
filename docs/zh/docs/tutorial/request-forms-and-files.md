# 请求表单与文件

FastAPI 支持同时使用 `File` 和 `Form` 定义文件和表单字段。

/// info | 说明

接收上传文件或表单数据，要预先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

例如，`pip install python-multipart`。

///

## 导入 `File` 与 `Form`

{* ../../docs_src/request_forms_and_files/tutorial001.py hl[1] *}

## 定义 `File` 与 `Form` 参数

创建文件和表单参数的方式与 `Body` 和 `Query` 一样：

{* ../../docs_src/request_forms_and_files/tutorial001.py hl[8] *}

文件和表单字段作为表单数据上传与接收。

声明文件可以使用 `bytes` 或 `UploadFile` 。

/// warning | 警告

可在一个*路径操作*中声明多个 `File` 与 `Form` 参数，但不能同时声明要接收 JSON 的 `Body` 字段。因为此时请求体的编码为 `multipart/form-data`，不是 `application/json`。

这不是 **FastAPI** 的问题，而是 HTTP 协议的规定。

///

## 小结

在同一个请求中接收数据和文件时，应同时使用 `File` 和 `Form`。
