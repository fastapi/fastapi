# 전역 의존성

일부 유형의 애플리케이션의 경우, 애플리케이션 전역에 의존성을 추가하고 싶을 수도 있습니다.

경로 작동 데코레이터에 `의존성`을 추가하는 것과 같이, `FastAPI` 애플리케이션에도 추가할 수 있습니다.

해당 경우에, 의존성들은 애플리케이션의 모든 *경로 작동*에 적용될 것 입니다:

=== "Python 3.9+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an.py!}
    ```

=== "Python 3.6 non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="15"
    {!> ../../../docs_src/dependencies/tutorial012.py!}
    ```

[*작업 경로 데코레이터*에 `의존성` 추가하기](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 섹션에 있는 모든 아이디어는
여전히 적용됩니다. 그러나 위 경우에는, 애플리케이션의 모든 *경로 작동*에 적용됩니다.

## *경로 작동* 집합을 위한 의존성

나중에, 어떻게 여러 개의 파일로 더 큰 애플리케이션을 구조화 하는지에 대해 읽을 때 ([애플리케이션 확장 - 여러 개의 파일](../../tutorial/bigger-applications.md){.internal-link target=_blank}), 어떻게 *작업 경로*의 묶음을 위한 하나의 `의존성` 매개변수를 선언하는지 배우게 될 겁니다.