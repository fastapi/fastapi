# 추가 스키마(Schema-Extra) - 예시  

JSON 스키마에 들어갈 추가 정보를 정의할 수 있습니다.

흔한 활용 사례는 문서에 보여질 `example`을 추가하는 것입니다.

추가적인 JSON 스키마 정보를 선언하는 여러가지 방법이 있습니다.

## Pydantic `schema_extra`

<a href="https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic의 문서: 스키마 맞춤화</a>에서 설명되어 있는 것과 같이 `Config`와 `schema_extra`를 사용하여 Pydantic 모델의 예시를 선언할 수 있습니다.


```Python hl_lines="15-23"
{!../../../docs_src/schema_extra_example/tutorial001.py!}
```

그 추가 정보는 현재 상태 그대로 JSON 스키마 출력에 추가될 것입니다.

## `Field` 추가적인 인자들(arguments)

`Field`, `Path`, `Query`, `Body` 및 나중에 보게 될 것들에서, 다른 어떤 임의의 인자(arguments)를 함수에 전달함으로써 JSON 스키마에 추가 정보를 선언할 수도 있습니다. 예를 들면, `example`을 추가하는 것과 같이 말입니다:

```Python hl_lines="4  10-13"
{!../../../docs_src/schema_extra_example/tutorial002.py!}
```

!!! 주의
    전달된 추가 인자들은 그 어떤 검증(validation)을 추가하지 않으며 오로지 문서화 목적으로 어노테이션만 추가함을 명심하십시오.

## `Body` 추가적인 인자들

`Field`에 추가 정보를 전달할 수 있는 것과 같은 방법으로, `Path`, `Query`, `Body`, 등에 대해서도 동일하게 할 수 있습니다.

예를 들면, 바디 요청에 대해 `example`을 `Body`에 전달할 수 있습니다:

```Python hl_lines="21-26"
{!../../../docs_src/schema_extra_example/tutorial003.py!}
```

## 문서 UI에서의 예시

위의 어떤 방법으로든 `/docs`에서는 이렇게 보일 것입니다:

<img src="/img/tutorial/body-fields/image01.png">

## 기술적 세부사항

`example`과 `examples`에 대하여...

JSON 스키마는 가장 최신 버전에서 필드 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>을 정의하지만, OPEN API는 `examples`가 없는 JSON 스키마의 이전 버전에 기반하고 있습니다.

그래서, OPEN API는 (`examples`가 아니라 `example`과) 동일한 목적으로 자체적인 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a>을 정의하며, 그것이 문서 UI에서 사용되는 것입니다(스웨거 UI 사용).

그래서, 비록 `example`은 JSON 스키마의 일부는 아니지만, 그것은 OPEN API의 일부분이고, 그것이 바로 문서 UI에서 사용될 것입니다.

## 다른 정보

같은 방식으로, 각 모델에 대한 JSON 스키마에 추가될 당신만의 맞춤형 추가 정보를 추가할 수 있습니다, 예를 들면 프론트엔드 사용자 인터페이스를 맞춤화(커스터마이즈)하는 것 등 입니다.
