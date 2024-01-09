# GraphQL

As **FastAPI** is based on the **ASGI** standard, it's very easy to integrate any **GraphQL** library also compatible with ASGI.

You can combine normal FastAPI *path operations* with GraphQL on the same application.

!!! tip
    **GraphQL** solves some very specific use cases.

    It has **advantages** and **disadvantages** when compared to common **web APIs**.

    Make sure you evaluate if the **benefits** for your use case compensate the **drawbacks**. 🤓

## GraphQL Libraries

Here are some of the **GraphQL** libraries that have **ASGI** support. You could use them with **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * With <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">docs for FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * With <a href="https://ariadnegraphql.org/docs/starlette-integration" class="external-link" target="_blank">docs for Starlette</a> (that also apply to FastAPI)
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * With <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> to provide ASGI integration
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * With <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL with Strawberry

If you need or want to work with **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> is the **recommended** library as it has the design closest to **FastAPI's** design, it's all based on **type annotations**.

Depending on your use case, you might prefer to use a different library, but if you asked me, I would probably suggest you try **Strawberry**.

Here's a small preview of how you could integrate Strawberry with FastAPI:

```Python hl_lines="3  22  25-26"
{!../../../docs_src/graphql/tutorial001.py!}
```

You can learn more about Strawberry in the <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry documentation</a>.

And also the docs about <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry with FastAPI</a>.

## Older `GraphQLApp` from Starlette

Previous versions of Starlette included a `GraphQLApp` class to integrate with <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

It was deprecated from Starlette, but if you have code that used it, you can easily **migrate** to <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, that covers the same use case and has an **almost identical interface**.

!!! tip
    If you need GraphQL, I still would recommend you check out <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, as it's based on type annotations instead of custom classes and types.

## Learn More

You can learn more about **GraphQL** in the <a href="https://graphql.org/" class="external-link" target="_blank">official GraphQL documentation</a>.

You can also read more about each those libraries described above in their links.
