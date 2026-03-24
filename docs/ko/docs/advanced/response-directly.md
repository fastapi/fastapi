# 응답을 직접 반환하기 { #return-a-response-directly }

**FastAPI**에서 *경로 처리(path operation)*를 생성할 때, 일반적으로 `dict`, `list`, Pydantic 모델, 데이터베이스 모델 등의 데이터를 반환할 수 있습니다.

[응답 모델](../tutorial/response-model.md)을 선언하면 FastAPI는 Pydantic을 사용해 데이터를 JSON으로 직렬화합니다.

응답 모델을 선언하지 않으면, FastAPI는 [JSON 호환 가능 인코더](../tutorial/encoder.md)에 설명된 `jsonable_encoder`를 사용해 데이터를 변환하고 이를 `JSONResponse`에 넣습니다.

또한 `JSONResponse`를 직접 생성해 반환할 수도 있습니다.

/// tip | 팁

일반적으로 `JSONResponse`를 직접 반환하는 것보다 [응답 모델](../tutorial/response-model.md)을 사용하는 편이 성능이 훨씬 좋습니다. 이렇게 하면 Pydantic이 Rust에서 데이터를 직렬화합니다.

///

## `Response` 반환하기 { #return-a-response }

`Response` 또는 그 하위 클래스를 반환할 수 있습니다.

/// info | 정보

`JSONResponse` 자체도 `Response`의 하위 클래스입니다.

///

그리고 `Response`를 반환하면 **FastAPI**가 이를 그대로 전달합니다.

Pydantic 모델로 데이터 변환을 수행하지 않으며, 내용을 다른 형식으로 변환하지 않습니다.

이로 인해 많은 유연성을 얻을 수 있습니다. 어떤 데이터 유형이든 반환할 수 있고, 데이터 선언이나 유효성 검사를 재정의할 수 있습니다.

또한 많은 책임도 따릅니다. 반환하는 데이터가 올바르고, 올바른 형식이며, 직렬화가 가능하도록 여러분이 직접 보장해야 합니다.

## `Response`에서 `jsonable_encoder` 사용하기 { #using-the-jsonable-encoder-in-a-response }

**FastAPI**는 반환하는 `Response`에 아무런 변경도 하지 않으므로, 그 내용이 준비되어 있는지 확인해야 합니다.

예를 들어, Pydantic 모델을 먼저 `dict`로 변환하고 `datetime`, `UUID` 등의 모든 데이터 타입을 JSON 호환 타입으로 변환하지 않으면 Pydantic 모델을 `JSONResponse`에 넣을 수 없습니다.

이러한 경우, 데이터를 응답에 전달하기 전에 `jsonable_encoder`를 사용하여 변환할 수 있습니다:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | 기술 세부사항

`from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `starlette.responses`를 `fastapi.responses`로 제공합니다. 하지만 대부분의 사용 가능한 응답은 Starlette에서 직접 제공합니다.

///

## 사용자 정의 `Response` 반환하기 { #returning-a-custom-response }

위 예제는 필요한 모든 부분을 보여주지만, 아직은 그다지 유용하지 않습니다. `item`을 그냥 직접 반환했어도 **FastAPI**가 기본으로 이를 `JSONResponse`에 넣고 `dict`로 변환하는 등의 작업을 모두 수행해 주었을 것이기 때문입니다.

이제, 이를 사용해 사용자 정의 응답을 반환하는 방법을 알아보겠습니다.

예를 들어 [XML](https://en.wikipedia.org/wiki/XML) 응답을 반환하고 싶다고 가정해 보겠습니다.

XML 내용을 문자열에 넣고, 이를 `Response`에 넣어 반환할 수 있습니다:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## 응답 모델 동작 방식 { #how-a-response-model-works }

경로 처리에서 [응답 모델 - 반환 타입](../tutorial/response-model.md)을 선언하면 **FastAPI**는 Pydantic을 사용해 데이터를 JSON으로 직렬화합니다.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

이는 Rust 측에서 처리되므로, 일반적인 Python과 `JSONResponse` 클래스로 수행하는 것보다 성능이 훨씬 좋습니다.

`response_model` 또는 반환 타입을 사용할 때 FastAPI는 `jsonable_encoder`로 데이터를 변환(이는 더 느립니다)하지도 않고, `JSONResponse` 클래스를 사용하지도 않습니다.

대신 응답 모델(또는 반환 타입)을 사용해 Pydantic이 생성한 JSON 바이트를 가져와, JSON에 맞는 미디어 타입(`application/json`)을 가진 `Response`를 직접 반환합니다.

## 참고 사항 { #notes }

`Response`를 직접 반환할 때, 그 데이터는 자동으로 유효성 검사되거나, 변환(직렬화)되거나, 문서화되지 않습니다.

그러나 [OpenAPI에서 추가 응답](additional-responses.md)에서 설명된 대로 문서화할 수 있습니다.

이후 섹션에서 자동 데이터 변환, 문서화 등을 계속 사용하면서 이러한 사용자 정의 `Response`를 사용하는/선언하는 방법을 확인할 수 있습니다.
