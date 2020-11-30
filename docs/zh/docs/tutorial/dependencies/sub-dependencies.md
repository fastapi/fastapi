# 子依赖项

您可以创建具有 **子依赖项** 的依赖项。

它们可以根据你需要的足够 **深**。

**FastAPI**将负责解析他们。

### 第一个依赖项 "dependable"

你可以创建第一个依赖 ("dependable") 比如:

```Python hl_lines="8-9"
{!../../../docs_src/dependencies/tutorial005.py!}
```

它声明一个可选的查询参数 `q` 声明为 `str` ，然后返回它。

这很简单(不是很有用)，但是可以帮助我们关注子依赖关系的工作方式。

### 第二个依赖，"可靠的" 和 "依赖的"

然后你可以创建另一个依赖函数(一个 "可依赖" )，同时声明它自己的依赖(所以它也是一个 "依赖" ):

```Python hl_lines="13"
{!../../../docs_src/dependencies/tutorial005.py!}
```

让我们关注一下声明的参数:

* 即使这个函数本身是一个依赖项 ("可依赖") 它也声明了另一个依赖项 (它"依赖"于其他东西e).
    * 它依赖 `query_extractor`, 并将依赖项的返回赋值给参数 `q`。
* 它同时也声明了一个可选的 cookie `last_query` 为一个 `str`.
    * 如果用户没有提供任何查询参数 `q` ，我们使用之前保存到一个cookie的上次使用的查询。

### 使用依赖关系

然后我们可以使用依赖:

```Python hl_lines="21"
{!../../../docs_src/dependencies/tutorial005.py!}
```

!!! info
    注意，我们只在 *路径操作函数* 中声明了一个依赖项，即 `query_or_cookie_extractor` 。

    但是 **FastAPI** 知道它必须首先解决 `query_extractor` ，以便在调用 `query_or_cookie_extractor` 时将结果传递给它。

```mermaid
graph TB

query_extractor(["query_extractor"])
query_or_cookie_extractor(["query_or_cookie_extractor"])

read_query["/items/"]

query_extractor --> query_or_cookie_extractor --> read_query
```

## 多次使用相同依赖项

如果您的一个依赖项为相同的 *路径操作* 声明了多次，例如，多个依赖项有一个公共子依赖项，那么 **FastAPI** 将知道每个请求只调用该子依赖项一次。

它将返回值保存在一个<abbr title="一个实用程序/系统来存储计算/生成的值，以便重用它们，而不是再次计算它们。">"cache"</abbr>并将其传递给在该特定请求中需要它的所有 "依赖项" ，而不是为同一请求多次调用依赖项。

在一个高级场景中，你知道你需要在同一个请求的每一步(可能多次)调用依赖项，而不是使用 "cached" 值，你可以在使用 `Depends` 时设置参数 `use_cache=False` :

```Python hl_lines="1"
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

## 总结

虽然这里使用的词汇十分华丽，但 **依赖注入** 系统非常简单。

只是与 *路径操作函数* 使用相同的函数。

但是，它仍然非常强大，允许您任意地声明深度嵌套的依赖关系 "图" (树)。

!!! tip
    对于这些简单的示例，所有这些似乎都不太有用。

    但是你会在关于 **安全** 的章节中看到它是多么有用。

    你还会看到它为你节省的代码量。
