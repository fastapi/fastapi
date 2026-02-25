# Python 类型提示简介 { #python-types-intro }

Python 支持可选的“类型提示”（也叫“类型注解”）。

这些“类型提示”或注解是一种特殊语法，用来声明变量的<dfn title="例如：str、int、float、bool">类型</dfn>。

通过为变量声明类型，编辑器和工具可以为你提供更好的支持。

这只是一个关于 Python 类型提示的快速入门/复习。它只涵盖与 **FastAPI** 一起使用所需的最少部分...实际上非常少。

**FastAPI** 完全基于这些类型提示构建，它们带来了许多优势和好处。

但即使你从不使用 **FastAPI**，了解一些类型提示也会让你受益。

/// note | 注意

如果你已经是 Python 专家，并且对类型提示了如指掌，可以跳到下一章。

///

## 动机 { #motivation }

让我们从一个简单的例子开始：

{* ../../docs_src/python_types/tutorial001_py310.py *}

运行这个程序会输出：

```
John Doe
```

这个函数做了下面这些事情：

* 接收 `first_name` 和 `last_name`。
* 通过 `title()` 将每个参数的第一个字母转换为大写。
* 用一个空格将它们<dfn title="把它们合在一起成为一个，内容一个接在另一个后面。">拼接</dfn>起来。

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### 修改它 { #edit-it }

这是一个非常简单的程序。

但现在想象你要从零开始写它。

在某个时刻你开始定义函数，并且准备好了参数……

接下来你需要调用“那个把首字母变大写的方法”。

是 `upper`？是 `uppercase`？`first_uppercase`？还是 `capitalize`？

然后，你试试程序员的老朋友——编辑器的自动补全。

你输入函数的第一个参数 `first_name`，再输入一个点（`.`），然后按下 `Ctrl+Space` 触发补全。

但很遗憾，没有什么有用的提示：

<img src="/img/python-types/image01.png">

### 添加类型 { #add-types }

我们来改前一个版本的一行代码。

把函数参数从：

```Python
    first_name, last_name
```

改成：

```Python
    first_name: str, last_name: str
```

就是这样。

这些就是“类型提示”：

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

这和声明默认值不同，比如：

```Python
    first_name="john", last_name="doe"
```

这是两码事。

我们用的是冒号（`:`），不是等号（`=`）。

而且添加类型提示通常不会改变代码本来的行为。

现在，再想象你又在编写这个函数了，不过这次加上了类型提示。

在同样的位置，你用 `Ctrl+Space` 触发自动补全，就能看到：

<img src="/img/python-types/image02.png">

这样，你可以滚动查看选项，直到找到那个“看着眼熟”的：

<img src="/img/python-types/image03.png">

## 更多动机 { #more-motivation }

看这个已经带有类型提示的函数：

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

因为编辑器知道变量的类型，你不仅能得到补全，还能获得错误检查：

<img src="/img/python-types/image04.png">

现在你知道需要修复它，用 `str(age)` 把 `age` 转成字符串：

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## 声明类型 { #declaring-types }

你刚刚看到的是声明类型提示的主要位置：函数参数。

这也是你在 **FastAPI** 中使用它们的主要场景。

### 简单类型 { #simple-types }

你不仅可以声明 `str`，还可以声明所有标准的 Python 类型。

例如：

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### typing 模块 { #typing-module }

在一些额外的用例中，你可能需要从标准库的 `typing` 模块导入内容。比如当你想声明“任意类型”时，可以使用 `typing` 中的 `Any`：

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### 泛型类型 { #generic-types }

有些类型可以在方括号中接收“类型参数”（type parameters），用于声明其内部值的类型。比如“字符串列表”可以写为 `list[str]`。

这些能接收类型参数的类型称为“泛型类型”（Generic types）或“泛型”（Generics）。

你可以把相同的内建类型作为泛型使用（带方括号和内部类型）：

* `list`
* `tuple`
* `set`
* `dict`

#### 列表 { #list }

例如，我们来定义一个由 `str` 组成的 `list` 变量。

用同样的冒号（`:`）语法声明变量。

类型写 `list`。

因为 list 是一种包含内部类型的类型，把内部类型写在方括号里：

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | 信息

方括号中的这些内部类型称为“类型参数”（type parameters）。

在这个例子中，`str` 是传给 `list` 的类型参数。

///

这表示：“变量 `items` 是一个 `list`，并且列表中的每一个元素都是 `str`”。

这样，即使是在处理列表中的元素时，编辑器也能给你提供支持：

<img src="/img/python-types/image05.png">

没有类型的话，这几乎是不可能做到的。

注意，变量 `item` 是列表 `items` 中的一个元素。

即便如此，编辑器仍然知道它是 `str`，并为此提供支持。

#### 元组和集合 { #tuple-and-set }

声明 `tuple` 和 `set` 的方式类似：

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

这表示：

* 变量 `items_t` 是一个含有 3 个元素的 `tuple`，分别是一个 `int`、另一个 `int`，以及一个 `str`。
* 变量 `items_s` 是一个 `set`，其中每个元素的类型是 `bytes`。

#### 字典 { #dict }

定义 `dict` 时，需要传入 2 个类型参数，用逗号分隔。

第一个类型参数用于字典的键。

第二个类型参数用于字典的值：

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

这表示：

* 变量 `prices` 是一个 `dict`：
    * 这个 `dict` 的键是 `str` 类型（比如，每个条目的名称）。
    * 这个 `dict` 的值是 `float` 类型（比如，每个条目的价格）。

#### Union { #union }

你可以声明一个变量可以是若干种类型中的任意一种，比如既可以是 `int` 也可以是 `str`。

定义时使用<dfn title='也叫“按位或运算符（bitwise or operator）”，但这里与该含义无关'>竖线（`|`）</dfn>把两种类型分开。

这称为“联合类型”（union），因为变量可以是这两类类型集合的并集中的任意一个。

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

这表示 `item` 可以是 `int` 或 `str`。

#### 可能为 `None` { #possibly-none }

你可以声明一个值的类型是某种类型（比如 `str`），但它也可能是 `None`。

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

使用 `str | None` 而不是仅仅 `str`，可以让编辑器帮助你发现把值当成总是 `str` 的错误（实际上它也可能是 `None`）。

### 类作为类型 { #classes-as-types }

你也可以把类声明为变量的类型。

假设你有一个名为 `Person` 的类，带有 name：

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

然后你可以声明一个变量是 `Person` 类型：

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

接着，你会再次获得所有的编辑器支持：

<img src="/img/python-types/image06.png">

注意，这表示“`one_person` 是类 `Person` 的一个实例（instance）”。

它并不表示“`one_person` 是名为 `Person` 的类本身（class）”。

## Pydantic 模型 { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 是一个用于执行数据校验的 Python 库。

你将数据的“结构”声明为带有属性的类。

每个属性都有一个类型。

然后你用一些值创建这个类的实例，它会校验这些值，并在需要时把它们转换为合适的类型，返回一个包含所有数据的对象。

你还能对这个结果对象获得完整的编辑器支持。

下面是来自 Pydantic 官方文档的一个示例：

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | 信息

想了解更多关于 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic 的信息，请查看其文档</a>。

///

**FastAPI** 完全建立在 Pydantic 之上。

你会在[教程 - 用户指南](tutorial/index.md){.internal-link target=_blank}中看到更多的实战示例。

## 带元数据注解的类型提示 { #type-hints-with-metadata-annotations }

Python 还提供了一个特性，可以使用 `Annotated` 在这些类型提示中放入额外的<dfn title="关于数据的数据，此处指关于类型的信息，例如描述。">元数据</dfn>。

你可以从 `typing` 导入 `Annotated`。

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python 本身不会对这个 `Annotated` 做任何处理。对于编辑器和其他工具，类型仍然是 `str`。

但你可以在 `Annotated` 中为 **FastAPI** 提供额外的元数据，来描述你希望应用如何行为。

重要的是要记住：传给 `Annotated` 的第一个类型参数才是实际类型。其余的只是给其他工具用的元数据。

现在你只需要知道 `Annotated` 的存在，并且它是标准 Python。😎

稍后你会看到它有多么强大。

/// tip | 提示

这是标准 Python，这意味着你仍然可以在编辑器里获得尽可能好的开发体验，并能和你用来分析、重构代码的工具良好协作等。✨

同时你的代码也能与许多其他 Python 工具和库高度兼容。🚀

///

## **FastAPI** 中的类型提示 { #type-hints-in-fastapi }

**FastAPI** 利用这些类型提示来完成多件事情。

在 **FastAPI** 中，用类型提示来声明参数，你将获得：

* 编辑器支持。
* 类型检查。

……并且 **FastAPI** 会使用相同的声明来：

* 定义要求：从请求路径参数、查询参数、请求头、请求体、依赖等。
* 转换数据：把请求中的数据转换为所需类型。
* 校验数据：对于每个请求：
    * 当数据无效时，自动生成错误信息返回给客户端。
* 使用 OpenAPI 记录 API：
    * 然后用于自动生成交互式文档界面。

这些听起来可能有点抽象。别担心。你会在[教程 - 用户指南](tutorial/index.md){.internal-link target=_blank}中看到所有这些的实际效果。

重要的是，通过使用标准的 Python 类型，而且只在一个地方声明（而不是添加更多类、装饰器等），**FastAPI** 会为你完成大量工作。

/// info | 信息

如果你已经读完所有教程，又回来想进一步了解类型，一个不错的资源是 <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy` 的“速查表”</a>。

///
