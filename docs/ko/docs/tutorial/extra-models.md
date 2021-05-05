# 추가 모델

이전의 예제에 이어서, 일반적으로는 한 가지 이상의 관계 모델을 가질 것입니다.

사용자 모델의 경우가 특히 그렇습니다. 왜냐하면:

* **입력 모델**은 비밀번호를 가질 수 있어야 합니다.
* **출력 모델**은 비밀번호가 없어야 합니다.
* **데이터베이스 모델**은 해시 된 비밀번호가 필요할 수 있습니다.

!!! danger "위험"
    사용자의 평문 비밀번호를 절대 저장하지 마십시오. 항상 검증할 수 있는 "안전한 해시"로 저장하십시오.

    만약 당신이 모른다면 [보안 챕터](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}에서 "비밀번호 해시"가 무엇인지 배울 수 있습니다.

## 복합 모델들

모델들이 비밀번호 필드와 그것이 사용되는 위치에서 어떻게 보일 수 있는지에 대한 일반적인 아이디어를 소개합니다.

```Python hl_lines="9  11  16  22  24  29-30  33-35  40-41"
{!../../../docs_src/extra_models/tutorial001.py!}
```

### `**user_in.dict()`에 관해

#### Pydantic에서의 `.dict()`

`user_in`은 `UserIn` 클래스의 Pydantic 모델입니다.

Pydantic 모델은 모델 데이터의 `dict`를 반환하는 `.dict()` 메소드가 있습니다.

그래서, 만약 우리가 Pydantic 객체인 `user_in`을 생성해보면:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

그리고 우리는 이렇게 호출합니다:

```Python
user_dict = user_in.dict()
```

우리는 `user_dict`(Pydantic 모델 객체 대신 `dict` 입니다) 변수 내부에 있는 데이터를 `dict`로 가져올 수 있습니다.

그리고 만약 우리가 이렇게 호출한다면:

```Python
print(user_dict)
```

우리는 파이썬 `dict`를 얻을 수 있습니다:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### `dict`를 풀기

우리가 `user_dict`같은 `dict`를 얻어오거나 `**user_dict`의 형태로 함수나 클래스로 전달할때, 파이썬은 이것을 "풀기(unwrap)"를 합니다. 이것은 `user_dict`의 키와 값을 키-값 인자(arguments)로 직접적으로 넘깁니다.

그래서, 위에서 설명했던 `user_dict`로 계속 진행하겠습니다:

```Python
UserInDB(**user_dict)
```

아래와 동등한 결과를 줄 것입니다.

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

또는 더 정확하게는 나중에 어떤내용을 담게 되더라도 `user_dict`를 직접적으로 사용하는 것입니다:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 또 다른 내용으로부터 Pydantic 모델

위의 예제에서는 `user_in.dict()`에서 `user_dict`를 얻을 수 있었습니다. 이 코드입니다:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

이것과 동등할 것입니다:

```Python
UserInDB(**user_in.dict())
```

... 왜냐하면 `user_in.dict()`는 `dict`이기 때문입니다. 그리고 우리는 `UserInDB` 앞에 `**`를 붙여서 전달함으로써 Python이 "풀기"를 하도록 할 수 있습니다.

그래서, 우리는 또다른 Pydantic 모델에 있는 데이터에서 Pydantic 모델을 얻을 수 있습니다.

#### `dict`를 풀기 그리고 추가 키워드들

그리고 추가 키워드 속성인 `hashed_password=hashed_password`을 추가하겠습니다. 아래와 같습니다:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

... 결국에는 이렇게 될 것입니다:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

!!! warning "경고"
    추가적인 함수 지원은 가능한 데이터 흐름을 보여주는 데모일 뿐이며, 당연히 그 어떤 실제 보안도 제공하지 않습니다.

## 중복 줄이기

중복 코드 줄이기는 **FASTAPI**의 핵심 개념 중 하나입니다.

코드 중복은 버그의 가능성, 보안 이슈, 코드 비동기화 문제(한 장소에는 업데이트 하지만 다른 곳에서는 그렇지 못할때) 등을 증가시킵니다.

그리고 이러한 모델들은 많은 데이터를 공유하고 타입과 인자 이름들을 반복적으로 사용하게 됩니다.

더 잘할 수 있습니다.

다른 모델들의 기초가 되는 `UserBase` 모델을 선언할 수 있습니다. 그리고 우리는 이 인자들(타입 선언, 검증 등)을 상속받은 모델인 서브클래스를 만들 수 있습니다.

모든 데이터의 변환, 검증, 문서화 등은 여전히 정상적으로 동작할 것입니다.

이러한 방법으로 우리는 모델들 사이의 차이만을 선언할 수 있습니다.(평문 `password`와 함께, `hashed_password`와 함께, 비밀번호는 없이)

```Python hl_lines="9  15-16  19-20  23-24"
{!../../../docs_src/extra_models/tutorial002.py!}
```

## `Union` 또는 `anyOf`

`Union`을 통해 두 가지 타입의 응답을 선언할 수 있습니다. 그 말은, 응답은 그 두 가지 중 아무거나 될 수 있다는 의미입니다.

이는 OpenAPI에서 `anyOf`로 정의할 수 있습니다.

이렇게 하기 위해서는 표준 파이썬 타입 힌트  <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>를 사용하십시오:

!!! note "참고"
    <a href="https://pydantic-docs.helpmanual.io/usage/types/#unions" class="external-link" target="_blank">`Union`</a>을 선언할 때, 가장 특정한 타입을 첫 번째로 포함하고, 덜 특정한 타입을 뒤에 붙이십시오. 예를 들어, `Union[PlaneItem, CarItem]`에서 더 특정한 `PlaneItem`은 `CarItem`보다 더 앞에 옵니다.

```Python hl_lines="1  14-15  18-20  33"
{!../../../docs_src/extra_models/tutorial003.py!}
```

## 모델들의 리스트

같은 방법으로, 객체의 리스트를 응답으로 선언할 수 있습니다.

이것을 위해서 표준 파이썬 `typing.List`를 사용하십시오:

```Python hl_lines="1  20"
{!../../../docs_src/extra_models/tutorial004.py!}
```

## 임의의 `dict`로 응답하기

Pydantic 모델을 사용하지 않고 단순히 키와 값의 타입으로 선언하는 평범한 임의의 `dict`로 응답을 선언할 수 있습니다.

미리 유효한 필드와 속성의 이름(이것은 아마 Pydantic 모델에 필요할 것입니다)을 알지 못할때 유용합니다.

이 상황에서 `typing.Dict`를 사용할 수 있습니다.:

```Python hl_lines="1  8"
{!../../../docs_src/extra_models/tutorial005.py!}
```

## 정리

각각의 상황에서 다수의 Pydantic 모델들을 사용하고 자유롭게 상속하십시오.

만약 개체가 다른 "상태"를 가질 수밖에 없다면, 굳이 하나의 개체당 하나의 데이터 모델을 가질 필요가 없습니다. `password`, `password_hash`는 있으나 비밀번호는 없는 사용자 "entity" 상황이 그렇습니다.
