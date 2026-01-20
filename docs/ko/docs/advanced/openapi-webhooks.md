# OpenAPI Webhooks { #openapi-webhooks }

앱이 어떤 데이터와 함께 (요청을 보내서) *사용자의* 앱을 호출할 수 있고, 보통 어떤 **이벤트**를 **알리기** 위해 그렇게 할 수 있다는 것을 API **사용자**에게 알려야 하는 경우가 있습니다.

이는 사용자가 여러분의 API로 요청을 보내는 일반적인 과정 대신, **여러분의 API**(또는 앱)가 **사용자의 시스템**(사용자의 API, 사용자의 앱)으로 **요청을 보낼 수 있다**는 의미입니다.

이를 보통 **webhook**이라고 합니다.

## Webhooks 단계 { #webhooks-steps }

일반적인 과정은, 여러분이 코드에서 보낼 메시지, 즉 **요청 본문(body)**이 무엇인지 **정의**하는 것입니다.

또한 여러분의 앱이 어떤 **시점**에 그 요청(또는 이벤트)을 보낼지도 어떤 방식으로든 정의합니다.

그리고 **사용자**는 (예: 어딘가의 웹 대시보드에서) 여러분의 앱이 그 요청을 보내야 할 **URL**을 어떤 방식으로든 정의합니다.

webhook의 URL을 등록하는 방법과 실제로 그 요청을 보내는 코드에 대한 모든 **로직**은 여러분에게 달려 있습니다. **여러분의 코드**에서 원하는 방식으로 작성하면 됩니다.

## **FastAPI**와 OpenAPI로 webhooks 문서화하기 { #documenting-webhooks-with-fastapi-and-openapi }

**FastAPI**에서는 OpenAPI를 사용해, 이러한 webhook의 이름, 여러분의 앱이 보낼 수 있는 HTTP 작업 타입(예: `POST`, `PUT` 등), 그리고 여러분의 앱이 보낼 요청 **본문(body)**을 정의할 수 있습니다.

이렇게 하면 사용자가 여러분의 **webhook** 요청을 받기 위해 **자신들의 API를 구현**하기가 훨씬 쉬워지고, 경우에 따라서는 자신의 API 코드 일부를 자동 생성할 수도 있습니다.

/// info | 정보

Webhooks는 OpenAPI 3.1.0 이상에서 사용할 수 있으며, FastAPI `0.99.0` 이상에서 지원됩니다.

///

## webhooks가 있는 앱 { #an-app-with-webhooks }

**FastAPI** 애플리케이션을 만들면, *경로 처리*를 정의하는 것과 같은 방식으로(예: `@app.webhooks.post()`), *webhooks*를 정의하는 데 사용할 수 있는 `webhooks` 속성이 있습니다.

{* ../../docs_src/openapi_webhooks/tutorial001_py39.py hl[9:13,36:53] *}

여러분이 정의한 webhook은 **OpenAPI** 스키마와 자동 **docs UI**에 포함됩니다.

/// info | 정보

`app.webhooks` 객체는 실제로 `APIRouter`일 뿐이며, 여러 파일로 앱을 구조화할 때 사용하는 것과 동일한 타입입니다.

///

webhook에서는 실제로(`/items/` 같은) *경로(path)*를 선언하지 않는다는 점에 유의하세요. 그곳에 전달하는 텍스트는 webhook의 **식별자**(이벤트 이름)일 뿐입니다. 예를 들어 `@app.webhooks.post("new-subscription")`에서 webhook 이름은 `new-subscription`입니다.

이는 **사용자**가 webhook 요청을 받고 싶은 실제 **URL 경로**를 다른 방식(예: 웹 대시보드)으로 정의할 것이라고 기대하기 때문입니다.

### 문서 확인하기 { #check-the-docs }

이제 앱을 실행하고 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>로 이동하세요.

문서에 일반적인 *경로 처리*가 보이고, 이제는 일부 **webhooks**도 함께 보일 것입니다:

<img src="/img/tutorial/openapi-webhooks/image01.png">
