# GraphQL { #graphql }

**FastAPI**는 **ASGI** 표준을 기반으로 하므로, ASGI와도 호환되는 어떤 **GraphQL** 라이브러리든 매우 쉽게 통합할 수 있습니다.

같은 애플리케이션에서 일반 FastAPI **경로 처리**와 GraphQL을 함께 조합할 수 있습니다.

/// tip | 팁

**GraphQL**은 몇 가지 매우 특정한 사용 사례를 해결합니다.

일반적인 **web API**와 비교했을 때 **장점**과 **단점**이 있습니다.

여러분의 사용 사례에서 **이점**이 **단점**을 상쇄하는지 꼭 평가해 보세요. 🤓

///

## GraphQL 라이브러리 { #graphql-libraries }

다음은 **ASGI** 지원이 있는 **GraphQL** 라이브러리들입니다. **FastAPI**와 함께 사용할 수 있습니다:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">FastAPI용 문서</a> 제공
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">FastAPI용 문서</a> 제공
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * ASGI 통합을 제공하기 위해 <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> 사용
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a> 사용

## Strawberry로 GraphQL 사용하기 { #graphql-with-strawberry }

**GraphQL**로 작업해야 하거나 작업하고 싶다면, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a>를 **권장**합니다. **FastAPI**의 설계와 가장 가깝고, 모든 것이 **type annotations**에 기반해 있기 때문입니다.

사용 사례에 따라 다른 라이브러리를 선호할 수도 있지만, 제게 묻는다면 아마 **Strawberry**를 먼저 시도해 보라고 제안할 것입니다.

다음은 Strawberry를 FastAPI와 통합하는 방법에 대한 간단한 미리보기입니다:

{* ../../docs_src/graphql_/tutorial001_py39.py hl[3,22,25] *}

<a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry 문서</a>에서 Strawberry에 대해 더 알아볼 수 있습니다.

또한 <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">FastAPI에서 Strawberry 사용</a>에 대한 문서도 확인해 보세요.

## Starlette의 예전 `GraphQLApp` { #older-graphqlapp-from-starlette }

이전 버전의 Starlette에는 <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>과 통합하기 위한 `GraphQLApp` 클래스가 포함되어 있었습니다.

이것은 Starlette에서 deprecated 되었지만, 이를 사용하던 코드가 있다면 같은 사용 사례를 다루고 **거의 동일한 인터페이스**를 가진 <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>로 쉽게 **마이그레이션**할 수 있습니다.

/// tip | 팁

GraphQL이 필요하다면, 커스텀 클래스와 타입 대신 type annotations에 기반한 <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>를 여전히 확인해 보시길 권장합니다.

///

## 더 알아보기 { #learn-more }

<a href="https://graphql.org/" class="external-link" target="_blank">공식 GraphQL 문서</a>에서 **GraphQL**에 대해 더 알아볼 수 있습니다.

또한 위에서 설명한 각 라이브러리에 대해서도 해당 링크에서 더 자세히 읽어볼 수 있습니다.
