# 路径操作配置 { #path-operation-configuration }

你可以向你的*路径操作装饰器*传递多个参数来进行配置。

/// warning | 警告

注意，这些参数是直接传给*路径操作装饰器*的，而不是传给你的*路径操作函数*。

///

## 响应状态码 { #response-status-code }

你可以定义（HTTP）`status_code`，用于你的*路径操作*响应中。

你可以直接传入 `int` 代码，比如 `404`。

但如果你记不住每个数字代码的用途，你可以使用 `status` 中的快捷常量：

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

该状态码会用于响应，并会被添加到 OpenAPI schema 中。

/// note | 技术细节

你也可以使用 `from starlette import status`。

**FastAPI** 提供了与 `starlette.status` 相同的 `fastapi.status`，只是为了方便你（开发者）。但它直接来自 Starlette。

///

## 标签 { #tags }

你可以为你的*路径操作*添加标签：传入参数 `tags`，其值为由 `str` 组成的 `list`（通常只有一个 `str`）：

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

它们会被添加到 OpenAPI schema，并被自动文档界面使用：

<img src="/img/tutorial/path-operation-configuration/image01.png">

### 使用 Enum 的标签 { #tags-with-enums }

如果你有一个大型应用，你可能最终会累积**多个标签**，并且你会希望确保对相关的*路径操作*始终使用**相同的标签**。

在这些情况下，把标签存到 `Enum` 中可能是有意义的。

**FastAPI** 对此的支持方式和普通字符串一样：

{* ../../docs_src/path_operation_configuration/tutorial002b_py39.py hl[1,8:10,13,18] *}

## 摘要和描述 { #summary-and-description }

你可以添加 `summary` 和 `description`：

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## 从 docstring 获取描述 { #description-from-docstring }

由于描述通常很长并且会跨越多行，你可以在函数的 <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation - 在函数内部作为第一个表达式的多行字符串（不赋值给任何变量），用于文档说明">docstring</abbr> 中声明*路径操作*的描述，**FastAPI** 会从那里读取。

你可以在 docstring 中编写 <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>，它会被正确解释并显示（会考虑 docstring 的缩进）。

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

它会用于交互式文档：

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 响应描述 { #response-description }

你可以使用参数 `response_description` 来指定响应描述：

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | 信息

注意，`response_description` 专门指响应，而 `description` 通常指*路径操作*本身。

///

/// check | 检查

OpenAPI 规定每个*路径操作*都需要一个响应描述。

因此，如果你没有提供，**FastAPI** 会自动生成一个 "Successful response"。

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 弃用*路径操作* { #deprecate-a-path-operation }

如果你需要将某个*路径操作*标记为 <abbr title="obsolete, recommended not to use it - 过时的，建议不要使用">deprecated</abbr>，但又不移除它，可以传入参数 `deprecated`：

{* ../../docs_src/path_operation_configuration/tutorial006_py39.py hl[16] *}

它会在交互式文档中被清晰地标记为已弃用：

<img src="/img/tutorial/path-operation-configuration/image04.png">

看看已弃用和未弃用的*路径操作*分别是什么样的：

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 小结 { #recap }

你可以通过向*路径操作装饰器*传递参数，轻松地为你的*路径操作*进行配置并添加元数据。
