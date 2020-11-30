# 全局依赖项

对于某些类型的应用程序，您可能需要向整个应用程序添加依赖项。

类似于您可以 [增加 `依赖项` 到 *路径操作装饰器*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, 您可以将他们添加到 `FastAPI` 应用程序中。

在这种情况下，它们将应用于应用程序中所有的*路径操作*:

```Python hl_lines="15"
{!../../../docs_src/dependencies/tutorial012.py!}
```

所有关于 [增加 `依赖项` 到 *路径操作装饰器*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 一章中的点子仍然适用， 但在本例中，适用于应用程序中的所有 *路径操作*。

## *路径操作* 组的依赖关系

稍后，当您阅读如何构造大型应用程序 ([大型应用程序-多个文件](../../tutorial/bigger-applications.md){.internal-link target=_blank})时, 可能包含多个文件，您将了解如何为一组 *路径操作* 声明单个的 `依赖项` 参数。
