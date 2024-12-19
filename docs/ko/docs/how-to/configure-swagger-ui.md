# Swagger UI 구성

추가적인 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 매개변수</a>를 구성할 수 있습니다.

구성을 하려면, `FastAPI()` 앱 객체를 생성할 때 또는 `get_swagger_ui_html()` 함수에 `swagger_ui_parameters` 인수를 전달하십시오.

`swagger_ui_parameters`는 Swagger UI에 직접 전달된 구성을 포함하는 딕셔너리를 받습니다.

FastAPI는 이 구성을 **JSON** 형식으로 변환하여 JavaScript와 호환되도록 합니다. 이는 Swagger UI에서 필요로 하는 형식입니다.

## 구문 강조 비활성화

예를 들어, Swagger UI에서 구문 강조 기능을 비활성화할 수 있습니다.

설정을 변경하지 않으면, 기본적으로 구문 강조 기능이 활성화되어 있습니다:

<img src="/img/tutorial/extending-openapi/image02.png">

그러나 `syntaxHighlight`를 `False`로 설정하여 구문 강조 기능을 비활성화할 수 있습니다:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...그럼 Swagger UI에서 더 이상 구문 강조 기능이 표시되지 않습니다:

<img src="/img/tutorial/extending-openapi/image03.png">

## 테마 변경

동일한 방식으로 `"syntaxHighlight.theme"` 키를 사용하여 구문 강조 테마를 설정할 수 있습니다 (중간에 점이 포함된 것을 참고하십시오).

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

이 설정은 구문 강조 색상 테마를 변경합니다:

<img src="/img/tutorial/extending-openapi/image04.png">

## 기본 Swagger UI 매개변수 변경

FastAPI는 대부분의 사용 사례에 적합한 몇 가지 기본 구성 매개변수를 포함하고 있습니다.

기본 구성에는 다음이 포함됩니다:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

`swagger_ui_parameters` 인수에 다른 값을 설정하여 이러한 기본값 중 일부를 재정의할 수 있습니다.

예를 들어, `deepLinking`을 비활성화하려면 `swagger_ui_parameters`에 다음 설정을 전달할 수 있습니다:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## 기타 Swagger UI 매개변수

사용할 수 있는 다른 모든 구성 옵션을 확인하려면, Swagger UI 매개변수에 대한 공식 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">문서</a>를 참조하십시오.

## JavaScript 전용 설정

Swagger UI는 **JavaScript 전용** 객체(예: JavaScript 함수)로 다른 구성을 허용하기도 합니다.

FastAPI는 이러한 JavaScript 전용 `presets` 설정을 포함하고 있습니다:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

이들은 문자열이 아닌 **JavaScript** 객체이므로 Python 코드에서 직접 전달할 수 없습니다.

이와 같은 JavaScript 전용 구성을 사용해야 하는 경우, 위의 방법 중 하나를 사용하여 모든 Swagger UI 경로 작업을 재정의하고 필요한 JavaScript를 수동으로 작성할 수 있습니다.
