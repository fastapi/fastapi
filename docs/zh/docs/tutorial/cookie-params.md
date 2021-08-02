# Cookie 参数

你可以像定义 `Query` 参数和 `Path` 参数一样来定义 `Cookie` 参数。

## 导入 `Cookie`

首先，导入 `Cookie`:

```Python hl_lines="3"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

## 声明 `Cookie` 参数

声明 `Cookie` 参数的结构与声明 `Query` 参数和 `Path` 参数时相同。

第一个值是参数的默认值，同时也可以传递所有验证参数或注释参数，来校验参数：


```Python hl_lines="9"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

!!! note "技术细节"
    `Cookie` 、`Path` 、`Query`是兄弟类，它们都继承自公共的 `Param` 类

    但请记住，当你从 `fastapi` 导入的 `Query`、`Path`、`Cookie` 或其他参数声明函数，这些实际上是返回特殊类的函数。

!!! info
    你需要使用 `Cookie` 来声明 cookie 参数，否则参数将会被解释为查询参数。

## 总结

使用 `Cookie` 声明 cookie 参数，使用方式与 `Query` 和 `Path` 类似。
