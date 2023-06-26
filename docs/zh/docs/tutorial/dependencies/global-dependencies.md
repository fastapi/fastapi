# 全局依赖项

有时，我们要为整个应用添加依赖项。

通过与定义[*路径装饰器依赖项*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 类似的方式，可以把依赖项添加至整个 `FastAPI` 应用。

这样一来，就可以为所有*路径操作*应用该依赖项：

```Python hl_lines="15"
{!../../../docs_src/dependencies/tutorial012.py!}
```

[*路径装饰器依赖项*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 一章的思路均适用于全局依赖项， 在本例中，这些依赖项可以用于应用中的所有*路径操作*。

## 为一组路径操作定义依赖项

稍后，[大型应用 - 多文件](../../tutorial/bigger-applications.md){.internal-link target=_blank}一章中会介绍如何使用多个文件创建大型应用程序，在这一章中，您将了解到如何为一组*路径操作*声明单个 `dependencies` 参数。
