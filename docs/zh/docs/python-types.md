# Python 类型提示

Python 支持可选的**类型提示**。

**类型提示**是声明变量<abbr title="例如：str、int、float、bool">类型</abbr>的特殊语法。

声明了变量类型，编辑器和开发工具就提供更好的支持。

本章只是 Python 类型提示的**快速入门**，仅介绍了 **FastAPI** 中与类型提示相关的内容……真的很少。

**FastAPI** 是基于类型提示开发的，写代码的体验非常不错。

就算不使用 **FastAPI**，了解一下类型提示也会让您获益匪浅。

!!! note "笔记"

    如果您是 Python 专家，已经熟知类型提示，就直接跳到下一章吧。

## 动机

先介绍一个简单的例子：

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

这段代码输出如下内容：

```
John Doe
```

该函数执行以下操作：

* 接收 `first_name` 和 `last_name` 参数
* 使用 `title()` 把参数的首字母转换为大写
* 使用空格<abbr title="按顺序把多个内容组合成一个整体。">拼接</abbr>两个参数的值

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### 编辑示例

这是个非常简单的程序。

现在，假设您要从头编写这段程序。

在某一时刻，开始定义函数，并且准备好了参数……

此时，需要调用**把首字母转换为大写的方法**。

等等，那个方法是什么来着？`upper`？ `uppercase`？`first_uppercase`？还是`capitalize`？ 

然后，您尝试向程序员老手的朋友——编辑器自动补全寻求帮助。

输入函数的第一个参数 `first_name`，输入点号（`.`），然后敲下 `Ctrl+Space` 触发代码补全。

可惜，这没有什么用：

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### 添加类型

接下来，修改上例中的一行代码。

把下面这行代码中的函数参数从：

```Python
    first_name, last_name
```

改成：

```Python
    first_name: str, last_name: str
```

就是这样。

这就是**类型提示**：

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

与声明默认值不同，例如：

```Python
    first_name="john", last_name="doe"
```

这两者不一样。

类型提示用的是冒号（`:`），不是等号（`=`）。

而且类型提示一般不会改变原有的运行结果。

再次创建这个函数，这次添加了类型提示。

在同一个位置，使用 `Ctrl+Space` 触发自动补全，就会发现：

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

这样，就可以滚动查看选项，找到需要的功能：

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## 更多动机

下面是个使用类型提示的函数：

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

因为编辑器已经知道了变量的类型，所以不仅能对代码进行补全，还能检查代码错误：

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

现在，必须先修复这个问题，使用 `str(age)` 把 `age` 转换成字符串：

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## 声明类型

您刚刚看到的就是类型提示常见的场景 ~ 用于函数的参数。

这也是在 **FastAPI** 中类型提示的常用场景。

### 简单类型

类型提示不只使用 `str`，还能声明所有 Python 标准类型。

比如，以下类型：

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### 通用类型的类型参数

`dict`、`list`、`set`、`tuple` 等数据结构可以包含其它值，而且其内部的值也有自己的类型。

Python 的 `typing` 标准库可以声明这些类型及其子类型。

这个标准库专门用来支持类型提示。

#### 列表

例如，定义由 `str` 组成的 `list` 变量。

从 `typing` 模块导入 `List`（注意 `L` 要大写）：

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

同样用冒号（`:`）声明变量。

类型是 `List`。

由于列表是包含**子类型**的类型，所以要把子类型放在方括号里：

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! tip "提示"

    方括号里的内部类型叫做**类型参数**。
    
    此时，`str` 是传递给 `List` 的类型参数。

即：**变量 `items` 的类型是 `list`，并且列表里的每个元素的类型都是 `str`**。

这样，即使在处理列表里的元素时，编辑器也能提供支持：

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

没有类型，这种支持几乎不可能实现。

注意，变量 `item` 是列表 `items` 里的元素。

而且，编辑器仍然把它识别为 `str`，并提供相关支持。

#### 元组和集合

声明 `tuple` 和 `set` 的方法也一样：

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

即：

* 变量 `items_t` 是包含 3 个元素的 `tuple`，分别是 `int`、 `int`、`str`
* 变量 `items_s` 是 `set`，其中每个元素的类型都是 `bytes`

#### 字典

定义 `dict` 要传入 2 个用逗号分隔的子类型。

第一个子类型声明 `dict` 的所有键。

第二个子类型声明 `dict` 的所有值：

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

即：

* 变量 `prices` 是 `dict`：
    * `dict` 的键的类型是 `str`（元素名称）
    * `dict` 的值的类型是 `float`（元素价格）

#### `Optional`

使用 `Optional` 把变量声明为 `str` 等类型，但该类型是**可选的**，因此也可以是 `None`:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

使用 `Optional[str]` 替代简单的 `str` 可以让编辑器检测值的类型应为 `str`，但也可能为 `None` 的错误。

#### 通用类型

以下类型使用方括号中的类型参数：

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* 等……

这些类型就是**通用类型**，也叫作 **Generics**。

### 类作为类型

类也可以声明为变量的类型。

假设有一个包含 `name` 属性的类 `Person`：

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

下面，把变量的类型声明为 `Person`：

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

再一次，获得了所有的编辑器支持：

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

## Pydantic 模型

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 是执行数据校验的 Python 库。

可以把数据**结构**声明为包含属性的类。

每个属性都有自己的类型。

接下来，用一些值创建类实例，FastAPI 会校验这些值，（在需要的情况下）把值转换为适当的类型，并返回包含所有数据的对象。

然后，这个对象就可以获得编辑器支持。

下面是 Pydantic 官方文档中的示例：

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! info "说明"

    进一步了解 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic，请参阅此文档</a>。

**FastAPI** 就是基于 Pydantic 开发的。

[教程 - 用户指南](tutorial/index.md){.internal-link target=_blank} 中列出了很多示例。

## **FastAPI** 中的类型提示

**FastAPI** 充分利用了类型提示的优势。

**FastAPI** 使用类型提示声明参数可以获得：

* **编辑器支持**
* **类型检查**

……**FastAPI** 还使用类型声明：

* **定义参数需求**：声明对请求路径参数、查询参数、请求头、请求体、依赖项等的需求
* **转换数据**：把请求中的数据转换为需要的类型
* **校验数据**： 对于每一个请求：
    * 数据校验失败时，自动生成**错误信息**，并返回给客户端
* 使用 OpenAPI **存档** API：
    * 并在 API 文档中显示

听上去有点抽象，不过不用担心。[教程 - 用户指南](tutorial/index.md){.internal-link target=_blank} 中详细介绍了上述所有内容。

最重要的是，使用 Python 标准类型，只要在一个地方声明（不用添加更多的类、装饰器等），**FastAPI** 就能完成很多工作。

!!! info "说明"

    学习完教程后，如果想了解更多类型的内容，<a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy` 的**速查表**</a>非常不错。

