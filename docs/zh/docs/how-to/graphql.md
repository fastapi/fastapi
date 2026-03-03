# GraphQL { #graphql }

由于 **FastAPI** 基于 **ASGI** 标准，因此很容易集成任何也兼容 ASGI 的 **GraphQL** 库。

你可以在同一个应用中将常规的 FastAPI 路径操作与 GraphQL 结合使用。

/// tip | 提示

**GraphQL** 解决一些非常特定的用例。

与常见的 **Web API** 相比，它有各自的**优点**和**缺点**。

请确保评估在你的用例中，这些**好处**是否足以弥补这些**缺点**。 🤓

///

## GraphQL 库 { #graphql-libraries }

以下是一些支持 **ASGI** 的 **GraphQL** 库。你可以将它们与 **FastAPI** 一起使用：

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * 提供 <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">面向 FastAPI 的文档</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * 提供 <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">面向 FastAPI 的文档</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * 提供用于 ASGI 集成的 <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a>
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * 可配合 <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a> 使用

## 使用 Strawberry 的 GraphQL { #graphql-with-strawberry }

如果你需要或想要使用 **GraphQL**，<a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> 是**推荐**的库，因为它的设计与 **FastAPI** 最为接近，全部基于**类型注解**。

根据你的用例，你可能会更喜欢其他库，但如果你问我，我大概率会建议你先试试 **Strawberry**。

下面是一个将 Strawberry 与 FastAPI 集成的小预览：

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

你可以在 <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry 文档</a>中了解更多信息。

还有关于 <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">将 Strawberry 与 FastAPI 结合使用</a>的文档。

## Starlette 中较早的 `GraphQLApp` { #older-graphqlapp-from-starlette }

早期版本的 Starlette 包含一个 `GraphQLApp` 类，用于与 <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a> 集成。

它已在 Starlette 中被弃用，但如果你的代码使用了它，你可以轻松**迁移**到 <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>，它覆盖相同的用例，且接口**几乎完全一致**。

/// tip | 提示

如果你需要 GraphQL，我仍然建议看看 <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>，因为它基于类型注解而不是自定义类和类型。

///

## 了解更多 { #learn-more }

你可以在 <a href="https://graphql.org/" class="external-link" target="_blank">GraphQL 官方文档</a>中了解更多关于 **GraphQL** 的内容。

你也可以通过上面的链接阅读各个库的更多信息。
