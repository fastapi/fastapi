# 查询参数和字符串校验

**FastAPI** 允许为参数声明附加信息与校验。

以下面的应用为例：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial001.py!}
```

查询参数 `q` 的类型是 `Optional[str]`，即它的类型是 `str`，但也可以是 `None`（其实，是它的默认值为 `None`），因此，FastAPI 把它当作可选参数。

!!! note " 笔记"

    因为默认值是 `= None`， 因此，FastAPI 可以识别出 `q` 的值是可选的。
    
    FastAPI 不使用 `Optional[str]` 中的 `Optional`，但使用 `Optional` 可以让编辑器提供更好的支持，并有助于检查错误。

## 附加校验

接下来，添加一些约束条件：即使 `q` 是可选的，但只要提供了该参数，**该参数的长度就不能超过 50 个字符**。

### 导入 `Query`

首先，从 `fastapi` 导入 `Query`：

```Python hl_lines="3"
{!../../../docs_src/query_params_str_validations/tutorial002.py!}
```

## 使用 `Query` 作为默认值

接下来，把 `Query` 作为查询参数的默认值，并把 `max_length` 参数设置为 50：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial002.py!}
```

由于必须用 `Query(None)` 替换默认值 `None`，`Query` 的第一个参数同样也用于定义默认值。

所以：

```Python
q: Optional[str] = Query(None)
```

……让参数变为可选，等效于：

```Python
q: Optional[str] = None
```

但 `Query` 可以显式声明查询参数。

!!! info "说明"

    注意，FastAPI 关注以下内容：
    
    ```Python
    = None
    ```
    
    或：
    
    ```Python
    = Query(None)
    ```
    
    并且通过 `None` 识别出查询参数是可选的。
    
    `Optional` 只是为了让编辑器提供更好的支持。

然后，就可以向 `Query` 传递更多参数。本例使用 `max_length` 参数约束字符串：

```Python
q: str = Query(None, max_length=50)
```

这行代码会校验数据，在数据无效时显示错误信息，并在 OpenAPI 概图的*路径操作*中存档该参数。

## 添加更多校验

FastAPI 还支持 `min_length` 参数：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial003.py!}
```

## 添加正则表达式

FastAPI 支持定义参数必须与<abbr title="正则表达式或正则是定义字符串搜索模式的字符序列。">正则表达式</abbr>相匹配：

```Python hl_lines="10"
{!../../../docs_src/query_params_str_validations/tutorial004.py!}
```

这个指定的正则表达式通过以下规则检查接收到的参数值：

- `^`：以该符号之后的字符开头，符号之前没有字符
- `fixedquery`：参数值应与 `fixedquery` 完全匹配
- `$`：到此符号结束，`fixedquery` 后没有其他字符

就算搞不定**「正则表达式」**也不用担心， 不只您一个人觉得它难。不用正则表达式也可以完成很多工作。

但只要有需要，请记住，**FastAPI** 支持正则表达式。

## 默认值

向 `Query` 的第一个参数传入 `None` 作为查询参数的默认值，同样，也可以传递其他默认值。

假设声明查询参数 `q`，且 `min_length` 是 `3`，默认值是 `fixedquery`：

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial005.py!}
```

!!! note "笔记"

    包含默认值让该参数成为可选参数。

## 标记为必选

不需要声明更多校验或元数据时，只要不声明默认值，就可以让 `q` 查询参数变为必选参数，比如：

```Python
q: str
```

替换：

```Python
q: str = None
```

但现在是用 `Query` 声明该参数，例如：

```Python
q: str = Query(None, min_length=3)
```

因此，用 `Query` 把值声明为必选时，可以把 `...` 当作第一个实参（argument）：

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006.py!}
```

!!! info "说明"

    如果您之前没见过 `...`：这是一个特殊的单值，是 <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">Python 的特殊符号，叫作「省略号」</a>。

这样一来，**FastAPI** 就能把该查询参数识别为必选参数。

## 查询参数列表 / 多个值

用 `Query` 显式定义查询参数时，还可以让它接收一组值，换句话说，就是接收多个值。

例如，要在 URL 中声明多个查询参数 `q`，可以参照以下代码：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial011.py!}
```

然后，输入以下网址：

```
http://localhost:8000/items/?q=foo&q=bar
```

就可以在*路径操作函数*的*查询参数* `q` 中以 Python `list` 的形式接收*查询参数* `q` 的多个值（`foo` 和 `bar`）。

因此，该 URL 的响应为：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip "提示"

    如上例所示，把查询参数的类型声明为 `list`，要显式使用 `Query`，否则该参数会被解释为请求体。

API 交互文档会进行响应更新，允许使用多个值：

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 包含默认值的查询参数列表 / 多个值

FastAPI 还支持在未给定值时，为 `List` 定义默认值：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial012.py!}
```

访问下面的网址：

```
http://localhost:8000/items/
```

`q` 的默认值是：`["foo", "bar"]`，响应是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### 使用 `list`

也可以直接用 `list` 代替 `List [str]`：

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial013.py!}
```

!!! note "笔记"

    注意，此时，FastAPI 不再校验列表中的元素。
    
    例如，`List[int]` 会校验（并存档）列表中的元素必须是整数。但如果只使用 `list`，就不会进行类似的校验。

## 声明更多元数据

FastAPI 还支持为参数添加更多信息。

这些信息包含在 OpenAPI 概图里，用于文档用户界面和外部工具。

!!! note "笔记"

    注意，不同工具对 OpenAPI 的支持可能不同。
    
    有些工具可能不会显示所有已声明的额外信息，尽管在大多数情况下，这些缺失的功能已经纳入了这些工具的开发计划。

为 `Query` 添加 `title` 参数：

```Python hl_lines="10"
{!../../../docs_src/query_params_str_validations/tutorial007.py!}
```

及 `description` 参数：

```Python hl_lines="13"
{!../../../docs_src/query_params_str_validations/tutorial008.py!}
```

## 参数别名

假设要使用的查询参数是 `item-query`。

如下所示：

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

但 `item-query` 不是有效的 Python 变量名。

最接近的有效名称是 `item_query`。

但如果必须在 URL 中使用 `item-query` ……

可以使用 `alias` 参数声明别名，用于在 URL 中查找这个参数值：

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial009.py!}
```

## 弃用参数

如果不再需要某个参数。

但因为某些客户端还在使用该参数，又不得不保留一段时间，此时，需要文档能把它清晰地显示为<abbr title ="已过时，建议不要使用它">已弃用</abbr>。

此时，可以在 `Query` 中使用参数 `deprecated=True`：

```Python hl_lines="18"
{!../../../docs_src/query_params_str_validations/tutorial010.py!}
```

文档显示内容如下图：

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 小结

FastAPI 支持为查询参数声明更多校验和元数据。

常用于校验和元数据的参数包括：

- `alias`
- `title`
- `description`
- `deprecated`

专用于校验字符串的参数包括：

- `min_length`
- `max_length`
- `regex`

本章介绍了如何校验 `str` 值。

下一章介绍如何校验数值等其他类型。
