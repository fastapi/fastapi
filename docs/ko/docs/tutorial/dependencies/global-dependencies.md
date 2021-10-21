# 전역 의존성

어떤 애플리케이션 유형은 전체 애플리케이션에 의존성을 추가하고 싶을 수 있습니다.

[*경로 작동 데코레이터*에 `dependencies` 추가](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}할 수 있던 것과 비슷한 방법으로, 그것들을 `FastAPI` 애플리케이션에 추가할 수 있습니다.

그 경우, 의존성이 애플리케이션 내부의 모든 *경로 작동*에 적용됩니다.

```Python hl_lines="15"
{!../../../docs_src/dependencies/tutorial012.py!}
```

그리고 [*경로 작동 데코레이터*에 `dependencies` 추가](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}에 관한 부분의 모든 개념은 여전히 적용되지만, 이 경우, 앱의 모든 *경로 작동*에 적용됩니다.

## *경로 작동* 그룹에 대한 의존성

이후에, 아마도 다중 파일을 사용한, 더 큰 애플리케이션을 설계하는 방법 ([더 큰 애플리케이션 - 다중 파일](../../tutorial/bigger-applications.md){.internal-link target=_blank}) 에 관해 읽게 될 때, *경로 작동* 그룹에 대한 단일 `dependencies` 매개변수 선언 방법을 배우게 됩니다.
