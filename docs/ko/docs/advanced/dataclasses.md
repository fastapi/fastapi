# Dataclasses 사용하기 { #using-dataclasses }

FastAPI는 **Pydantic** 위에 구축되어 있으며, 지금까지는 Pydantic 모델을 사용해 요청과 응답을 선언하는 방법을 보여드렸습니다.

하지만 FastAPI는 <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a>도 같은 방식으로 사용하는 것을 지원합니다:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

이는 **Pydantic** 덕분에 여전히 지원되는데, Pydantic이 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">`dataclasses`에 대한 내부 지원</a>을 제공하기 때문입니다.

따라서 위 코드처럼 Pydantic을 명시적으로 사용하지 않더라도, FastAPI는 Pydantic을 사용해 표준 dataclasses를 Pydantic의 dataclasses 변형으로 변환합니다.

그리고 물론 다음과 같은 기능도 동일하게 지원합니다:

* 데이터 검증
* 데이터 직렬화
* 데이터 문서화 등

이는 Pydantic 모델을 사용할 때와 같은 방식으로 동작합니다. 그리고 실제로도 내부적으로는 Pydantic을 사용해 같은 방식으로 구현됩니다.

/// info | 정보

dataclasses는 Pydantic 모델이 할 수 있는 모든 것을 할 수는 없다는 점을 기억하세요.

그래서 여전히 Pydantic 모델을 사용해야 할 수도 있습니다.

하지만 이미 여러 dataclasses를 가지고 있다면, 이것은 FastAPI로 웹 API를 구동하는 데 그것들을 활용할 수 있는 좋은 방법입니다. 🤓

///

## `response_model`에서 Dataclasses 사용하기 { #dataclasses-in-response-model }

`response_model` 매개변수에서도 `dataclasses`를 사용할 수 있습니다:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

dataclass는 자동으로 Pydantic dataclass로 변환됩니다.

이렇게 하면 해당 스키마가 API docs 사용자 인터페이스에 표시됩니다:

<img src="/img/tutorial/dataclasses/image01.png">

## 중첩 데이터 구조에서 Dataclasses 사용하기 { #dataclasses-in-nested-data-structures }

`dataclasses`를 다른 타입 애너테이션과 조합해 중첩 데이터 구조를 만들 수도 있습니다.

일부 경우에는 Pydantic 버전의 `dataclasses`를 사용해야 할 수도 있습니다. 예를 들어 자동 생성된 API 문서에서 오류가 발생하는 경우입니다.

그런 경우 표준 `dataclasses`를 드롭인 대체재인 `pydantic.dataclasses`로 간단히 바꾸면 됩니다:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. 표준 `dataclasses`에서 `field`를 계속 임포트합니다.

2. `pydantic.dataclasses`는 `dataclasses`의 드롭인 대체재입니다.

3. `Author` dataclass에는 `Item` dataclasses의 리스트가 포함됩니다.

4. `Author` dataclass가 `response_model` 매개변수로 사용됩니다.

5. 요청 본문으로 dataclasses와 함께 다른 표준 타입 애너테이션을 사용할 수 있습니다.

    이 경우에는 `Item` dataclasses의 리스트입니다.

6. 여기서는 dataclasses 리스트인 `items`를 포함하는 딕셔너리를 반환합니다.

    FastAPI는 여전히 데이터를 JSON으로 <abbr title="converting the data to a format that can be transmitted - 데이터를 전송 가능한 형식으로 변환하는 것">serializing</abbr>할 수 있습니다.

7. 여기서 `response_model`은 `Author` dataclasses 리스트에 대한 타입 애너테이션을 사용합니다.

    다시 말해, `dataclasses`를 표준 타입 애너테이션과 조합할 수 있습니다.

8. 이 *경로 처리 함수*는 `async def` 대신 일반 `def`를 사용하고 있다는 점에 주목하세요.

    언제나처럼 FastAPI에서는 필요에 따라 `def`와 `async def`를 조합해 사용할 수 있습니다.

    어떤 것을 언제 사용해야 하는지 다시 확인하고 싶다면, [`async`와 `await`](../async.md#in-a-hurry){.internal-link target=_blank} 문서의 _"급하신가요?"_ 섹션을 확인하세요.

9. 이 *경로 처리 함수*는 dataclasses를(물론 반환할 수도 있지만) 반환하지 않고, 내부 데이터를 담은 딕셔너리들의 리스트를 반환합니다.

    FastAPI는 `response_model` 매개변수(dataclasses 포함)를 사용해 응답을 변환합니다.

`dataclasses`는 다른 타입 애너테이션과 매우 다양한 조합으로 결합해 복잡한 데이터 구조를 구성할 수 있습니다.

더 구체적인 내용은 위 코드 내 애너테이션 팁을 확인하세요.

## 더 알아보기 { #learn-more }

`dataclasses`를 다른 Pydantic 모델과 조합하거나, 이를 상속하거나, 여러분의 모델에 포함하는 등의 작업도 할 수 있습니다.

자세한 내용은 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">dataclasses에 관한 Pydantic 문서</a>를 참고하세요.

## 버전 { #version }

이 기능은 FastAPI `0.67.0` 버전부터 사용할 수 있습니다. 🔖
