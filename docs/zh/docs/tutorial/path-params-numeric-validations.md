# 路径参数与数值校验 { #path-parameters-and-numeric-validations }

与你可以使用 `Query` 为查询参数声明更多校验和元数据的方式相同，你也可以使用 `Path` 为路径参数声明同类型的校验和元数据。

## 导入 `Path` { #import-path }

首先，从 `fastapi` 导入 `Path`，并导入 `Annotated`：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | 信息

FastAPI 在 0.95.0 版本中增加了对 `Annotated` 的支持（并开始推荐使用它）。

如果你的版本更旧，在尝试使用 `Annotated` 时会报错。

在使用 `Annotated` 之前，请确保将 FastAPI 版本至少[升级到 0.95.1](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}。

///

## 声明元数据 { #declare-metadata }

你可以声明与 `Query` 相同的所有参数。

例如，要为路径参数 `item_id` 声明一个 `title` 元数据值，你可以这样写：

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | 注意

路径参数总是必需的，因为它必须是路径的一部分。即使你用 `None` 声明它或设置一个默认值，也不会影响任何事情，它仍然总是必需的。

///

## 按需对参数排序 { #order-the-parameters-as-you-need }

/// tip | 提示

如果你使用 `Annotated`，这可能就没那么重要或必要了。

///

假设你想把查询参数 `q` 声明为必需的 `str`。

而且你不需要为该参数声明任何其他内容，所以实际上你并不需要使用 `Query`。

但是你仍然需要对路径参数 `item_id` 使用 `Path`。并且由于某些原因你不想使用 `Annotated`。

如果你把带有“默认值”的值放在没有“默认值”的值之前，Python 会报错。

但是你可以重新排序，把没有默认值的值（查询参数 `q`）放到最前面。

对 **FastAPI** 来说这无关紧要。它会通过参数的名称、类型和默认声明（`Query`、`Path` 等）来检测参数，它不关心顺序。

因此，你可以将函数声明为：

{* ../../docs_src/path_params_numeric_validations/tutorial002_py39.py hl[7] *}

但请记住，如果你使用 `Annotated`，就不会有这个问题，因为你不会把函数参数默认值用于 `Query()` 或 `Path()`。

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py *}

## 按需对参数排序的小技巧 { #order-the-parameters-as-you-need-tricks }

/// tip | 提示

如果你使用 `Annotated`，这可能就没那么重要或必要了。

///

这里有一个**小技巧**，可能会很方便，但你不会经常需要它。

如果你想要：

* 不使用 `Query` 且不提供任何默认值来声明查询参数 `q`
* 使用 `Path` 声明路径参数 `item_id`
* 让它们按不同的顺序出现
* 不使用 `Annotated`

...Python 对此有一个小小的特殊语法。

把 `*` 作为函数的第一个参数传入。

Python 不会对这个 `*` 做任何事情，但它会知道后面的所有参数都应该以关键字参数（键值对）的方式调用，也被称为 <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>。即使它们没有默认值。

{* ../../docs_src/path_params_numeric_validations/tutorial003_py39.py hl[7] *}

### 使用 `Annotated` 更好 { #better-with-annotated }

请记住，如果你使用 `Annotated`，由于你并没有使用函数参数默认值，你就不会遇到这个问题，并且你可能也不需要使用 `*`。

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py hl[10] *}

## 数值校验：大于等于 { #number-validations-greater-than-or-equal }

使用 `Query` 和 `Path`（以及你后面会看到的其他对象）可以声明数值约束。

这里通过 `ge=1`，`item_id` 必须是一个“`g`reater than or `e`qual”（大于或等于）`1` 的整数。

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py hl[10] *}

## 数值校验：大于和小于等于 { #number-validations-greater-than-and-less-than-or-equal }

同样适用于：

* `gt`：`g`reater `t`han
* `le`：`l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py hl[10] *}

## 数值校验：浮点数、大于和小于 { #number-validations-floats-greater-than-and-less-than }

数值校验也适用于 `float` 值。

这时能够声明 <abbr title="greater than - 大于"><code>gt</code></abbr> 而不仅仅是 <abbr title="greater than or equal - 大于等于"><code>ge</code></abbr> 就变得很重要了。因为你可以要求例如某个值必须大于 `0`，即使它小于 `1`。

因此，`0.5` 是有效值。但 `0.0` 或 `0` 不是。

对 <abbr title="less than - 小于"><code>lt</code></abbr> 也是一样的。

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py hl[13] *}

## 总结 { #recap }

使用 `Query`、`Path`（以及你还没见过的其他对象）可以用与 [查询参数与字符串校验](query-params-str-validations.md){.internal-link target=_blank} 相同的方式声明元数据和字符串校验。

并且你还可以声明数值校验：

* `gt`：`g`reater `t`han
* `ge`：`g`reater than or `e`qual
* `lt`：`l`ess `t`han
* `le`：`l`ess than or `e`qual

/// info | 信息

`Query`、`Path` 以及你后面会看到的其他类都是同一个 `Param` 类的子类。

它们都共享你已看到的、用于额外校验和元数据的相同参数。

///

/// note | 技术细节

当你从 `fastapi` 导入 `Query`、`Path` 等时，它们实际上是函数。

它们在被调用时，会返回同名类的实例。

因此，你导入的是函数 `Query`。当你调用它时，它会返回同样名为 `Query` 的类的一个实例。

这些函数之所以存在（而不是直接使用类），是为了让你的编辑器不会标记它们类型相关的错误。

这样，你就可以使用常规编辑器和编码工具，而无需添加自定义配置来忽略这些错误。

///
