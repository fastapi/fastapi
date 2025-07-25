# 큰 애플리케이션 - 여러 파일

애플리케이션이나 웹 API를 구축할 때, 모든 것을 단일 파일에 넣는 경우는 거의 없습니다.

**FastAPI**는 모든 유연성을 유지하면서 애플리케이션을 구조화할 수 있는 편리한 도구를 제공합니다.

/// info

Flask에서 오셨다면, 이는 Flask의 Blueprints와 동등한 것입니다.

///

## 예제 파일 구조

다음과 같은 파일 구조가 있다고 가정해봅시다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip

여러 개의 `__init__.py` 파일이 있습니다: 각 디렉토리나 하위 디렉토리마다 하나씩.

이는 한 파일에서 다른 파일로 코드를 임포트할 수 있게 해주는 것입니다.

예를 들어, `app/main.py`에서 다음과 같은 줄을 가질 수 있습니다:

```
from app.routers import items
```

///

* `app` 디렉토리는 모든 것을 포함합니다. 그리고 빈 파일 `app/__init__.py`를 가지고 있으므로, "Python 패키지"("Python 모듈"들의 모음)입니다: `app`.
* `app/main.py` 파일을 포함합니다. Python 패키지(`__init__.py` 파일이 있는 디렉토리) 내부에 있으므로, 해당 패키지의 "모듈"입니다: `app.main`.
* `app/main.py`와 마찬가지로 `app/dependencies.py` 파일도 있으며, 이는 "모듈"입니다: `app.dependencies`.
* 다른 `__init__.py` 파일이 있는 하위 디렉토리 `app/routers/`가 있으므로, "Python 하위 패키지"입니다: `app.routers`.
* 파일 `app/routers/items.py`는 패키지 `app/routers/` 내부에 있으므로, 하위 모듈입니다: `app.routers.items`.
* `app/routers/users.py`도 마찬가지로, 또 다른 하위 모듈입니다: `app.routers.users`.
* 다른 `__init__.py` 파일이 있는 하위 디렉토리 `app/internal/`도 있으므로, 또 다른 "Python 하위 패키지"입니다: `app.internal`.
* 그리고 파일 `app/internal/admin.py`는 또 다른 하위 모듈입니다: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

주석이 있는 동일한 파일 구조:

```
.
├── app                  # "app"은 Python 패키지입니다
│   ├── __init__.py      # 이 파일이 "app"을 "Python 패키지"로 만듭니다
│   ├── main.py          # "main" 모듈, 예: import app.main
│   ├── dependencies.py  # "dependencies" 모듈, 예: import app.dependencies
│   └── routers          # "routers"는 "Python 하위 패키지"입니다
│   │   ├── __init__.py  # "routers"를 "Python 하위 패키지"로 만듭니다
│   │   ├── items.py     # "items" 하위 모듈, 예: import app.routers.items
│   │   └── users.py     # "users" 하위 모듈, 예: import app.routers.users
│   └── internal         # "internal"은 "Python 하위 패키지"입니다
│       ├── __init__.py  # "internal"을 "Python 하위 패키지"로 만듭니다
│       └── admin.py     # "admin" 하위 모듈, 예: import app.internal.admin
```

## `APIRouter`

사용자만 처리하는 전용 파일이 `/app/routers/users.py`의 하위 모듈이라고 가정해봅시다.

사용자와 관련된 *경로 동작*을 나머지 코드와 분리하여 정리된 상태로 유지하고 싶습니다.

하지만 여전히 동일한 **FastAPI** 애플리케이션/웹 API의 일부입니다(동일한 "Python 패키지"의 일부).

`APIRouter`를 사용하여 해당 모듈의 *경로 동작*을 만들 수 있습니다.

### `APIRouter` 임포트하기

`FastAPI` 클래스와 동일한 방식으로 임포트하고 "인스턴스"를 만듭니다:

```Python hl_lines="1  3" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

### `APIRouter`로 *경로 동작* 만들기

그런 다음 이를 사용하여 *경로 동작*을 선언합니다.

`FastAPI` 클래스를 사용하는 것과 동일한 방식으로 사용합니다:

```Python hl_lines="6  11  16" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

`APIRouter`를 "미니 `FastAPI`" 클래스로 생각할 수 있습니다.

동일한 옵션이 모두 지원됩니다.

동일한 `parameters`, `responses`, `dependencies`, `tags` 등이 모두 지원됩니다.

/// tip

이 예제에서는 변수를 `router`라고 했지만, 원하는 대로 이름을 지을 수 있습니다.

///

이 `APIRouter`를 메인 `FastAPI` 앱에 포함시킬 것입니다. 하지만 먼저 의존성과 다른 `APIRouter`를 확인해봅시다.

## 의존성

애플리케이션의 여러 곳에서 사용되는 일부 의존성이 필요할 것입니다.

따라서 자체 `dependencies` 모듈(`app/dependencies.py`)에 넣습니다.

이제 커스텀 `X-Token` 헤더를 읽는 간단한 의존성을 사용하겠습니다:

//// tab | Python 3.9+

```Python hl_lines="3  6-8" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an_py39/dependencies.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  5-7" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an/dependencies.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

가능하면 `Annotated` 버전을 사용하는 것을 선호합니다.

///

```Python hl_lines="1  4-6" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app/dependencies.py!}
```

////

/// tip

이 예제를 단순화하기 위해 임의의 헤더를 사용하고 있습니다.

하지만 실제 경우에는 통합된 [보안 유틸리티](security/index.md){.internal-link target=_blank}를 사용하여 더 나은 결과를 얻을 수 있습니다.

///

## `APIRouter`가 있는 다른 모듈

`app/routers/items.py` 모듈에서 애플리케이션의 "items" 처리 전용 엔드포인트도 있다고 가정해봅시다.

다음을 위한 *경로 동작*이 있습니다:

* `/items/`
* `/items/{item_id}`

`app/routers/users.py`와 동일한 구조입니다.

하지만 더 똑똑하게 코드를 조금 단순화하고 싶습니다.

이 모듈의 모든 *경로 동작*이 동일한 것을 가지고 있다는 것을 알고 있습니다:

* 경로 `prefix`: `/items`.
* `tags`: (하나의 태그: `items`).
* 추가 `responses`.
* `dependencies`: 모두 우리가 만든 `X-Token` 의존성이 필요합니다.

따라서 각 *경로 동작*에 모든 것을 추가하는 대신, `APIRouter`에 추가할 수 있습니다.

```Python hl_lines="5-10  16  21" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

각 *경로 동작*의 경로는 다음과 같이 `/`로 시작해야 하므로:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...prefix는 마지막 `/`를 포함하지 않아야 합니다.

따라서 이 경우 prefix는 `/items`입니다.

이 라우터에 포함된 모든 *경로 동작*에 적용될 `tags` 목록과 추가 `responses`도 추가할 수 있습니다.

그리고 라우터의 모든 *경로 동작*에 추가되고 각 요청에 대해 실행/해결될 `dependencies` 목록을 추가할 수 있습니다.

/// tip

[*경로 동작 데코레이터의 의존성*](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}과 마찬가지로, 값이 *경로 동작 함수*에 전달되지 않는다는 점에 주의하세요.

///

최종 결과는 이제 item 경로가 다음과 같다는 것입니다:

* `/items/`
* `/items/{item_id}`

...의도한 대로입니다.

* 단일 문자열 `"items"`를 포함하는 태그 목록으로 표시됩니다.
    * 이러한 "태그"는 특히 자동 대화형 문서 시스템(OpenAPI 사용)에 유용합니다.
* 모든 것이 미리 정의된 `responses`를 포함할 것입니다.
* 이러한 모든 *경로 동작*은 그들 이전에 평가/실행되는 `dependencies` 목록을 가질 것입니다.
    * 특정 *경로 동작*에서도 의존성을 선언하면, **그것들도 실행될 것입니다**.
    * 라우터 의존성이 먼저 실행되고, 그 다음에 [데코레이터의 `dependencies`](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, 그리고 일반 매개변수 의존성이 실행됩니다.
    * [`scopes`가 있는 `Security` 의존성](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}도 추가할 수 있습니다.

/// tip

`APIRouter`에 `dependencies`를 갖는 것은, 예를 들어 전체 *경로 동작* 그룹에 대해 인증을 요구하는 데 사용할 수 있습니다. 각각에 개별적으로 의존성을 추가하지 않더라도 말입니다.

///

/// check

`prefix`, `tags`, `responses`, `dependencies` 매개변수는 (다른 많은 경우와 마찬가지로) 코드 중복을 피하는 데 도움이 되는 **FastAPI**의 기능일 뿐입니다.

///

### 의존성 임포트하기

이 코드는 모듈 `app.routers.items`, 파일 `app/routers/items.py`에 있습니다.

그리고 모듈 `app.dependencies`, 파일 `app/dependencies.py`에서 의존성 함수를 가져와야 합니다.

따라서 의존성에 대해 `..`를 사용하여 상대 임포트를 사용합니다:

```Python hl_lines="3" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

#### 상대 임포트 작동 방식

/// tip

임포트가 어떻게 작동하는지 완벽히 알고 있다면, 아래 다음 섹션으로 계속 진행하세요.

///

다음과 같은 단일 점 `.`:

```Python
from .dependencies import get_token_header
```

의미는:

* 이 모듈(파일 `app/routers/items.py`)이 있는 동일한 패키지(디렉토리 `app/routers/`)에서 시작하여...
* 모듈 `dependencies`(가상의 파일 `app/routers/dependencies.py`)를 찾고...
* 그것에서 함수 `get_token_header`를 임포트합니다.

하지만 그 파일은 존재하지 않습니다. 우리의 의존성은 `app/dependencies.py` 파일에 있습니다.

우리의 앱/파일 구조가 어떻게 생겼는지 기억하세요:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

다음과 같은 두 개의 점 `..`:

```Python
from ..dependencies import get_token_header
```

의미는:

* 이 모듈(파일 `app/routers/items.py`)이 있는 동일한 패키지(디렉토리 `app/routers/`)에서 시작하여...
* 부모 패키지(디렉토리 `app/`)로 이동하고...
* 그곳에서 모듈 `dependencies`(파일 `app/dependencies.py`)를 찾고...
* 그것에서 함수 `get_token_header`를 임포트합니다.

이것이 올바르게 작동합니다! 🎉

---

다음과 같은 세 개의 점 `...`을 사용했다면:

```Python
from ...dependencies import get_token_header
```

의미는:

* 이 모듈(파일 `app/routers/items.py`)이 있는 동일한 패키지(디렉토리 `app/routers/`)에서 시작하여...
* 부모 패키지(디렉토리 `app/`)로 이동하고...
* 그 패키지의 부모로 이동합니다(부모 패키지가 없습니다. `app`이 최상위입니다 😱)...
* 그곳에서 모듈 `dependencies`(파일 `app/dependencies.py`)를 찾고...
* 그것에서 함수 `get_token_header`를 임포트합니다.

이는 `app/` 위의 어떤 패키지를 참조할 것이며, 자체 `__init__.py` 파일 등을 가지고 있을 것입니다. 하지만 우리는 그것을 가지고 있지 않습니다. 따라서 우리 예제에서는 에러가 발생할 것입니다. 🚨

하지만 이제 어떻게 작동하는지 알았으므로, 앱이 얼마나 복잡하든 상관없이 자신의 앱에서 상대 임포트를 사용할 수 있습니다. 🤓

### 일부 커스텀 `tags`, `responses`, `dependencies` 추가하기

우리는 `APIRouter`에 prefix `/items`나 `tags=["items"]`를 추가했기 때문에 각 *경로 동작*에 추가하지 않습니다.

하지만 특정 *경로 동작*에 적용될 _더 많은_ `tags`와 해당 *경로 동작*에 특정한 일부 추가 `responses`를 여전히 추가할 수 있습니다:

```Python hl_lines="30-31" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

/// tip

이 마지막 경로 동작은 태그의 조합을 가질 것입니다: `["items", "custom"]`.

그리고 문서에서 두 응답을 모두 가질 것입니다. 하나는 `404`이고 하나는 `403`입니다.

///

## 메인 `FastAPI`

이제 `app/main.py`의 모듈을 살펴봅시다.

여기서 `FastAPI` 클래스를 임포트하고 사용합니다.

이것은 모든 것을 함께 묶는 애플리케이션의 메인 파일이 될 것입니다.

그리고 대부분의 로직이 이제 자체 특정 모듈에 있을 것이므로, 메인 파일은 매우 간단할 것입니다.

### `FastAPI` 임포트하기

평소와 같이 `FastAPI` 클래스를 임포트하고 생성합니다.

그리고 각 `APIRouter`의 의존성과 결합될 [전역 의존성](dependencies/global-dependencies.md){.internal-link target=_blank}도 선언할 수 있습니다:

```Python hl_lines="1  3  7" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### `APIRouter` 임포트하기

이제 `APIRouter`가 있는 다른 하위 모듈을 임포트합니다:

```Python hl_lines="4-5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

파일 `app/routers/users.py`와 `app/routers/items.py`는 동일한 Python 패키지 `app`의 일부인 하위 모듈이므로, "상대 임포트"를 사용하여 단일 점 `.`을 사용하여 임포트할 수 있습니다.

### 임포트 작동 방식

섹션:

```Python
from .routers import items, users
```

의미는:

* 이 모듈(파일 `app/main.py`)이 있는 동일한 패키지(디렉토리 `app/`)에서 시작하여...
* 하위 패키지 `routers`(디렉토리 `app/routers/`)를 찾고...
* 그것에서 하위 모듈 `items`(파일 `app/routers/items.py`)와 `users`(파일 `app/routers/users.py`)를 임포트합니다...

모듈 `items`는 변수 `router`(`items.router`)를 가질 것입니다. 이는 파일 `app/routers/items.py`에서 생성한 것과 동일하며, `APIRouter` 객체입니다.

그리고 모듈 `users`에 대해서도 동일하게 수행합니다.

다음과 같이 임포트할 수도 있습니다:

```Python
from app.routers import items, users
```

/// info

첫 번째 버전은 "상대 임포트"입니다:

```Python
from .routers import items, users
```

두 번째 버전은 "절대 임포트"입니다:

```Python
from app.routers import items, users
```

Python 패키지와 모듈에 대해 더 알아보려면, <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">모듈에 대한 공식 Python 문서</a>를 읽어보세요.

///

### 이름 충돌 피하기

우리는 단지 변수 `router`를 임포트하는 대신 하위 모듈 `items`를 직접 임포트하고 있습니다.

이는 하위 모듈 `users`에도 `router`라는 이름의 다른 변수가 있기 때문입니다.

다음과 같이 하나씩 임포트했다면:

```Python
from .routers.items import router
from .routers.users import router
```

`users`의 `router`가 `items`의 것을 덮어쓸 것이고 동시에 둘 다 사용할 수 없을 것입니다.

따라서 같은 파일에서 둘 다 사용할 수 있도록, 하위 모듈을 직접 임포트합니다:

```Python hl_lines="5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### `users`와 `items`의 `APIRouter` 포함하기

이제 하위 모듈 `users`와 `items`의 `router`를 포함시켜봅시다:

```Python hl_lines="10-11" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

/// info

`users.router`는 파일 `app/routers/users.py` 내부의 `APIRouter`를 포함합니다.

그리고 `items.router`는 파일 `app/routers/items.py` 내부의 `APIRouter`를 포함합니다.

///

`app.include_router()`로 각 `APIRouter`를 메인 `FastAPI` 애플리케이션에 추가할 수 있습니다.

해당 라우터의 모든 경로를 그것의 일부로 포함할 것입니다.

/// note | 기술적 세부사항

실제로는 내부적으로 `APIRouter`에서 선언된 각 *경로 동작*에 대해 *경로 동작*을 생성할 것입니다.

따라서 배후에서는 실제로 모든 것이 동일한 단일 앱인 것처럼 작동할 것입니다.

///

/// check

라우터를 포함할 때 성능에 대해 걱정할 필요가 없습니다.

이는 마이크로초가 걸리고 시작 시에만 발생합니다.

따라서 성능에 영향을 주지 않습니다. ⚡

///

### 커스텀 `prefix`, `tags`, `responses`, `dependencies`가 있는 `APIRouter` 포함하기

이제 조직에서 `app/internal/admin.py` 파일을 제공했다고 상상해봅시다.

조직이 여러 프로젝트 간에 공유하는 일부 관리자 *경로 동작*이 있는 `APIRouter`를 포함합니다.

이 예제에서는 매우 간단할 것입니다. 하지만 조직의 다른 프로젝트와 공유되기 때문에, 이를 수정하여 `prefix`, `dependencies`, `tags` 등을 `APIRouter`에 직접 추가할 수 없다고 가정해봅시다:

```Python hl_lines="3" title="app/internal/admin.py"
{!../../docs_src/bigger_applications/app/internal/admin.py!}
```

하지만 `APIRouter`를 포함할 때 모든 *경로 동작*이 `/admin`으로 시작하도록 커스텀 `prefix`를 설정하고, 이 프로젝트에 이미 있는 `dependencies`로 보안을 유지하며, `tags`와 `responses`를 포함하고 싶습니다.

원본 `APIRouter`를 수정하지 않고도 `app.include_router()`에 해당 매개변수를 전달하여 모든 것을 선언할 수 있습니다:

```Python hl_lines="14-17" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

이렇게 하면 원본 `APIRouter`는 수정되지 않은 상태로 유지되므로, 조직의 다른 프로젝트와 동일한 `app/internal/admin.py` 파일을 여전히 공유할 수 있습니다.

결과는 우리 앱에서 `admin` 모듈의 각 *경로 동작*이 다음을 가진다는 것입니다:

* prefix `/admin`.
* 태그 `admin`.
* 의존성 `get_token_header`.
* 응답 `418`. 🍵

하지만 그것은 우리 앱의 해당 `APIRouter`에만 영향을 미치고, 그것을 사용하는 다른 코드에는 영향을 미치지 않습니다.

따라서 예를 들어, 다른 프로젝트는 다른 인증 방법으로 동일한 `APIRouter`를 사용할 수 있습니다.

### *경로 동작* 포함하기

*경로 동작*을 `FastAPI` 앱에 직접 추가할 수도 있습니다.

여기서 그렇게 합니다... 그냥 할 수 있다는 것을 보여주기 위해서입니다 🤷:

```Python hl_lines="21-23" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

그리고 `app.include_router()`로 추가된 다른 모든 *경로 동작*과 함께 올바르게 작동할 것입니다.

/// info | 매우 기술적인 세부사항

**참고**: 이는 아마도 **그냥 건너뛸 수 있는** 매우 기술적인 세부사항입니다.

---

`APIRouter`들은 "마운트"되지 않고, 애플리케이션의 나머지 부분과 분리되지 않습니다.

OpenAPI 스키마와 사용자 인터페이스에 그들의 *경로 동작*을 포함하고 싶기 때문입니다.

그들을 분리하고 나머지와 독립적으로 "마운트"할 수 없으므로, *경로 동작*들은 "복제"(재생성)되고 직접 포함되지 않습니다.

///

## 자동 API 문서 확인하기

이제 앱을 실행하세요:

<div class="termy">

```console
$ fastapi dev app/main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그리고 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 문서를 열어보세요.

모든 하위 모듈의 경로를 포함하여, 올바른 경로(및 prefix)와 올바른 태그를 사용한 자동 API 문서를 볼 수 있습니다:

<img src="/img/tutorial/bigger-applications/image01.png">

## 다른 `prefix`로 동일한 라우터를 여러 번 포함하기

다른 prefix를 사용하여 *동일한* 라우터로 `.include_router()`를 여러 번 사용할 수도 있습니다.

이는 예를 들어 동일한 API를 다른 prefix 하에서 노출하는 데 유용할 수 있습니다. 예: `/api/v1`과 `/api/latest`.

이는 실제로 필요하지 않을 수도 있는 고급 사용법이지만, 필요한 경우를 위해 있습니다.

## 다른 곳에 `APIRouter` 포함하기

`FastAPI` 애플리케이션에 `APIRouter`를 포함할 수 있는 것과 같은 방식으로, 다음을 사용하여 `APIRouter`를 다른 `APIRouter`에 포함할 수 있습니다:

```Python
router.include_router(other_router)
```

`router`를 `FastAPI` 앱에 포함하기 전에 이를 수행하여 `other_router`의 *경로 동작*도 포함되도록 해야 합니다.
