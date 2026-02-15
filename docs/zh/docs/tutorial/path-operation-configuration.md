# 路径操作配置 { #path-operation-configuration }

*路径操作装饰器*支持多种配置参数。

/// warning | 警告

注意：以下参数应直接传递给*路径操作装饰器*，不能传递给*路径操作函数*。

///

## 响应状态码 { #response-status-code }

可以在*路径操作*的响应中定义（HTTP）`status_code`。

可以直接传递 `int` 代码，比如 `404`。

如果记不住数字码的含义，也可以用 `status` 的快捷常量：

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

该状态码会用于响应中，并会被添加到 OpenAPI 概图。

/// note | 技术细节

也可以使用 `from starlette import status` 导入状态码。

**FastAPI** 提供的 `fastapi.status` 与 `starlette.status` 相同，方便你作为开发者使用。实际上它直接来自 Starlette。

///

## 标签 { #tags }

可以通过传入由 `str` 组成的 `list`（通常只有一个 `str`）的参数 `tags`，为*路径操作*添加标签：

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

OpenAPI 概图会自动添加标签，供 API 文档接口使用：

<img src="/img/tutorial/path-operation-configuration/image01.png">

### 使用 Enum 的标签 { #tags-with-enums }

如果你的应用很大，可能会积累出很多标签，你会希望确保相关的*路径操作*始终使用相同的标签。

这种情况下，把标签存放在 `Enum` 中会更合适。

**FastAPI** 对此的支持与使用普通字符串相同：

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## 摘要和描述 { #summary-and-description }

可以添加 `summary` 和 `description`：

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## 从 docstring 获取描述 { #description-from-docstring }

描述内容比较长且占用多行时，可以在函数的 <dfn title="作为函数内部的第一个表达式（不赋给任何变量）的多行字符串，用于文档用途">docstring</dfn> 中声明*路径操作*的描述，**FastAPI** 会从中读取。

文档字符串支持 <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>，能正确解析和显示 Markdown 的内容，但要注意文档字符串的缩进。

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

它会在交互式文档中使用：

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 响应描述 { #response-description }

`response_description` 参数用于定义响应的描述说明：

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | 信息

注意，`response_description` 只用于描述响应，`description` 一般则用于描述*路径操作*。

///

/// check | 检查

OpenAPI 规定每个*路径操作*都要有响应描述。

如果没有定义响应描述，**FastAPI** 则自动生成内容为 "Successful response" 的响应描述。

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 弃用*路径操作* { #deprecate-a-path-operation }

如果需要把*路径操作*标记为<dfn title="过时，建议不要使用">弃用</dfn>，但不删除它，可以传入 `deprecated` 参数：

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

API 文档会把该路径操作标记为弃用：

<img src="/img/tutorial/path-operation-configuration/image04.png">

下图显示了正常*路径操作*与弃用*路径操作* 的区别：

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 小结 { #recap }

通过传递参数给*路径操作装饰器*，即可轻松地配置*路径操作*、添加元数据。
