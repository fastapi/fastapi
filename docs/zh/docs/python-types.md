# Python 类型简介 { #python-types-intro }

Python 支持可选的“类型提示”（也叫“类型注解”）。

这些 **“类型提示”** 或注解是一种特殊语法，允许声明变量的 <abbr title="例如：str、int、float、bool">类型</abbr>。

通过为变量声明类型，编辑器和工具可以给你更好的支持。

这只是一个关于 Python 类型提示的**快速教程 / 复习**。它只涵盖与 **FastAPI** 一起使用所需的最少内容……实际上非常少。

**FastAPI** 完全基于这些类型提示构建，它们为 FastAPI 带来了很多优势和好处。

但即使你从不使用 **FastAPI**，了解一点它们也会让你受益。

/// note | 注意

如果你是 Python 专家，并且已经完全了解类型提示相关的一切内容，跳到下一章即可。

///

## 动机 { #motivation }

让我们从一个简单示例开始：

{* ../../docs_src/python_types/tutorial001_py39.py *}

调用这个程序会输出：

```
John Doe
```

这个函数做了如下事情：

* 接收 `first_name` 和 `last_name`。
* 使用 `title()` 将每个参数的第一个字母转换为大写。
* 用中间的空格把它们 <abbr title="把它们拼在一起，作为一个整体。一个的内容接在另一个之后。">拼接</abbr> 起来。

{* ../../docs_src/python_types/tutorial001_py39.py hl[2] *}

### 修改它 { #edit-it }

这是一个非常简单的程序。

但现在想象一下你要从零开始写它。

在某个时刻，你会开始定义这个函数，参数也准备好了……

但随后你需要调用“那个把第一个字母转换为大写的方法”。

是 `upper` 吗？是 `uppercase`？`first_uppercase`？`capitalize`？

然后，你去找程序员的老朋友：编辑器自动补全。

你输入函数的第一个参数 `first_name`，然后输入一个点号（`.`），再按下 `Ctrl+Space` 来触发补全。

但很遗憾，你得不到任何有用的东西：

<img src="/img/python-types/image01.png">

### 添加类型 { #add-types }

让我们修改上一版本中的一行代码。

把函数参数这一段从：

```Python
    first_name, last_name
```

改成：

```Python
    first_name: str, last_name: str
```

就这样。

这些就是“类型提示”：

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

这和声明默认值（如下）不一样：

```Python
    first_name="john", last_name="doe"
```

这不是同一回事。

我们用的是冒号（`:`），不是等号（`=`）。

而且添加类型提示通常不会改变不添加它们时的运行结果。

但现在，想象你又一次在创建这个函数，不过这次加上了类型提示。

在同样的位置，你尝试用 `Ctrl+Space` 触发自动补全，你会看到：

<img src="/img/python-types/image02.png">

这样你就可以滚动查看选项，直到你找到那个“有点眼熟”的：

<img src="/img/python-types/image03.png">

## 更多动机 { #more-motivation }

看看这个函数，它已经有类型提示了：

{* ../../docs_src/python_types/tutorial003_py39.py hl[1] *}

因为编辑器知道变量的类型，你不仅能得到补全，还能得到错误检查：

<img src="/img/python-types/image04.png">

现在你知道必须修复它，用 `str(age)` 把 `age` 转换成字符串：

{* ../../docs_src/python_types/tutorial004_py39.py hl[2] *}

## 声明类型 { #declaring-types }

你刚刚看到了声明类型提示的主要位置：函数参数。

这也是你在 **FastAPI** 中使用它们的主要位置。

### 简单类型 { #simple-types }

你可以声明所有标准的 Python 类型，不仅仅是 `str`。

例如你可以用：

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py39.py hl[1] *}

### 带类型参数的泛型 { #generic-types-with-type-parameters }

有一些数据结构可以包含其他值，比如 `dict`、`list`、`set` 和 `tuple`。它们内部的值也可以有自己的类型。

这些带有内部类型的类型被称为“**泛型**”类型。并且可以声明它们，甚至包括它们的内部类型。

要声明这些类型及其内部类型，你可以使用标准 Python 模块 `typing`。它专门用来支持这些类型提示。

#### 较新版本的 Python { #newer-versions-of-python }

使用 `typing` 的语法与所有版本（从 Python 3.6 到最新版本，包括 Python 3.9、Python 3.10 等）都 **兼容**。

随着 Python 的发展，**更高版本**对这些类型注解提供了更好的支持，在很多情况下你甚至不需要导入和使用 `typing` 模块来声明类型注解。

如果你可以为项目选择较新的 Python 版本，你就能利用这些额外的简化。

在所有文档中，都有与各个 Python 版本兼容的示例（当存在差异时）。

例如，“**Python 3.6+**”表示兼容 Python 3.6 或更高版本（包括 3.7、3.8、3.9、3.10 等）。“**Python 3.9+**”表示兼容 Python 3.9 或更高版本（包括 3.10 等）。

如果你可以使用 **最新版本的 Python**，就使用对应最新版本的示例；这些示例会有 **最好且最简单的语法**，例如“**Python 3.10+**”。

#### 列表 { #list }

例如，让我们定义一个变量，它是由 `str` 组成的 `list`。

用同样的冒号（`:`）语法声明变量。

类型写 `list`。

因为 list 是包含内部类型的类型，你把它们放在方括号里：

{* ../../docs_src/python_types/tutorial006_py39.py hl[1] *}

/// info | 信息

方括号中的这些内部类型被称为“type parameters”（类型参数）。

在这个例子中，`str` 是传给 `list` 的类型参数。

///

这意味着：“变量 `items` 是一个 `list`，并且这个 list 中的每个元素都是 `str`”。

这样，你的编辑器甚至在处理 list 中的元素时也能提供支持：

<img src="/img/python-types/image05.png">

没有类型的话，这几乎不可能做到。

注意变量 `item` 是 list `items` 中的一个元素。

即便如此，编辑器仍然知道它是 `str`，并为此提供支持。

#### 元组和集合 { #tuple-and-set }

你可以用同样的方法声明 `tuple` 和 `set`：

{* ../../docs_src/python_types/tutorial007_py39.py hl[1] *}

这意味着：

* 变量 `items_t` 是一个包含 3 个元素的 `tuple`：一个 `int`、另一个 `int`、以及一个 `str`。
* 变量 `items_s` 是一个 `set`，并且其中每个元素都是 `bytes` 类型。

#### 字典 { #dict }

要定义 `dict`，你传入 2 个类型参数，用逗号分隔。

第一个类型参数用于 `dict` 的键。

第二个类型参数用于 `dict` 的值：

{* ../../docs_src/python_types/tutorial008_py39.py hl[1] *}

这意味着：

* 变量 `prices` 是一个 `dict`：
    * 这个 `dict` 的键是 `str` 类型（比如每个条目的名称）。
    * 这个 `dict` 的值是 `float` 类型（比如每个条目的价格）。

#### Union { #union }

你可以声明一个变量可以是 **多种类型** 中的任意一种，例如 `int` 或 `str`。

在 Python 3.6 及以上（包括 Python 3.10），你可以使用 `typing` 中的 `Union` 类型，并在方括号中放入可接受的类型。

在 Python 3.10 中还有一种 **新语法**：用 <abbr title='也叫“按位或运算符”，但这里这个含义并不相关'>竖线（`|`）</abbr> 分隔可选类型。

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b_py39.py!}
```

////

两种写法都表示 `item` 可以是 `int` 或 `str`。

#### 可能为 `None` { #possibly-none }

你可以声明一个值可以是某个类型（例如 `str`），但它也可能是 `None`。

在 Python 3.6 及以上（包括 Python 3.10），你可以通过从 `typing` 模块导入并使用 `Optional` 来声明它。

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009_py39.py!}
```

使用 `Optional[str]` 而不是仅用 `str`，可以让编辑器帮助你发现错误：你可能以为某个值总是 `str`，但它实际上也可能是 `None`。

`Optional[Something]` 实际上是 `Union[Something, None]` 的快捷写法，它们是等价的。

这也意味着在 Python 3.10 中，你可以使用 `Something | None`：

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009_py39.py!}
```

////

//// tab | Python 3.9+ alternative

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b_py39.py!}
```

////

#### 使用 `Union` 或 `Optional` { #using-union-or-optional }

如果你使用的 Python 版本低于 3.10，从我非常 **主观** 的角度给你一个建议：

* 🚨 避免使用 `Optional[SomeType]`
* 改为 ✨ **使用 `Union[SomeType, None]`** ✨。

二者等价，底层实现也一样，但我会推荐用 `Union` 而不是 `Optional`，因为“**optional**”这个词看起来像是在暗示该值是可选的；而它实际含义是“它可以是 `None`”，即使这个参数不是可选的、仍然是必填的。

我认为 `Union[SomeType, None]` 对其含义表达得更明确。

这主要是关于用词和命名。但这些词会影响你和队友对代码的理解方式。

举个例子，看看这个函数：

{* ../../docs_src/python_types/tutorial009c_py39.py hl[1,4] *}

参数 `name` 被定义为 `Optional[str]`，但它 **不是可选的**，你不能在不传该参数的情况下调用这个函数：

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

`name` 参数 **仍然是必需的**（不是*可选的*），因为它没有默认值。不过，`name` 仍然接受 `None` 作为值：

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

好消息是，一旦你使用 Python 3.10，你就不用担心这个问题了，因为你可以简单地用 `|` 来定义类型的联合：

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

然后你也不必再为 `Optional` 和 `Union` 这种名字烦恼了。 😎

#### 泛型类型 { #generic-types }

这些在方括号里接收类型参数的类型被称为 **Generic types** 或 **Generics**，例如：

//// tab | Python 3.10+

你可以将同样的内置类型作为泛型来使用（方括号里放类型）：

* `list`
* `tuple`
* `set`
* `dict`

以及和之前 Python 版本一样，从 `typing` 模块导入：

* `Union`
* `Optional`
* ...and others.

在 Python 3.10 中，作为使用泛型 `Union` 和 `Optional` 的替代方案，你可以使用 <abbr title='也叫“按位或运算符”，但这里这个含义并不相关'>竖线（`|`）</abbr> 来声明类型的联合，这样更好也更简单。

////

//// tab | Python 3.9+

你可以将同样的内置类型作为泛型来使用（方括号里放类型）：

* `list`
* `tuple`
* `set`
* `dict`

以及 `typing` 模块中的泛型：

* `Union`
* `Optional`
* ...and others.

////

### 类作为类型 { #classes-as-types }

你也可以将类声明为变量的类型。

比如你有一个名为 `Person` 的类，带有 name：

{* ../../docs_src/python_types/tutorial010_py39.py hl[1:3] *}

然后你可以声明一个变量为 `Person` 类型：

{* ../../docs_src/python_types/tutorial010_py39.py hl[6] *}

然后，你同样会获得所有编辑器支持：

<img src="/img/python-types/image06.png">

注意，这意味着“`one_person` 是类 `Person` 的一个 **实例**”。

它并不意味着“`one_person` 是名为 `Person` 的 **类**”。

## Pydantic 模型 { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 是一个用于执行数据校验的 Python 库。

你可以将数据的“形状”声明为带属性的类。

并且每个属性都有一个类型。

然后你用一些值创建该类的实例，它会校验这些值，把它们转换为合适的类型（如果需要的话），并返回一个包含所有数据的对象。

然后你可以对这个最终得到的对象获得全部编辑器支持。

一个来自 Pydantic 官方文档的例子：

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | 信息

要进一步了解 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic，请查看其文档</a>。

///

**FastAPI** 完全基于 Pydantic。

你会在 [教程 - 用户指南](tutorial/index.md){.internal-link target=_blank} 中看到更多这些内容在实践中的应用。

/// tip | 提示

当你在不提供默认值的情况下使用 `Optional` 或 `Union[Something, None]` 时，Pydantic 有一个特殊行为；你可以在 Pydantic 关于 <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a> 的文档中了解更多。

///

## 带元数据注解的类型提示 { #type-hints-with-metadata-annotations }

Python 还有一个功能：允许使用 `Annotated` 在这些类型提示里放入 **额外的 <abbr title="关于数据的数据，在这里是关于类型的信息，例如描述。">元数据</abbr>**。

从 Python 3.9 开始，`Annotated` 是标准库的一部分，因此你可以从 `typing` 导入它。

{* ../../docs_src/python_types/tutorial013_py39.py hl[1,4] *}

Python 本身不会对这个 `Annotated` 做任何事。对编辑器和其他工具来说，它的类型仍然是 `str`。

但你可以使用 `Annotated` 中的这个位置，为 **FastAPI** 提供关于你希望应用如何表现的额外元数据。

需要记住的重点是：你传给 `Annotated` 的 **第一个*类型参数*** 是 **实际类型**。其余的只是给其他工具用的元数据。

目前你只需要知道 `Annotated` 的存在，以及它是标准 Python。 😎

之后你会看到它可以有多么 **强大**。

/// tip | 提示

因为这是 **标准 Python**，这意味着你仍然能在编辑器中、以及你用来分析和重构代码等的工具中，获得 **尽可能好的开发体验**。 ✨

也意味着你的代码会与许多其他 Python 工具和库非常兼容。 🚀

///

## **FastAPI** 中的类型提示 { #type-hints-in-fastapi }

**FastAPI** 利用这些类型提示来做几件事。

使用 **FastAPI** 时，你用类型提示来声明参数，你会获得：

* **编辑器支持**。
* **类型检查**。

……并且 **FastAPI** 还会用这些声明来：

* **定义要求**：包括请求路径参数、查询参数、请求头、请求体、依赖等。
* **转换数据**：将来自请求的数据转换为所需类型。
* **校验数据**：来自每个请求的数据：
    * 当数据无效时，生成返回给客户端的**自动错误**。
* 使用 OpenAPI **记录** API：
    * 然后用于自动交互式文档的用户界面。

这听起来可能有点抽象。别担心。你会在 [教程 - 用户指南](tutorial/index.md){.internal-link target=_blank} 中看到这一切的实际效果。

最重要的是，通过在一个地方使用标准 Python 类型（而不是添加更多的类、装饰器等），**FastAPI** 会为你完成大量工作。

/// info | 信息

如果你已经学完全部教程并回来看更多关于类型的内容，一个很好的资源是 <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">来自 `mypy` 的“cheat sheet”</a>。

///
