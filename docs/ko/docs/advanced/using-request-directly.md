# `Request` 직접 사용하기

지금까지 요청에서 필요한 부분을 각 타입으로 선언하여 사용해 왔습니다.

다음과 같은 곳에서 데이터를 가져왔습니다:

* 경로의 파라미터로부터.
* 헤더.
* 쿠키.
* 기타 등등.

이렇게 함으로써, **FastAPI**는 데이터를 검증하고 변환하며, API에 대한 문서를 자동화로 생성합니다.

하지만 `Request` 객체에 직접 접근해야 하는 상황이 있을 수 있습니다.

## `Request` 객체에 대한 세부 사항

**FastAPI**는 실제로 내부에 **Starlette**을 사용하며, 그 위에 여러 도구를 덧붙인 구조입니다. 따라서 여러분이 필요할 때 Starlette의 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> 객체를 직접 사용할 수 있습니다.

`Request` 객체에서 데이터를 직접 가져오는 경우(예: 본문을 읽기)에는 FastAPI가 해당 데이터를 검증하거나 변환하지 않으며, 문서화(OpenAPI를 통한 문서 자동화(로 생성된) API 사용자 인터페이스)도 되지 않습니다.

그러나 다른 매개변수(예: Pydantic 모델을 사용한 본문)는 여전히 검증, 변환, 주석 추가 등이 이루어집니다.

하지만 특정한 경우에는 `Request` 객체에 직접 접근하는 것이 유용할 수 있습니다.

## `Request` 객체를 직접 사용하기

여러분이 클라이언트의 IP 주소/호스트 정보를 *경로 작동 함수* 내부에서 가져와야 한다고 가정해 보겠습니다.

이를 위해서는 요청에 직접 접근해야 합니다.

{* ../../docs_src/using_request_directly/tutorial001.py hl[1,7:8] *}

*경로 작동 함수* 매개변수를 `Request` 타입으로 선언하면 **FastAPI**가 해당 매개변수에 `Request` 객체를 전달하는 것을 알게 됩니다.

/// tip | 팁

이 경우, 요청 매개변수와 함께 경로 매개변수를 선언한 것을 볼 수 있습니다.

따라서, 경로 매개변수는 추출되고 검증되며 지정된 타입으로 변환되고 OpenAPI로 주석이 추가됩니다.

이와 같은 방식으로, 다른 매개변수들을 평소처럼 선언하면서, 부가적으로 `Request`도 가져올 수 있습니다.

///

## `Request` 설명서

여러분은 `Request` 객체에 대한 더 자세한 내용을 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">공식 Starlette 설명서 사이트</a>에서 읽어볼 수 있습니다.

/// note | 기술 세부사항

`from starlette.requests import Request`를 사용할 수도 있습니다.

**FastAPI**는 여러분(개발자)를 위한 편의를 위해 이를 직접 제공하지만, 실제로는 Starlette에서 가져온 것입니다.

///
