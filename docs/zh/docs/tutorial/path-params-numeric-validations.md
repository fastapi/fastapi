# 路径参数和数值校验

除了可以为 `Query` 查询参数声明校验和元数据，还可以为 `Path` 路径参数声明相同类型的校验和元数据。

## 导入 Path

首先，从 `fastapi` 导入 `Path`：

```Python hl_lines="3"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

## 声明元数据

可以声明与 `Query` 相同的所有参数。

例如，为路径参数 `item_id` 声明 `title` 元数据的值时，可以输入：

```Python hl_lines="10"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

!!! note "笔记"

    因为路径参数必须是路径的一部分，所以路径参数总是必选的。
    
    因此，声明路径参数时要使用 `...`，把它标记为必选参数。
    
    不过，就算使用 `None` 声明路径参数，或设置其他默认值也不会有任何影响，路径参数依然是必选参数。

## 按需排序参数

假设要把查询参数 `q` 声明为必选的 `str` 类型。

而且，因为不用为该参数声明任何其他内容，因此无需使用 `Query`。

但仍需使用 `Path` 声明路径参数 `item_id`。

如果把有「默认值」的参数置于无「默认值」的参数前，Python 会报错。

但可以重新排序，把无默认值的查询参数 `q` 放到最前面。

**FastAPI** 不关注参数排序。只是通过声明的参数名称、类型和默认值（`Query`、`Path` 等）来检测参数，不关注参数的顺序。

因此，可以把函数声明为：

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## 按需排序参数的技巧

如果不想使用 `Query` 声明没有默认值的查询参数 `q`，但同时还要使用 `Path` 声明路径参数 `item_id`，并使用不同的排序方式，可以使用 Python 的特殊语法。

把 `*` 作为函数的第一个参数。

Python 不对 `*` 执行任何操作，但会把 `*` 之后的所有参数都当作关键字参数（键值对），也叫 <abbr title="来自：K-ey W-ord Arg-uments"><code>kwargs</code></abbr>。即便这些参数并没有默认值。

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## 数值校验：大于等于

使用 `Query` 和 `Path`（以及后文中的其他类）时，既可以声明字符串约束，也可以声明数值约束。

此处，添加 `ge=1` 后，`item_id` 就必须是大于（`g`reater than）等于（`e`qual）`1` 的整数。

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## 数值校验：大于、小于等于

同样：

- `gt`：大于（`g`reater `t`han）
- `le`：小于等于（`l`ess than or `e`qual）

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## 数值校验：浮点数、大于和小于

数值校验同样适用于 `float` 值。

此处，重要的是声明 <abbr title="大于"><code>gt</code></abbr>，而不仅是 <abbr title="大于等于"><code>ge</code></abbr>。例如，值必须大于 `0`，即使该值小于 `1`。

因此，`0.5` 是有效的，但 `0.0`或 `0` 则无效。

对于小于（<abbr title="less than"><code>lt</code></abbr>）也是一样的。

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## 小结

`Query`、`Path`（及其他尚未介绍的类）可以使用[查询参数和字符串校验](query-params-str-validations.md){.internal-link target=\_blank} 中的方式声明元数据和字符串校验。

同样，也可以声明数值校验：

- `gt`：大于（`g`reater `t`han）
- `ge`：大于等于（`g`reater than or `e`qual）
- `lt`：小于（`l`ess `t`han）
- `le`：小于等于（`l`ess than or `e`qual）

!!! info "说明"

    `Query`、`Path` 及后文中要介绍的其他类都继承自同一个 `Param` 类（无需直接使用）。
    
    而且，它们共享使用所有前文中介绍过的，用于添加更多校验和元数据的参数。

!!! note "技术细节"

    实际上，从 `fastapi` 导入的 `Query`、`Path` 等对象都是函数。
    
    调用它们时会返回同名的类实例。
    
    因此，调用导入的 `Query` 函数时，它返回的类实例也命名为 `Query` 。
    
    使用函数（而不是直接使用类）的原因是为了不让编辑器显示类型错误。
    
    这样，在使用编辑器和开发工具时，不用添加自定义配置来忽略这些错误。
