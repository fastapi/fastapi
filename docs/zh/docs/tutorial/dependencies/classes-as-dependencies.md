# 用类定义依赖项

在深入研究**依赖注入**系统前，我们先升级一下上一节中的示例。

## 上节示例中的 `dict`

上节示例中，依赖项返回的是**字典**  ：

```Python hl_lines="9"
{!../../../docs_src/dependencies/tutorial001.py!}
```

随后，这个**字典**被传递给*路径操作函数*的参数 `commons`。

因为编辑器不能获取**字典**中键值的类型，所以无法为**字典**提供代码补全等更多支持。

FastAPI 可以做的更好……

## 依赖项到底是什么

在此之前，我们只用函数定义过依赖项。

尽管这种定义依赖项的方式很常用，但并不是定义依赖项的唯一方式。

这里的核心理念是，依赖项应该是**可调用项**。

Python **可调用项**是指任何与函数类似的、**可调用**的对象。

所以，如果能以如下方式**调用**或执行对象 `something`（**不一定是**函数）：

```Python
something()
```

或

```Python
something(some_argument, some_keyword_argument="foo")
```

这个对象就是**可调用项**。

## 用类定义依赖项

注意，Python 使用与调用函数相同的语法创建类实例。

例如：

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

`fluffy` 是类 `Cat` 的实例。

创建 `fluffy` 需要**调用**`Cat` 。

因此，Python 的类也是**可调用项** 。

然后，**FastAPI** 就可以用 Python 的类声明依赖项。

实际上，FastAPI 检查的是该对象是不是**可调用项**（函数、类等）及所定义的参数。

在 **FastAPI** 中传递**可调用**依赖项时，FastAPI 会分析**可调用项**的参数，并用与处理*路径操作函数*的参数相同的方式处理这些参数，包括子依赖项。

这种方式也适用于无参数调用，处理方式与无参数的*路径操作函数*相同。

接下来，把上例中的依赖项 `common_parameters` 改为 `CommonQueryParams`：

```Python hl_lines="11-15"
{!../../../docs_src/dependencies/tutorial002.py!}
```

请注意下例中创建类实例的 `__init__` 方法：

```Python hl_lines="12"
{!../../../docs_src/dependencies/tutorial002.py!}
```

…… 它的参数与 `common_parameters` 的参数一样：

```Python hl_lines="8"
{!../../../docs_src/dependencies/tutorial001.py!}
```

**FastAPI** 用这些参数**处理**依赖项。

在这两种情况下，依赖项的参数包括：

- 可选的查询参数 `q` 
- 查询参数 `skip`，默认值为 `0` 
- 查询参数 `limit`，默认值为 `100` 

无论哪种情况，FastAPI 都会转换与验证数据，并在 OpenAPI 概图的 API 文档中显示。

## 使用声明的类

接下来，使用 `CommonQueryParams` 类定义依赖项。

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial002.py!}
```

**FastAPI** 调用 `CommonQueryParams` 类，创建**类实例**，并用参数 `commons` 把这个类实例传递给路径操作函数。

## 类型注释 vs `Depends`

注意，上述代码中使用了两次 `CommonQueryParams` :

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

实际上，**FastAPI** 通过下面这行代码中的 `CommonQueryParams` 判断哪个对象是依赖项：

```Python
... = Depends(CommonQueryParams)
```

FastAPI 从这段代码中提取声明的参数，也就是 FastAPI 实际调用的对象。

---

本例中，下面这行代码中的 `CommonQueryParams` 对于 **FastAPI** 没有实际意义：

```Python
commons: CommonQueryParams ...
```

FastAPI 不用这个参数转换与验证数据，因为该参数已经使用了 `= Depends(CommonQueryParams)` 执行这些操作。

这段代码其实可以写成下面的形式：

```Python
commons = Depends(CommonQueryParams)
```

…… 如下：

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial003.py!}
```

不过，我们还是鼓励声明类型，这样做能让编辑器知道参数 `commons` 传递的是哪个对象，从而实现代码补全、类型检查等更多支持：

<img src="/img/tutorial/dependencies/image02.png">

## 快捷方式

这段代码里重复写了两次 `CommonQueryParams` :

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

对于这种用类定义依赖项，且 **FastAPI** 调用类实例自身的情况，**FastAPI** 提供了优化的快捷方式。

对于这种特定情况，可以用如下方式编写代码：

无需在两个位置都写上调用的类：

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

……可以简写成：

```Python
commons: CommonQueryParams = Depends()
```

这段代码用依赖项声明参数的类型，并把 `Depends()` 作为该参数（在 `=` 之后）的**默认值**。因为 `Depends()` 中没有参数，所以不用在 `Depends()`中*重复*写出完整的类，`Depends(CommonQueryParams)`。

下面的代码与前例的效果一样：

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial004.py!}
```

…… **FastAPI** 知道下一步该怎么做。

!!! tip "提示"

    如果您觉得这种快捷方式没什么用处，反而增添了困扰，尽可弃之不用，*不用*快捷方式也没问题。
    
    这只是一种快捷方式，**FastAPI** 希望能让您尽量少写一些重复代码。
