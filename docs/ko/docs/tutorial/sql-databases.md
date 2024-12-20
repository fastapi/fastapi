# SQL (관계형) 데이터베이스

**FastAPI**에서 SQL(관계형) 데이터베이스 사용은 필수가 아닙니다. 여러분이 원하는 **어떤 데이터베이스든** 사용할 수 있습니다.

여기서는 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a>을 사용하는 예제를 살펴보겠습니다.

**SQLModel**은 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>와 Pydantic을 기반으로 구축되었습니다.SQLModel은 **SQL 데이터베이스**를 사용하는 FastAPI 애플리케이션에 완벽히 어울리도록 **FastAPI**의 제작자가 설계한 도구입니다.

/// tip | 팁

다른 SQL 또는 NoSQL 데이터베이스 라이브러리를 사용할 수도 있습니다 (일부는 <abbr title="객체 관계 매퍼(Object Relational Mapper), SQL 테이블을 나타내는 클래스를 제공하고 테이블의 행을 인스턴스로 표현하는 라이브러리를 지칭하는 용어">"ORM"</abbr>이라고도 불립니다), FastAPI는 특정 라이브러리의 사용을 강요하지 않습니다. 😎

///

SQLModel은 SQLAlchemy를 기반으로 하므로, SQLAlchemy에서 **지원하는 모든 데이터베이스**를 손쉽게 사용할 수 있습니다(SQLModel에서도 동일하게 지원됩니다). 예를 들면:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 등.

이 예제에서는 **SQLite**를 사용합니다. SQLite는 단일 파일을 사용하고 파이썬에서 기본적으로 지원하기 때문입니다. 따라서 이 예제를 그대로 복사하여 실행할 수 있습니다.

나중에 실제 프로덕션 애플리케이션에서는 **PostgreSQL**과 같은 데이터베이스 서버를 사용하는 것이 좋습니다.

/// tip | 팁

**FastAPI**와 **PostgreSQL**를 포함하여 프론트엔드와 다양한 도구를 제공하는 공식 프로젝트 생성기가 있습니다: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

이 튜토리얼은 매우 간단하고 짧습니다. 데이터베이스 기본 개념, SQL, 또는 더 복잡한 기능에 대해 배우고 싶다면, <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel 문서</a>를 참고하세요.

## `SQLModel` 설치하기

먼저, [가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화한 다음, `sqlmodel`을 설치하세요:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 단일 모델로 애플리케이션 생성하기

우선 단일 **SQLModel** 모델을 사용하여 애플리케이션의 가장 간단한 첫 번째 버전을 생성해보겠습니다.

이후 **다중 모델**을 추가하여 보안과 유연성을 강화할 것입니다. 🤓

### 모델 생성하기

`SQLModel`을 가져오고 데이터베이스 모델을 생성합니다:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 클래스는 Pydantic 모델과 매우 유사합니다 (실제로 내부적으로 *Pydantic 모델이기도 합니다*).

몇 가지 차이점이 있습니다:

* `table=True`는 SQLModel에 이 모델이 *테이블 모델*이며, 단순한 데이터 모델이 아니라 SQL 데이터베이스의 **테이블**을 나타낸다는 것을 알려줍니다. (다른 일반적인 Pydantic 클래스처럼) 단순한 *데이터 모델*이 아닙니다.

* `Field(primary_key=True)`는 SQLModel에 `id`가 SQL 데이터베이스의 **기본 키**임을 알려줍니다 (SQL 기본 키에 대한 자세한 내용은 SQLModel 문서를 참고하세요).

    `int | None` 유형으로 설정하면, SQLModel은 해당 열이 SQL 데이터베이스에서 `INTEGER` 유형이며 `NULLABLE` 값이어야 한다는 것을 알 수 있습니다.

* `Field(index=True)`는 SQLModel에 해당 열에 대해 **SQL 인덱스**를 생성하도록 지시합니다. 이를 통해 데이터베이스에서 이 열으로 필터링된 데이터를 읽을 때 더 빠르게 조회할 수 있습니다.

    SQLModel은 `str`으로 선언된 항목이 SQL 데이터베이스에서 `TEXT` (또는 데이터베이스에 따라 `VARCHAR`) 유형의 열로 저장된다는 것을 인식합니다.

### 엔진 생성하기

SQLModel의 `engine` (내부적으로는 SQLAlchemy `engine`)은 데이터베이스에 대한 **연결을 유지**하는 역할을 합니다.

**하나의 단일 engine 객체**를 통해 코드 전체에서 동일한 데이터베이스에 연결할 수 있습니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False`를 사용하면 FastAPI에서 여러 스레드에서 동일한 SQLite 데이터베이스를 사용할 수 있습니다. 이는 **하나의 단일 요청**이 **여러 스레드**를 사용할 수 있기 때문에 필요합니다(예: 의존성에서 사용되는 경우).

걱정하지 마세요. 코드가 구조화된 방식으로 인해, 이후에 **각 요청마다 단일 SQLModel *세션*을 사용**하도록 보장할 것입니다. 실제로 그것이 `check_same_thread`가 하려는 것입니다.

### 테이블 생성하기

그 다음 `SQLModel.metadata.create_all(engine)`을 사용하여 모든 *테이블 모델*의 **테이블을 생성**하는 함수를 추가합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 세션 의존성 생성하기

**`Session`**은 **메모리에 객체**를 저장하고 데이터에 필요한 모든 변경 사항을 추적한 후, **`engine`을 통해** 데이터베이스와 통신합니다.

`yield`를 사용해 FastAPI의 **의존성**을 생성하여 각 요청마다 새로운 `Session`을 제공합니다. 이는 요청당 하나의 세션만 사용되도록 보장합니다. 🤓

그런 다음 이 의존성을 사용하는 코드를 간소화하기 위해 `Annotated` 의존성 `SessionDep`을 생성합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 시작 시 데이터베이스 테이블 생성하기

애플리케이션 시작 시 데이터베이스 테이블을 생성합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

여기서는 애플리케이션 시작 이벤트 시 테이블을 생성합니다.

프로덕션 환경에서는 애플리케이션을 시작하기 전에 실행되는 마이그레이션 스크립트를 사용할 가능성이 높습니다. 🤓

/// tip | 팁

SQLModel은 Alembic을 감싸는 마이그레이션 유틸리티를 제공할 예정입니다. 하지만 현재 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>을 직접 사용할 수 있습니다.

///

### Hero 생성하기

각 SQLModel 모델은 Pydantic 모델이기도 하므로, Pydantic 모델을 사용할 수 있는 **타입 어노테이**션에서 동일하게 사용할 수 있습니다.

예를 들어, 파라미터를 `Hero` 타입으로 선언하면 **JSON 본문**에서 값을 읽어옵니다.

마찬가지로, 함수의 **반환 타입**으로 선언하면 해당 데이터의 구조가 자동으로 생성되는 API 문서의 UI에 나타납니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

</details>

여기서 `SessionDep` 의존성 (즉, `Session`)을 사용하여 새로운 `Hero`를 `Session` 인스턴스에 추가하고, 데이터베이스에 변경 사항을 커밋하고, `hero` 데이터의 최신 상태를 갱신한 다음 이를 반환합니다.

### Heroes 조회하기

`select()`를 사용하여 데이터베이스에서 `Hero`를 **조회**할 수 있습니다. 결과에 페이지네이션을 적용하기 위해 `limit`와 `offset`을 포함할 수 있습니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 단일 Hero 조회하기

단일 `Hero`를 **조회**할 수도 있습니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero 삭제하기

`Hero`를 **삭제**하는 것도 가능합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 애플리케이션 실행하기

애플리케이션을 실행하려면 다음 명령을 사용합니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그런 다음 `/docs` UI로 이동하면, **FastAPI**가 해당 **model들**을 사용하여 API **문서를 생성**하는 것으르 확인할 수 있습니다. 또한 이 모델들은 데이터를 직렬화하고 검증하는 데에도 사용됩니다.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 여러 모델로 애플리케이션 업데이트

이제 애플리케이션을 약간 **리팩토링**하여 **보안**과 **유연성**을 개선해 보겠습니다.

이전 애플리케이션의 UI를 보면, 지금까지는 클라이언트가 생성할 `Hero`의 `id`를 직접 지정할 수 있다는 것을 알 수 있습니다. 😱

이는 허용되어선 안 됩니다. 클라이언트가 이미 데이터베이스에 저장된 `id`를 덮어쓸 위험이 있기 때문입니다. `id`는 **백엔드** 또는 **데이터베이스**가 결정해야 하며, **클라이언트**가 결정해서는 안 됩니다.

또한 hero의 `secret_name`을 생성하긴 했지만, 지금까지는 이 값을 어디에서나 반환하고 있습니다. 이는 그다지 **비밀스럽지** 않습니다... 😅

이러한 문제를 해결하기 위해 몇 가지 **추가 모델**을 추가할 것입니다. 바로 여기서 SQLModel이 빛을 발하게 됩니다. ✨

### 여러 모델 생성하기

**SQLModel**에서 `table=True`가 설정된 모델 클래스는 **테이블 모델**입니다.

`table=True`가 없는 모델 클래스는 **데이터 모델**로, 이는 실제로 몇 가지 추가 기능이 포함된 Pydantic 모델에 불과합니다. 🤓

SQLModel을 사용하면 **상속**을 통해 모든 경우에 필드를 **중복 선언하지 않아도** 됩니다.

#### `HeroBase` - 기본 클래스

모든 모델에서 **공유되는 필드**를 가진 `HeroBase` 모델을 시작해 봅시다:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *테이블 모델*

다음으로 실제 *테이블 모델*인 `Hero`를 생성합니다. 이 모델은 다른 모델에는 항상 포함되는 건 아닌 **추가 필드**를 포함합니다:

* `id`
* `secret_name`

`Hero`는 `HeroBase`를 상속하므로 `HeroBase`에 선언된 필드도 포함합니다. 따라서 `Hero`는 다음 **필드들도** 가지게 됩니다:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 공개 *데이터 모델*

다음으로 `HeroPublic` 모델을 생성합니다. 이 모델은 API 클라이언트에 **반환**되는 모델입니다.

`HeroPublic`은 `HeroBase`와 동일한 필드를 가지며, `secret_name`은 포함하지 않습니다.

마침내 우리의 heroes의 정체가 보호됩니다! 🥷

또한 `id: int`를 다시 선언합니다. 이를 통해, API 클라이언트와 **계약**을 맺어 `id`가 항상 존재하며 항상 `int` 타입이라는 것을 보장합니다(`None`이 될 수 없습니다).

/// tip | 팁

반환 모델이 값이 항상 존재하고 항상 `int`(`None`이 아님)를 보장하는 것은 API 클라이언트에게 매우 유용합니다. 이를 통해 API와 통신하는 개발자가 훨씬 더 간단한 코드를 작성할 수 있습니다.

또한 **자동으로 생성된 클라이언트**는 더 단순한 인터페이스를 제공하므로, API와 소통하는 개발자들이 훨씬 수월하게 작업할 수 있습니다. 😎

///

`HeroPublic`의 모든 필드는 `HeroBase`와 동일하며, `id`는 `int`로 선언됩니다(`None`이 아님):

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - hero 생성용 *데이터 모델*

이제 `HeroCreate` 모델을 생성합니다. 이 모델은 클라이언트로부터 받은 데이터를 **검증**하는 역할을 합니다.

`HeroCreate`는 `HeroBase와` 동일한 필드를 가지며, 추가로 `secret_name을` 포함합니다.

클라이언트가 **새 hero을 생성**할 때 `secret_name`을 보내고, 이는 데이터베이스에 저장되지만, 해당 비밀 이름은 API를 통해 클라이언트에게 반환되지 않습니다.

/// tip | 팁

이 방식은 **비밀번호**를 처리하는 방법과 동일합니다. 비밀번호를 받지만, 이를 API에서 반환하지는 않습니다.

비밀번호 값을 저장하기 전에 **해싱**하여 저장하고, **평문으로 저장하지 마십시오**.

///

`HeroCreate`의 필드는 다음과 같습니다:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - hero 수정용 *데이터 모델*

이전 애플리케이션에서는 **hero를 수정**할 방법이 없었지만, 이제 **다중 모델**을 통해 수정 기능을 추가할 수 있습니다. 🎉

`HeroUpdate` *데이터 모델*은 약간 특별한데, 새 hero을 생성할 때 필요한 **모든 동일한 필드**를 가지지만, 모든 필드가 **선택적**(기본값이 있음)입니다. 이렇게 하면 hero을 수정할 때 수정하려는 필드만 보낼 수 있습니다.

모든 **필드가 변경되기** 때문에(타입이 `None`을 포함하고, 기본값이 `None`으로 설정됨), 모든 필드를 **다시 선언**해야 합니다.

엄밀히 말하면 `HeroBase`를 상속할 필요는 없습니다. 모든 필드를 다시 선언하기 때문입니다. 일관성을 위해 상속을 유지하긴 했지만, 필수는 아닙니다. 이는 개인적인 취향의 문제입니다. 🤷

`HeroUpdate`의 필드는 다음과 같습니다:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate`로 생성하고 `HeroPublic` 반환하기

이제 **다중 모델**을 사용하므로 애플리케이션의 관련 부분을 업데이트할 수 있습니다.

요청에서 `HeroCreate` *데이터 모델*을 받아 이를 기반으로 `Hero` *테이블 모델*을 생성합니다.

이 새 *테이블 모델* `Hero`는 클라이언트에서 보낸 필드를 가지며, 데이터베이스에서 생성된 `id`도 포함합니다.

그런 다음 함수를 통해 동일한 *테이블 모델* `Hero`를 반환합니다. 하지만 `response_model`로 `HeroPublic` *데이터 모델*을 선언했기 때문에, **FastAPI**는 `HeroPublic`을 사용하여 데이터를 검증하고 직렬화합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 팁

이제 **반환 타입 주석** `-> HeroPublic` 대신 `response_model=HeroPublic`을 사용합니다. 반환하는 값이 실제로 `HeroPublic`이 *아니기* 때문입니다.

만약 `-> HeroPublic`으로 선언했다면, 에디터와 린터에서 반환값이 `HeroPublic`이 아니라 `Hero`라고 경고했을 것입니다. 이는 적절한 경고입니다.

`response_model`에 선언함으로써 **FastAPI**가 이를 처리하도록 하고, 타입 어노테이션과 에디터 및 다른 도구의 도움에는 영향을 미치지 않도록 설정합니다.

///

### `HeroPublic`으로 Heroes 조회하기

이전과 동일하게 `Hero`를 **조회**할 수 있습니다. 이번에도 `response_model=list[HeroPublic]`을 사용하여 데이터가 올바르게 검증되고 직렬화되도록 보장합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic`으로 단일 Hero 조회하기

단일 hero을 **조회**할 수도 있습니다:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate`로 Hero 수정하기

**hero를 수정**할 수도 있습니다. 이를 위해 HTTP `PATCH` 작업을 사용합니다.

코드에서는 클라이언트가 보낸 데이터를 딕셔너리 형태(`dict`)로 가져옵니다. 이는 **클라이언트가 보낸 데이터만 포함**하며, 기본값으로 들어가는 값은 제외합니다. 이를 위해 `exclude_unset=True`를 사용합니다. 이것이 주요 핵심입니다. 🪄

그런 다음, `hero_db.sqlmodel_update(hero_data)`를 사용하여 `hero_data`의 데이터를 `hero_db`에 업데이트합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Hero 다시 삭제하기

hero **삭제**는 이전과 거의 동일합니다.

이번에는 모든 것을 리팩토링하고 싶은 욕구를 만족시키지 못할 것 같습니다. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### 애플리케이션 다시 실행하기

다음 명령을 사용해 애플리케이션을 다시 실행할 수 있습니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

`/docs` API UI로 이동하면 업데이트된 것을 확인할 수 있습니다. 클라이언트가 영웅을 생성할 때 `id`를 제공할 필요가 없게 되는 등의 변화도 보입니다.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## 요약

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a>을 사용하여 SQL 데이터베이스와 상호작용하고, *데이터 모델* 및 *테이블 모델*로 코드를 간소화할 수 있습니다.

더 많은 내용을 배우고 싶다면, **SQLModel** 문서를 참고하세요. <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">SQLModel을 **FastAPI**와 함께 사용하는 것에 대한 더 긴 미니 튜토리얼</a>도 제공합니다. 🚀
