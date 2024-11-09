# 조건부적인 OpenAPI

필요한 경우, 설정 및 환경 변수를 사용하여 환경에 따라 조건부로 OpenAPI를 구성하고 완전히 비활성화할 수도 있습니다.

## 보안, API 및 docs에 대해서

프로덕션에서, 문서화된 사용자 인터페이스(UI)를 숨기는 것이 API를 보호하는 방법이 *되어서는 안 됩니다*.

이는 API에 추가적인 보안을 제공하지 않으며, *경로 작업*은 여전히 동일한 위치에서 사용 할 수 있습니다.

코드에 보안 결함이 있다면, 그 결함은 여전히 존재할 것입니다.

문서를 숨기는 것은 API와 상호작용하는 방법을 이해하기 어렵게 만들며, 프로덕션에서 디버깅을 더 어렵게 만들 수 있습니다. 이는 단순히 <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">'모호성에 의한 보안'</a>의 한 형태로 간주될 수 있습니다.

API를 보호하고 싶다면, 예를 들어 다음과 같은 더 나은 방법들이 있습니다:

* 요청 본문과 응답에 대해 잘 정의된 Pydantic 모델을 사용하도록 하세요.

* 종속성을 사용하여 필요한 권한과 역할을 구성하세요.

* 평문 비밀번호를 절대 저장하지 말고, 오직 암호화된 비밀번호만 저장하세요.

* Passlib과 JWT 토큰과 같은 잘 알려진 암호화 도구들을 구현하고 사용하세요.

* 필요한 곳에 OAuth2 범위를 사용하여 더 세분화된 권한 제어를 추가하세요.

* 등등....

그럼에도 불구하고, 특정 환경(예: 프로덕션)에서 또는 환경 변수의 설정에 따라 API 문서를 비활성화해야 하는 매우 특정한 사용 사례가 있을 수 있습니다.

## 설정 및 환경변수의 조건부 OpenAPI

동일한 Pydantic 설정을 사용하여 생성된 OpenAPI 및 문서 UI를 쉽게 구성할 수 있습니다.

예를 들어:

{* ../../docs_src/conditional_openapi/tutorial001.py hl[6,11] *}

여기서 `openapi_url` 설정을 기본값인 `"/openapi.json"`으로 선언합니다.

그런 뒤, 우리는 `FastAPI` 앱을 만들 때 그것을 사용합니다.

환경 변수 `OPENAPI_URL`을 빈 문자열로 설정하여 OpenAPI(문서 UI 포함)를 비활성화할 수도 있습니다. 예를 들어:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그리고 `/openapi.json`, `/docs` 또는 `/redoc`의 URL로 이동하면 `404 Not Found`라는 오류가 다음과 같이 표시됩니다:

```JSON
{
    "detail": "Not Found"
}
```
