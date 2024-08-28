# 关于 FastAPI 版本

**FastAPI** 已在许多应用程序和系统的生产环境中使用。 并且测试覆盖率保持在100%。 但其开发进度仍在快速推进。

经常添加新功能，定期修复错误，并且代码仍在持续改进。

这就是为什么当前版本仍然是`0.x.x`，这反映出每个版本都可能有Breaking changes。 这遵循<a href="https://semver.org/" class="external-link" target="_blank">语义版本控制</a>的约定。

你现在就可以使用 **FastAPI** 创建生产环境应用程序（你可能已经这样做了一段时间），你只需确保使用的版本可以与其余代码正确配合即可。

## 固定你的 `fastapi` 版本

你应该做的第一件事是将你正在使用的 **FastAPI** 版本“固定”到你知道适用于你的应用程序的特定最新版本。

例如，假设你在应用程序中使用版本`0.45.0`。

如果你使用`requirements.txt`文件，你可以使用以下命令指定版本：

````txt
fastapi==0.45.0
````

这意味着你将使用版本`0.45.0`。

或者你也可以将其固定为：

````txt
fastapi>=0.45.0,<0.46.0
````

这意味着你将使用`0.45.0`或更高版本，但低于`0.46.0`，例如，版本`0.45.2`仍会被接受。

如果你使用任何其他工具来管理你的安装，例如 Poetry、Pipenv 或其他工具，它们都有一种定义包的特定版本的方法。

## 可用版本

你可以在[发行说明](../release-notes.md){.internal-link target=_blank}中查看可用版本（例如查看当前最新版本）。

## 关于版本

遵循语义版本控制约定，任何低于`1.0.0`的版本都可能会添加 breaking changes。

FastAPI 还遵循这样的约定：任何`PATCH`版本更改都是为了bug修复和non-breaking changes。

/// tip

"PATCH"是最后一个数字，例如，在`0.2.3`中，PATCH版本是`3`。

///

因此，你应该能够固定到如下版本：

```txt
fastapi>=0.45.0,<0.46.0
```

"MINOR"版本中会添加breaking changes和新功能。

/// tip

"MINOR"是中间的数字，例如，在`0.2.3`中，MINOR版本是`2`。

///

## 升级FastAPI版本

你应该为你的应用程序添加测试。

使用 **FastAPI** 编写测试非常简单（感谢 Starlette），请参考文档：[测试](../tutorial/testing.md){.internal-link target=_blank}

添加测试后，你可以将 **FastAPI** 版本升级到更新版本，并通过运行测试来确保所有代码都能正常工作。

如果一切正常，或者在进行必要的更改之后，并且所有测试都通过了，那么你可以将`fastapi`固定到新的版本。

## 关于Starlette

你不应该固定`starlette`的版本。

不同版本的 **FastAPI** 将使用特定的较新版本的 Starlette。

因此，**FastAPI** 自己可以使用正确的 Starlette 版本。

## 关于 Pydantic

Pydantic 包含针对 **FastAPI** 的测试及其自己的测试，因此 Pydantic 的新版本（`1.0.0`以上）始终与 FastAPI 兼容。

你可以将 Pydantic 固定到适合你的`1.0.0`以上和`2.0.0`以下的任何版本。

例如：

````txt
pydantic>=1.2.0,<2.0.0
````
