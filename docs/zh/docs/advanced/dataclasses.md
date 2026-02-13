# 使用数据类 { #using-dataclasses }

FastAPI 基于 **Pydantic** 构建，我已经向你展示过如何使用 Pydantic 模型声明请求与响应。

但 FastAPI 也支持以相同方式使用 <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a>：

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

这仍然得益于 **Pydantic**，因为它对 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">`dataclasses` 的内置支持</a>。

因此，即便上面的代码没有显式使用 Pydantic，FastAPI 也会使用 Pydantic 将那些标准数据类转换为 Pydantic 风格的 dataclasses。

并且，它仍然支持以下功能：

* 数据验证
* 数据序列化
* 数据文档等

这与使用 Pydantic 模型时的工作方式相同。而且底层实际上也是借助 Pydantic 实现的。

/// info | 信息

请注意，数据类不能完成 Pydantic 模型能做的所有事情。

因此，你可能仍然需要使用 Pydantic 模型。

但如果你已有一堆数据类，这个技巧可以让它们很好地为使用 FastAPI 的 Web API 所用。🤓

///

## 在 `response_model` 中使用数据类 { #dataclasses-in-response-model }

你也可以在 `response_model` 参数中使用 `dataclasses`：

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

该数据类会被自动转换为 Pydantic 的数据类。

这样，它的模式会显示在 API 文档界面中：

<img src="/img/tutorial/dataclasses/image01.png">

## 在嵌套数据结构中使用数据类 { #dataclasses-in-nested-data-structures }

你也可以把 `dataclasses` 与其它类型注解组合在一起，创建嵌套数据结构。

在某些情况下，你可能仍然需要使用 Pydantic 的 `dataclasses` 版本。例如，如果自动生成的 API 文档出现错误。

在这种情况下，你可以直接把标准的 `dataclasses` 替换为 `pydantic.dataclasses`，它是一个可直接替换的实现：

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. 我们仍然从标准库的 `dataclasses` 导入 `field`。
2. `pydantic.dataclasses` 是 `dataclasses` 的可直接替换版本。
3. `Author` 数据类包含一个由 `Item` 数据类组成的列表。
4. `Author` 数据类被用作 `response_model` 参数。
5. 你可以将其它标准类型注解与数据类一起用作请求体。

   在本例中，它是一个 `Item` 数据类列表。
6. 这里我们返回一个字典，里面的 `items` 是一个数据类列表。

   FastAPI 仍然能够将数据<dfn title="把数据转换为可以传输的格式">序列化</dfn>为 JSON。
7. 这里的 `response_model` 使用了 “`Author` 数据类列表” 的类型注解。

   同样，你可以将 `dataclasses` 与标准类型注解组合使用。
8. 注意，这个 *路径操作函数* 使用的是常规的 `def` 而不是 `async def`。

   一如既往，在 FastAPI 中你可以按需组合 `def` 和 `async def`。

   如果需要回顾何时用哪一个，请查看关于 [`async` 和 `await`](../async.md#in-a-hurry){.internal-link target=_blank} 的文档中的 _“急不可待？”_ 一节。
9. 这个 *路径操作函数* 返回的不是数据类（当然也可以返回数据类），而是包含内部数据的字典列表。

   FastAPI 会使用（包含数据类的）`response_model` 参数来转换响应。

你可以将 `dataclasses` 与其它类型注解以多种不同方式组合，来构建复杂的数据结构。

更多细节请参考上面代码中的内联注释提示。

## 深入学习 { #learn-more }

你还可以把 `dataclasses` 与其它 Pydantic 模型组合、从它们继承、把它们包含到你自己的模型中等。

想了解更多，请查看 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">Pydantic 关于 dataclasses 的文档</a>。

## 版本 { #version }

自 FastAPI 版本 `0.67.0` 起可用。🔖
