# GraphQL { #graphql }

**FastAPI** は **ASGI** 標準に基づいているため、ASGI に対応した任意の **GraphQL** ライブラリを簡単に統合できます。

同じアプリケーション内で通常の FastAPI の *path operation* と GraphQL を組み合わせて使えます。

/// tip | 豆知識

**GraphQL** は非常に特定のユースケースを解決します。

一般的な **Web API** と比べると、**長所** と **短所** があります。

ご自身のユースケースで得られる **利点** が **欠点** を補うかどうかを評価してください。 🤓

///

## GraphQL ライブラリ { #graphql-libraries }

**ASGI** をサポートする **GraphQL** ライブラリの一部を以下に示します。**FastAPI** と組み合わせて使用できます:

* [Strawberry](https://strawberry.rocks/) 🍓
    * [FastAPI 向けドキュメント](https://strawberry.rocks/docs/integrations/fastapi)あり
* [Ariadne](https://ariadnegraphql.org/)
    * [FastAPI 向けドキュメント](https://ariadnegraphql.org/docs/fastapi-integration)あり
* [Tartiflette](https://tartiflette.io/)
    * ASGI 連携用の [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) あり
* [Graphene](https://graphene-python.org/)
    * [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) あり

## Strawberry で GraphQL { #graphql-with-strawberry }

**GraphQL** が必要、または利用したい場合は、[**Strawberry**](https://strawberry.rocks/) を**推奨**します。**FastAPI** の設計に最も近く、すべてが**型アノテーション**に基づいています。

ユースケースによっては他のライブラリを選ぶ方がよい場合もありますが、私に尋ねられれば、おそらく **Strawberry** を試すことを勧めるでしょう。

FastAPI と Strawberry を統合する方法の簡単なプレビューです:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

詳細は [Strawberry のドキュメント](https://strawberry.rocks/)をご覧ください。

また、[Strawberry と FastAPI](https://strawberry.rocks/docs/integrations/fastapi) の連携に関するドキュメントもあります。

## Starlette の旧 `GraphQLApp` { #older-graphqlapp-from-starlette }

以前の Starlette には、[Graphene](https://graphene-python.org/) と統合するための `GraphQLApp` クラスが含まれていました。

これは Starlette からは非推奨になりましたが、もしそれを使用しているコードがある場合は、同じユースケースをカバーし、**ほぼ同一のインターフェース**を持つ [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) へ容易に**移行**できます。

/// tip | 豆知識

GraphQL が必要であれば、依然として [Strawberry](https://strawberry.rocks/) の利用を推奨します。独自のクラスや型ではなく、型アノテーションに基づいているためです。

///

## さらに学ぶ { #learn-more }

**GraphQL** については、[公式 GraphQL ドキュメント](https://graphql.org/)でさらに学べます。

上記の各ライブラリについては、リンク先のドキュメントをご参照ください。
