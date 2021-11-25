# SQL (관계형) 데이터베이스

**FastAPI**에서 반드시 SQL(관계형) 데이터베이스를 사용해야하는 것은 아닙니다.

하지만 원한다면 어떤 관계형 데이터베이스도 사용할 수 있습니다.

이 문서에서는 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>를 사용한 예시를 보게 될 것입니다.

SQLAlchemy가 지원하는 어느 데이터베이스든 쉽게 적용할 수 있습니다:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 등.

하나의 파일을 사용하고 파이썬이 통합된 지원을 제공하기 때문에, 이 예시에서는 **SQLite**를 사용할 것입니다. 따라서 동 예시를 복사해서 그대로 실행할 수 있습니다.

추후 프로덕션용 응용 프로그램에는 **PostgreSQL**과 같은 데이터베이스 서버를 사용할 수 있습니다.

!!! tip "팁" 
    **도커**를 기반으로 하고, 프론트엔드와 많은 도구들을 포함한 **FastAPI** 및 **PostgreSQL**을 사용하는 공식적인 프로젝트 생성기가 있습니다: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! note "참고"
    대부분의 코드는 모든 프레임워크에서 사용하는 표준 `SQLAlchemy` 코드입니다.

    **FastAPI** 특정 코드는 언제나 그렇듯 많지 않습니다.

## ORM(객체 관계 매핑)

**FastAPI**는 모든 데이터베이스 및 모든 스타일의 라이브러리에서 동작하며 데이터베이스와 통신합니다.

흔한 패턴 중 하나는 "객체 관계 매핑(ORM, object-relational mapping 라이브러리)"을 사용하는 것입니다.

ORM에는 코드의 *객체*(*object*)와 데이터베이스 테이블(*"관계: relation"*)간 변환(*"매핑: mapping"*)을 하는 도구들이 있습니다.

ORM을 사용하여, SQL 데이터베이스의 테이블을 나타내는 클래스와, 이름과 형을 가진 열을 나타내는 해당 클래스의 각 속성들을 생성합니다.

예를들어 클래스 `Pet` 은 SQL 테이블 `pets` 을 나타낼 수 있습니다.

그리고 해당 클래스의 각 인스턴스 객체는 데이터베이스의 행을 나타냅니다.

예를들어 `Pet` 의 인스턴스인 `orion_cat` 객체는 `type` 열에 대해 `orion_cat.type` 속성을 가질 수 있습니다. 그리고 속성의 값은 일례로, `"cat"` 이 될 수 있습니다.

이러한 ORM에는 테이블 또는 개체 사이의 연결이나 관계를 생성하는 도구들이 있습니다.

이를 통해  `orion_cat.owner` 속성을 가질 수 있으며, owner(주인)은 *owners* 테이블로부터 가져온 pet(반려동물)의 owner(주인)에 대한 데이터를 포함합니다.

따라서, `orion_cat.owner.name` 은 `owners` 테이블의 `name` 에서 가져온 반려동물 주인의 이름이 될 수 있습니다.

이는 `"Arquilian"` 와 같은 값이 될 것입니다.

그리고 ORM은 반려동물(pet) 객체에서 *주인(owners)* 테이블로 접근하려고 할 때 해당 테이블로부터 정보를 얻기 위한 모든 작업을 수행합니다.

많이 사용되는 ORM에는 다음의 것들이 있습니다: Django-ORM (Django 프레임워크의 일부), SQLAlchemy ORM(프레임워크와 독립적인, SQLAlchemy의 일부), Peewee(프레임워크로부터 독립적).

여기서 우리는 **SQLAlchemy ORM**을 사용해 작업하는 방법을 살펴볼 것입니다.

비슷한 방법으로 다른 모든 ORM을 사용할 수 있습니다.

!!! tip "팁"
    Peewee를 사용하는 문서도 제공되고 있습니다.

## 파일 구조

이 예시에서, 다음과 같은 구조를 가진  `sql_app`을 하위 디렉터리로 갖는  `my_super_project` 라는 디렉터리가 있다고 가정해보겠습니다:

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

`__init__.py` 는 빈 파일이지만, 파이썬에게 `sql_app`과 이것의 모든 모듈들(파이썬 파일들)이 패키지라는 것을 알려줍니다.

이제 각각의 파일/모듈이 어떤 일을 하는지 봅시다.

## SQLAlchemy 부분 생성

`sql_app/database.py` 파일을 봅시다.

### SQLAlchemy 부분 임포트

```Python hl_lines="1-3"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### SQLAlchemy을 위한 데이터베이스 URL 생성

```Python hl_lines="5-6"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

이 예시에서, SQLite 데이터베이스와 "연결"합니다(SQLite 데이터베이스를 사용해 파일 열기).

해당 파일은 `sql_app.db` 파일과 동일한 디렉토리에 위치할 것입니다.

마지막 부분이 `./sql_app.db` 인 이유입니다.

**PostgreSQL**을 사용하는 경우, 하기 행의 주석 처리를 제거하면 됩니다.

```Python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
```

그리고 데이터베이스 데이터 및 자격증명(credentials)을 조정하세요(MySQL, MariaDB, 기타 다른 데이터베이스도 동일).

!!! tip "팁"

    이것은 다른 데이터베이스를 사용하고자 할 때 수정해야하는 주된 행입니다.

### SQLAlchemy `engine` 생성

첫번째로 해야할 일은 SQLAlchemy "엔진(engine)"을 생성하는 것입니다.

추후 해당 `engine` 을 다른 곳에서도 사용할 것입니다.

```Python hl_lines="8-10"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

#### 참고

다음 인수:

```Python
connect_args={"check_same_thread": False}
```

는 `SQLite` 를 사용할 때만 필요합니다. 다른 데이터베이스에서는 필요하지 않습니다.

!!! note "기술적 세부사항"

    기본적으로 SQLite는 각 스레드가 독립적인 요청을 처리한다고 가정하고, 하나의 스레드만 통신하도록 허용합니다.

    이것은 서로 다른 작업(서로 다른 요청)에 대해 뜻하지 않게 동일한 연결을 공유하는 것을 방지하기 위함입니다.

    하지만 FastAPI에서, 일반적인 함수(`def`)를 사용하면 둘 이상의 스레드가 동일한 요청에 대해 데이터베이스와 상호작용하는 것이 가능하고, 따라서 `connect_args={"check_same_thread": False}` 를 사용해 SQLite가 이것을 허용하도록 설정할 필요가 있습니다.

    또한, 각각의 요청은 의존성에서 자체적인 데이터베이스 연결 세션을 가지므로 기본 메커니즘이 필요하지 않습니다.

### `SessionLocal` 클래스 생성

`SessionLocal` 클래스의 각 인스턴스는 데이터베이스 세션이 될 것입니다. 클래스 자체는 아직 데이터베이스 세션이 아닙니다.

하지만 `SessionLocal` 클래스에 인스턴스를 생성하면, 해당 인스턴스는 실질적인 데이터베이스 세션이 됩니다.

SQLAlchemy로부터 임포트하는 `Session` 과 구분하기 위해 `SessionLocal` 이라고 이름을 붙였습니다.

SQLAlchemy로부터 임포트하는 `Session` 은 추후 사용할 것입니다.

`SessionLocal` 클래스를 생성하기 위해, `sessionmaker` 함수를 사용합니다:

```Python hl_lines="11"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### `Base` 클래스 생성

이제 클래스를 반환하기 위해 `declarative_base()` 함수를 사용합니다.

이후 각각의 데이터베이스 모델 또는 클래스(ORM 모델)를 생성하기 위해 해당 클래스로부터 상속받을 것입니다:

```Python hl_lines="13"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

## 데이터베이스 모델 생성

`sql_app/models.py` 파일을 봅시다.

### `Base` 클래스로부터 SQLAlchemy 모델 생성

SQLAlchemy 모델을 만들기 전에 우리가 생성한 `Base` 클래스를 사용합니다.

!!! tip "팁"
    SQLAlchemy에서는 데이터베이스와 상호작용하는 클래스 및 인스턴스를 "**모델**"이라고 지칭합니다.

    하지만 Pydantic 또한 다른 것들을 지칭하기 위해 "**모델**"이라는 용어를 사용하는데, 여기서는 데이터 유효성 검사, 변환, 그리고 클래스 및 인스턴스의 문서화를 의미합니다.
    
`database` (상기 `database.py` 파일)로부터 `Base` 를 임포트하십시오.

이것을 상속받는 클래스들을 생성합니다.

이 클래스들은 SQLAlchemy 모델들입니다.

```Python hl_lines="4  7-8  18-19"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`__tablename__` 속성은 각각의 모델들에 대한 데이터베이스 테이블 이름을 SQLAlchemy에게 알려줍니다.

### 모델 어트리뷰트/열 생성

이제 모든 모델 (클래스) 어트리뷰트를 생성합니다.

각 속성들은 해당 데이터베이스 테이블의 열을 나타냅니다.

SQLAlchemy의 `Column` 을 기본값으로 사용합니다.

그리고 `Integer` , `String` , `Boolean` 과 같이 데이터베이스에서 유형을 정의하는 SQLAlchemy 클래스 "형(type)"을 매개변수로 전달합니다.

```Python hl_lines="1  10-13  21-24"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

### 관계 생성

이제 관계를 생성합니다.

이를 위해 SQLAlchemy ORM에서 제공하는 `relationship` 을 사용합니다.

이것은 이와 관계가 있는 다른 테이블의 값을 포함하는 "마법"과도 같은 속성이 될 것입니다.

```Python hl_lines="2  15  26"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`my_user.items` 로  `User` 의 `items` 속성에 접근하면, 이것은 `users` 테이블의 해당 레코드를 가리키는 외래키를 갖는 SQLAlchemy 모델인 (`items` 테이블의) `Item` 의 리스트를 갖게 됩니다.

`my_user.items` 에 접근하면, SQLAlchemy는 실제로 데이터베이스로부터 `items` 테이블의 항목을 가져와 이 리스트에 그들을 넣습니다. 

그리고 `Item` 의 `owner` 속성에 접근하면, 이것은 `users` 테이블의 `User` SQLAlchemy 모델을 포함하게 됩니다. 이것은 `users` 테이블에서 어느 레코드를 가져올지 판단하기 위해 `owner_id` 어트리뷰트/열과 그것의 외래키를 사용합니다.

## Pydantic 모델 생성

이제 `sql_app/schemas.py` 파일을 봅니다.

!!! tip "팁"
    SQLAlchemy의 *모델*과 Pydantic의 *모델* 사이의 혼란을 방지하기 위해, `models.py` 파일에서 SQLAlchemy 모델을, `schemas.py` 에서 Pydantic 모델을 관리합니다.

    이 Pydantic 모델들은 유효한 데이터 형태인 "스키마(schema)"를 정의합니다.

    따라서 이는 이는 이 둘을 사용할 때 오는 혼란을 방지할 수 있습니다.

### Pydantic 초기 *모델* / 스키마 생성

데이터를 생성하거나 읽을 때 공통적인 속성을 갖도록 `ItemBase` 과 `UserBase` Pydantic *모델*(또는 "스키마")을 생성합니다.

그리고 그들과 같은 속성을 갖도록 그들로부터 상속받은 `ItemCreate` 과 `UserCreate` 을 만들고, 생성을 위해 필요한 추가적인 데이터 (어트리뷰트)를 추가합니다.

사용자는 생성될 때 `password` 도 갖게 될 것입니다.

하지만 보안상의 문제로, `password` 는 다른 Pydantic *모델*에는 존재하지 않을 것입니다. 예를들어, 사용자 데이터를 읽는 API로부터 전송되지는 않습니다.

```Python hl_lines="3  6-8  11-12  23-24  27-28"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

#### SQLAlchemy 스타일과 Pydantic 스타일

SQLAlchemy *모델*은 `=` 을 사용해서 속성을 정의하고, `Column` 매개변수에 형을 전달합니다:

```Python
name = Column(String)
```

한편 Pydantic *모델*은 새로운 형 어노테이션 구문/형식 힌트인 `:`을 사용해 형을 선언합니다: 

```Python
name: str
```

`=` 과 `:` 을 헷갈리지 않기 위해 이것을 기억하십시오.

### 읽고 반환하기 위한 Pydantic *모델* / 스키마 생성

이제 데이터를 읽고 API를 통해 반환할 때 사용되는 Pydantic *모델*(스키마)를 생성합니다.

예를 들어, 항목을 생성하기 전에는 어떤 ID를 할당해야할지 모르지만, 해당 항목을 읽을 때(API를 통해 반환할 때) 우리는 그것의 ID를 알고 있을 것입니다.

같은 방식으로, 사용자를 읽을 때, 우리는 해당 사용자에 속한 아이템을 포함하는 `items`를 선언할 수 있습니다.

해당 아이템들의 ID뿐 아니라 아이템을 읽기 위해 정의한 모든 Pydantic *모델*의 데이터를 선언할 수 있습니다: `Item` .

```Python hl_lines="15-17  31-34"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

!!! tip "팁"
    API로부터 반환되어 사용자를 읽기 위해 사용되는 Pydantic *모델* `User` 은 `password` 를 포함하지 않는다는 것을 주의하십시오.

### Pydantic의 `orm_mode` 사용

이제, 읽기위한 Pydantic *모델*들인 `Item` 과 `User` 에 내부적인 `Config` 클래스를 추가합니다.

이 <a href="https://pydantic-docs.helpmanual.io/#config" class="external-link" target="_blank">`Config`</a> 클래스는 Pydantic 환경 설정을 위해 사용됩니다.

`Config` 에서, `orm_mode = True` 로 설정합니다.

```Python hl_lines="15  19-20  31  36-37"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

!!! tip "팁"
    `=` 를 사용해 다음과 같이 값을 할당한다는 것에 주의하십시오:

    `orm_mode = True`

    형 선언 때처럼 `:`를 사용하지 않습니다.

    이것은 설정값을 할당하는 것이지, 형을 선언하는 것이 아닙니다.

Pydantic의 `orm_mode` 는 Pydantic *모델*에게 `dict` 가 아닌 ORM 모델(또는 다른 속성이 있는 임의의 객체)이어도 데이터를 읽을 것을 지시합니다.

이 방법으로, `dict` 에서 `id` 값을 가져오기 위해 다음을 사용하는 대신:

```Python
id = data["id"]
```

다음과 같은 방법으로 속성으로부터 값을 가져올 수 있습니다:

```Python
id = data.id
```

이로써 Pydantic *모델*이 ORM과 호환되며, *경로 작동*의 `response_model` 인자로 선언할 수 있습니다.

데이터베이스 모델을 반환받고 이로부터 데이터를 읽을 수 있습니다.

#### ORM 모드에 대한 기술적 세부사항

SQLAlchemy와 많은 다른 ORM들은 자동적으로 "지연 로딩(lazy loading)"을 합니다.

이는 당신이 해당 데이터가 포함된 어트리뷰트에 접근하지 않는 한 데이터베이스에서 관계에 관한 데이터를 가져오지 않는다는 것을 의미합니다. 

예를 들어, `items` 속성에 접근하면:

```Python
current_user.items
```

SQLAlchemy는 그제서야 `items` 테이블에 가서 해당 유저에 속한 아이템들을 가져옵니다.

`orm_mode`가 없다면, *경로 작동*으로부터 SQLAlchemy 모델을 반환할 때 관계에 대한 정보는 포함하지 않습니다.

Pydantic 모델에서 해당 관계들을 선언한 경우라도 그러합니다.

그러나 ORM 모드를 사용하면 Pydantic이 `dict` 로 가정하는 대신 어트리뷰트에서 필요한 데이터에 접근하려고 하기 때문에, 반환하고자 하는 특정한 데이터를 선언할 수 있으며 ORM에서도 데이터들을 가져올 수 있습니다.  

## CRUD 유틸리티

`sql_app/crud.py` 파일을 참고하십시오.

이 파일에서는 데이터베이스의 데이터와 상호작용 하기 위한 재사용 가능한 함수들을 정의할 것입니다.

**CRUD**는 다음의 것들을 의미합니다: 생성(**C**reate), 읽기(**R**ead), 업데이트(**U**pdate), 삭제(**D**elete).

하지만 예시에서는 생성과 읽기만 다룹니다.

### 데이터 읽기

`sqlalchemy.orm` 에서 `Session` 을 임포트하십시오. 이로써 `db` 매개변수의 형을 선언할 수 있으며 더 나은 형 체크 및 함수의 완성도를 기대할 수 있습니다.

`models`(SQLAlchemy 모델)와 `schemas`(Pydantic *모델* / 스키마)를 임포트 하십시오.

다음을 위한 유틸리티 함수들을 생성합니다:

* ID와 이메일을 이용해 하나의 사용자 읽기
* 다수의 사용자 읽기
* 다수의 아이템 읽기

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip "팁" 
    *경로 작동 함수*와는 별개로 데이터베이스와 상호 작용하는 데에만 사용되는 함수들(사용자 또는 아이템을 가져오는 함수)을 생성함으로써 여러 부분에서 이들을 쉽게 재사용할 수 있으며 <abbr title="코드로 작성된, 다른 부분의 코드가 올바르게 동작하는지 확인하는 자동화된 테스트.">단위 테스트</abbr>를 추가할 수 있습니다. 

### 데이터 생성

데이터를 생성하는 유틸리티 함수를 생성합니다.

단계는 다음과 같습니다:

* 데이터와 함께 SQLAlchemy 모델 *인스턴스* 생성
* 해당 인스턴스 객체를 데이터베이스 세션에 추가(`add`)
* 변경 사항이 저장될 수 있도록 데이터베이스에 커밋(`commit`)
* 생성된 ID와 같은, 데이터베이스의 새로운 데이터를 포함할 수 있도록 인스턴스 새로고침(`refresh`)

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip "팁" 
    `User` 을 위한 SQLAlchemy 모델은 안전하게 암호화된 비밀번호인 `hashed_password` 를 포함해야 합니다.

    그러나 API 클라이언트가 제공하는 것은 암호화되지 않은 비밀번호이기 때문에, 그것을 추출한 다음 응용 프로그램에서 암호화된 비밀번호를 생성해야합니다.

    그 다음, 해당 값을 `hashed_password` 인자에 전달하고 저장합니다.

!!! warning "경고" 
    비밀번호가 암호화되지 않았기 때문에 이 예시는 안전하지 않습니다.

    실제 응용 프로그램에서는 비밀번호를 암호화하고 절대 플레인 텍스트로 저장하지 마십시오.

    더 많은 정보가 필요하다면, 자습서의 보안(Security) 항목을 참고하십시오.

    여기서는 데이터베이스의 도구와 역학에만 초점을 맞출 것입니다.

!!! tip "팁" 
    각각의 키워드 인자들을 `Item` 에 전달하고 이들 각각을 Pydantic *모델*로 읽는 대신, 다음과 같이 Pydantic *모델*의 데이터로 `dict` 를 생성할 수 있습니다:

    `item.dict()`

    그다음 `dict`의 키-값 쌍들을 SQLAlchemy `Item`의 키워드 인자들로 전달합니다:

    `Item(**item.dict())`

    이후 Pydantic *모델*이 제공하지 않는 여분의 키워드 인자인 `owner_id`를 전달합니다:

    `Item(**item.dict(), owner_id=user_id)`

## Main **FastAPI** 응용 프로그램

이제 `sql_app/main.py` 파일에서 지금까지 작성한 모든 부분들을 통합하고 사용합시다.

### 데이터베이스 테이블 생성

데이터베이스 테이블을 생성하는 매우 간단한 방법은 다음과 같습니다:

```Python hl_lines="9"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

#### Alembic 참고사항

일반적으로 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>을 사용하여 데이터베이스를 초기화(테이블 생성 등)할 수 있습니다.

또한 Alembic을 사용하여 "마이그레이션"을 할 수도 있습니다 (이것이 Alembic의 주요 역할이기도 합니다).

"마이그레이션"이란 SQLAlchemy 모델 구조에 변화가 생기거나, 새로운 속성을 추가하는 등의 작업이 이루어질 때마다 그러한 변경사항들을 데이터베이스에 복제하거나, 새로운 컬럼 및 테이블을 추가하기 위해 필요한 단계의 집합입니다.

FastAPI 프로젝트에서의 Alembic에 대한 예시를 [Project Generation - Template](../../../en/docs/project-generation.md){.internal-link target=_blank}의 템플릿들에서 찾을 수 있습니다. <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/" class="external-link" target="_blank">소스코드의 `alembic` 디렉터리</a>를 참고하십시오.

### 의존성 생성

!!! info "정보" 
    이 작업을 수행하기 위해, **파이썬 3.7** 이상의 버전을 사용하거나 **파이썬 3.6** 버전 사용시 "backports"를 설치하여야 합니다:

    ```console
    $ pip install async-exit-stack async-generator
    ```

    이것은 <a href="https://github.com/sorcio/async_exit_stack" class="external-link" target="_blank">async-exit-stack</a>과 <a href="https://github.com/python-trio/async_generator" class="external-link" target="_blank">async-generator</a>를 설치합니다.

    마지막에 설명할 "미들웨어"와 함께 다른 메서드들을 사용할 수도 있습니다.

이제 의존성을 생성하기 위해 `sql_app/databases.py` 파일의 `SessionLocal` 클래스를 사용하십시오.

각 요청마다 독립적인 데이터베이스 세션/연결 (`SessionLocal` )이 있고, 모든 요청에 대해 동일한 세션을 사용한 후 요청이 완료되면 종료해야 합니다.

이후 다음 요청에 대해서는 새로운 세션이 생성될 것입니다.

이를 위해, [`yield`를 사용한 의존성](../../../en/docs/tutorial/dependencies/dependencies-with-yield.md)에서 설명한 것과 같이 `yield` 를 사용해 새로운 의존성을 생성합니다.

이 의존성은 하나의 요청에 대해서만 사용된 후 요청이 완료되면 종료되는 새로운 SQLAlchemy `SessionLocal` 을 생성할 것입니다.

```Python hl_lines="15-20"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

!!! info "정보" 
    `SessionLocal()` 의 생성과 요청의 처리를 `try` 블록에 배치합니다.

    그리고 `finally` 블록에서 이를 종료합니다.

    이를 통해 요청 이후 데이터베이스 세션이 언제나 닫혀있다는 사실을 확실히 할 수 있습니다. 요청 처리 도중 예외가 발생한 경우라도 그러합니다.

    그러나 종료 코드(`yield` 이후)에서 다른 예외를 발생시킬 수는 없습니다. 자세한 사항은 [`yield` 및 `HTTPException`을 사용한 의존성](../../../en/docs/tutorial/dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception)을 참고하십시오.

그런 다음, *경로 작동 함수*에서 의존성을 사용할 때, SQLAlchemy로부터 직접 임포트한 `Session` 형으로 이것을 선언합니다.

이를 통해 에디터가 `db` 매개변수가 `Session` 형임을 알 수 있으므로 경로 작동 함수 내부에서 더 나은 에디터 지원을 제공할 수 있게 됩니다:

```Python hl_lines="24  32  38  47  53"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

!!! info "기술적 세부사항" 
    `db` 매개변수는 사실 `SessionLocal` 형이지만, ( `sessionmaker()` 로부터 만들어진) 해당 클래스가 SQLAlchemy `Session` 의 "프록시"이므로, 에디터는 어떤 메서드들이 제공되는지는 알지 못합니다.

    하지만 `Session` 형으로 선언함으로써, 에디터는 사용 가능한 메서드들(`.add()`, `.query()`, `.commit()` 등)을 알 수 있고 (자동완성과 같은) 더 나은 지원을 제공할 수 있습니다. 형 선언이 실제 객체에 영향을 미치지는 않습니다.

### **FastAPI** *경로 동작* 생성

드디어, 여기 표준 **FastAPI** 경로 작동 코드가 있습니다.

```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

의존성 내부에서 `yield`를 사용해 각 요청 이전에 데이터베이스 세션을 생성하고 이후 종료합니다.

그다음 해당 세션을 직접 가져오기 위해 *경로 작동  함수* 내부에서 필요한 의존성을 생성할 수 있습니다.

이를 통해, *경로 작동 함수* 내부에서 `crud.get_user`를 직접 호출해서 해당 세션을 사용할 수 있습니다.

!!! tip "팁" 
    반환되는 값은 SQLAlchemy 모델이거나 SQLAlchemy 모델들의 목록이라는 점을 주의하세요.

    하지만 모든 *경로 작동*이 'orm_mode'을 사용하여 Pydantic *모델* /스키마를 사용한 'response_model'을 가지고 있으므로 Pydantic 모델에 선언된 데이터는 이로부터 추출된 후 모든 일반 필터링 및 유효성 검사를 통해 클라이언트에게 반환됩니다.

!!! tip "팁" 
    `List[schemas.Item]`과 같은 표준 파이썬 형을 가진 `response_models`가 있다는 것도 주의하세요.

    그러나 `List`의 요쇼 / 매개변수는 'orm_mode'가 있는 Pydantic *모델*이기 때문에, 데이터는 문제 없이 클라이언트에게 반환됩니다.

### `def` vs `async def`

여기서 우리는 경로 작동 함수 내부와 의존성에서 SQLAlchemy 코드를 사용하고, 결과적으로 외부 데이터베이스와 통신합니다.

이는 잠재적으로 "대기"를 필요로 할 수 있습니다.

그러나 SQLAlchemy에서는 다음과 같은 직접적인 `await`의 사용이 불가합니다: 

```Python
user = await db.query(User).first()
```

대신 이렇게 사용합니다:

```Python
user = db.query(User).first()
```

이후 `async def`가 아닌 일반적인 `def`를 사용해서 *경로 작동 함수*와 의존성을 다음과 같이 선언합니다:

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info "정보" 
    관계형 데이터베이스에 비동기적으로 연결해야할 경우, [Async SQL (Relational) Databases](../../../en/docs/advanced/async-sql-databases.md){.internal-link target=_blank}를 참고하십시오.

!!! note "매우 세부적인 기술적 사항" 
    만약 당신이 호기심이 있고 깊은 기술적 지식을 갖고있을 경우, `async def` vs `def`가 어떻게 처리되는지에 대해 [Async](../../../en/docs/async.md#very-technical-details) 문서의 매우 세부적인 기술적 사항들을 확인해 보십시오.

## 마이그레이션

우리는 SQLAlchemy를 직접적으로 사용하고 있으며 이것이 **FastAPI**와 동작하기 위해 어떠한 종류의 플러그인도 필요로하지 않기 때문에, 데이터베이스 <abbr title="모델에서 정의한 새로운 열에 대한 자동적인 데이터베이스 업데이트">마이그레이션</abbr>을 <a href="https://alembic.sqlalchemy.org" class="external-link" target="_blank">Alembic</a>과 직접 통합할 수 있습니다.

그리고 SQLAlchemy와 관련된 코드와 SQLAlchemy 모델들이 분리된 독립적인 파일들에 존재하기 때문에, Alembic을 사용한 마이그레이션을 FastAPI, Pydantic 기타 어느 것도 설치하지 않고 수행할 수 있습니다.

같은 방식으로, 동일한 SQLAlchemy 모델 및 유틸리티를 **FastAPI**와 관련이 없는 다른 부분의 코드에서도 사용할 수 있습니다.

예를 들어, <a href="https://docs.celeryproject.org" class="external-link" target="_blank">Celery</a>, <a href="https://python-rq.org/" class="external-link" target="_blank">RQ</a>, 또는 <a href="https://arq-docs.helpmanual.io/" class="external-link" target="_blank">ARQ</a>와 함께 백그라운드 작업자에서의 사용이 가능합니다.

## 모든 파일 검토

`sql_app`을 하위 디렉토리로 갖는`my_super_project`디렉토리가 있어야 합니다.

`sql_app`에는 다음의 파일들이 있습니다:

- `sql_app/__init__.py`: 빈 파일

- `sql_app/database.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

* `sql_app/schemas.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

* `sql_app/main.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

## 확인하십시오

이 코드를 복사해서 그대로 사용할 수 있습니다.

!!! info "정보"

    사실 이 문서들의 대부분의 코드와 마찬가지로 여기에 표시된 코드는 테스트의 일부입니다.

Uvicorn을 통해 실행합니다:


<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그다음, <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 브라우저를 열 수 있습니다.

이제 FastAPI 응용 프로그램과 상호작용하며 실제 데이터베이스에서 데이터를 읽는 것이 가능합니다:

<img src="/img/tutorial/sql-databases/image01.png">

## 데이터베이스와 직접적인 상호작용

FastAPI와 관계 없이 디버깅을 하거나, 테이블, 컬럼, 레코드를 추가하거나, 데이터를 수정하는 등의 작업을 위해  SQLite 데이터베이스(파일)를 직접 실행하고 싶다면, <a href="https://sqlitebrowser.org/" class="external-link" target="_blank">DB Browser for SQLite</a>를 사용할 수 있습니다.

그것은 다음과 같습니다:

<img src="/img/tutorial/sql-databases/image02.png">

<a href="https://inloop.github.io/sqlite-viewer/" class="external-link" target="_blank">SQLite Viewer</a>나 <a href="https://extendsclass.com/sqlite-browser.html" class="external-link" target="_blank">ExtendsClass</a>와 같은 온라인 SQLite 브라우저를 사용할 수도 있습니다.

## 미들웨어가 있는 대체 DB 세션

**파이썬 3.7**을 사용하고 있지 않거나 **파이썬 3.6**에서 상기 언급한 “backports”를 설치할 수 없어 `yield`를 사용한 의존성을 사용할 수 없다면 유사한 방식으로 “미들웨어”에 세션을 설정할 수 있습니다.

“미들웨어”는 요청이 있을 때마다 실행되는 함수로, 일부는 사전에, 일부는 함수의 종점 이후에 실행됩니다.

### 미들웨어 생성

우리가 추가할 미들웨어(단순한 함수)는 각 요청마다 새로운 SQLAlchemy `SessionLocal`을 생성, 요청에 이를 추가하고 요청이 완료되면 이를 종료할 것입니다.

```Python hl_lines="14-22"
{!../../../docs_src/sql_databases/sql_app/alt_main.py!}
```

!!! info "정보"  
    `SessionLocal()` 의 생성과 요청의 처리를 `try` 블록에 배치합니다.

    그리고 `finally` 블록에서 이를 종료합니다.

    이를 통해 요청 이후 데이터베이스 세션이 언제나 닫혀있다는 사실을 확실히 할 수 있습니다. 요청 처리 도중 예외가 발생한 경우라도 그러합니다.

### `request.state`에 대해

`request.state`는 각 `Request` 객체에 대한 프로퍼티입니다. 이 경우에서의 데이터베이스 세션과 같이 요청 자체와 연결된 임의의 객체를 저장하기 위해 존재합니다. <a href="https://www.starlette.io/requests/#other-state" class="external-link" target="_blank">`Request` 상태에 관한 Starlette 문서</a>에서 더 자세한 사항을 확인할 수 있습니다.

이 경우에서, 이것은 하나의 데이터베이스 세션이 모든 요청에 대해 사용되고 이후 (미들웨어에서) 종료되는 것을 보장합니다.

### `yield`를 사용하는 의존성 또는 미들웨어와

**미들웨어**를 추가하는 것은 `yield`를 사용하는 의존성이 하는 것과 유사하지만, 몇 가지 차이점이 존재합니다:

* 더 많은 코드를 필요로하고 조금 더 복잡합니다.
* 미들웨어는 `async` 함수여야 합니다.
    * 내부에 네트워크를 “대기”하는 코드가 있다면, 이는 응용 프로그램을 "차단"하고 성능을 약간 저하시킬 수 있습니다.
    * `SQLAlchemy`가 작동하는 방식에 문제가 되지 않을 수도 있습니다.
    * 하지만 <abbr title="인풋과 아웃풋">I/O</abbr> 대기를 해야하는 코드를 미들웨어에 다수 추가하면 문제가 될 수 있습니다.
* 미들웨어는 *모든* 요청시에 실행됩니다.
    * 따라서 매 요청시 연결이 생성됩니다.
    * *경로 작동*이 데이터베이스와 관련 없는 요청을 처리하는 경우에도 그렇습니다.

!!! tip "팁"
    `yield`를 사용하는 의존성만으로도 충분하다면, 이를 사용하는 것이 더 나을 수 있습니다.

!!! info "정보" 
    `yield`를 사용하는 의존성은 **FastAPI**에 최근에 추가되었습니다.

    이전 버전의 자습서에서는 미들웨어에 대한 예시만 있었고 데이터베이스 세션 관리를 위해 미들웨어를 사용하는 여러 응용 프로그램이 있을 수 있습니다.
