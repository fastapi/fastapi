# 추가 모델

지난 예제에 이어서, 연관된 모델을 여러개 갖는 것은 흔한 일입니다.

특히 사용자 모델의 경우에 그러한데, 왜냐하면:

* **입력 모델** 은 비밀번호를 가져야 합니다.
* **출력 모델** 은 비밀번호를 가지면 안됩니다.
* **데이터베이스 모델** 은 해시처리된 비밀번호를 가질 것입니다.

/// danger | 위험

절대 사용자의 비밀번호를 평문으로 저장하지 마세요. 항상 이후에 검증 가능한 "안전한 해시(secure hash)"로 저장하세요.

만약 이게 무엇인지 모르겠다면, [security chapters](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.에서 비밀번호 해시에 대해 배울 수 있습니다.

///

## 다중 모델

아래는 비밀번호 필드와 해당 필드가 사용되는 위치를 포함하여, 각 모델들이 어떤 형태를 가질 수 있는지 전반적인 예시입니다:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}


/// info | 정보

Pydantic v1에서는 해당 메서드가 `.dict()`로 불렸으며, Pydantic v2에서는 `.model_dump()`로 이름이 변경되었습니다. `.dict()`는 여전히 지원되지만 더 이상 권장되지 않습니다.

여기에서 사용하는 예제는 Pydantic v1과의 호환성을 위해 `.dict()`를 사용하지만, Pydantic v2를 사용할 수 있다면 `.model_dump()`를 사용하는 것이 좋습니다.

///

### `**user_in.dict()` 에 대하여

#### Pydantic의 `.dict()`

`user_in`은 Pydantic 모델 클래스인 `UserIn`입니다.

Pydantic 모델은 모델 데이터를 포함한 `dict`를 반환하는 `.dict()` 메서드를 제공합니다.

따라서, 다음과 같이 Pydantic 객체 `user_in`을 생성할 수 있습니다:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

그 다음, 다음과 같이 호출합니다:

```Python
user_dict = user_in.dict()
```

이제 변수 `user_dict`에 데이터가 포함된 `dict`를 가지게 됩니다(이는 Pydantic 모델 객체가 아닌 `dict`입니다).

그리고 다음과 같이 호출하면:

```Python
print(user_dict)
```

Python의 `dict`가 다음과 같이 출력됩니다:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### `dict` 언패킹(Unpacking)

`user_dict`와 같은 `dict`를 함수(또는 클래스)에 `**user_dict`로 전달하면, Python은 이를 "언팩(unpack)"합니다. 이 과정에서 `user_dict`의 키와 값을 각각 키-값 인자로 직접 전달합니다.

따라서, 위에서 생성한 `user_dict`를 사용하여 다음과 같이 작성하면:

```Python
UserInDB(**user_dict)
```

다음과 같은 결과를 생성합니다:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

혹은 더 정확히 말하자면, `user_dict`를 직접 사용하는 것은, 나중에 어떤 값이 추가되더라도 아래와 동일한 효과를 냅니다:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 다른 모델 데이터로 새 Pydantic 모델 생성

위의 예제에서 `user_in.dict()`로부터 `user_dict`를 생성한 것처럼, 아래 코드는:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

다음과 동일합니다:

```Python
UserInDB(**user_in.dict())
```

...왜냐하면 `user_in.dict()`는 `dict`이며, 이를 `**`로 Python이 "언팩(unpack)"하도록 하여 `UserInDB`에 전달하기 때문입니다.

따라서, 다른 Pydantic 모델의 데이터를 사용하여 새로운 Pydantic 모델을 생성할 수 있습니다.

#### `dict` 언패킹(Unpacking)과 추가 키워드

그리고 다음과 같이 추가 키워드 인자 `hashed_password=hashed_password`를 추가하면:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

다음과 같은 결과를 생성합니다:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | 경고

추가적으로 제공된 함수 `fake_password_hasher`와 `fake_save_user`는 데이터 흐름을 시연하기 위한 예제일 뿐이며, 실제 보안을 제공하지 않습니다.

///

## 중복 줄이기

코드 중복을 줄이는 것은 **FastAPI**의 핵심 아이디어 중 하나입니다.

코드 중복은 버그, 보안 문제, 코드 비동기화 문제(한 곳은 업데이트되었지만 다른 곳은 업데이트되지 않는 문제) 등의 가능성을 증가시킵니다.

그리고 이 모델들은 많은 데이터를 공유하면서 속성 이름과 타입을 중복하고 있습니다.

더 나은 방법이 있습니다.

`UserBase` 모델을 선언하여 다른 모델들의 기본(base)으로 사용할 수 있습니다. 그런 다음 이 모델을 상속받아 속성과 타입 선언(유형 선언, 검증 등)을 상속하는 서브클래스를 만들 수 있습니다.

모든 데이터 변환, 검증, 문서화 등은 정상적으로 작동할 것입니다.

이렇게 하면 각 모델 간의 차이점만 선언할 수 있습니다(평문 `password`가 있는 경우, `hashed_password`만 있는 경우, 혹은 비밀번호가 없는 경우):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 또는 `anyOf`

두 가지 이상의 타입을 포함하는 `Union`으로 응답을 선언할 수 있습니다. 이는 응답이 그 중 하나의 타입일 수 있음을 의미합니다.

OpenAPI에서는 이를 `anyOf`로 정의합니다.

이를 위해 표준 Python 타입 힌트인 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>을 사용할 수 있습니다:

/// note | 참고

<a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a>을 정의할때는 더 구체적인 타입을 먼저 포함하고, 덜 구체적인 타입을 그 뒤에 나열해야합니다. 아래 예제에서는 `Union[PlaneItem, CarItem]` 를 보면, 더 구체적인 `PlaneItem`이 `CarItem`보다 앞에 위치합니다.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}


### Python 3.10에서 `Union`

위의 예제에서는 `response_model` 인자 값으로 `Union[PlaneItem, CarItem]`을 전달합니다.

이 경우, 이를 **타입 어노테이션(type annotation)** 이 아닌 **인자 값(argument value)** 으로 전달하고 있기 때문에 Python 3.10에서도 `Union`을 사용해야 합니다.

만약 타입 어노테이션에 사용한다면, 다음과 같이 수직 막대(|)를 사용할 수 있습니다:

```Python
some_variable: PlaneItem | CarItem
```

하지만 이를 `response_model=PlaneItem | CarItem`과 같이 할당하면 에러가 발생합니다. 이는 Python이 이를 타입 어노테이션으로 해석하지 않고, `PlaneItem`과 `CarItem` 사이의 **잘못된 연산(invalid operation)**을 시도하기 때문입니다

## 모델 리스트

마찬가지로, 객체 리스트 형태의 응답을 선언할 수도 있습니다.

이를 위해 표준 Python의 `typing.List`를 사용하세요(또는 Python 3.9 이상에서는 단순히 `list`를 사용할 수 있습니다):

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}


## 임의의 `dict` 응답

Pydantic 모델을 사용하지 않고, 키와 값의 타입만 선언하여 평범한 임의의 `dict`로 응답을 선언할 수도 있습니다.

이는 Pydantic 모델에 필요한 유효한 필드/속성 이름을 사전에 알 수 없는 경우에 유용합니다.

이 경우, `typing.Dict`를 사용할 수 있습니다(또는 Python 3.9 이상에서는 단순히 `dict`를 사용할 수 있습니다):

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}


## 요약

여러 Pydantic 모델을 사용하고, 각 경우에 맞게 자유롭게 상속하세요.

엔터티가 서로 다른 "상태"를 가져야 하는 경우, 엔터티당 단일 데이터 모델을 사용할 필요는 없습니다. 예를 들어, 사용자 "엔터티"가 `password`, `password_hash`, 또는 비밀번호가 없는 상태를 포함할 수 있는 경우처럼 말입니다.
