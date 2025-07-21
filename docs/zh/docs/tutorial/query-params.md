# 查询参数

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数。

{* ../../docs_src/query_params/tutorial001.py hl[9] *}

查询字符串是键值对的集合，这些键值对位于 URL 的 `?` 之后，以 `&` 分隔。

例如，以下 URL 中：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

……查询参数为：

* `skip`：值为 `0`
* `limit`：值为 `10`

这些值都是 URL 的组成部分，因此，它们的类型**本应**是字符串。

但声明 Python 类型（上例中为 `int`）之后，这些值就会转换为声明的类型，并进行类型校验。

所有应用于路径参数的流程也适用于查询参数：

* （显而易见的）编辑器支持
* 数据<abbr title="将来自 HTTP 请求的字符串转换为 Python 数据类型">**解析**</abbr>
* 数据校验
* API 文档

## 默认值

查询参数不是路径的固定内容，它是可选的，还支持默认值。

上例用 `skip=0` 和 `limit=10` 设定默认值。

访问 URL：

```
http://127.0.0.1:8000/items/
```

与访问以下地址相同：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

但如果访问：

```
http://127.0.0.1:8000/items/?skip=20
```

查询参数的值就是：

* `skip=20`：在 URL 中设定的值
* `limit=10`：使用默认值

## 可选参数

同理，把默认值设为 `None` 即可声明**可选的**查询参数：

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

本例中，查询参数 `q` 是可选的，默认值为 `None`。

/// check | 检查

注意，**FastAPI** 可以识别出 `item_id` 是路径参数，`q` 不是路径参数，而是查询参数。

///

/// note | 笔记

因为默认值为 `= None`，FastAPI 把 `q` 识别为可选参数。

FastAPI 不使用 `Optional[str]` 中的 `Optional`（只使用 `str`），但 `Optional[str]` 可以帮助编辑器发现代码中的错误。

///

## 查询参数类型转换

参数还可以声明为 `bool` 类型，FastAPI 会自动转换参数类型：


{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

本例中，访问：

```
http://127.0.0.1:8000/items/foo?short=1
```

或

```
http://127.0.0.1:8000/items/foo?short=True
```

或

```
http://127.0.0.1:8000/items/foo?short=true
```

或

```
http://127.0.0.1:8000/items/foo?short=on
```

或

```
http://127.0.0.1:8000/items/foo?short=yes
```

或其它任意大小写形式（大写、首字母大写等），函数接收的 `short` 参数都是布尔值 `True`。值为 `False` 时也一样。


## 多个路径和查询参数

**FastAPI** 可以识别同时声明的多个路径参数和查询参数。

而且声明查询参数的顺序并不重要。

FastAPI 通过参数名进行检测：

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## 必选查询参数

为不是路径参数的参数声明默认值（至此，仅有查询参数），该参数就**不是必选**的了。

如果只想把参数设为**可选**，但又不想指定参数的值，则要把默认值设为 `None`。

如果要把查询参数设置为**必选**，就不要声明默认值：

{* ../../docs_src/query_params/tutorial005.py hl[6:7] *}

这里的查询参数 `needy` 是类型为 `str` 的必选查询参数。

在浏览器中打开如下 URL：

```
http://127.0.0.1:8000/items/foo-item
```

……因为路径中没有必选参数 `needy`，返回的响应中会显示如下错误信息：

```JSON
{
    "detail": [
        {
            "loc": [
                "query",
                "needy"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

`needy` 是必选参数，因此要在 URL 中设置值：

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

……这样就正常了：

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

当然，把一些参数定义为必选，为另一些参数设置默认值，再把其它参数定义为可选，这些操作都是可以的：

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

本例中有 3 个查询参数：

* `needy`，必选的 `str` 类型参数
* `skip`，默认值为 `0` 的 `int` 类型参数
* `limit`，可选的 `int` 类型参数

/// tip | 提示

还可以像在[路径参数](path-params.md#_8){.internal-link target=_blank} 中那样使用 `Enum`。

///
