# SQL (관계형) 데이터베이스 { #sql-relational-databases }

**FastAPI**에서 SQL(관계형) 데이터베이스 사용은 필수가 아닙니다. 하지만 여러분이 원하는 **어떤 데이터베이스든** 사용할 수 있습니다.

여기서는 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a>을 사용하는 예제를 살펴보겠습니다.

**SQLModel**은 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>와 Pydantic을 기반으로 구축되었습니다. **SQL 데이터베이스**를 사용해야 하는 FastAPI 애플리케이션에 완벽히 어울리도록 **FastAPI**와 같은 제작자가 만든 도구입니다.

/// tip | 팁

다른 SQL 또는 NoSQL 데이터베이스 라이브러리를 사용할 수도 있습니다 (일부는 <abbr title="Object Relational Mapper: a fancy term for a library where some classes represent SQL tables and instances represent rows in those tables">"ORMs"</abbr>이라고도 불립니다), FastAPI는 특정 라이브러리의 사용을 강요하지 않습니다. 😎

///

SQLModel은 SQLAlchemy를 기반으로 하므로, SQLAlchemy에서 **지원하는 모든 데이터베이스**를 손쉽게 사용할 수 있습니다(이것들은 SQLModel에서도 지원됩니다). 예를 들면:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 등.

이 예제에서는 **SQLite**를 사용합니다. SQLite는 단일 파일을 사용하고 Python에서 통합 지원하기 때문입니다. 따라서 이 예제를 그대로 복사하여 실행할 수 있습니다.

나중에 프로덕션 애플리케이션에서는 **PostgreSQL**과 같은 데이터베이스 서버를 사용하는 것이 좋습니다.

/// tip | 팁

프론트엔드와 더 많은 도구를 포함하여 **FastAPI**와 **PostgreSQL**을 포함한 공식 프로젝트 생성기가 있습니다: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

이 튜토리얼은 매우 간단하고 짧습니다. 데이터베이스 기본 개념, SQL, 또는 더 고급 기능에 대해 배우고 싶다면, <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel 문서</a>를 참고하세요.

## `SQLModel` 설치하기 { #install-sqlmodel }

먼저, [가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화한 다음, `sqlmodel`을 설치하세요:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 단일 모델로 애플리케이션 생성하기 { #create-the-app-with-a-single-model }

우선 단일 **SQLModel** 모델을 사용하여 애플리케이션의 가장 간단한 첫 번째 버전을 생성해보겠습니다.

이후 아래에서 **여러 모델**로 보안과 유연성을 강화하며 개선하겠습니다. 🤓

### 모델 생성하기 { #create-models }

`SQLModel`을 가져오고 데이터베이스 모델을 생성합니다:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 클래스는 Pydantic 모델과 매우 유사합니다 (실제로 내부적으로 *Pydantic 모델이기도 합니다*).

몇 가지 차이점이 있습니다:

* `table=True`는 SQLModel에 이 모델이 *테이블 모델*이며, SQL 데이터베이스의 **테이블**을 나타내야 한다는 것을 알려줍니다. (다른 일반적인 Pydantic 클래스처럼) 단순한 *데이터 모델*이 아닙니다.

* `Field(primary_key=True)`는 SQLModel에 `id`가 SQL 데이터베이스의 **기본 키**임을 알려줍니다 (SQL 기본 키에 대한 자세한 내용은 SQLModel 문서를 참고하세요).

    **참고:** 기본 키 필드에 `int | None`을 사용하는 이유는, Python 코드에서 *`id` 없이 객체를 생성*할 수 있게 하기 위해서입니다(`id=None`). 데이터베이스가 *저장할 때 생성해 줄 것*이라고 가정합니다. SQLModel은 데이터베이스가 `id`를 제공한다는 것을 이해하고, 데이터베이스 스키마에서 *해당 열을 null이 아닌 `INTEGER`*로 정의합니다. 자세한 내용은 <a href="https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id" class="external-link" target="_blank">기본 키에 대한 SQLModel 문서</a>를 참고하세요.

* `Field(index=True)`는 SQLModel에 해당 열에 대해 **SQL 인덱스**를 생성하도록 지시합니다. 이를 통해 데이터베이스에서 이 열로 필터링된 데이터를 읽을 때 더 빠르게 조회할 수 있습니다.

    SQLModel은 `str`으로 선언된 항목이 SQL 데이터베이스에서 `TEXT` (또는 데이터베이스에 따라 `VARCHAR`) 유형의 열로 저장된다는 것을 인식합니다.

### 엔진 생성하기 { #create-an-engine }

SQLModel의 `engine` (내부적으로는 SQLAlchemy `engine`)은 데이터베이스에 대한 **연결을 유지**하는 역할을 합니다.

코드 전체에서 동일한 데이터베이스에 연결하기 위해 **하나의 단일 `engine` 객체**를 사용합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False`를 사용하면 FastAPI에서 여러 스레드에서 동일한 SQLite 데이터베이스를 사용할 수 있습니다. 이는 **하나의 단일 요청**이 **둘 이상의 스레드**를 사용할 수 있기 때문에 필요합니다(예: 의존성에서 사용되는 경우).

걱정하지 마세요. 코드가 구조화된 방식으로 인해, 이후에 **각 요청마다 단일 SQLModel *세션*을 사용**하도록 보장할 것입니다. 실제로 이것이 `check_same_thread`가 하려는 것입니다.

### 테이블 생성하기 { #create-the-tables }

그 다음 `SQLModel.metadata.create_all(engine)`을 사용하여 모든 *테이블 모델*의 **테이블을 생성**하는 함수를 추가합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 세션 의존성 생성하기 { #create-a-session-dependency }

**`Session`**은 **메모리에 객체**를 저장하고 데이터에 필요한 모든 변경 사항을 추적한 후, **`engine`을 통해** 데이터베이스와 통신합니다.

`yield`를 사용해 FastAPI의 **의존성**을 생성하여 각 요청마다 새로운 `Session`을 제공합니다. 이는 요청당 하나의 세션만 사용되도록 보장합니다. 🤓

그런 다음 이 의존성을 사용하는 나머지 코드를 간소화하기 위해 `Annotated` 의존성 `SessionDep`을 생성합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 시작 시 데이터베이스 테이블 생성하기 { #create-database-tables-on-startup }

애플리케이션 시작 시 데이터베이스 테이블을 생성합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

여기서는 애플리케이션 시작 이벤트 시 테이블을 생성합니다.

프로덕션 환경에서는 애플리케이션을 시작하기 전에 실행되는 마이그레이션 스크립트를 사용할 가능성이 높습니다. 🤓

/// tip | 팁

SQLModel은 Alembic을 감싸는 마이그레이션 유틸리티를 제공할 예정입니다. 하지만 현재 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>을 직접 사용할 수 있습니다.

///

### Hero 생성하기 { #create-a-hero }

각 SQLModel 모델은 Pydantic 모델이기도 하므로, Pydantic 모델을 사용할 수 있는 동일한 **타입 어노테이션**에서 사용할 수 있습니다.

예를 들어, 파라미터를 `Hero` 타입으로 선언하면 **JSON 본문**에서 값을 읽어옵니다.

마찬가지로, 함수의 **반환 타입**으로 선언하면 해당 데이터의 구조가 자동으로 생성되는 API 문서의 UI에 나타납니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

여기서는 `SessionDep` 의존성(`Session`)을 사용하여 새로운 `Hero`를 `Session` 인스턴스에 추가하고, 데이터베이스에 변경 사항을 커밋하고, `hero` 데이터의 최신 상태를 갱신한 다음 이를 반환합니다.

### Heroes 조회하기 { #read-heroes }

`select()`를 사용하여 데이터베이스에서 `Hero`를 **조회**할 수 있습니다. 결과에 페이지네이션을 적용하기 위해 `limit`와 `offset`을 포함할 수 있습니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 단일 Hero 조회하기 { #read-one-hero }

단일 `Hero`를 **조회**할 수도 있습니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero 삭제하기 { #delete-a-hero }

`Hero`를 **삭제**하는 것도 가능합니다.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 애플리케이션 실행하기 { #run-the-app }

애플리케이션을 실행할 수 있습니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그런 다음 `/docs` UI로 이동하면, **FastAPI**가 이 **모델**들을 사용해 API를 **문서화**하고, 데이터를 **직렬화**하고 **검증**하는 데에도 사용하는 것을 확인할 수 있습니다.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 여러 모델로 애플리케이션 업데이트 { #update-the-app-with-multiple-models }

이제 이 애플리케이션을 약간 **리팩터링**하여 **보안**과 **유연성**을 개선해 보겠습니다.

이전 애플리케이션을 확인해 보면, 지금까지는 UI에서 클라이언트가 생성할 `Hero`의 `id`를 결정할 수 있게 되어 있는 것을 볼 수 있습니다. 😱

이렇게 해서는 안 됩니다. 클라이언트가 DB에 이미 할당되어 있는 `id`를 덮어쓸 수 있기 때문입니다. `id`를 결정하는 것은 **백엔드** 또는 **데이터베이스**가 해야 하며, **클라이언트**가 해서는 안 됩니다.

또한 hero에 대한 `secret_name`을 생성하지만, 지금까지는 이 값을 어디에서나 반환하고 있습니다. 이는 그다지 **비밀스럽지** 않습니다... 😅

이러한 문제는 몇 가지 **추가 모델**을 추가해 해결하겠습니다. 바로 여기서 SQLModel이 빛을 발하게 됩니다. ✨

### 여러 모델 생성하기 { #create-multiple-models }

**SQLModel**에서 `table=True`가 설정된 모델 클래스는 **테이블 모델**입니다.

그리고 `table=True`가 없는 모델 클래스는 **데이터 모델**인데, 이것들은 실제로는 (몇 가지 작은 추가 기능이 있는) Pydantic 모델일 뿐입니다. 🤓

SQLModel을 사용하면 **상속**을 통해 모든 경우에 필드를 **중복 선언하지 않아도** 됩니다.

#### `HeroBase` - 기본 클래스 { #herobase-the-base-class }

모든 모델에서 **공유되는 필드**를 가진 `HeroBase` 모델을 시작해 봅시다:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *테이블 모델* { #hero-the-table-model }

다음으로 실제 *테이블 모델*인 `Hero`를 생성합니다. 이 모델은 다른 모델에는 항상 포함되는 건 아닌 **추가 필드**를 포함합니다:

* `id`
* `secret_name`

`Hero`는 `HeroBase`를 상속하므로 `HeroBase`에 선언된 필드도 **또한** 포함합니다. 따라서 `Hero`의 모든 필드는 다음과 같습니다:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 공개 *데이터 모델* { #heropublic-the-public-data-model }

다음으로 `HeroPublic` 모델을 생성합니다. 이 모델은 API 클라이언트에 **반환**되는 모델입니다.

`HeroPublic`은 `HeroBase`와 동일한 필드를 가지므로, `secret_name`은 포함하지 않습니다.

마침내 우리의 heroes의 정체가 보호됩니다! 🥷

또한 `id: int`를 다시 선언합니다. 이를 통해, API 클라이언트와 **계약**을 맺어 `id`가 항상 존재하며 항상 `int` 타입이라는 것을 보장합니다(`None`이 될 수 없습니다).

/// tip | 팁

반환 모델이 값이 항상 존재하고 항상 `int`(`None`이 아님)를 보장하는 것은 API 클라이언트에게 매우 유용합니다. 이를 통해 API 클라이언트는 이런 확신을 바탕으로 훨씬 더 간단한 코드를 작성할 수 있습니다.

또한 **자동으로 생성된 클라이언트**는 더 단순한 인터페이스를 제공하므로, API와 소통하는 개발자들이 API를 사용하면서 훨씬 더 좋은 경험을 할 수 있습니다. 😎

///

`HeroPublic`의 모든 필드는 `HeroBase`와 동일하며, `id`는 `int`로 선언됩니다(`None`이 아님):

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - hero 생성용 *데이터 모델* { #herocreate-the-data-model-to-create-a-hero }

이제 `HeroCreate` 모델을 생성합니다. 이 모델은 클라이언트로부터 받은 데이터를 **검증**하는 역할을 합니다.

`HeroCreate`는 `HeroBase`와 동일한 필드를 가지며, `secret_name`도 포함합니다.

이제 클라이언트가 **새 hero를 생성**할 때 `secret_name`을 보내면, 데이터베이스에 저장되지만, 그 비밀 이름은 API를 통해 클라이언트에게 반환되지 않습니다.

/// tip | 팁

이 방식은 **비밀번호**를 처리하는 방법과 동일합니다. 비밀번호를 받지만, 이를 API에서 반환하지는 않습니다.

또한 비밀번호 값을 저장하기 전에 **해싱**하여 저장하고, **평문으로 저장하지 마십시오**.

///

`HeroCreate`의 필드는 다음과 같습니다:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - hero 수정용 *데이터 모델* { #heroupdate-the-data-model-to-update-a-hero }

이전 버전의 애플리케이션에서는 **hero를 수정**할 방법이 없었지만, 이제 **여러 모델**로 이를 할 수 있습니다. 🎉

`HeroUpdate` *데이터 모델*은 약간 특별한데, 새 hero를 생성할 때 필요한 **모든 동일한 필드**를 가지지만, 모든 필드가 **선택적**(기본값이 있음)입니다. 이렇게 하면 hero를 수정할 때 수정하려는 필드만 보낼 수 있습니다.

모든 **필드가 실제로 변경**되기 때문에(타입이 이제 `None`을 포함하고, 기본값도 이제 `None`이 됨), 우리는 필드를 **다시 선언**해야 합니다.

`HeroBase`를 상속할 필요는 없습니다. 모든 필드를 다시 선언하기 때문입니다. 일관성을 위해 상속을 유지하긴 했지만, 필수는 아닙니다. 이는 개인적인 취향의 문제입니다. 🤷

`HeroUpdate`의 필드는 다음과 같습니다:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate`로 생성하고 `HeroPublic` 반환하기 { #create-with-herocreate-and-return-a-heropublic }

이제 **여러 모델**을 사용하므로 애플리케이션의 관련 부분을 업데이트할 수 있습니다.

요청에서 `HeroCreate` *데이터 모델*을 받아 이를 기반으로 `Hero` *테이블 모델*을 생성합니다.

이 새 *테이블 모델* `Hero`는 클라이언트에서 보낸 필드를 가지며, 데이터베이스에서 생성된 `id`도 포함합니다.

그런 다음 함수를 통해 동일한 *테이블 모델* `Hero`를 그대로 반환합니다. 하지만 `response_model`로 `HeroPublic` *데이터 모델*을 선언했기 때문에, **FastAPI**는 `HeroPublic`을 사용하여 데이터를 검증하고 직렬화합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 팁

이제 **반환 타입 어노테이션** `-> HeroPublic` 대신 `response_model=HeroPublic`을 사용합니다. 반환하는 값이 실제로 `HeroPublic`이 *아니기* 때문입니다.

만약 `-> HeroPublic`으로 선언했다면, 에디터와 린터에서 `HeroPublic` 대신 `Hero`를 반환한다고 (당연히) 불평할 것입니다.

`response_model`에 선언함으로써 **FastAPI**가 처리하도록 하고, 타입 어노테이션과 에디터 및 다른 도구의 도움에는 영향을 미치지 않도록 합니다.

///

### `HeroPublic`으로 Heroes 조회하기 { #read-heroes-with-heropublic }

이전과 동일하게 `Hero`를 **조회**할 수 있습니다. 이번에도 `response_model=list[HeroPublic]`을 사용하여 데이터가 올바르게 검증되고 직렬화되도록 보장합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic`으로 단일 Hero 조회하기 { #read-one-hero-with-heropublic }

단일 hero를 **조회**할 수도 있습니다:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate`로 Hero 수정하기 { #update-a-hero-with-heroupdate }

**hero를 수정**할 수도 있습니다. 이를 위해 HTTP `PATCH` 작업을 사용합니다.

그리고 코드에서는 클라이언트가 보낸 모든 데이터가 담긴 `dict`를 가져오는데, **클라이언트가 보낸 데이터만** 포함하고, 기본값이어서 들어가 있는 값은 제외합니다. 이를 위해 `exclude_unset=True`를 사용합니다. 이것이 주요 핵심입니다. 🪄

그런 다음, `hero_db.sqlmodel_update(hero_data)`를 사용하여 `hero_data`의 데이터로 `hero_db`를 업데이트합니다.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Hero 다시 삭제하기 { #delete-a-hero-again }

hero **삭제**는 이전과 거의 동일합니다.

이번에는 모든 것을 리팩터링하고 싶은 욕구를 만족시키지 못하겠습니다. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### 애플리케이션 다시 실행하기 { #run-the-app-again }

애플리케이션을 다시 실행할 수 있습니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

`/docs` API UI로 이동하면 이제 업데이트되어 있고, hero를 생성할 때 클라이언트가 `id`를 보낼 것이라고 기대하지 않는 것 등을 확인할 수 있습니다.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## 요약 { #recap }

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a>을 사용하여 SQL 데이터베이스와 상호작용하고, *데이터 모델* 및 *테이블 모델*로 코드를 간소화할 수 있습니다.

더 많은 내용을 배우려면 **SQLModel** 문서를 참고하세요. **FastAPI**와 함께 SQLModel을 사용하는 더 긴 미니 <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">튜토리얼</a>도 있습니다. 🚀
