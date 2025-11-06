# 템플릿

**FastAPI**와 함께 원하는 어떤 템플릿 엔진도 사용할 수 있습니다.

일반적인 선택은 Jinja2로, Flask와 다른 도구에서도 사용됩니다.

설정을 쉽게 할 수 있는 유틸리티가 있으며, 이를 **FastAPI** 애플리케이션에서 직접 사용할 수 있습니다(Starlette 제공).

## 의존성 설치

가상 환경을 생성하고(virtual environment{.internal-link target=_blank}), 활성화한 후 jinja2를 설치해야 합니다:


<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 사용하기 `Jinja2Templates`

* `Jinja2Templates`를 가져옵니다.
* 나중에 재사용할 수 있는 `templates` 객체를 생성합니다.
* 템플릿을 반환할 경로 작업에 `Request` 매개변수를 선언합니다.
* 생성한 `templates`를 사용하여 `TemplateResponse`를 렌더링하고 반환합니다. 템플릿의 이름, 요청 객체 및 Jinja2 템플릿 내에서 사용될 키-값 쌍이 포함된 "컨텍스트" 딕셔너리도 전달합니다.


```Python hl_lines="4  11  15-18"
{!../../docs_src/templates/tutorial001.py!}
```

/// note | 참고

FastAPI 0.108.0 이전과 Starlette 0.29.0에서는 `name`이 첫 번째 매개변수였습니다.

또한 이전 버전에서는 `request` 객체가 Jinja2의 컨텍스트에서 키-값 쌍의 일부로 전달되었습니다.

///

/// tip | 팁

`response_class=HTMLResponse`를 선언하면 문서 UI 응답이 HTML임을 알 수 있습니다.

///

/// note | 기술 세부 사항
`from starlette.templating import Jinja2Templates`를 사용할 수도 있습니다.

**FastAPI**는 개발자를 위한 편리함으로 `fastapi.templating` 대신 `starlette.templating`을 제공합니다. 하지만 대부분의 사용 가능한 응답은 Starlette에서 직접 옵니다. `Request` 및 `StaticFiles`도 마찬가지입니다.
///

## 템플릿 작성하기

그런 다음 `templates/item.html`에 템플릿을 작성할 수 있습니다. 예를 들면:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 템플릿 컨텍스트 값

다음과 같은 HTML에서:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...이는 전달한 "컨텍스트" `dict`에서 가져온 `id`를 표시합니다:

```Python
{"id": id}
```

예를 들어, ID가 `42`일 경우, 이는 다음과 같이 렌더링됩니다:

```html
Item ID: 42
```

### 템플릿 `url_for` 인수

템플릿 내에서 `url_for()`를 사용할 수도 있으며, 이는 *경로 작업 함수*에서 사용될 인수와 동일한 인수를 받습니다.

따라서 다음과 같은 부분에서:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...이는 *경로 작업 함수* `read_item(id=id)`가 처리할 동일한 URL로 링크를 생성합니다.

예를 들어, ID가 `42`일 경우, 이는 다음과 같이 렌더링됩니다:
```html
<a href="/items/42">
```

## 템플릿과 정적 파일

템플릿 내에서 `url_for()`를 사용할 수 있으며, 예를 들어 `name="static"`으로 마운트한 `StaticFiles`와 함께 사용할 수 있습니다.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

이 예제에서는 `static/styles.css`에 있는 CSS 파일에 연결될 것입니다:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

그리고 `StaticFiles`를 사용하고 있으므로, 해당 CSS 파일은 **FastAPI** 애플리케이션에서 `/static/styles.css` URL로 자동 제공됩니다.

## 더 많은 세부 사항

템플릿 테스트를 포함한 더 많은 세부 사항은 <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette의 템플릿 문서</a>를 확인하세요.
