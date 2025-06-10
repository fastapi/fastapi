# 전역 의존성

몇몇 애플리케이션에서는 애플리케이션 전체에 의존성을 추가하고 싶을 수 있습니다.

[*경로 작동 데코레이터*에 `dependencies` 추가하기](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}와 유사한 방법으로 `FastAPI` 애플리케이션에 그것들을 추가할 수 있습니다.

그런 경우에, 애플리케이션의 모든 *경로 작동*에 적용될 것입니다:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}

그리고 [*경로 작동 데코레이터*에 `dependencies` 추가하기](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}에 대한 아이디어는 여전히 적용되지만 여기에서는 앱에 있는 모든 *경로 작동*에 적용됩니다.

## *경로 작동* 모음에 대한 의존성

이후에 여러 파일들을 가지는 더 큰 애플리케이션을 구조화하는 법([더 큰 애플리케이션 - 여러 파일들](../../tutorial/bigger-applications.md){.internal-link target=_blank})을 읽을 때, *경로 작동* 모음에 대한 단일 `dependencies` 매개변수를 선언하는 법에 대해서 배우게 될 것입니다.
