# 路径操作装饰器中的依赖项 { #dependencies-in-path-operation-decorators }

在某些情况下，你其实并不需要在*路径操作函数*中使用依赖项的返回值。

或者依赖项不返回值。

但你仍然需要它被执行/解析。

对于这些情况，与其用 `Depends` 声明一个*路径操作函数*参数，不如在*路径操作装饰器*中添加一个由 `dependencies` 组成的 `list`。

## 在*路径操作装饰器*中添加 `dependencies` { #add-dependencies-to-the-path-operation-decorator }

*路径操作装饰器*接收一个可选参数 `dependencies`。

它应该是一个由 `Depends()` 组成的 `list`：

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[19] *}

这些依赖项会像普通依赖项一样被执行/解析。但是它们的值（如果有返回值）不会被传递给你的*路径操作函数*。

/// tip | 提示

有些编辑器会检查未使用的函数参数，并将其显示为错误。

在*路径操作装饰器*中使用这些 `dependencies`，你可以确保它们会被执行，同时避免编辑器/工具链报错。

它也可能帮助避免新开发者看到你代码里一个未使用的参数而产生困惑，并认为它是不必要的。

///

/// info | 信息

在这个例子中，我们使用了虚构的自定义 headers `X-Key` 和 `X-Token`。

但在真实场景中，实现安全措施时，使用集成的[安全工具（下一章）](../security/index.md){.internal-link target=_blank}会获得更多收益。

///

## 依赖项错误和返回值 { #dependencies-errors-and-return-values }

你可以使用平时正常使用的同一个依赖项*函数*。

### 依赖项的需求项 { #dependency-requirements }

它们可以声明请求的需求项（比如 headers）或其他子依赖项：

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[8,13] *}

### 触发异常 { #raise-exceptions }

这些依赖项可以像普通依赖项一样 `raise` 异常：

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[10,15] *}

### 返回值 { #return-values }

并且它们可以返回值或不返回值，这些值都不会被使用。

因此，你可以复用你已经在别处用过的、（会返回值的）普通依赖项，即使这个值不会被使用，该依赖项也会被执行：

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[11,16] *}

## 为一组*路径操作*定义依赖项 { #dependencies-for-a-group-of-path-operations }

稍后，当你阅读如何组织更大的应用（[大型应用 - 多文件](../../tutorial/bigger-applications.md){.internal-link target=_blank}）时，可能会涉及多个文件，你将学习如何为一组*路径操作*声明单个 `dependencies` 参数。

## 全局依赖项 { #global-dependencies }

接下来我们将学习如何为整个 `FastAPI` 应用程序添加依赖项，使它们应用于每个*路径操作*。
