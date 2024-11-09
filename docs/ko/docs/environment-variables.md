# 환경 변수

/// tip | 팁

만약 "환경 변수"가 무엇이고, 어떻게 사용하는지 알고 계시다면, 이 챕터를 스킵하셔도 좋습니다.

///

환경 변수는 파이썬 코드의 **바깥**인, **운영 체제**에 존재하는 변수입니다. 파이썬 코드나 다른 프로그램에서 읽을 수 있습니다.

환경 변수는 애플리케이션 **설정**을 처리하거나, 파이썬의 **설치** 과정의 일부로 유용합니다.

## 환경 변수를 만들고 사용하기

파이썬 없이도, **셸 (터미널)** 에서 환경 변수를 **생성** 하고 사용할 수 있습니다.

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 파이썬에서 환경 변수 읽기

파이썬 **바깥**인 터미널에서(다른 도구로도 가능) 환경 변수를 생성도 할 수도 있고, 이를 **파이썬에서 읽을 수 있습니다.**

예를 들어 다음과 같은 `main.py` 파일이 있다고 합시다:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | 팁

<a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> 의 두 번째 인자는 반환할 기본값입니다.

여기서는 `"World"`를 넣었기에 기본값으로써 사용됩니다. 넣지 않으면 `None` 이 기본값으로 사용됩니다.

///

그러면 해당 파이썬 프로그램을 다음과 같이 호출할 수 있습니다:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

환경변수는 코드 바깥에서 설정될 수 있지만, 코드에서 읽을 수 있고, 나머지 파일과 함께 저장(`git`에 커밋)할 필요가 없으므로, 구성이나 **설정** 에 사용하는 것이 일반적입니다.

**특정 프로그램 호출**에 대해서만 사용할 수 있는 환경 변수를 만들 수도 있습니다. 해당 프로그램에서만 사용할 수 있고, 해당 프로그램이 실행되는 동안만 사용할 수 있습니다.

그렇게 하려면 프로그램 바로 앞, 같은 줄에 환경 변수를 만들어야 합니다:

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | 팁

<a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a> 에서 좀 더 자세히 알아볼 수 있습니다.

///

## 타입과 검증

이 환경변수들은 오직 **텍스트 문자열**로만 처리할 수 있습니다. 텍스트 문자열은 파이썬 외부에 있으며 다른 프로그램 및 나머지 시스템(Linux, Windows, macOS 등 다른 운영 체제)과 호환되어야 합니다.

즉, 파이썬에서 환경 변수로부터 읽은 **모든 값**은 **`str`**이 되고, 다른 타입으로의 변환이나 검증은 코드에서 수행해야 합니다.

**애플리케이션 설정**을 처리하기 위한 환경 변수 사용에 대한 자세한 내용은 [고급 사용자 가이드 - 설정 및 환경 변수](./advanced/settings.md){.internal-link target=\_blank} 에서 확인할 수 있습니다.

## `PATH` 환경 변수

**`PATH`**라고 불리는, **특별한** 환경변수가 있습니다. 운영체제(Linux, Windows, macOS 등)에서 실행할 프로그램을 찾기위해 사용됩니다.

변수 `PATH`의 값은 Linux와 macOS에서는 콜론 `:`, Windows에서는 세미콜론 `;`으로 구분된 디렉토리로 구성된 긴 문자열입니다.

예를 들어, `PATH` 환경 변수는 다음과 같습니다:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

이는 시스템이 다음 디렉토리에서 프로그램을 찾아야 함을 의미합니다:

-   `/usr/local/bin`
-   `/usr/bin`
-   `/bin`
-   `/usr/sbin`
-   `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

이는 시스템이 다음 디렉토리에서 프로그램을 찾아야 함을 의미합니다:

-   `C:\Program Files\Python312\Scripts`
-   `C:\Program Files\Python312`
-   `C:\Windows\System32`

////

터미널에 **명령어**를 입력하면 운영 체제는 `PATH` 환경 변수에 나열된 **각 디렉토리**에서 프로그램을 **찾습니다.**

예를 들어 터미널에 `python`을 입력하면 운영 체제는 해당 목록의 **첫 번째 디렉토리**에서 `python`이라는 프로그램을 찾습니다.

찾으면 **사용합니다**. 그렇지 않으면 **다른 디렉토리**에서 계속 찾습니다.

### 파이썬 설치와 `PATH` 업데이트

파이썬을 설치할 때, 아마 `PATH` 환경 변수를 업데이트 할 것이냐고 물어봤을 겁니다.

//// tab | Linux, macOS

파이썬을 설치하고 그것이 `/opt/custompython/bin` 디렉토리에 있다고 가정해 보겠습니다.

`PATH` 환경 변수를 업데이트하도록 "예"라고 하면 설치 관리자가 `/opt/custompython/bin`을 `PATH` 환경 변수에 추가합니다.

다음과 같이 보일 수 있습니다:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

이렇게 하면 터미널에 `python`을 입력할 때, 시스템이 `/opt/custompython/bin`(마지막 디렉토리)에서 파이썬 프로그램을 찾아 사용합니다.

////

//// tab | Windows

파이썬을 설치하고 그것이 `C:\opt\custompython\bin` 디렉토리에 있다고 가정해 보겠습니다.

`PATH` 환경 변수를 업데이트하도록 "예"라고 하면 설치 관리자가 `C:\opt\custompython\bin`을 `PATH` 환경 변수에 추가합니다.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

이렇게 하면 터미널에 `python`을 입력할 때, 시스템이 `C:\opt\custompython\bin`(마지막 디렉토리)에서 파이썬 프로그램을 찾아 사용합니다.

////

그래서, 다음과 같이 입력한다면:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

시스템은 `/opt/custompython/bin`에서 `python` 프로그램을 **찾아** 실행합니다.

다음과 같이 입력하는 것과 거의 같습니다:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

시스템은 `C:\opt\custompython\bin\python`에서 `python` 프로그램을 **찾아** 실행합니다.

다음과 같이 입력하는 것과 거의 같습니다:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

이 정보는 [가상 환경](virtual-environments.md){.internal-link target=\_blank} 에 대해 알아볼 때 유용할 것입니다.

## 결론

이 문서를 읽고 **환경 변수**가 무엇이고 파이썬에서 어떻게 사용하는지 기본적으로 이해하셨을 겁니다.

또한 <a href="https://ko.wikipedia.org/wiki/환경_변수" class="external-link" target="_blank">환경 변수에 대한 위키피디아(한국어)</a>에서 이에 대해 자세히 알아볼 수 있습니다.

많은 경우에서, 환경 변수가 어떻게 유용하고 적용 가능한지 바로 명확하게 알 수는 없습니다. 하지만 개발할 때 다양한 시나리오에서 계속 나타나므로 이에 대해 아는 것이 좋습니다.

예를 들어, 다음 섹션인 [가상 환경](virtual-environments.md)에서 이 정보가 필요합니다.
