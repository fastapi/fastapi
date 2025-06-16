# 폼 모델

FastAPI에서 **Pydantic 모델**을 이용하여 **폼 필드**를 선언할 수 있습니다.

/// info | 정보

폼(Form)을 사용하려면, 먼저 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>를 설치하세요.

[가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화한 다음, 아래와 같이 설치할 수 있습니다:

```console
$ pip install python-multipart
```

///

/// note | 참고

이 기능은 FastAPI 버전 `0.113.0` 이후부터 지원됩니다. 🤓

///

## Pydantic 모델을 사용한 폼

**폼 필드**로 받고 싶은 필드를 **Pydantic 모델**로 선언한 다음, 매개변수를 `Form`으로 선언하면 됩니다:

{* ../../docs_src/request_form_models/tutorial001_an_py39.py hl[9:11,15] *}

**FastAPI**는 요청에서 받은 **폼 데이터**에서 **각 필드**에 대한 데이터를 **추출**하고 정의한 Pydantic 모델을 줍니다.

## 문서 확인하기

문서 UI `/docs`에서 확인할 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 추가 폼 필드 금지하기

일부 특별한 사용 사례(흔하지는 않겠지만)에서는 Pydantic 모델에서 정의한 폼 필드를 **제한**하길 원할 수도 있습니다. 그리고 **추가** 필드를 **금지**할 수도 있습니다.

/// note | 참고

이 기능은 FastAPI 버전 `0.114.0` 이후부터 지원됩니다. 🤓

///

Pydantic의 모델 구성을 사용하여 추가(`extra`) 필드를 금지(`forbid`)할 수 있습니다:

{* ../../docs_src/request_form_models/tutorial002_an_py39.py hl[12] *}

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

## 요약

Pydantic 모델을 사용하여 FastAPI에서 폼 필드를 선언할 수 있습니다. 😎
