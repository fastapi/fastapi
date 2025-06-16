# Cookie 参数

 定义 `Cookie` 参数与定义 `Query` 和 `Path` 参数一样。

## 导入 `Cookie`

首先，导入 `Cookie`：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## 声明 `Cookie` 参数

声明 `Cookie` 参数的方式与声明 `Query` 和 `Path` 参数相同。

第一个值是默认值，还可以传递所有验证参数或注释参数：


{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 技术细节

`Cookie` 、`Path` 、`Query` 是**兄弟类**，都继承自共用的 `Param` 类。

注意，从 `fastapi` 导入的 `Query`、`Path`、`Cookie` 等对象，实际上是返回特殊类的函数。

///

/// info | 说明

必须使用 `Cookie` 声明 cookie 参数，否则该参数会被解释为查询参数。

///

## 小结

使用 `Cookie` 声明 cookie 参数的方式与 `Query` 和 `Path` 相同。
