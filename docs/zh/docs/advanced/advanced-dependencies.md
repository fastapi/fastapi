# 高级依赖项

## 参数化的依赖项

我们之前看到的所有依赖项都是写死的函数或类。

但也可以为依赖项设置参数，避免声明多个不同的函数或类。

假设要创建校验查询参数 `q` 是否包含固定内容的依赖项。

但此处要把待检验的固定内容定义为参数。

## **可调用**实例

Python 可以把类实例变为**可调用项**。

这里说的不是类本身（类本就是可调用项），而是类实例。

为此，需要声明 `__call__` 方法：

{* ../../docs_src/dependencies/tutorial011.py hl[10] *}

本例中，**FastAPI**  使用 `__call__` 检查附加参数及子依赖项，稍后，还要调用它向*路径操作函数*传递值。

## 参数化实例

接下来，使用 `__init__` 声明用于**参数化**依赖项的实例参数：

{* ../../docs_src/dependencies/tutorial011.py hl[7] *}

本例中，**FastAPI** 不使用 `__init__`，我们要直接在代码中使用。

## 创建实例

使用以下代码创建类实例：

{* ../../docs_src/dependencies/tutorial011.py hl[16] *}

这样就可以**参数化**依赖项，它包含 `checker.fixed_content` 的属性 - `"bar"`。

## 把实例作为依赖项

然后，不要再在 `Depends(checker)` 中使用 `Depends(FixedContentQueryChecker)`， 而是要使用 `checker`，因为依赖项是类实例 - `checker`，不是类。

处理依赖项时，**FastAPI** 以如下方式调用 `checker`：

```Python
checker(q="somequery")
```

……并用*路径操作函数*的参数 `fixed_content_included` 返回依赖项的值：

{* ../../docs_src/dependencies/tutorial011.py hl[20] *}

/// tip | 提示

本章示例有些刻意，也看不出有什么用处。

这个简例只是为了说明高级依赖项的运作机制。

在有关安全的章节中，工具函数将以这种方式实现。

只要能理解本章内容，就能理解安全工具背后的运行机制。

///
