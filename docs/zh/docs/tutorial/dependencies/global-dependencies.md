# 全局依赖项 { #global-dependencies }

有时，对于某些类型的应用，你可能希望把依赖项添加到整个应用。

与[给*路径操作装饰器*添加 `dependencies`](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}的方式类似，你也可以把它们添加到 `FastAPI` 应用中。

在这种情况下，它们会应用到该应用中的所有*路径操作*：

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[17] *}


关于[给*路径操作装饰器*添加 `dependencies`](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}这一节中的所有思路仍然适用，但在这里，它会应用到该应用中的所有*路径操作*。

## 为一组*路径操作*定义依赖项 { #dependencies-for-groups-of-path-operations }

稍后，在阅读如何组织更大型的应用（[大型应用 - 多文件](../../tutorial/bigger-applications.md){.internal-link target=_blank}）时，可能会涉及多个文件，你将学习如何为一组*路径操作*声明单个 `dependencies` 参数。
