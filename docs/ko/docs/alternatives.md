# 대안, 영감, 비교 { #alternatives-inspiration-and-comparisons }

**FastAPI**에 영감을 준 것들, 대안과의 비교, 그리고 그로부터 무엇을 배웠는지에 대한 내용입니다.

## 소개 { #intro }

다른 사람들의 이전 작업이 없었다면 **FastAPI**는 존재하지 않았을 것입니다.

그 전에 만들어진 많은 도구들이 **FastAPI**의 탄생에 영감을 주었습니다.

저는 여러 해 동안 새로운 framework를 만드는 것을 피하고 있었습니다. 먼저 **FastAPI**가 다루는 모든 기능을 여러 서로 다른 framework, plug-in, 도구를 사용해 해결해 보려고 했습니다.

하지만 어느 시점에는, 이전 도구들의 가장 좋은 아이디어를 가져와 가능한 최선의 방식으로 조합하고, 이전에는 존재하지 않았던 언어 기능(Python 3.6+ type hints)을 활용해 이 모든 기능을 제공하는 무언가를 만드는 것 외에는 다른 선택지가 없었습니다.

## 이전 도구들 { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

가장 인기 있는 Python framework이며 널리 신뢰받고 있습니다. Instagram 같은 시스템을 만드는 데 사용됩니다.

상대적으로 관계형 데이터베이스(예: MySQL 또는 PostgreSQL)와 강하게 결합되어 있어서, NoSQL 데이터베이스(예: Couchbase, MongoDB, Cassandra 등)를 주 저장 엔진으로 사용하는 것은 그리 쉽지 않습니다.

백엔드에서 HTML을 생성하기 위해 만들어졌지, 현대적인 프런트엔드(예: React, Vue.js, Angular)나 다른 시스템(예: <abbr title="Internet of Things - 사물 인터넷">IoT</abbr> 기기)에서 사용되는 API를 만들기 위해 설계된 것은 아닙니다.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Django REST framework는 Django를 기반으로 Web API를 구축하기 위한 유연한 toolkit으로 만들어졌고, Django의 API 기능을 개선하기 위한 목적이었습니다.

Mozilla, Red Hat, Eventbrite를 포함해 많은 회사에서 사용합니다.

**자동 API 문서화**의 초기 사례 중 하나였고, 이것이 특히 **FastAPI**를 "찾게 된" 첫 아이디어 중 하나였습니다.

/// note | 참고

Django REST Framework는 Tom Christie가 만들었습니다. **FastAPI**의 기반이 되는 Starlette와 Uvicorn을 만든 사람과 동일합니다.

///

/// check | **FastAPI**에 영감을 준 것

자동 API 문서화 웹 사용자 인터페이스를 제공하기.

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask는 "microframework"로, Django에 기본으로 포함된 데이터베이스 통합이나 여러 기능들을 포함하지 않습니다.

이 단순함과 유연성 덕분에 NoSQL 데이터베이스를 주 데이터 저장 시스템으로 사용하는 같은 작업이 가능합니다.

매우 단순하기 때문에 비교적 직관적으로 배울 수 있지만, 문서가 어떤 지점에서는 다소 기술적으로 깊어지기도 합니다.

또한 데이터베이스, 사용자 관리, 혹은 Django에 미리 구축되어 있는 다양한 기능들이 꼭 필요하지 않은 다른 애플리케이션에도 흔히 사용됩니다. 물론 이런 기능들 중 다수는 plug-in으로 추가할 수 있습니다.

이런 구성요소의 분리와, 필요한 것만 정확히 덧붙여 확장할 수 있는 "microframework"라는 점은 제가 유지하고 싶었던 핵심 특성이었습니다.

Flask의 단순함을 고려하면 API를 구축하는 데 잘 맞는 것처럼 보였습니다. 다음으로 찾고자 했던 것은 Flask용 "Django REST Framework"였습니다.

/// check | **FastAPI**에 영감을 준 것

micro-framework가 되기. 필요한 도구와 구성요소를 쉽게 조합할 수 있도록 하기.

단순하고 사용하기 쉬운 routing 시스템을 갖기.

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI**는 실제로 **Requests**의 대안이 아닙니다. 둘의 범위는 매우 다릅니다.

실제로 FastAPI 애플리케이션 *내부에서* Requests를 사용하는 경우도 흔합니다.

그럼에도 FastAPI는 Requests로부터 꽤 많은 영감을 얻었습니다.

**Requests**는 (클라이언트로서) API와 *상호작용*하기 위한 라이브러리이고, **FastAPI**는 (서버로서) API를 *구축*하기 위한 라이브러리입니다.

대략 말하면 서로 반대편에 있으며, 서로를 보완합니다.

Requests는 매우 단순하고 직관적인 설계를 가졌고, 합리적인 기본값을 바탕으로 사용하기가 아주 쉽습니다. 동시에 매우 강력하고 커스터마이징도 가능합니다.

그래서 공식 웹사이트에서 말하듯이:

> Requests is one of the most downloaded Python packages of all time

사용 방법은 매우 간단합니다. 예를 들어 `GET` 요청을 하려면 다음처럼 작성합니다:

```Python
response = requests.get("http://example.com/some/url")
```

이에 대응하는 FastAPI의 API *경로 처리*는 다음과 같이 보일 수 있습니다:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)`와 `@app.get(...)`의 유사성을 확인해 보세요.

/// check | **FastAPI**에 영감을 준 것

* 단순하고 직관적인 API를 갖기.
* HTTP method 이름(operations)을 직접, 직관적이고 명확한 방식으로 사용하기.
* 합리적인 기본값을 제공하되, 강력한 커스터마이징을 가능하게 하기.

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

제가 Django REST Framework에서 가장 원했던 주요 기능은 자동 API 문서화였습니다.

그 후 JSON(또는 JSON의 확장인 YAML)을 사용해 API를 문서화하는 표준인 Swagger가 있다는 것을 알게 되었습니다.

그리고 Swagger API를 위한 웹 사용자 인터페이스도 이미 만들어져 있었습니다. 그래서 API에 대한 Swagger 문서를 생성할 수 있다면, 이 웹 사용자 인터페이스를 자동으로 사용할 수 있게 됩니다.

어느 시점에 Swagger는 Linux Foundation으로 넘어가 OpenAPI로 이름이 바뀌었습니다.

그래서 2.0 버전을 이야기할 때는 "Swagger"라고 말하는 것이 일반적이고, 3+ 버전은 "OpenAPI"라고 말하는 것이 일반적입니다.

/// check | **FastAPI**에 영감을 준 것

커스텀 schema 대신, API 사양을 위한 열린 표준을 채택하고 사용하기.

또한 표준 기반의 사용자 인터페이스 도구를 통합하기:

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

이 두 가지는 꽤 대중적이고 안정적이기 때문에 선택되었습니다. 하지만 간단히 검색해보면 OpenAPI를 위한 대안 UI가 수십 가지나 있다는 것을 알 수 있습니다(**FastAPI**와 함께 사용할 수 있습니다).

///

### Flask REST framework들 { #flask-rest-frameworks }

Flask REST framework는 여러 개가 있지만, 시간을 들여 조사해 본 결과, 상당수가 중단되었거나 방치되어 있었고, 해결되지 않은 여러 이슈 때문에 적합하지 않은 경우가 많았습니다.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

API 시스템에 필요한 주요 기능 중 하나는 데이터 "<abbr title="also called marshalling, conversion - 마샬링, 변환이라고도 합니다">serialization</abbr>"입니다. 이는 코드(Python)에서 데이터를 가져와 네트워크로 전송할 수 있는 형태로 변환하는 것을 의미합니다. 예를 들어 데이터베이스의 데이터를 담은 객체를 JSON 객체로 변환하거나, `datetime` 객체를 문자열로 변환하는 등의 작업입니다.

API에 또 하나 크게 필요한 기능은 데이터 검증입니다. 특정 파라미터를 기준으로 데이터가 유효한지 확인하는 것입니다. 예를 들어 어떤 필드가 `int`인지, 임의의 문자열이 아닌지 확인하는 식입니다. 이는 특히 들어오는 데이터에 유용합니다.

데이터 검증 시스템이 없다면, 모든 검사를 코드에서 수동으로 해야 합니다.

이런 기능들을 제공하기 위해 Marshmallow가 만들어졌습니다. 훌륭한 라이브러리이며, 저도 이전에 많이 사용했습니다.

하지만 Python type hints가 존재하기 전에 만들어졌습니다. 그래서 각 <abbr title="the definition of how data should be formed - 데이터가 어떻게 구성되어야 하는지에 대한 정의">schema</abbr>를 정의하려면 Marshmallow가 제공하는 특정 유틸리티와 클래스를 사용해야 합니다.

/// check | **FastAPI**에 영감을 준 것

데이터 타입과 검증을 제공하는 "schema"를 코드로 정의하고, 이를 자동으로 활용하기.

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

API에 필요한 또 다른 큰 기능은 들어오는 요청에서 데이터를 <abbr title="reading and converting to Python data - 읽어서 Python 데이터로 변환하기">parsing</abbr>하는 것입니다.

Webargs는 Flask를 포함한 여러 framework 위에서 이를 제공하기 위해 만들어진 도구입니다.

내부적으로 Marshmallow를 사용해 데이터 검증을 수행합니다. 그리고 같은 개발자들이 만들었습니다.

아주 훌륭한 도구이며, 저도 **FastAPI**를 만들기 전에 많이 사용했습니다.

/// info | 정보

Webargs는 Marshmallow와 같은 개발자들이 만들었습니다.

///

/// check | **FastAPI**에 영감을 준 것

들어오는 요청 데이터의 자동 검증을 갖기.

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow와 Webargs는 plug-in 형태로 검증, parsing, serialization을 제공합니다.

하지만 문서화는 여전히 부족했습니다. 그래서 APISpec이 만들어졌습니다.

이는 여러 framework를 위한 plug-in이며(Starlette용 plug-in도 있습니다).

작동 방식은, 각 route를 처리하는 함수의 docstring 안에 YAML 형식으로 schema 정의를 작성하고,

그로부터 OpenAPI schema를 생성합니다.

Flask, Starlette, Responder 등에서 이런 방식으로 동작합니다.

하지만 다시, Python 문자열 내부(큰 YAML)에서 micro-syntax를 다루어야 한다는 문제가 있습니다.

에디터가 이를 크게 도와주지 못합니다. 또한 파라미터나 Marshmallow schema를 수정해놓고 YAML docstring도 같이 수정하는 것을 잊어버리면, 생성된 schema는 오래된 상태가 됩니다.

/// info | 정보

APISpec은 Marshmallow와 같은 개발자들이 만들었습니다.

///

/// check | **FastAPI**에 영감을 준 것

API를 위한 열린 표준인 OpenAPI를 지원하기.

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

Flask plug-in으로, Webargs, Marshmallow, APISpec을 묶어줍니다.

Webargs와 Marshmallow의 정보를 사용해 APISpec으로 OpenAPI schema를 자동 생성합니다.

훌륭한 도구인데도 과소평가되어 있습니다. 다른 많은 Flask plug-in보다 훨씬 더 유명해져야 합니다. 문서가 너무 간결하고 추상적이라서 그럴 수도 있습니다.

이 도구는 Python docstring 내부에 YAML(또 다른 문법)을 작성해야 하는 문제를 해결했습니다.

Flask + Flask-apispec + Marshmallow + Webargs 조합은 **FastAPI**를 만들기 전까지 제가 가장 좋아하던 백엔드 stack이었습니다.

이를 사용하면서 여러 Flask full-stack generator가 만들어졌습니다. 이것들이 지금까지 저(그리고 여러 외부 팀)가 사용해 온 주요 stack입니다:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

그리고 이 동일한 full-stack generator들이 [**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank}의 기반이 되었습니다.

/// info | 정보

Flask-apispec은 Marshmallow와 같은 개발자들이 만들었습니다.

///

/// check | **FastAPI**에 영감을 준 것

serialization과 validation을 정의하는 동일한 코드로부터 OpenAPI schema를 자동 생성하기.

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (그리고 <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>) { #nestjs-and-angular }

이건 Python도 아닙니다. NestJS는 Angular에서 영감을 받은 JavaScript(TypeScript) NodeJS framework입니다.

Flask-apispec으로 할 수 있는 것과 어느 정도 비슷한 것을 달성합니다.

Angular 2에서 영감을 받은 의존성 주입 시스템이 통합되어 있습니다. 제가 아는 다른 의존성 주입 시스템들처럼 "injectable"을 사전에 등록해야 하므로, 장황함과 코드 반복이 늘어납니다.

파라미터가 TypeScript 타입(Python type hints와 유사함)으로 설명되기 때문에 에디터 지원은 꽤 좋습니다.

하지만 TypeScript 데이터는 JavaScript로 컴파일된 뒤에는 보존되지 않기 때문에, 타입에 의존해 검증, serialization, 문서화를 동시에 정의할 수 없습니다. 이 점과 일부 설계 결정 때문에, 검증/serialization/자동 schema 생성을 하려면 여러 곳에 decorator를 추가해야 하며, 결과적으로 매우 장황해집니다.

중첩 모델을 잘 처리하지 못합니다. 즉, 요청의 JSON body가 내부 필드를 가진 JSON 객체이고 그 내부 필드들이 다시 중첩된 JSON 객체인 경우, 제대로 문서화하고 검증할 수 없습니다.

/// check | **FastAPI**에 영감을 준 것

Python 타입을 사용해 뛰어난 에디터 지원을 제공하기.

강력한 의존성 주입 시스템을 갖추기. 코드 반복을 최소화하는 방법을 찾기.

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

`asyncio` 기반의 매우 빠른 Python framework 중 초기 사례였습니다. Flask와 매우 유사하게 만들어졌습니다.

/// note | 기술 세부사항

기본 Python `asyncio` 루프 대신 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a>를 사용했습니다. 이것이 매우 빠르게 만든 요인입니다.

이는 Uvicorn과 Starlette에 명확히 영감을 주었고, 현재 공개 benchmark에서는 이 둘이 Sanic보다 더 빠릅니다.

///

/// check | **FastAPI**에 영감을 준 것

미친 성능을 낼 수 있는 방법을 찾기.

그래서 **FastAPI**는 Starlette를 기반으로 합니다. Starlette는 사용 가능한 framework 중 가장 빠르기 때문입니다(서드파티 benchmark로 테스트됨).

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon은 또 다른 고성능 Python framework로, 최소한으로 설계되었고 Hug 같은 다른 framework의 기반으로 동작하도록 만들어졌습니다.

함수가 두 개의 파라미터(하나는 "request", 하나는 "response")를 받도록 설계되어 있습니다. 그런 다음 request에서 일부를 "읽고", response에 일부를 "작성"합니다. 이 설계 때문에, 표준 Python type hints를 함수 파라미터로 사용해 요청 파라미터와 body를 선언하는 것이 불가능합니다.

따라서 데이터 검증, serialization, 문서화는 자동으로 되지 않고 코드로 해야 합니다. 또는 Hug처럼 Falcon 위에 framework를 얹어 구현해야 합니다. request 객체 하나와 response 객체 하나를 파라미터로 받는 Falcon의 설계에서 영감을 받은 다른 framework에서도 같은 구분이 나타납니다.

/// check | **FastAPI**에 영감을 준 것

훌륭한 성능을 얻는 방법을 찾기.

Hug(= Falcon 기반)과 함께, 함수에서 `response` 파라미터를 선언하도록 **FastAPI**에 영감을 주었습니다.

다만 FastAPI에서는 선택 사항이며, 주로 헤더, 쿠키, 그리고 대체 status code를 설정하는 데 사용됩니다.

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

**FastAPI**를 만들기 시작한 초기 단계에서 Molten을 알게 되었고, 꽤 비슷한 아이디어를 갖고 있었습니다:

* Python type hints 기반
* 이 타입으로부터 검증과 문서화 생성
* 의존성 주입 시스템

Pydantic 같은 서드파티 라이브러리를 사용해 데이터 검증/serialization/문서화를 하지 않고 자체 구현을 사용합니다. 그래서 이런 데이터 타입 정의를 쉽게 재사용하기는 어렵습니다.

조금 더 장황한 설정이 필요합니다. 또한 WSGI(ASGI가 아니라) 기반이므로, Uvicorn, Starlette, Sanic 같은 도구가 제공하는 고성능을 활용하도록 설계되지 않았습니다.

의존성 주입 시스템은 의존성을 사전에 등록해야 하고, 선언된 타입을 기반으로 의존성을 해결합니다. 따라서 특정 타입을 제공하는 "component"를 두 개 이상 선언할 수 없습니다.

Route는 한 곳에서 선언하고, 다른 곳에 선언된 함수를 사용합니다(엔드포인트를 처리하는 함수 바로 위에 둘 수 있는 decorator를 사용하는 대신). 이는 Flask(및 Starlette)보다는 Django 방식에 가깝습니다. 코드에서 상대적으로 강하게 결합된 것들을 분리해 놓습니다.

/// check | **FastAPI**에 영감을 준 것

모델 속성의 "default" 값으로 데이터 타입에 대한 추가 검증을 정의하기. 이는 에디터 지원을 개선하며, 이전에는 Pydantic에 없었습니다.

이것은 실제로 Pydantic의 일부를 업데이트하여 같은 검증 선언 스타일을 지원하도록 하는 데 영감을 주었습니다(이 기능은 이제 Pydantic에 이미 포함되어 있습니다).

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug는 Python type hints를 사용해 API 파라미터 타입을 선언하는 기능을 구현한 초기 framework 중 하나였습니다. 이는 다른 도구들도 같은 방식을 하도록 영감을 준 훌륭한 아이디어였습니다.

표준 Python 타입 대신 커스텀 타입을 선언에 사용했지만, 여전히 큰 진전이었습니다.

또한 전체 API를 JSON으로 선언하는 커스텀 schema를 생성한 초기 framework 중 하나였습니다.

OpenAPI나 JSON Schema 같은 표준을 기반으로 하지 않았기 때문에 Swagger UI 같은 다른 도구와 통합하는 것은 직관적이지 않았습니다. 하지만 역시 매우 혁신적인 아이디어였습니다.

흥미롭고 흔치 않은 기능이 하나 있습니다. 같은 framework로 API뿐 아니라 CLI도 만들 수 있습니다.

동기식 Python 웹 framework의 이전 표준(WSGI) 기반이어서 Websockets와 다른 것들을 처리할 수는 없지만, 성능은 여전히 높습니다.

/// info | 정보

Hug는 Timothy Crosley가 만들었습니다. Python 파일에서 import를 자동으로 정렬하는 훌륭한 도구인 <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>의 제작자이기도 합니다.

///

/// check | **FastAPI**에 영감을 준 아이디어들

Hug는 APIStar의 일부에 영감을 주었고, 저는 APIStar와 함께 Hug를 가장 유망한 도구 중 하나로 보았습니다.

Hug는 Python type hints로 파라미터를 선언하고, API를 정의하는 schema를 자동으로 생성하도록 **FastAPI**에 영감을 주었습니다.

Hug는 헤더와 쿠키를 설정하기 위해 함수에 `response` 파라미터를 선언하도록 **FastAPI**에 영감을 주었습니다.

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5) { #apistar-0-5 }

**FastAPI**를 만들기로 결정하기 직전에 **APIStar** 서버를 발견했습니다. 찾고 있던 거의 모든 것을 갖추고 있었고 설계도 훌륭했습니다.

NestJS와 Molten보다 앞서, Python type hints를 사용해 파라미터와 요청을 선언하는 framework 구현을 제가 처음 본 사례들 중 하나였습니다. Hug와 거의 같은 시기에 발견했습니다. 하지만 APIStar는 OpenAPI 표준을 사용했습니다.

여러 위치에서 동일한 type hints를 기반으로 자동 데이터 검증, 데이터 serialization, OpenAPI schema 생성을 제공했습니다.

Body schema 정의는 Pydantic처럼 동일한 Python type hints를 사용하지는 않았고 Marshmallow와 조금 더 비슷해서 에디터 지원은 그만큼 좋지 않았지만, 그래도 APIStar는 당시 사용할 수 있는 최선의 선택지였습니다.

당시 최고의 성능 benchmark를 가졌습니다(Starlette에 의해서만 추월됨).

처음에는 자동 API 문서화 웹 UI가 없었지만, Swagger UI를 추가할 수 있다는 것을 알고 있었습니다.

의존성 주입 시스템도 있었습니다. 위에서 언급한 다른 도구들처럼 component의 사전 등록이 필요했지만, 여전히 훌륭한 기능이었습니다.

보안 통합이 없어서 전체 프로젝트에서 사용해 볼 수는 없었습니다. 그래서 Flask-apispec 기반 full-stack generator로 갖추고 있던 모든 기능을 대체할 수 없었습니다. 그 기능을 추가하는 pull request를 만드는 것이 제 백로그에 있었습니다.

하지만 이후 프로젝트의 초점이 바뀌었습니다.

더 이상 API web framework가 아니게 되었는데, 제작자가 Starlette에 집중해야 했기 때문입니다.

이제 APIStar는 web framework가 아니라 OpenAPI 사양을 검증하기 위한 도구 모음입니다.

/// info | 정보

APIStar는 Tom Christie가 만들었습니다. 다음을 만든 사람과 동일합니다:

* Django REST Framework
* Starlette(**FastAPI**의 기반)
* Uvicorn(Starlette와 **FastAPI**에서 사용)

///

/// check | **FastAPI**에 영감을 준 것

존재하게 만들기.

동일한 Python 타입으로 여러 가지(데이터 검증, serialization, 문서화)를 선언하면서 동시에 뛰어난 에디터 지원을 제공한다는 아이디어는 제가 매우 훌륭하다고 생각했습니다.

그리고 오랫동안 비슷한 framework를 찾아 여러 대안을 테스트한 끝에, APIStar가 그때 이용 가능한 최선의 선택지였습니다.

그 후 APIStar 서버가 더는 존재하지 않게 되고 Starlette가 만들어졌는데, 이는 그런 시스템을 위한 더 새롭고 더 나은 기반이었습니다. 이것이 **FastAPI**를 만들게 된 최종 영감이었습니다.

저는 **FastAPI**를 APIStar의 "정신적 후계자"로 생각합니다. 동시에, 이 모든 이전 도구들에서 배운 것들을 바탕으로 기능, typing 시스템, 그리고 다른 부분들을 개선하고 확장했습니다.

///

## **FastAPI**가 사용하는 것 { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic은 Python type hints를 기반으로 데이터 검증, serialization, 문서화(JSON Schema 사용)를 정의하는 라이브러리입니다.

그 덕분에 매우 직관적입니다.

Marshmallow와 비교할 수 있습니다. 다만 benchmark에서 Marshmallow보다 빠릅니다. 그리고 동일한 Python type hints를 기반으로 하므로 에디터 지원도 훌륭합니다.

/// check | **FastAPI**가 이를 사용하는 목적

모든 데이터 검증, 데이터 serialization, 자동 모델 문서화(JSON Schema 기반)를 처리하기.

그 다음 **FastAPI**는 그 JSON Schema 데이터를 가져와 OpenAPI에 포함시키며, 그 외에도 여러 작업을 수행합니다.

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette는 경량 <abbr title="The new standard for building asynchronous Python web applications - 비동기 Python 웹 애플리케이션을 구축하기 위한 새로운 표준">ASGI</abbr> framework/toolkit으로, 고성능 asyncio 서비스를 만들기에 이상적입니다.

매우 단순하고 직관적입니다. 쉽게 확장할 수 있도록 설계되었고, 모듈식 component를 갖습니다.

다음이 포함됩니다:

* 정말 인상적인 성능.
* WebSocket 지원.
* 프로세스 내 백그라운드 작업.
* 시작 및 종료 이벤트.
* HTTPX 기반의 테스트 클라이언트.
* CORS, GZip, Static Files, Streaming responses.
* 세션 및 쿠키 지원.
* 100% 테스트 커버리지.
* 100% 타입 주석이 달린 코드베이스.
* 소수의 필수 의존성.

Starlette는 현재 테스트된 Python framework 중 가장 빠릅니다. 단, framework가 아니라 서버인 Uvicorn이 더 빠릅니다.

Starlette는 웹 microframework의 기본 기능을 모두 제공합니다.

하지만 자동 데이터 검증, serialization, 문서화는 제공하지 않습니다.

그것이 **FastAPI**가 위에 추가하는 핵심 중 하나이며, 모두 Python type hints(Pydantic 사용)를 기반으로 합니다. 여기에 더해 의존성 주입 시스템, 보안 유틸리티, OpenAPI schema 생성 등도 포함됩니다.

/// note | 기술 세부사항

ASGI는 Django 코어 팀 멤버들이 개발 중인 새로운 "표준"입니다. 아직 "Python 표준"(PEP)은 아니지만, 그 방향으로 진행 중입니다.

그럼에도 이미 여러 도구에서 "표준"으로 사용되고 있습니다. 이는 상호운용성을 크게 개선합니다. 예를 들어 Uvicorn을 다른 ASGI 서버(예: Daphne 또는 Hypercorn)로 교체할 수도 있고, `python-socketio` 같은 ASGI 호환 도구를 추가할 수도 있습니다.

///

/// check | **FastAPI**가 이를 사용하는 목적

핵심 웹 부분을 모두 처리하기. 그 위에 기능을 추가하기.

`FastAPI` 클래스 자체는 `Starlette` 클래스를 직접 상속합니다.

따라서 Starlette로 할 수 있는 모든 것은 기본적으로 **FastAPI**로도 직접 할 수 있습니다. 즉, **FastAPI**는 사실상 Starlette에 강력한 기능을 더한 것입니다.

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn은 uvloop과 httptools로 구축된 초고속 ASGI 서버입니다.

web framework가 아니라 서버입니다. 예를 들어 경로 기반 routing을 위한 도구는 제공하지 않습니다. 그런 것은 Starlette(또는 **FastAPI**) 같은 framework가 위에서 제공합니다.

Starlette와 **FastAPI**에서 권장하는 서버입니다.

/// check | **FastAPI**가 이를 권장하는 방식

**FastAPI** 애플리케이션을 실행하기 위한 주요 웹 서버.

또한 `--workers` 커맨드라인 옵션을 사용하면 비동기 멀티프로세스 서버로 실행할 수도 있습니다.

자세한 내용은 [배포](deployment/index.md){.internal-link target=_blank} 섹션을 확인하세요.

///

## 벤치마크와 속도 { #benchmarks-and-speed }

Uvicorn, Starlette, FastAPI 사이의 차이를 이해하고 비교하려면 [벤치마크](benchmarks.md){.internal-link target=_blank} 섹션을 확인하세요.
