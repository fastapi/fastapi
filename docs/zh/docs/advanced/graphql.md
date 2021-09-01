# GraphQL 查询

**FastAPI** 通过 `graphene` 支持库使用可选的 GraphQL（由 Starlette 直接提供支持）。

 **FastAPI** 可在同一个应用中合并使用普通*路径操作*与 GraphQL。

## 导入与使用 `graphene`

Python 中通过 `Graphene` 实现 GraphQL，详见 <a href="https://docs.graphene-python.org/en/latest/quickstart/" class="external-link" target="_blank">Graphene 官档</a>。

导入 `graphene`，并定义 GraphQL 数据：

```Python hl_lines="1  6-10"
{!../../../docs_src/graphql/tutorial001.py!}
```

## 添加 Starlette 的 `GraphQLApp`

导入并添加 Starlette 的 `GraphQLApp`：

```Python hl_lines="3  14"
{!../../../docs_src/graphql/tutorial001.py!}
```

!!! info "说明"

    `.add_route` 是 Starlette 添加路由的方式（由 FastAPI 继承），无需声明指定操作（如 `.get()`、`.post()` 等）。

## 查看文档

使用 uvicorn 运行服务，在浏览器中打开 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000。</a>

查看 GraphQL 网络用户界面：

<img src="/img/tutorial/graphql/image01.png">

## 更多说明

更多详情，如：

* 访问请求信息
* 添加后台任务
* 使用普通函数或异步函数等

详见 <a href="https://www.starlette.io/graphql/" class="external-link" target="_blank">Starlette 官档 - GraphQL</a>。
