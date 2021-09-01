# 请求体 - 嵌套模型

基于 Pydantic，**FastAPI** 能够定义、校验、存档、使用任意深度的嵌套模型。

## List 字段

模型属性可以定义为子类型。例如，Python **列表**：

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial001.py!}
```

`tags` 是由多个元素组成的列表。但上例未声明列表内元素的类型。

## 带类型参数的 List 字段

Python 可以声明包含内部类型（**类型参数**）的列表：

### 导入 typing 的 `List`

首先，从 Python 标准库的 `typing` 模块中导入 `List`：

```Python hl_lines="1"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

### 声明带类型参数的 `List`

声明包含 `list`、`dict`、`tuple` 等类型参数（内部类型）的类型：

* 从 `typing` 模块导入所需类型，如 `List`
* 使用方括号 `[]` 传递**类型参数**（内部类型）

```Python
from types import List

my_list: List[str]
```

这些都是标准的 Python 类型声明语法。

包含内部类型的模型属性也使用这些标准语法。

本例把 `tags` 声明为**字符串列表**：

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

## Set 类型

标签（tags）不能重复，每个标签字符串都应该是唯一的。

Python 提供了专门保存一组唯一元素的数据类型，集合（`set`）。

导入 `Set`，并把 `tags` 声明为由 `str` 组成的 `set`：

```Python hl_lines="1 14"
{!../../../docs_src/body_nested_models/tutorial003.py!}
```

收到的请求中包含重复数据时，会被转换为只包含唯一元素的集合。

而且，每次输出数据时，即使源数据中有重复项，输出的也是只包含唯一元素的集合。

并且还会在文档中进行相应地注释/存档。

## 嵌套模型

Pydantic 模型的每个属性都有自己的类型。

而且，这些属性的类型也可以是 Pydantic 模型。

因此，Pydantic 模型可以声明拥有特定属性名、类型和校验的深度嵌套 JSON 对象。

所有这些对象，都可以任意嵌套。

### 定义子模型

例如，定义一个 `Image` 模型：

```Python hl_lines="9-11"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

### 把子模型用作类型

然后，把 `Image` 模型声明为属性的类型：

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

再一次，声明之后，就可以通过 **FastAPI** 获得：

* 编辑器对嵌套模型的自动补全等支持
* 数据转换
* 数据校验
* API 文档

## 特殊类型与校验

除了 `str`、`int`、`float` 等普通单值类型外，还可以使用从 `str` 继承的复杂单值类型。

所有选项详见 <a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">Pydantic 官档 - 外部类型</a>。下一章介绍一些示例。

例如，把 `Image` 模型的 `url` 字段声明为 Pydantic 的 `HttpUrl`，而不是 `str`：

```Python hl_lines="4 10"
{!../../../docs_src/body_nested_models/tutorial005.py!}
```

FastAPI 校验该字符串是否为有效的 URL，并在 JSON Schema / OpenAPI 中存档。

## 包含子模型列表的属性

`list`、`set` 的子类型也可以是 Pydantic 模型：

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

    注意，`images` 键中包含了 image 对象列表。

## 深度嵌套模型

定义任意深度的嵌套模型：

```Python hl_lines="9 14 20 23 27"
{!../../../docs_src/body_nested_models/tutorial007.py!}
```

!!! info "说明"

    注意，`Offer` 中嵌套了 `Item` 列表，而 `Item` 又嵌套了可选的 `Image` 列表。

## 纯列表请求体

JSON 请求体的最外层是 JSON `array`（ Python **列表**）时，在路径操作函数的参数中，可以使用与声明 Pydantic 模型相同的方式声明该参数的类型：

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

直接使用**字典**，不使用 Pydantic 模型时，无法获得这种编辑器支持。

但不必担心，传入的字典会被自动转换，输出数据也会被自动转换为 JSON。

## 由**字典**构成的请求体

请求体可以声明为**字典**，并且字典的键与值可以声明为不同类型。

因为使用了 Pydantic 模型，不必事先知道可用的字段 / 属性名。

接收未知的键时，这种方式很有用。

---

常见用例包括接收 `int` 等类型的键。

下面介绍这种用例。

本例中，路径操作函数可以接收键的类型是 `int`，值的类型是 `float` 的**字典**：

```Python hl_lines="9"
{!../../../docs_src/body_nested_models/tutorial009.py!}
```

!!! tip "提示"

    注意，JSON 的键只支持**字符串**。
    
    但 Pydantic 可以自动转换数据类型。
    
    也就是说，即使 API 客户端只能发送字符串类型的键，但只要这些字符串只包含整数，Pydantic 就能转换并校验该键。
    
    这样一来，字典 `weights` 的键的类型就是 `int`，而值的类型则为 `float`。

## 小结

**FastAPI** 拥有 Pydantic 模型的高度灵活性，还能让代码更加简短、优雅。

并且支持以下功能：

* 编辑器支持（无处不在的自动补全！）
* 数据转换（即解析/序列化）
* 数据校验
* 概图存档
* API 文档
