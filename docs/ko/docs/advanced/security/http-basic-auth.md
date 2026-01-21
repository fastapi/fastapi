# HTTP Basic Auth { #http-basic-auth }

가장 단순한 경우에는 HTTP Basic Auth를 사용할 수 있습니다.

HTTP Basic Auth에서는 애플리케이션이 사용자명과 비밀번호가 들어 있는 헤더를 기대합니다.

이를 받지 못하면 HTTP 401 "Unauthorized" 오류를 반환합니다.

그리고 값이 `Basic`이고 선택적으로 `realm` 파라미터를 포함하는 `WWW-Authenticate` 헤더를 반환합니다.

이는 브라우저가 사용자명과 비밀번호를 입력하는 통합 프롬프트를 표시하도록 알려줍니다.

그다음 사용자명과 비밀번호를 입력하면, 브라우저가 자동으로 해당 값을 헤더에 담아 전송합니다.

## 간단한 HTTP Basic Auth { #simple-http-basic-auth }

* `HTTPBasic`과 `HTTPBasicCredentials`를 임포트합니다.
* `HTTPBasic`을 사용해 "`security` scheme"을 생성합니다.
* *경로 처리*에서 dependency로 해당 `security`를 사용합니다.
* `HTTPBasicCredentials` 타입의 객체를 반환합니다:
    * 전송된 `username`과 `password`를 포함합니다.

{* ../../docs_src/security/tutorial006_an_py39.py hl[4,8,12] *}

처음으로 URL을 열어보면(또는 문서에서 "Execute" 버튼을 클릭하면) 브라우저가 사용자명과 비밀번호를 물어봅니다:

<img src="/img/tutorial/security/image12.png">

## 사용자명 확인하기 { #check-the-username }

더 완전한 예시입니다.

dependency를 사용해 사용자명과 비밀번호가 올바른지 확인하세요.

이를 위해 Python 표준 모듈 <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a>를 사용해 사용자명과 비밀번호를 확인합니다.

`secrets.compare_digest()`는 `bytes` 또는 ASCII 문자(영어에서 사용하는 문자)만 포함한 `str`을 받아야 합니다. 즉, `Sebastián`의 `á` 같은 문자가 있으면 동작하지 않습니다.

이를 처리하기 위해 먼저 `username`과 `password`를 UTF-8로 인코딩해서 `bytes`로 변환합니다.

그런 다음 `secrets.compare_digest()`를 사용해 `credentials.username`이 `"stanleyjobson"`이고 `credentials.password`가 `"swordfish"`인지 확실히 확인할 수 있습니다.

{* ../../docs_src/security/tutorial007_an_py39.py hl[1,12:24] *}

이는 다음과 비슷합니다:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

하지만 `secrets.compare_digest()`를 사용하면 "timing attacks"라고 불리는 한 유형의 공격에 대해 안전해집니다.

### Timing Attacks { #timing-attacks }

그렇다면 "timing attack"이란 무엇일까요?

공격자들이 사용자명과 비밀번호를 추측하려고 한다고 가정해봅시다.

그리고 사용자명 `johndoe`, 비밀번호 `love123`으로 요청을 보냅니다.

그러면 애플리케이션의 Python 코드는 대략 다음과 같을 것입니다:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

하지만 Python이 `johndoe`의 첫 글자 `j`를 `stanleyjobson`의 첫 글자 `s`와 비교하는 순간, 두 문자열이 같지 않다는 것을 이미 알게 되어 `False`를 반환합니다. 이는 “나머지 글자들을 비교하느라 계산을 더 낭비할 필요가 없다”고 판단하기 때문입니다. 그리고 애플리케이션은 "Incorrect username or password"라고 말합니다.

그런데 공격자들이 사용자명을 `stanleyjobsox`, 비밀번호를 `love123`으로 다시 시도합니다.

그러면 애플리케이션 코드는 다음과 비슷하게 동작합니다:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python은 두 문자열이 같지 않다는 것을 알아차리기 전까지 `stanleyjobsox`와 `stanleyjobson` 양쪽의 `stanleyjobso` 전체를 비교해야 합니다. 그래서 "Incorrect username or password"라고 응답하기까지 추가로 몇 마이크로초가 더 걸릴 것입니다.

#### 응답 시간은 공격자에게 도움이 됩니다 { #the-time-to-answer-helps-the-attackers }

이 시점에서 서버가 "Incorrect username or password" 응답을 보내는 데 몇 마이크로초 더 걸렸다는 것을 알아채면, 공격자들은 _무언가_ 맞았다는 것(초기 몇 글자가 맞았다는 것)을 알게 됩니다.

그리고 `johndoe`보다는 `stanleyjobsox`에 더 가까운 값을 시도해야 한다는 것을 알고 다시 시도할 수 있습니다.

#### "전문적인" 공격 { #a-professional-attack }

물론 공격자들은 이런 작업을 손으로 하지 않습니다. 보통 초당 수천~수백만 번 테스트할 수 있는 프로그램을 작성할 것이고, 한 번에 정답 글자 하나씩 추가로 얻어낼 수 있습니다.

그렇게 하면 몇 분 또는 몇 시간 만에, 응답에 걸린 시간만을 이용해(우리 애플리케이션의 “도움”을 받아) 올바른 사용자명과 비밀번호를 추측할 수 있게 됩니다.

#### `secrets.compare_digest()`로 해결하기 { #fix-it-with-secrets-compare-digest }

하지만 우리 코드는 실제로 `secrets.compare_digest()`를 사용하고 있습니다.

요약하면, `stanleyjobsox`와 `stanleyjobson`을 비교하는 데 걸리는 시간은 `johndoe`와 `stanleyjobson`을 비교하는 데 걸리는 시간과 같아집니다. 비밀번호도 마찬가지입니다.

이렇게 애플리케이션 코드에서 `secrets.compare_digest()`를 사용하면, 이러한 범위의 보안 공격 전반에 대해 안전해집니다.

### 오류 반환하기 { #return-the-error }

자격 증명이 올바르지 않다고 판단되면, 상태 코드 401(자격 증명이 제공되지 않았을 때와 동일)을 사용하는 `HTTPException`을 반환하고 브라우저가 로그인 프롬프트를 다시 표시하도록 `WWW-Authenticate` 헤더를 추가하세요:

{* ../../docs_src/security/tutorial007_an_py39.py hl[26:30] *}
