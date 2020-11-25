# 请求体 - 嵌套模型

使用 **FastAPI**, 您可以定义，验证，生成文档和使用任意深度嵌套的模型（这要归功于Pydantic）。

## 列表字段

您可以将属性定义为子类型。 例如，Python的 `list`:

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial001.py!}
```

这将使 `tags` 成为一个项目列表。虽然它没有声明每个项的类型。

## 带有类型参数的列表字段

但是Python有一个特定的方法来声明带有内部类型的列表，或者 "类型参数" :

### 导入 typing 的 `List`

首先，从标准的Python `typing` 模块导入 `List`：

```Python hl_lines="1"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

### 使用类型参数声明一个 `List`

要声明具有类型参数的类型(内部类型)，如 `list`, `dict`, `tuple`:

* 从 `typing` 模块导入他们
* 使用方括号: `[` 和 `]`传递一个内部类型作为 "类型参数"

```Python
from typing import List

my_list: List[str]
```

这都是用于类型声明的标准Python语法。

对具有内部类型的模型属性使用相同的标准语法。

因此，在我们的例子中，我们可以使 `tags` 成为一个 "字符串列表"  :

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

## 设置类型

但之后我们想了想，意识到标签不应该重复，它们可能是唯一的字符串。

Python有一种特殊的数据类型来表示一组唯一的项，叫做 `set`.

然后我们导入 `Set` 并声明 `tags` 作为一个 `str` 的 `set`:

```Python hl_lines="1  14"
{!../../../docs_src/body_nested_models/tutorial003.py!}
```

这样，即使接收到具有重复数据的请求，也会将其转换为一组惟一的项。

无论何时输出该数据，即使原数据有重复，它也将作为一组惟一的项输出。

它也会相应地注释/生成文档。

## 嵌套模型

Pydantic模型的每个属性都有一个类型。

但这种类型本身可能是另一种Pydantic模型。

因此，您可以使用特定的属性名称、类型和验证声明深度嵌套的JSON "对象" 。

所有这些都是任意嵌套的。

### 定义子模型

例如，我们可以定义一个 `Image` 模型:

```Python hl_lines="9-11"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

### 使用子模型作为类型

然后我们可以使用它作为属性的类型:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

这将表示 **FastAPI** 会期望一个请求体类似于:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

同样，只需要做那个声明，使用**FastAPI**你就得到:

* 编辑器支持(补全等)，即使是嵌套模型
* 数据转换
* 数据验证
* 自动文档

## 特殊类型和验证

除了像 `str`, `int`, `float` 等普通的单数类型之外。您可以使用继承自 `str` 的更复杂的单数类型。

要查看所有选项，请查看文档 <a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">Pydantic's exotic types</a>。你将在下一章看到一些例子。

例如，在 `Image` 模型中，我们有一个 `url` 字段, 我们可以将其定义为一个 Pydantic's `HttpUrl`， 而不是 `str`:

```Python hl_lines="4  10"
{!../../../docs_src/body_nested_models/tutorial005.py!}
```

The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.
该字符串将被当作一个有效的URL检查，并在JSON Schema / OpenAPI中生成文档。

## 具有子模型列表的属性

你也可以使用Pydantic模型作为 `list`, `set` 等的子类型:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial006.py!}
```

这将期望 (转换，验证，文档等) 一个 JSON 请求体，就像:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

!!! info
    注意`images` 键现在是如何拥有一个image对象列表的。

## 深度嵌套模型

您可以任意定义深嵌套模型:

```Python hl_lines="9  14  20  23  27"
{!../../../docs_src/body_nested_models/tutorial007.py!}
```

!!! info
    注意 `Offer` 如何拥有一个 `Item` 的列表, 它转而拥有一个可选的 `Image` 列表。

## 纯列表的请求体

If the top level value of the JSON body you expect is a JSON `array` (a Python `list`), you can declare the type in the parameter of the function, the same as in Pydantic models:
如果你期望的JSON请求体的顶级值是一个JSON `数组` (一个Python `列表` )，你可以在函数的参数中声明类型，和Pydantic模型一样:

```Python
images: List[Image]
```

正如:

```Python hl_lines="15"
{!../../../docs_src/body_nested_models/tutorial008.py!}
```

## 编辑器支持无处不在

你可以得到编辑器的支持。

即使是列表中的项目:

<img src="/img/tutorial/body-nested-models/image01.png">

如果你直接使用 `dict` 而不是Pydantic模型，就无法获得这种编辑器支持。

.但是您也不必担心它们，传入的dict会自动转换，您的输出也会自动转换为JSON。

## 任意的 `dict` 请求体

还可以将主体声明为具有某些类型的键和其他类型的值的 `dict` 。

不需要事先知道什么是有效的字段/属性名(就像Pydantic模型一样)。

如果您想接收您不知道的密钥，这将非常有用。

---


其他有用的情况是当你想拥有其他类型的键时，例如 `int`.

这就是我们将要看到的。

在这种情况下，你会接受任何 `dict` 只要它有 `int` 键和 `float` 值:

```Python hl_lines="15"
{!../../../docs_src/body_nested_models/tutorial009.py!}
```

!!! tip
    请记住，JSON只支持 `str` 作为键.

    但是Pydantic有自动数据转换功能。

    这意味着，即使您的API客户端只能将字符串作为键发送，只要这些字符串包含纯整数，Pydantic将对它们进行转换和验证。
    
    并且你接收的作为 `weights` 的 `dict` 实际上会具有 `int` 键和 `float` 值。

## 回顾

通过使用 **FastAPI** 您可以获得Pydantic模型提供的最大灵活性，同时保持代码的简单、简短和优雅。

同时具有如下许多好处:

* 编辑器支持(随处可见的补全!)
* 数据转换(即解析/序列化)
* 数据验证
* 模式文档
* 自动文档
