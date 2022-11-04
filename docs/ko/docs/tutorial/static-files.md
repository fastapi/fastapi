# 정적 파일

`StaticFiles`을 사용하여 디렉토리에 자동으로 정적 파일을 추가할 수 있습니다.

## `StaticFiles` 사용

* `StaticFiles` 임포트.
* 특정 경로에 `StaticFiles()` 인스턴스를 "마운트"합니다.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "기술적 세부사항"
    `from starlette.staticfiles import StaticFiles`를 사용할 수도 있습니다.

    **FastAPI**는 개발자 여러분의 편의를 위해 `fastapi.staticfiles`와 동일한 `starlette.staticfiles`를 제공합니다. 그러나 실제로는 Starlette에서 직접 제공됩니다.


### "마운팅"이란 무엇인가

"마운팅"은 특정 경로에 완전히 "독립적인" 애플리케이션을 추가하는 것을 의미하며, 이후에 모든 하위 경로를 처리합니다.

이것은 마운트된 애플리케이션이 완전히 독립적인 `APIRouter`를 사용하는 것과 다릅니다. 메인 애플리케이션의 OpenAPI 및 문서에는 마운트된 애플리케이션 등의 어떠한 것도 포함되지 않습니다.

**고급 사용자 가이드**에서 이에 대한 자세한 내용을 읽을 수 있습니다.

## 세부사항

첫 번째로 `"/static"`은 이 "하위 응용 프로그램"이 "마운트"될 하위 경로를 나타냅니다. 따라서 `"/static"`으로 시작하는 모든 경로는 이 경로에서 처리됩니다.

`directory="static"`은 정적 파일이 포함된 디렉토리의 이름을 나타냅니다.

`name="static"`은 **FastAPI**에서 내부적으로 사용할 수 있는 이름을 지정합니다.

이러한 모든 매개변수는 "`static`"과 다를 수 있으므로 필요에 따라 조정하고 애플리케이션의 특정 세부사항을 조정하십시오.

## 더 많은 정보

자세한 내용과 옵션은 <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">정적 파일에 대한 Starlette의 문서</a>를 확인하세요.
