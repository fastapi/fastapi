# 使用数据类

FastAPI 基于 **Pydantic** 构建，前文已经介绍过如何使用 Pydantic 模型声明请求与响应。

但 FastAPI 还可以使用数据类（<a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a>）：

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

这还是借助于 **Pydantic** 及其<a href="https://pydantic-docs.helpmanual.io/usage/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">内置的 `dataclasses`</a>。

因此，即便上述代码没有显式使用 Pydantic，FastAPI 仍会使用 Pydantic 把标准数据类转换为 Pydantic 数据类（`dataclasses`）。

并且，它仍然支持以下功能：

* 数据验证
* 数据序列化
* 数据存档等

数据类的和运作方式与 Pydantic 模型相同。实际上，它的底层使用的也是 Pydantic。

/// info | 说明

注意，数据类不支持 Pydantic 模型的所有功能。

因此，开发时仍需要使用 Pydantic 模型。

但如果数据类很多，这一技巧能给 FastAPI 开发 Web API 增添不少助力。🤓

///

## `response_model` 使用数据类

在 `response_model` 参数中使用 `dataclasses`：

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

本例把数据类自动转换为 Pydantic 数据类。

API 文档中也会显示相关概图：

<img src="/img/tutorial/dataclasses/image01.png">

## 在嵌套数据结构中使用数据类

您还可以把 `dataclasses` 与其它类型注解组合在一起，创建嵌套数据结构。

还有一些情况也可以使用 Pydantic 的 `dataclasses`。例如，在 API 文档中显示错误。

本例把标准的 `dataclasses` 直接替换为 `pydantic.dataclasses`：

```{ .python .annotate hl_lines="1  5  8-11  14-17  23-25  28" }
{!../../docs_src/dataclasses/tutorial003.py!}
```

1. 本例依然要从标准的 `dataclasses` 中导入 `field`；

2. 使用 `pydantic.dataclasses` 直接替换 `dataclasses`；

3. `Author` 数据类包含 `Item` 数据类列表；

4. `Author` 数据类用于 `response_model` 参数；

5. 其它带有数据类的标准类型注解也可以作为请求体；

    本例使用的是 `Item` 数据类列表；

6. 这行代码返回的是包含 `items` 的字典，`items` 是数据类列表；

    FastAPI 仍能把数据<abbr title="把数据转换为可以传输的格式">序列化</abbr>为 JSON；

7. 这行代码中，`response_model` 的类型注解是 `Author` 数据类列表；

    再一次，可以把 `dataclasses` 与标准类型注解一起使用；

8. 注意，*路径操作函数*使用的是普通函数，不是异步函数；

    与往常一样，在 FastAPI 中，可以按需组合普通函数与异步函数；

    如果不清楚何时使用异步函数或普通函数，请参阅**急不可待？**一节中对 <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank" class="internal-link">`async` 与 `await`</a> 的说明；

9. *路径操作函数*返回的不是数据类（虽然它可以返回数据类），而是返回内含数据的字典列表；

    FastAPI 使用（包含数据类的） `response_model` 参数转换响应。

把 `dataclasses` 与其它类型注解组合在一起，可以组成不同形式的复杂数据结构。

更多内容详见上述代码内的注释。

## 深入学习

您还可以把 `dataclasses` 与其它 Pydantic 模型组合在一起，继承合并的模型，把它们包含在您自己的模型里。

详见 <a href="https://pydantic-docs.helpmanual.io/usage/dataclasses/" class="external-link" target="_blank">Pydantic 官档 - 数据类</a>。

## 版本

本章内容自 FastAPI `0.67.0` 版起生效。🔖
