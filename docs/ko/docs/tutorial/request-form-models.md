# 폼 모델 { #form-models }

FastAPI에서 **Pydantic 모델**을 이용하여 **폼 필드**를 선언할 수 있습니다.

/// note | 참고

폼을 사용하려면, 먼저 [`python-multipart`](https://github.com/Kludex/python-multipart)를 설치하세요.

프로젝트에 추가하세요:

```console
$ uv add python-multipart
```

///

/// note | 참고

이 기능은 FastAPI 버전 `0.113.0` 이후부터 지원됩니다. 🤓

///

## 폼을 위한 Pydantic 모델 { #pydantic-models-for-forms }

**폼 필드**로 받고 싶은 필드를 **Pydantic 모델**로 선언한 다음, 매개변수를 `Form`으로 선언하면 됩니다:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI**는 요청에서 받은 **폼 데이터**에서 **각 필드**에 대한 데이터를 **추출**하고 정의한 Pydantic 모델을 줍니다.

[HTML 체크박스](request-forms.md#boolean-form-fields)에는 기본값이 `False`인 불리언 필드를 선언하세요.

## 문서 확인하기 { #check-the-docs }

문서 UI `/docs`에서 확인할 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 추가 폼 필드 금지하기 { #forbid-extra-form-fields }

일부 특별한 사용 사례(아마도 흔하지는 않겠지만)에서는 Pydantic 모델에서 선언된 폼 필드로만 **제한**하길 원할 수도 있습니다. 그리고 **추가** 필드를 **금지**할 수도 있습니다.

/// note | 참고

이 기능은 FastAPI 버전 `0.114.0` 이후부터 지원됩니다. 🤓

///

Pydantic의 모델 구성을 사용하여 `extra` 필드를 `forbid`할 수 있습니다:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

클라이언트가 추가 데이터를 보내려고 하면 **오류** 응답을 받게 됩니다.

예를 들어, 클라이언트가 폼 필드를 보내려고 하면:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

`extra` 필드가 허용되지 않는다는 오류 응답을 받게 됩니다:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## 폼 모델 조합하기 { #combine-form-models }

여러 폼 모델을 개별 `Form` 매개변수와 함께 사용할 수 있습니다.

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

클라이언트는 `name`, `tags`, `token`을 폼 필드로 전송합니다. 각 모델은 폼 필드를 독립적으로 검증합니다.

각 모델의 `extra` 설정은 다른 매개변수나 의존성에 선언된 필드와 파일을 포함하여 모든 폼 필드에 적용됩니다. `extra="forbid"`이면 해당 모델에 없는 필드는 모두 거부됩니다. `extra="allow"`이면 이러한 필드는 모델의 추가 필드로 포함됩니다.

여러 선언이 같은 폼 필드 이름을 사용하면, 각각 해당 필드의 값을 검증합니다. OpenAPI 스키마에서 일관되게 설명할 수 있도록 공유 필드에는 호환되는 타입과 제약 조건을 사용하세요.

## 선택적 폼 모델 { #optional-form-models }

폼 필드 그룹을 선택적으로 만들려면, 모델에 `| None`을 사용하고 기본값을 `None`으로 선언하세요.

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

`name`과 `age`가 모두 전송되지 않으면 `profile`은 `None`입니다. 둘 중 하나라도 전송되면 FastAPI는 모델을 검증하며 두 필드를 모두 요구합니다. 빈 값을 전송해도 해당 필드를 제공한 것으로 간주됩니다.

기본값 없이 `| None`만 사용하면 매개변수는 여전히 필수입니다.

추가 필드는 모델의 `extra` 설정을 따릅니다. 무시되는 추가 필드만으로는 모델이 제공된 것으로 간주하지 않습니다.

선택적 모델에 선택하지 않은 체크박스만 있으면 해당 모델은 생략됩니다. 명시적으로 제공하려면 `enabled=false` 같은 값을 전송하세요.

## 폼 모델의 선택적 유니온 { #optional-unions-of-form-models }

모델들의 선택적 유니온을 사용할 수도 있습니다.

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

폼 필드가 전송되지 않으면 `contact`는 `None`입니다. `kind=person`과 `name`을 함께 보내거나, `kind=company`와 `company_name`을 함께 보내세요. 판별자(discriminator)가 검증할 모델을 선택합니다.

## 폼 모델 유니온 조합하기 { #combine-unions-of-form-models }

유니온을 다른 폼 모델, 개별 `Form` 매개변수, `File` 매개변수와 함께 사용할 수 있습니다. 각 유니온은 독립적으로 검증됩니다.

{* ../../docs_src/request_form_models/tutorial007_an_py310.py hl[31:35] *}

모든 필드를 같은 폼에 담아 전송하세요. 예를 들어, `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com`, `token=secret`을 전송합니다.

`notification`을 `None`으로 두려면 알림 관련 필드를 생략하세요.

## 폼 모델과 파일 { #form-models-and-files }

폼 모델을 [파일 매개변수](request-files.md)와 함께 사용할 수도 있습니다.

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

여기서 클라이언트는 `multipart/form-data`를 사용하여 `name` 필드와 `avatar` 파일을 전송합니다.

## 요약 { #summary }

Pydantic 모델을 사용하여 FastAPI에서 폼 필드를 선언할 수 있습니다. 😎
