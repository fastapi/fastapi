# 본문 - 필드

`Query`,`Path` 및`Body`를 사용하여 *경로 동작 함수* 매개변수에서 추가 검증 및 메타데이터를 선언할 수있는 것과 마찬가지로, Pydantic의 `Field`를 사용하여 Pydantic 모델 내부에서 검증 및 메타데이터를 선언할 수 있습니다.

## `Field` 임포트

우선, 이를 임포트합니다:

```Python hl_lines="4"
{!../../../docs_src/body_fields/tutorial001.py!}
```

!!! warning "경고"
    `Field`는 나머지 것들(`Query`, `Path`, `Body`, 등)과 마찬가지로 `fastapi`가 아니라 `pydantic`에서 직접 임포트 합니다

##모델 어트리뷰트 선언

모델 어트리뷰트와 함께 `Field`를 사용할 수 있습니다:

```Python hl_lines="11-14"
{!../../../docs_src/body_fields/tutorial001.py!}
```

`Field`는 `Query`, `Path` 및 `Body`와 동일한 방식으로 작동하며, 모든 매개변수 등이 동일합니다.

!!! note "기술 세부사항"
    사실, `Query`, `Path` 그리고 여러분이 나중에 보게 될 다른 것들은 `FieldInfo` 클래스의 서브 클래스인 공통 `Param` 클래스의 서브 클래스 객체를 만듭니다.

    또한 Pydantic의 `Field`는 `FieldInfo`의 인스턴스 역시 반환합니다.

    `Body` 역시 `FieldInfo`의 서브 클래스의 객체를 직접 반환합니다. 그리고 나중에 보게 될 `Body` 클래스의 서브 클래스도 있습니다.

    `fastapi`에서 `Query`, `Path` 및 다른 것들을 임포트하면, 이들 모두 특별한 클래스를 반환하는 실제 함수임을 기억하세요.

!!! tip "팁"
    타입, 기본값, 그리고 `Field`를 갖는 각 모델의 어트리뷰트가 `Field` 대신 `Path`, `Query` 및 `Body`를 사용하여 *경로 동작 함수* 매개변수와 어떻게 동일한 구조를 갖는지 알아두세요.

## 추가 정보 추가

`Field`, `Query`, `Body` 등에 추가 정보를 선언할 수 있습니다. 그리고 이 정보는 생성된 JSON 스키마에 포함됩니다.

예제 선언하는 것을 배울때 문서에 추가 정보를 선언하는 방법을 배울 것입니다.

## 요약

모델 어트리뷰트를 위한 추가 검증과 메타데이터를 선언하기 위해 Pydantic의 `Field` 를 사용할 수 있습니다.

추가 JSON 스키마 메타데이터를 전달하기 위해 추가 키워드 인자 또한 사용할 수 있습니다.
