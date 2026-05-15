# GraphQL { #graphql }

由於 FastAPI 基於 ASGI 標準，整合任何與 ASGI 相容的 GraphQL 函式庫都很容易。

你可以在同一個應用程式中同時使用一般的 FastAPI 路徑操作 (path operation) 與 GraphQL。

/// tip

GraphQL 解決某些非常特定的使用情境。

與一般的 Web API 相比，它有優點也有缺點。

請確認在你的使用情境中，這些效益是否足以彌補其限制。 🤓

///

## GraphQL 函式庫 { #graphql-libraries }

下面是支援 ASGI 的部分 GraphQL 函式庫，你可以與 FastAPI 一起使用：

* [Strawberry](https://strawberry.rocks/) 🍓
    * 提供 [FastAPI 文件](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * 提供 [FastAPI 文件](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * 使用 [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) 提供 ASGI 整合
* [Graphene](https://graphene-python.org/)
    * 搭配 [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## 使用 Strawberry 的 GraphQL { #graphql-with-strawberry }

如果你需要或想使用 GraphQL，[Strawberry](https://strawberry.rocks/) 是推薦的函式庫，因為它的設計與 FastAPI 最接近，全部都基於型別註解 (type annotations)。

視你的使用情境而定，你可能會偏好其他函式庫，但如果你問我，我大概會建議你先試試 Strawberry。

以下是如何將 Strawberry 與 FastAPI 整合的一個小例子：

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

你可以在 [Strawberry 文件](https://strawberry.rocks/) 中進一步了解 Strawberry。

也可以參考關於 [Strawberry 與 FastAPI](https://strawberry.rocks/docs/integrations/fastapi) 的文件。

## 來自 Starlette 的較舊 `GraphQLApp` { #older-graphqlapp-from-starlette }

早期版本的 Starlette 提供 `GraphQLApp` 類別以整合 [Graphene](https://graphene-python.org/)。

它已在 Starlette 中被棄用，但如果你的程式碼使用了它，可以輕鬆遷移到 [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)，涵蓋相同的使用情境，且介面幾乎相同。

/// tip

如果你需要 GraphQL，我仍建議你看看 [Strawberry](https://strawberry.rocks/)，因為它基於型別註解，而不是自訂的類別與型別。

///

## 進一步了解 { #learn-more }

你可以在 [官方 GraphQL 文件](https://graphql.org/) 中進一步了解 GraphQL。

你也可以透過上述連結閱讀各個函式庫的更多內容。
