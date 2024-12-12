# Header 参数

定义 `Header` 参数的方式与定义 `Query`、`Path`、`Cookie` 参数相同。

## 导入 `Header`

首先，导入 `Header`：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## 声明 `Header` 参数

然后，使用和 `Path`、`Query`、`Cookie` 一样的结构定义 header 参数。

第一个值是默认值，还可以传递所有验证参数或注释参数：

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | 技术细节

`Header` 是 `Path`、`Query`、`Cookie` 的**兄弟类**，都继承自共用的 `Param` 类。

注意，从 `fastapi` 导入的 `Query`、`Path`、`Header` 等对象，实际上是返回特殊类的函数。

///

/// info | 说明

必须使用 `Header` 声明 header 参数，否则该参数会被解释为查询参数。

///

## 自动转换

`Header` 比 `Path`、`Query` 和 `Cookie` 提供了更多功能。

大部分标准请求头用**连字符**分隔，即**减号**（`-`）。

但是 `user-agent` 这样的变量在 Python 中是无效的。

因此，默认情况下，`Header` 把参数名中的字符由下划线（`_`）改为连字符（`-`）来提取并存档请求头 。

同时，HTTP 的请求头不区分大小写，可以使用 Python 标准样式（即 **snake_case**）进行声明。

因此，可以像在 Python 代码中一样使用 `user_agent` ，无需把首字母大写为 `User_Agent` 等形式。

如需禁用下划线自动转换为连字符，可以把 `Header` 的 `convert_underscores` 参数设置为 `False`：

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | 警告

注意，使用 `convert_underscores = False` 要慎重，有些 HTTP 代理和服务器不支持使用带有下划线的请求头。

///

## 重复的请求头

有时，可能需要接收重复的请求头。即同一个请求头有多个值。

类型声明中可以使用 `list` 定义多个请求头。

使用 Python `list` 可以接收重复请求头所有的值。

例如，声明 `X-Token` 多次出现的请求头，可以写成这样：

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

与*路径操作*通信时，以下面的方式发送两个 HTTP 请求头：

```
X-Token: foo
X-Token: bar
```

响应结果是：

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## 小结

使用 `Header` 声明请求头的方式与 `Query`、`Path` 、`Cookie` 相同。

不用担心变量中的下划线，**FastAPI** 可以自动转换。
