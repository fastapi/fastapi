# 입력과 출력에 대해 OpenAPI 스키마를 분리할지 여부 { #separate-openapi-schemas-for-input-and-output-or-not }

**Pydantic v2**가 릴리스된 이후, 생성되는 OpenAPI는 이전보다 조금 더 정확하고 **올바르게** 만들어집니다. 😎

실제로 어떤 경우에는, 같은 Pydantic 모델에 대해 OpenAPI 안에 **두 개의 JSON Schema**가 생기기도 합니다. **기본값(default value)**이 있는지 여부에 따라, 입력용과 출력용으로 나뉩니다.

이것이 어떻게 동작하는지, 그리고 필요하다면 어떻게 변경할 수 있는지 살펴보겠습니다.

## 입력과 출력을 위한 Pydantic 모델 { #pydantic-models-for-input-and-output }

예를 들어, 다음처럼 기본값이 있는 Pydantic 모델이 있다고 해보겠습니다:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### 입력용 모델 { #model-for-input }

이 모델을 다음처럼 입력으로 사용하면:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...`description` 필드는 **필수가 아닙니다**. `None`이라는 기본값이 있기 때문입니다.

### 문서에서의 입력 모델 { #input-model-in-docs }

문서에서 `description` 필드에 **빨간 별표**가 없고, 필수로 표시되지 않는 것을 확인할 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### 출력용 모델 { #model-for-output }

하지만 같은 모델을 다음처럼 출력으로 사용하면:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...`description`에 기본값이 있기 때문에, 그 필드에 대해 **아무것도 반환하지 않더라도** 여전히 그 **기본값**이 들어가게 됩니다.

### 출력 응답 데이터용 모델 { #model-for-output-response-data }

문서에서 직접 동작시켜 응답을 확인해 보면, 코드가 `description` 필드 중 하나에 아무것도 추가하지 않았더라도 JSON 응답에는 기본값(`null`)이 포함되어 있습니다:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

이는 해당 필드가 **항상 값을 가진다는 것**을 의미합니다. 다만 그 값이 때로는 `None`(JSON에서는 `null`)일 수 있습니다.

즉, API를 사용하는 클라이언트는 값이 존재하는지 여부를 확인할 필요가 없고, **필드가 항상 존재한다고 가정**할 수 있습니다. 다만 어떤 경우에는 기본값 `None`이 들어갑니다.

이를 OpenAPI에서 표현하는 방법은, 그 필드를 **required**로 표시하는 것입니다. 항상 존재하기 때문입니다.

이 때문에, 하나의 모델이라도 **입력용인지 출력용인지**에 따라 JSON Schema가 달라질 수 있습니다:

* **입력**에서는 `description`이 **필수가 아님**
* **출력**에서는 **필수임** (그리고 값은 `None`일 수도 있으며, JSON 용어로는 `null`)

### 문서에서의 출력용 모델 { #model-for-output-in-docs }

문서에서 출력 모델을 확인해 보면, `name`과 `description` **둘 다** **빨간 별표**로 **필수**로 표시되어 있습니다:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### 문서에서의 입력과 출력 모델 { #model-for-input-and-output-in-docs }

또 OpenAPI에서 사용 가능한 모든 Schemas(JSON Schemas)를 확인해 보면, `Item-Input` 하나와 `Item-Output` 하나, 이렇게 두 개가 있는 것을 볼 수 있습니다.

`Item-Input`에서는 `description`이 **필수가 아니며**, 빨간 별표가 없습니다.

하지만 `Item-Output`에서는 `description`이 **필수이며**, 빨간 별표가 있습니다.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

**Pydantic v2**의 이 기능 덕분에 API 문서는 더 **정밀**해지고, 자동 생성된 클라이언트와 SDK가 있다면 그것들도 더 정밀해져서 더 나은 **developer experience**와 일관성을 제공할 수 있습니다. 🎉

## 스키마를 분리하지 않기 { #do-not-separate-schemas }

이제 어떤 경우에는 **입력과 출력에 대해 같은 스키마를 사용**하고 싶을 수도 있습니다.

가장 대표적인 경우는, 이미 자동 생성된 클라이언트 코드/SDK가 있고, 아직은 그 자동 생성된 클라이언트 코드/SDK들을 전부 업데이트하고 싶지 않은 경우입니다. 언젠가는 업데이트해야 할 가능성이 높지만, 지금 당장은 아닐 수도 있습니다.

그런 경우에는, **FastAPI**에서 `separate_input_output_schemas=False` 파라미터로 이 기능을 비활성화할 수 있습니다.

/// info | 정보

`separate_input_output_schemas` 지원은 FastAPI `0.102.0`에 추가되었습니다. 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### 문서에서 입력과 출력 모델에 같은 스키마 사용 { #same-schema-for-input-and-output-models-in-docs }

이제 모델에 대해 입력과 출력 모두에 사용되는 단일 스키마(오직 `Item`만)가 생성되며, `description`은 **필수가 아닌 것**으로 표시됩니다:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
