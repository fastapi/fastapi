# 请求体 - 嵌套模型 { #body-nested-models }

使用 **FastAPI**，你可以定义、校验、记录文档并使用任意深度嵌套的模型（归功于 Pydantic）。

## List 字段 { #list-fields }

你可以将一个属性定义为某个子类型。例如 Python `list`：

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

这将使 `tags` 成为一个 list，虽然它没有声明 list 中元素的类型。

## 带类型参数的 List 字段 { #list-fields-with-type-parameter }

但是 Python 有一种特定的方法来声明带有内部类型（或“类型参数”）的 list：

### 声明带类型参数的 `list` { #declare-a-list-with-a-type-parameter }

要声明带有类型参数（内部类型）的类型，例如 `list`、`dict`、`tuple`，
使用方括号 `[` 和 `]` 将内部类型作为“类型参数”传入

```Python
my_list: list[str]
```

这完全是用于类型声明的标准 Python 语法。

对具有内部类型的模型属性也使用相同的标准语法。

因此，在我们的示例中，我们可以将 `tags` 明确地指定为一个“字符串列表”：

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set 类型 { #set-types }

但是随后我们考虑了一下，意识到标签不应该重复，它们很可能会是唯一的字符串。

并且 Python 有一种用于保存一组唯一项的特殊数据类型，即 `set`。

然后我们可以将 `tags` 声明为一个字符串的 set：

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

这样，即使你收到带有重复数据的请求，它也会被转换为一组唯一项。

并且每当你输出该数据时，即使源数据有重复，也会作为一组唯一项输出。

并且还会被相应地标注 / 记录文档。

## 嵌套模型 { #nested-models }

Pydantic 模型的每个属性都具有类型。

但是这个类型本身可以是另一个 Pydantic 模型。

因此，你可以声明拥有特定属性名称、类型和校验的深度嵌套的 JSON “对象”。

上述这些都可以任意地嵌套。

### 定义子模型 { #define-a-submodel }

例如，我们可以定义一个 `Image` 模型：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### 将子模型用作类型 { #use-the-submodel-as-a-type }

然后我们可以将其用作一个属性的类型：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

这意味着 **FastAPI** 将期望类似于以下内容的请求体：

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

再一次，仅仅进行这样的声明，你将通过 **FastAPI** 获得：

* 编辑器支持（自动补全等），即使是嵌套模型也一样
* 数据转换
* 数据校验
* 自动生成文档

## 特殊类型和校验 { #special-types-and-validation }

除了普通的单一值类型（如 `str`、`int`、`float` 等）外，你还可以使用从 `str` 继承的更复杂的单一值类型。

要查看你拥有的所有选项，请查看 <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic 的 Type Overview</a>。你将在下一章节中看到一些示例。

例如，在 `Image` 模型中我们有一个 `url` 字段，我们可以把它声明为 Pydantic 的 `HttpUrl` 实例，而不是 `str`：

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

该字符串将被检查是否为有效的 URL，并在 JSON Schema / OpenAPI 中据此记录文档。

## 带有子模型列表的属性 { #attributes-with-lists-of-submodels }

你还可以将 Pydantic 模型用作 `list`、`set` 等的子类型：

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

这将期望（转换、校验、记录文档等）下面这样的 JSON 请求体：

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

/// info | 信息

请注意 `images` 键现在具有一个 image 对象列表是如何发生的。

///

## 深度嵌套模型 { #deeply-nested-models }

你可以定义任意深度的嵌套模型：

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | 信息

请注意 `Offer` 拥有一个 `Item` 的列表，而 `Item` 反过来又有一个可选的 `Image` 列表

///

## 纯列表请求体 { #bodies-of-pure-lists }

如果你期望的 JSON 请求体的顶层值是一个 JSON `array`（即 Python `list`），则可以在函数参数中声明该类型，就像在 Pydantic 模型中一样：

```Python
images: list[Image]
```

例如：

{* ../../docs_src/body_nested_models/tutorial008_py39.py hl[13] *}

## 无处不在的编辑器支持 { #editor-support-everywhere }

并且你可以随处获得编辑器支持。

即使是列表中的元素：

<img src="/img/tutorial/body-nested-models/image01.png">

如果你直接使用 `dict` 而不是 Pydantic 模型，那你将无法获得这种编辑器支持。

但是你根本不必担心它们，传入的 dict 会自动被转换，你的输出也会自动被转换为 JSON。

## 任意 `dict` 构成的请求体 { #bodies-of-arbitrary-dicts }

你也可以将请求体声明为一个 `dict`，其键为某种类型、值为另一种类型。

这样，你无需事先知道哪些字段/属性名是有效的（像使用 Pydantic 模型那样）。

如果你想接收一些你尚不知道的键，这会很有用。

---

另一个有用的场景是当你想要使用另一种类型的键时（例如 `int`）。

这就是我们接下来要看的内容。

在这种情况下，你会接受任何 `dict`，只要它使用 `int` 类型的键且值为 `float`：

{* ../../docs_src/body_nested_models/tutorial009_py39.py hl[7] *}

/// tip | 提示

请记住 JSON 仅支持将 `str` 作为键。

但是 Pydantic 具有自动数据转换。

这意味着，即使你的 API 客户端只能将字符串作为键发送，只要这些字符串内容是纯整数，Pydantic 就会对其进行转换并校验。

并且你接收的名为 `weights` 的 `dict` 实际上将具有 `int` 类型的键和 `float` 类型的值。

///

## 总结 { #recap }

使用 **FastAPI** 你可以拥有 Pydantic 模型提供的最大灵活性，同时保持代码的简单、简短和优雅。

同时还具备所有这些好处：

* 编辑器支持（处处皆可自动补全！）
* 数据转换（也被称为 parsing / serialization）
* 数据校验
* Schema 文档
* 自动生成文档
