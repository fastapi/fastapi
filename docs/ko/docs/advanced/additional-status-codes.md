# 추가 상태 코드

기본적으로 **FastAPI**는 `JSONResponse`를 사용하여 응답을 반환하고, *path operation*에서 반환한 내용을 해당 `JSONResponse`에 대입합니다.

기본 상태 코드나 여러분이 *path operation*에서 설정한 상태 코드를 사용합니다.

## 추가 상태 코드

여러분이 만약 기본 상태 코드 이외의 추가 상태 코드를 반환하시려면 `JSONResponse`와 같이 `Response`를 직접 반환하시고 추가 상태 코드를 직접 설정하시면 됩니다.

예를 들어 여러분이 아이템 업데이트를 허용하고 성공할 경우 HTTP 상태 코드 200 "OK"를 반환하는 *path operation*을 원한다고 가정해 보겠습니다.

그러나 여러분은 새로운 아이템 수락도 원합니다. 아이템이 이미 존재하지 않은 경우 아이템을 생성하고 HTTP 상태 코드 201 "Created"를 반환합니다.

이를 달성하기 위해 `JSONResponse`를 임포트하고 원하는 `status_code`를 설정하여 콘텐츠를 직접 반환합니다:

=== "Python 3.10+"

    ```Python hl_lines="4  25"
    {!> ../../../docs_src/additional_status_codes/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="4  25"
    {!> ../../../docs_src/additional_status_codes/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4  26"
    {!> ../../../docs_src/additional_status_codes/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip "팁"
        가능하다면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="2  23"
    {!> ../../../docs_src/additional_status_codes/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "팁"
        가능하다면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="4  25"
    {!> ../../../docs_src/additional_status_codes/tutorial001.py!}
    ```

!!! warning "주의"
    위 예시처럼 `Response`를 직접 반환하면 바로 반환됩니다.

    모델 등으로 직렬화되지 않습니다.

    여러분이 원하시는 테이터가 내장되어 있고 유효한 JSON 값인지 확인하십시오 (`JSONResponse`를 사용하는 경우).

!!! note "기술적 세부 사항"
    `from starlette.responses import JSONResponse` 사용도 가능합니다.

    **FastAPI**는 개발자의 편의를 위해 `fastapi.responses`와 동일한 `starlette.responses`를 제공합니다. 그러나 사용할 수 있는 응답의 대부분은 Starlette에서 직접 제공됩니다. `status`도 마찬가지입니다.

## OpenAPI와 API 문서

만약 여러분이 추가 상태 코드와 응답을 직접 반환하신다면 FastAPI는 반환되는 항목을 미리 알 수 없기 때문에 OpenAPI 스키마(API 문서)에 포함되지 않습니다.

그렇지만 다음을 상용하여 코드에 문서화하실 수 있습니다: [추가 응답](additional-responses.md){.internal-link target=_blank}.