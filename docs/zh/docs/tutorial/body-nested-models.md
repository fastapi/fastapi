# 请求体 - 嵌套模型

基于 Pydantic，**FastAPI** 可以定义、校验、存档，并使用任意深度的嵌套模型。

## List 字段

模型属性可以定义为子类型。例如，Python 的 `list`：

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial001.py!}
```

`tags` 是由多个元素组成的列表。不过，上例并未声明列表内元素的类型。

## 具有子类型的 List 字段

Python 可以声明包含内部类型（也叫作「类型参数」）的列表：

### 从 typing 导入 `List`

首先，从 Python 标准库的 `typing` 模块中导入 `List`：

```Python hl_lines="1"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

### 声明包含子类型的 `List`

声明包含 `list`、`dict`、`tuple` 等类型参数（内部类型）的类型：

* 从 `typing` 模块导入所需子类型
* 使用方括号 `[` 和 `]` 传入「类型参数」

```Python
from typing import List

my_list: List[str]
```

这些都是 Python 进行类型声明的标准语法。

包含内部类型的模型属性也使用相同的标准语法。

本例中，把 `tags` 指定为「字符串列表」：

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

## Set 类型

但标签（tag）不能重复，标签字符串应该是唯一的。

Python 提供了专门用于保存一组唯一元素的数据类型，`set`。

导入 `Set`，并把 `tags` 声明为由 `str` 组成的 `set`：

```Python hl_lines="1 14"
{!../../../docs_src/body_nested_models/tutorial003.py!}
```

如果收到的请求中包含重复数据，就会被转换为一组唯一项。

而且，每次输出数据时，即使源数据中有重复项，输出的也是一组唯一项。

并且还会在文档中进行相应地注释 / 存档。

## 嵌套模型

Pydantic 模型的每个属性都有其类型。

模型属性的类型也可以是另一个 Pydantic 模型。

因此，可以声明拥有特定属性名、类型和校验的深度嵌套 JSON 对象。

上述模型都可以实现任意嵌套。

### 定义子模型

例如，定义一个 `Image` 模型：

```Python hl_lines="9-11"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

### 子模型当作类型

然后，把 `Image` 模型当作属性的类型：

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

**FastAPI** 返回如下请求体：

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

只进行这样的声明，就可以再次通过 **FastAPI** 获得：

* 编辑器对嵌套模型的自动补全等支持
* 数据转换
* 数据校验
* 自动文档

## 特殊类型与校验

除了 `str`、`int`、`float` 等普通单值类型外，还可以使用从 `str` 继承的复杂单值类型。

要了解所有可用选项，请参阅 <a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">Pydantic 外部类型</a>文档。下一章会介绍一些示例。

例如，`Image` 模型中包含的 `url` 字段，可以声明为 Pydantic 的 `HttpUrl`，而不是 `str`：

```Python hl_lines="4 10"
{!../../../docs_src/body_nested_models/tutorial005.py!}
```

FastAPI 校验该字符串是否为有效的 URL，并在 JSON Schema / OpenAPI 中存档。

## 包含子模型列表的属性

`list`、`set` 等类型的子类型也可以是 Pydantic 模型：

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial006.py!}
```

 JSON 请求体以如下方式转换、校验并存档：

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

!!! info "说明"

    注意，`images` 键中包含了一组 image 对象列表。

## 深度嵌套模型

可以定义任意深度的嵌套模型：

```Python hl_lines="9 14 20 23 27"
{!../../../docs_src/body_nested_models/tutorial007.py!}
```

!!! info "说明"

    注意，`Offer` 由 `Item` 列表组成，而 `Item` 又是由可选的 `Image` 列表组成。

## 纯列表请求体

如果 JSON 请求体的最外层是 JSON `array`（即 Python `list`），则可以在路径操作函数的参数中，以与 Pydantic 模型一样的方式声明此类型：

```Python
images: List[Image]
```

例如：

```Python hl_lines="15"
{!../../../docs_src/body_nested_models/tutorial008.py!}
```

## 无处不在的编辑器支持

编辑器的支持无处不在。

即使是列表中的元素：

<img src="/img/tutorial/body-nested-models/image01.png">

如果不使用 Pydantic 模型，而是直接使用 `dict`，就无法获得这种编辑器支持。

但不必担心，传入的字典会被自动转换，输出数据也会被自动转换为 JSON。

## 由 `dict` 构成的请求体

请求体可以声明为 `dict`，并且可以把字典的键声明某种类型，把值声明为另一种类型。

而且，（因为使用了 Pydantic 模型），不必事先知道可用的字段 / 属性名。

需要接收未知的键时，这种方式很有用。

---

接收 `int` 等其他类型的键也是常见的用例。

下面介绍这种用例。

本例中，路径操作函数可以接收键的类型是 `int`，值的类型是 `float` 的 `dict`：

```Python hl_lines="9"
{!../../../docs_src/body_nested_models/tutorial009.py!}
```

!!! tip "提示"

    注意，JSON 的键仅支持 `str`。
    
    但 Pydantic 可以自动转换数据类型。
    
    也就是说，即使 API 客户端只能发送字符串类型的键，只要这些字符串仅包含整数，Pydantic 就会对其进行转换并校验。
    
    这样一来，接收的字典 `weights` 的键的类型就是 `int`，而值的类型则为 `float` 。

## 小结

**FastAPI** 拥有 Pydantic 模型的极高灵活性，还能让代码更加简短、优雅。

并且支持以下功能：

* 编辑器支持（无处不在的自动补全！）
* 数据转换（亦称为解析/序列化）
* 数据校验
* 概图存档
* 自动文档
