# 依赖项 - `Depends()` 和 `Security()`

## `Depends()`

依赖关系主要通过特殊函数 `Depends()` 来处理。

下面是该函数及其参数的引用。

您可以直接从 `fastapi` 中导入该参数：

```python
from fastapi import Depends
```

::: fastapi.Depends

## `Security()`

在许多情况下，您可以使用 `Depends()`，通过依赖关系来处理安全性（授权、身份验证等）。

但如果您也想声明 OAuth2 作用域，则可以使用 `Security()`，而不是 `Depends()`。

你可以直接从 `fastapi` 导入 `Security()`：

```python
from fastapi import Security
```

::: fastapi.Security
