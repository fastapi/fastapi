# 경로 작동 데코레이터에서의 의존성

몇몇 경우에는, *경로 작동 함수* 안에서 의존성의 반환 값이 필요하지 않습니다.

또는 의존성이 값을 반환하지 않습니다.

그러나 여전히 실행/해결될 필요가 있습니다.

그런 경우에, `Depends`를 사용하여 *경로 작동 함수*의 매개변수로 선언하는 것보다 *경로 작동 데코레이터*에 `dependencies`의 `list`를 추가할 수 있습니다.

## *경로 작동 데코레이터*에 `dependencies` 추가하기

*경로 작동 데코레이터*는 `dependencies`라는 선택적인 인자를 받습니다.

`Depends()`로 된 `list`이어야합니다:

=== "Python 3.9+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/dependencies/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/dependencies/tutorial006_an.py!}
    ```

=== "Python 3.8 Annotated가 없는 경우"

    !!! tip "팁"
        가능하다면 `Annotated`가 달린 버전을 권장합니다.

    ```Python hl_lines="17"
    {!> ../../../docs_src/dependencies/tutorial006.py!}
    ```

이러한 의존성들은 기존 의존성들과 같은 방식으로 실행/해결됩니다. 그러나 값은 (무엇이든 반환한다면) *경로 작동 함수*에 제공되지 않습니다.

!!! tip "팁"
    일부 편집기에서는 사용되지 않는 함수 매개변수를 검사하고 오류로 표시합니다.

    *경로 작동 데코레이터*에서 `dependencies`를 사용하면 편집기/도구 오류를 피하며 실행되도록 할 수 있습니다.

    또한 코드에서 사용되지 않는 매개변수를 보고 불필요하다고 생각할 수 있는 새로운 개발자의 혼란을 방지하는데 도움이 될 수 있습니다.

!!! info "정보"
    이 예시에서 `X-Key`와 `X-Token`이라는 커스텀 헤더를 만들어 사용했습니다.

    그러나 실제로 보안을 구현할 때는 통합된 [보안 유틸리티 (다음 챕터)](../security/index.md){.internal-link target=_blank}를 사용하는 것이 더 많은 이점을 얻을 수 있습니다.

## 의존성 오류와 값 반환하기

평소에 사용하던대로 같은 의존성 *함수*를 사용할 수 있습니다.

### 의존성 요구사항

(헤더같은) 요청 요구사항이나 하위-의존성을 선언할 수 있습니다:

=== "Python 3.9+"

    ```Python hl_lines="8  13"
    {!> ../../../docs_src/dependencies/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="7  12"
    {!> ../../../docs_src/dependencies/tutorial006_an.py!}
    ```

=== "Python 3.8 Annotated가 없는 경우"

    !!! tip "팁"
        가능하다면 `Annotated`가 달린 버전을 권장합니다.

    ```Python hl_lines="6  11"
    {!> ../../../docs_src/dependencies/tutorial006.py!}
    ```

### 오류 발생시키기

다음 의존성은 기존 의존성과 동일하게 예외를 `raise`를 일으킬 수 있습니다:

=== "Python 3.9+"

    ```Python hl_lines="10  15"
    {!> ../../../docs_src/dependencies/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9  14"
    {!> ../../../docs_src/dependencies/tutorial006_an.py!}
    ```

=== "Python 3.8 Annotated가 없는 경우"

    !!! tip "팁"
        가능하다면 `Annotated`가 달린 버전을 권장합니다.

    ```Python hl_lines="8  13"
    {!> ../../../docs_src/dependencies/tutorial006.py!}
    ```

### 값 반환하기

값을 반환하거나, 그러지 않을 수 있으며 값은 사용되지 않습니다.

그래서 이미 다른 곳에서 사용된 (값을 반환하는) 일반적인 의존성을 재사용할 수 있고, 비록 값은 사용되지 않지만 의존성은 실행될 것입니다:

=== "Python 3.9+"

    ```Python hl_lines="11  16"
    {!> ../../../docs_src/dependencies/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10  15"
    {!> ../../../docs_src/dependencies/tutorial006_an.py!}
    ```

=== "Python 3.8 Annotated가 없는 경우"

    !!! tip "팁"
        가능하다면 `Annotated`가 달린 버전을 권장합니다.

    ```Python hl_lines="9  14"
    {!> ../../../docs_src/dependencies/tutorial006.py!}
    ```

## *경로 작동* 모음에 대한 의존성

나중에 여러 파일을 가지고 있을 수 있는 더 큰 애플리케이션을 구조화하는 법([더 큰 애플리케이션 - 여러 파일들](../../tutorial/bigger-applications.md){.internal-link target=_blank})을 읽을 때, *경로 작동* 모음에 대한 단일 `dependencies` 매개변수를 선언하는 법에 대해서 배우게 될 것입니다.

## 전역 의존성

다음으로 각 *경로 작동*에 적용되도록 `FastAPI` 애플리케이션 전체에 의존성을 추가하는 법을 볼 것입니다.
