# 路径操作配置

有几个参数可以传递给您的*path操作装饰器* 用来配置它。

!!! warning
    注意，这些参数被直接传递给 *路径操作装时器*, 而不是您的 *路径操作函数*.

## 响应状态代码

您可以定义您的 *路径操作* 响应中将会使用的 (HTTP) `status_code` 。

你可以直接传递 `int` 编码， 比如 `404`。

但如果你不记得每个数字代码是什么，你可以使用 `status` 中的快捷常量:

```Python hl_lines="3  17"
{!../../../docs_src/path_operation_configuration/tutorial001.py!}
```

该状态代码将用于响应，并将添加到OpenAPI模式中。

!!! note "技术细节"
    你也可以使用 `from starlette import status`.

    **FastAPI** 提供的`fastapi.status` 和 `starlette.status` 是一样的，只是为了方便开发者。但是它是直接来自 Starlette 的。

## 标签

你也可以给你的 *路径操作* 添加标签，只需给 `tags` 参数传递一个 `str` 的 `list` （通常只是一个 `str` ）：

```Python hl_lines="17  22  27"
{!../../../docs_src/path_operation_configuration/tutorial002.py!}
```

它们将被添加到OpenAPI模式中，并由自动文档接口使用:

<img src="/img/tutorial/path-operation-configuration/image01.png">

## 总结和描述

你可以添加一个 `summary` 和 `description`:

```Python hl_lines="20-21"
{!../../../docs_src/path_operation_configuration/tutorial003.py!}
```

## docstring 中的描述

由于描述往往很长并且覆盖多个行，您可以在函数<abbr title="函数中作为第一个表达式，用于文档目的的一个多行字符串（并没有被分配个任何变量）">docstring</abbr> 中声明 *路径操作* 描述，**FastAPI** 将会从那里读取他。

你可以在docstring写 <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> 它将被正确解释和显示(考虑到文档字符串缩进)。

```Python hl_lines="19-27"
{!../../../docs_src/path_operation_configuration/tutorial004.py!}
```

它将在交互式文档中使用:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 响应描述

您可以使用参数 `response_description` 来指定响应描述:

```Python hl_lines="21"
{!../../../docs_src/path_operation_configuration/tutorial005.py!}
```

!!! info
    注意， `response_description` 专门指响应， `description` 通常指 *路径操作* 。

!!! check
    OpenAPI指定每个*路径操作* 都需要一个响应描述。

    因此，如果您不提供一个，**FastAPI** 将为 "Successful response" 自动生成一个。

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 弃用一个 *路径操作*

如果您需要将一个 *路径操作* 标记为 <abbr title="过时，建议不要使用">弃用</abbr>, 不需要删除它，传递参数 `deprecated`:

```Python hl_lines="16"
{!../../../docs_src/path_operation_configuration/tutorial006.py!}
```

在交互式文档中将清楚地标记为弃用:

<img src="/img/tutorial/path-operation-configuration/image04.png">

检查已弃用和未弃用的*路径操作* 是什么样的:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 回顾

你可以通过将参数传递给 *路径操作装饰器* ，轻松地为*路径操作* 进行配置和添加元数据。
