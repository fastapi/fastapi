# 路径参数和数值校验 { #path-parameters-and-numeric-validations }

与使用 `Query` 为查询参数声明更多的校验和元数据的方式相同，你也可以使用 `Path` 为路径参数声明相同类型的校验和元数据。

## 导入 `Path` { #import-path }

首先，从 `fastapi` 导入 `Path`，并导入 `Annotated`：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | 信息

FastAPI 在 0.95.0 版本添加了对 `Annotated` 的支持（并开始推荐使用它）。

如果你使用的是更旧的版本，尝试使用 `Annotated` 会报错。

请确保在使用 `Annotated` 之前，将 FastAPI 版本[升级](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}到至少 0.95.1。

///

## 声明元数据 { #declare-metadata }

你可以声明与 `Query` 相同的所有参数。

例如，要为路径参数 `item_id` 声明 `title` 元数据值，你可以这样写：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | 注意

路径参数总是必需的，因为它必须是路径的一部分。即使你将其声明为 `None` 或设置了默认值，也不会产生任何影响，它依然始终是必需参数。

///

## 按需对参数排序 { #order-the-parameters-as-you-need }

/// tip | 提示

如果你使用 `Annotated`，这点可能不那么重要或必要。

///

假设你想要将查询参数 `q` 声明为必需的 `str`。

并且你不需要为该参数声明其他内容，所以实际上不需要用到 `Query`。

但是你仍然需要为路径参数 `item_id` 使用 `Path`。并且出于某些原因你不想使用 `Annotated`。

如果你将带有“默认值”的参数放在没有“默认值”的参数之前，Python 会报错。

不过你可以重新排序，让没有默认值的参数（查询参数 `q`）放在最前面。

对 **FastAPI** 来说这无关紧要。它会通过参数的名称、类型和默认值声明（`Query`、`Path` 等）来检测参数，而不关心顺序。

因此，你可以将函数声明为：

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

但请记住，如果你使用 `Annotated`，你就不会遇到这个问题，因为你没有使用 `Query()` 或 `Path()` 作为函数参数的默认值。

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## 按需对参数排序的技巧 { #order-the-parameters-as-you-need-tricks }

/// tip | 提示

如果你使用 `Annotated`，这点可能不那么重要或必要。

///

这里有一个小技巧，可能会很方便，但你并不会经常需要它。

如果你想要：

* 在没有 `Query` 且没有任何默认值的情况下声明查询参数 `q`
* 使用 `Path` 声明路径参数 `item_id`
* 让它们的顺序与上面不同
* 不使用 `Annotated`

...Python 为此有一个小的特殊语法。

在函数的第一个参数位置传入 `*`。

Python 不会对这个 `*` 做任何事，但它会知道之后的所有参数都应该作为关键字参数（键值对）来调用，也被称为 <abbr title="来自：K-ey W-ord Arg-uments"><code>kwargs</code></abbr>。即使它们没有默认值。

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### 使用 `Annotated` 更好 { #better-with-annotated }

请记住，如果你使用 `Annotated`，因为你没有使用函数参数的默认值，所以你不会有这个问题，你大概率也不需要使用 `*`。

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## 数值校验：大于等于 { #number-validations-greater-than-or-equal }

使用 `Query` 和 `Path`（以及你稍后会看到的其他类）你可以声明数值约束。

在这里，使用 `ge=1` 后，`item_id` 必须是一个整数，值要「`g`reater than or `e`qual」1。

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## 数值校验：大于和小于等于 { #number-validations-greater-than-and-less-than-or-equal }

同样适用于：

* `gt`：大于（`g`reater `t`han）
* `le`：小于等于（`l`ess than or `e`qual）

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## 数值校验：浮点数、大于和小于 { #number-validations-floats-greater-than-and-less-than }

数值校验同样适用于 `float` 值。

能够声明 <abbr title="greater than - 大于"><code>gt</code></abbr> 而不仅仅是 <abbr title="greater than or equal - 大于等于"><code>ge</code></abbr> 在这里变得很重要。例如，你可以要求一个值必须大于 `0`，即使它小于 `1`。

因此，`0.5` 将是有效值。但是 `0.0` 或 `0` 不是。

对于 <abbr title="less than - 小于"><code>lt</code></abbr> 也是一样的。

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## 总结 { #recap }

你能够以与[查询参数和字符串校验](query-params-str-validations.md){.internal-link target=_blank}相同的方式使用 `Query`、`Path`（以及其他你还没见过的类）声明元数据和字符串校验。

而且你还可以声明数值校验：

* `gt`：大于（`g`reater `t`han）
* `ge`：大于等于（`g`reater than or `e`qual）
* `lt`：小于（`l`ess `t`han）
* `le`：小于等于（`l`ess than or `e`qual）

/// info | 信息

`Query`、`Path` 以及你后面会看到的其他类，都是一个通用 `Param` 类的子类。

它们都共享相同的参数，用于你已看到的额外校验和元数据。

///

/// note | 技术细节

当你从 `fastapi` 导入 `Query`、`Path` 和其他对象时，它们实际上是函数。

当被调用时，它们会返回同名类的实例。

也就是说，你导入的是函数 `Query`。当你调用它时，它会返回一个同名的 `Query` 类的实例。

之所以使用这些函数（而不是直接使用类），是为了让你的编辑器不要因为它们的类型而标记错误。

这样你就可以使用常规的编辑器和编码工具，而不必添加自定义配置来忽略这些错误。

///
