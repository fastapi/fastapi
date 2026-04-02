# 더 큰 애플리케이션 - 여러 파일 { #bigger-applications-multiple-files }

애플리케이션이나 웹 API를 만들 때, 모든 것을 하나의 파일에 담을 수 있는 경우는 드뭅니다.

**FastAPI**는 모든 유연성을 유지하면서도 애플리케이션을 구조화할 수 있게 해주는 편리한 도구를 제공합니다.

/// info | 정보

Flask를 사용해 보셨다면, 이는 Flask의 Blueprints에 해당하는 개념입니다.

///

## 예시 파일 구조 { #an-example-file-structure }

다음과 같은 파일 구조가 있다고 해봅시다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | 팁

`__init__.py` 파일이 여러 개 있습니다: 각 디렉터리 또는 하위 디렉터리에 하나씩 있습니다.

이 파일들이 한 파일의 코드를 다른 파일로 import할 수 있게 해줍니다.

예를 들어 `app/main.py`에는 다음과 같은 줄이 있을 수 있습니다:

```
from app.routers import items
```

///

* `app` 디렉터리에는 모든 것이 들어 있습니다. 그리고 비어 있는 파일 `app/__init__.py`가 있어 "Python package"(“Python modules”의 모음)인 `app`이 됩니다.
* `app/main.py` 파일이 있습니다. Python package(`__init__.py` 파일이 있는 디렉터리) 안에 있으므로, 이 package의 "module"입니다: `app.main`.
* `app/dependencies.py` 파일도 있습니다. `app/main.py`와 마찬가지로 "module"입니다: `app.dependencies`.
* `app/routers/` 하위 디렉터리가 있고, 여기에 또 `__init__.py` 파일이 있으므로 "Python subpackage"입니다: `app.routers`.
* `app/routers/items.py` 파일은 `app/routers/` package 안에 있으므로, submodule입니다: `app.routers.items`.
* `app/routers/users.py`도 동일하게 또 다른 submodule입니다: `app.routers.users`.
* `app/internal/` 하위 디렉터리도 있고 여기에 `__init__.py`가 있으므로 또 다른 "Python subpackage"입니다: `app.internal`.
* 그리고 `app/internal/admin.py` 파일은 또 다른 submodule입니다: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

같은 파일 구조에 주석을 추가하면 다음과 같습니다:

```bash
.
├── app                  # 'app'은 Python 패키지입니다
│   ├── __init__.py      # 이 파일로 'app'이 'Python 패키지'가 됩니다
│   ├── main.py          # 'main' 모듈, 예: import app.main
│   ├── dependencies.py  # 'dependencies' 모듈, 예: import app.dependencies
│   └── routers          # 'routers'는 'Python 하위 패키지'입니다
│   │   ├── __init__.py  # 이 파일로 'routers'가 'Python 하위 패키지'가 됩니다
│   │   ├── items.py     # 'items' 서브모듈, 예: import app.routers.items
│   │   └── users.py     # 'users' 서브모듈, 예: import app.routers.users
│   └── internal         # 'internal'은 'Python 하위 패키지'입니다
│       ├── __init__.py  # 이 파일로 'internal'이 'Python 하위 패키지'가 됩니다
│       └── admin.py     # 'admin' 서브모듈, 예: import app.internal.admin
```

## `APIRouter` { #apirouter }

사용자만 처리하는 전용 파일이 `/app/routers/users.py`의 submodule이라고 해봅시다.

코드를 정리하기 위해 사용자와 관련된 *path operations*를 나머지 코드와 분리해 두고 싶을 것입니다.

하지만 이것은 여전히 같은 **FastAPI** 애플리케이션/웹 API의 일부입니다(같은 "Python Package"의 일부입니다).

`APIRouter`를 사용해 해당 모듈의 *path operations*를 만들 수 있습니다.

### `APIRouter` import하기 { #import-apirouter }

`FastAPI` 클래스와 동일한 방식으로 import하고 "instance"를 생성합니다:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### `APIRouter`로 *path operations* 만들기 { #path-operations-with-apirouter }

그 다음 이를 사용해 *path operations*를 선언합니다.

`FastAPI` 클래스를 사용할 때와 동일한 방식으로 사용합니다:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

`APIRouter`는 "미니 `FastAPI`" 클래스라고 생각할 수 있습니다.

동일한 옵션들이 모두 지원됩니다.

동일한 `parameters`, `responses`, `dependencies`, `tags` 등등.

/// tip | 팁

이 예시에서는 변수 이름이 `router`이지만, 원하는 이름으로 지어도 됩니다.

///

이제 이 `APIRouter`를 메인 `FastAPI` 앱에 포함(include)할 것이지만, 먼저 dependencies와 다른 `APIRouter` 하나를 확인해 보겠습니다.

## Dependencies { #dependencies }

애플리케이션의 여러 위치에서 사용되는 dependencies가 일부 필요하다는 것을 알 수 있습니다.

그래서 이를 별도의 `dependencies` 모듈(`app/dependencies.py`)에 둡니다.

이제 간단한 dependency를 사용해 커스텀 `X-Token` 헤더를 읽어 보겠습니다:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | 팁

이 예시를 단순화하기 위해 임의로 만든 헤더를 사용하고 있습니다.

하지만 실제 상황에서는 통합된 [Security 유틸리티](security/index.md)를 사용하는 것이 더 좋은 결과를 얻을 수 있습니다.

///

## `APIRouter`가 있는 또 다른 모듈 { #another-module-with-apirouter }

애플리케이션의 "items"를 처리하는 전용 endpoint들도 `app/routers/items.py` 모듈에 있다고 해봅시다.

여기에는 다음에 대한 *path operations*가 있습니다:

* `/items/`
* `/items/{item_id}`

구조는 `app/routers/users.py`와 완전히 동일합니다.

하지만 우리는 조금 더 똑똑하게, 코드를 약간 단순화하고 싶습니다.

이 모듈의 모든 *path operations*에는 다음이 동일하게 적용됩니다:

* 경로 `prefix`: `/items`.
* `tags`: (태그 하나: `items`).
* 추가 `responses`.
* `dependencies`: 모두 우리가 만든 `X-Token` dependency가 필요합니다.

따라서 각 *path operation*마다 매번 모두 추가하는 대신, `APIRouter`에 한 번에 추가할 수 있습니다.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

각 *path operation*의 경로는 다음처럼 `/`로 시작해야 하므로:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...prefix에는 마지막 `/`가 포함되면 안 됩니다.

따라서 이 경우 prefix는 `/items`입니다.

또한 이 router에 포함된 모든 *path operations*에 적용될 `tags` 목록과 추가 `responses`도 넣을 수 있습니다.

그리고 router의 모든 *path operations*에 추가될 `dependencies` 목록도 추가할 수 있으며, 해당 경로들로 들어오는 각 요청마다 실행/해결됩니다.

/// tip | 팁

[*path operation decorator의 dependencies*](dependencies/dependencies-in-path-operation-decorators.md)와 마찬가지로, *path operation function*에 어떤 값도 전달되지 않습니다.

///

최종적으로 item 경로는 다음과 같습니다:

* `/items/`
* `/items/{item_id}`

...의도한 그대로입니다.

* 단일 문자열 `"items"`를 포함하는 태그 목록으로 표시됩니다.
    * 이 "tags"는 자동 대화형 문서 시스템(OpenAPI 사용)에 특히 유용합니다.
* 모두 미리 정의된 `responses`를 포함합니다.
* 이 모든 *path operations*는 실행되기 전에 `dependencies` 목록이 평가/실행됩니다.
    * 특정 *path operation*에 dependencies를 추가로 선언하면 **그것들도 실행됩니다**.
    * router dependencies가 먼저 실행되고, 그 다음에 [decorator의 `dependencies`](dependencies/dependencies-in-path-operation-decorators.md), 그리고 일반 파라미터 dependencies가 실행됩니다.
    * [`scopes`가 있는 `Security` dependencies](../advanced/security/oauth2-scopes.md)도 추가할 수 있습니다.

/// tip | 팁

`APIRouter`에 `dependencies`를 두는 것은 예를 들어 전체 *path operations* 그룹에 인증을 요구할 때 사용할 수 있습니다. 각 경로 처리에 개별적으로 dependencies를 추가하지 않아도 됩니다.

///

/// check | 확인

`prefix`, `tags`, `responses`, `dependencies` 파라미터는 (다른 많은 경우와 마찬가지로) 코드 중복을 피하도록 도와주는 **FastAPI**의 기능입니다.

///

### dependencies import하기 { #import-the-dependencies }

이 코드는 모듈 `app.routers.items`, 파일 `app/routers/items.py`에 있습니다.

그리고 dependency 함수는 모듈 `app.dependencies`, 파일 `app/dependencies.py`에서 가져와야 합니다.

그래서 dependencies에 대해 `..`를 사용하는 상대 import를 사용합니다:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### 상대 import가 동작하는 방식 { #how-relative-imports-work }

/// tip | 팁

import가 동작하는 방식을 완벽히 알고 있다면, 아래 다음 섹션으로 넘어가세요.

///

다음과 같이 점 하나 `.`를 쓰면:

```Python
from .dependencies import get_token_header
```

의미는 다음과 같습니다:

* 이 모듈(파일 `app/routers/items.py`)이 속한 같은 package(디렉터리 `app/routers/`)에서 시작해서...
* `dependencies` 모듈(가상의 파일 `app/routers/dependencies.py`)을 찾고...
* 그 안에서 함수 `get_token_header`를 import합니다.

하지만 그 파일은 존재하지 않습니다. dependencies는 `app/dependencies.py` 파일에 있습니다.

우리 앱/파일 구조를 다시 떠올려 보세요:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

다음처럼 점 두 개 `..`를 쓰면:

```Python
from ..dependencies import get_token_header
```

의미는 다음과 같습니다:

* 이 모듈(파일 `app/routers/items.py`)이 속한 같은 package(디렉터리 `app/routers/`)에서 시작해서...
* 상위 package(디렉터리 `app/`)로 올라가고...
* 그 안에서 `dependencies` 모듈(파일 `app/dependencies.py`)을 찾고...
* 그 안에서 함수 `get_token_header`를 import합니다.

이렇게 하면 제대로 동작합니다! 🎉

---

같은 방식으로 점 세 개 `...`를 사용했다면:

```Python
from ...dependencies import get_token_header
```

의미는 다음과 같습니다:

* 이 모듈(파일 `app/routers/items.py`)이 속한 같은 package(디렉터리 `app/routers/`)에서 시작해서...
* 상위 package(디렉터리 `app/`)로 올라가고...
* 그 package의 상위로 또 올라가는데(상위 package가 없습니다, `app`이 최상위입니다 😱)...
* 그 안에서 `dependencies` 모듈(파일 `app/dependencies.py`)을 찾고...
* 그 안에서 함수 `get_token_header`를 import합니다.

이는 `app/` 위쪽의 어떤 package(자신의 `__init__.py` 파일 등을 가진)에 대한 참조가 됩니다. 하지만 우리는 그런 것이 없습니다. 그래서 이 예시에서는 에러가 발생합니다. 🚨

이제 어떻게 동작하는지 알았으니, 앱이 얼마나 복잡하든 상대 import를 사용할 수 있습니다. 🤓

### 커스텀 `tags`, `responses`, `dependencies` 추가하기 { #add-some-custom-tags-responses-and-dependencies }

`APIRouter`에 이미 prefix `/items`와 `tags=["items"]`를 추가했기 때문에 각 *path operation*에 이를 추가하지 않습니다.

하지만 특정 *path operation*에만 적용될 _추가_ `tags`를 더할 수도 있고, 그 *path operation* 전용의 추가 `responses`도 넣을 수 있습니다:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | 팁

이 마지막 경로 처리는 `["items", "custom"]` 태그 조합을 갖게 됩니다.

그리고 문서에는 `404`용 응답과 `403`용 응답, 두 가지 모두가 표시됩니다.

///

## 메인 `FastAPI` { #the-main-fastapi }

이제 `app/main.py` 모듈을 봅시다.

여기에서 `FastAPI` 클래스를 import하고 사용합니다.

이 파일은 모든 것을 하나로 엮는 애플리케이션의 메인 파일이 될 것입니다.

그리고 대부분의 로직이 각자의 특정 모듈로 분리되어 있으므로, 메인 파일은 꽤 단순해집니다.

### `FastAPI` import하기 { #import-fastapi }

평소처럼 `FastAPI` 클래스를 import하고 생성합니다.

또한 각 `APIRouter`의 dependencies와 결합될 [global dependencies](dependencies/global-dependencies.md)도 선언할 수 있습니다:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### `APIRouter` import하기 { #import-the-apirouter }

이제 `APIRouter`가 있는 다른 submodule들을 import합니다:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

`app/routers/users.py`와 `app/routers/items.py` 파일은 같은 Python package `app`에 속한 submodule들이므로, 점 하나 `.`를 사용해 "상대 import"로 가져올 수 있습니다.

### import가 동작하는 방식 { #how-the-importing-works }

다음 구문은:

```Python
from .routers import items, users
```

의미는 다음과 같습니다:

* 이 모듈(파일 `app/main.py`)이 속한 같은 package(디렉터리 `app/`)에서 시작해서...
* subpackage `routers`(디렉터리 `app/routers/`)를 찾고...
* 그 안에서 submodule `items`(파일 `app/routers/items.py`)와 `users`(파일 `app/routers/users.py`)를 import합니다...

`items` 모듈에는 `router` 변수(`items.router`)가 있습니다. 이는 `app/routers/items.py` 파일에서 만든 것과 동일하며 `APIRouter` 객체입니다.

그리고 `users` 모듈도 같은 방식입니다.

다음처럼 import할 수도 있습니다:

```Python
from app.routers import items, users
```

/// info | 정보

첫 번째 버전은 "상대 import"입니다:

```Python
from .routers import items, users
```

두 번째 버전은 "절대 import"입니다:

```Python
from app.routers import items, users
```

Python Packages와 Modules에 대해 더 알아보려면 [Modules에 대한 Python 공식 문서](https://docs.python.org/3/tutorial/modules.html)를 읽어보세요.

///

### 이름 충돌 피하기 { #avoid-name-collisions }

submodule `items`를 직접 import하고, 그 안의 `router` 변수만 import하지는 않습니다.

이는 submodule `users`에도 `router`라는 이름의 변수가 있기 때문입니다.

만약 다음처럼 순서대로 import했다면:

```Python
from .routers.items import router
from .routers.users import router
```

`users`의 `router`가 `items`의 `router`를 덮어써서 동시에 사용할 수 없게 됩니다.

따라서 같은 파일에서 둘 다 사용할 수 있도록 submodule들을 직접 import합니다:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### `users`와 `items`용 `APIRouter` 포함하기 { #include-the-apirouters-for-users-and-items }

이제 submodule `users`와 `items`의 `router`를 포함해 봅시다:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | 정보

`users.router`는 `app/routers/users.py` 파일 안의 `APIRouter`를 담고 있습니다.

`items.router`는 `app/routers/items.py` 파일 안의 `APIRouter`를 담고 있습니다.

///

`app.include_router()`로 각 `APIRouter`를 메인 `FastAPI` 애플리케이션에 추가할 수 있습니다.

그 router의 모든 route가 애플리케이션의 일부로 포함됩니다.

/// note | 기술 세부사항

내부적으로는 `APIRouter`에 선언된 각 *path operation*마다 *path operation*을 실제로 생성합니다.

즉, 내부적으로는 모든 것이 동일한 하나의 앱인 것처럼 동작합니다.

///

/// check | 확인

router를 포함(include)할 때 성능을 걱정할 필요는 없습니다.

이 작업은 마이크로초 단위이며 시작 시에만 발생합니다.

따라서 성능에 영향을 주지 않습니다. ⚡

///

### 커스텀 `prefix`, `tags`, `responses`, `dependencies`로 `APIRouter` 포함하기 { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

이제 조직에서 `app/internal/admin.py` 파일을 받았다고 가정해 봅시다.

여기에는 조직에서 여러 프로젝트 간에 공유하는 관리자용 *path operations*가 있는 `APIRouter`가 들어 있습니다.

이 예시에서는 매우 단순하게 만들겠습니다. 하지만 조직 내 다른 프로젝트와 공유되기 때문에, 이를 수정할 수 없어 `prefix`, `dependencies`, `tags` 등을 `APIRouter`에 직접 추가할 수 없다고 해봅시다:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

하지만 `APIRouter`를 포함할 때 커스텀 `prefix`를 지정해 모든 *path operations*가 `/admin`으로 시작하게 하고, 이 프로젝트에서 이미 가진 `dependencies`로 보호하고, `tags`와 `responses`도 포함하고 싶습니다.

원래 `APIRouter`를 수정하지 않고도 `app.include_router()`에 파라미터를 전달해서 이를 선언할 수 있습니다:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

이렇게 하면 원래 `APIRouter`는 수정되지 않으므로, 조직 내 다른 프로젝트에서도 동일한 `app/internal/admin.py` 파일을 계속 공유할 수 있습니다.

결과적으로 우리 앱에서 `admin` 모듈의 각 *path operations*는 다음을 갖게 됩니다:

* prefix `/admin`.
* tag `admin`.
* dependency `get_token_header`.
* 응답 `418`. 🍵

하지만 이는 우리 앱에서 그 `APIRouter`에만 영향을 주며, 이를 사용하는 다른 코드에는 영향을 주지 않습니다.

따라서 다른 프로젝트들은 같은 `APIRouter`를 다른 인증 방식으로 사용할 수도 있습니다.

### *path operation* 포함하기 { #include-a-path-operation }

*path operations*를 `FastAPI` 앱에 직접 추가할 수도 있습니다.

여기서는 가능하다는 것을 보여주기 위해... 그냥 해봅니다 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

그리고 `app.include_router()`로 추가한 다른 모든 *path operations*와 함께 올바르게 동작합니다.

/// info | 매우 기술적인 세부사항

**참고**: 이는 매우 기술적인 세부사항이라 아마 **그냥 건너뛰어도 됩니다**.

---

`APIRouter`는 "mount"되는 것이 아니며, 애플리케이션의 나머지 부분과 격리되어 있지 않습니다.

이는 OpenAPI 스키마와 사용자 인터페이스에 그들의 *path operations*를 포함시키고 싶기 때문입니다.

나머지와 독립적으로 격리해 "mount"할 수 없으므로, *path operations*는 직접 포함되는 것이 아니라 "clone"(재생성)됩니다.

///

## `pyproject.toml`에서 `entrypoint` 구성하기 { #configure-the-entrypoint-in-pyproject-toml }

FastAPI `app` 객체가 `app/main.py`에 있으므로 `pyproject.toml` 파일에서 `entrypoint`를 다음과 같이 구성할 수 있습니다:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

이는 다음과 같이 import하는 것과 동일합니다:

```python
from app.main import app
```

이렇게 하면 `fastapi` 명령어가 여러분의 앱이 어디에 있는지 알 수 있습니다.

/// Note | 참고

명령어에 경로를 직접 전달할 수도 있습니다:

```console
$ fastapi dev app/main.py
```

하지만 `fastapi` 명령어를 실행할 때마다 올바른 경로를 기억해 전달해야 합니다.

또한 [VS Code 확장](../editor-support.md)이나 [FastAPI Cloud](https://fastapicloud.com) 같은 다른 도구들이 이를 찾지 못할 수도 있으므로, `pyproject.toml`의 `entrypoint`를 사용하는 것을 권장합니다.

///

## 자동 API 문서 확인하기 { #check-the-automatic-api-docs }

이제 앱을 실행하세요:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그리고 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)에서 문서를 여세요.

올바른 경로(및 prefix)와 올바른 태그를 사용해, 모든 submodule의 경로를 포함한 자동 API 문서를 볼 수 있습니다:

<img src="/img/tutorial/bigger-applications/image01.png">

## 같은 router를 다른 `prefix`로 여러 번 포함하기 { #include-the-same-router-multiple-times-with-different-prefix }

`.include_router()`를 사용해 *같은* router를 서로 다른 prefix로 여러 번 포함할 수도 있습니다.

예를 들어 `/api/v1`과 `/api/latest`처럼 서로 다른 prefix로 동일한 API를 노출할 때 유용할 수 있습니다.

이는 고급 사용 방식이라 실제로 필요하지 않을 수도 있지만, 필요할 때를 위해 제공됩니다.

## `APIRouter`에 다른 `APIRouter` 포함하기 { #include-an-apirouter-in-another }

`APIRouter`를 `FastAPI` 애플리케이션에 포함할 수 있는 것과 같은 방식으로, 다음을 사용해 `APIRouter`를 다른 `APIRouter`에 포함할 수 있습니다:

```Python
router.include_router(other_router)
```

`FastAPI` 앱에 `router`를 포함하기 전에 수행해야 하며, 그래야 `other_router`의 *path operations*도 함께 포함됩니다.
