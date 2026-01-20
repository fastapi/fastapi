# 정적 파일 { #static-files }

`StaticFiles`를 사용하면 디렉터리에서 정적 파일을 자동으로 제공할 수 있습니다.

## `StaticFiles` 사용 { #use-staticfiles }

* `StaticFiles`를 임포트합니다.
* 특정 경로에 `StaticFiles()` 인스턴스를 "마운트"합니다.

{* ../../docs_src/static_files/tutorial001_py39.py hl[2,6] *}

/// note | 기술 세부사항

`from starlette.staticfiles import StaticFiles`를 사용할 수도 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 `fastapi.staticfiles`로 `starlette.staticfiles`와 동일한 것을 제공합니다. 하지만 실제로는 Starlette에서 직접 가져온 것입니다.

///

### "마운팅"이란 { #what-is-mounting }

"마운팅"은 특정 경로에 완전한 "독립적인" 애플리케이션을 추가하고, 그 애플리케이션이 모든 하위 경로를 처리하도록 하는 것을 의미합니다.

마운트된 애플리케이션은 완전히 독립적이므로 `APIRouter`를 사용하는 것과는 다릅니다. 메인 애플리케이션의 OpenAPI 및 문서에는 마운트된 애플리케이션의 내용 등이 포함되지 않습니다.

자세한 내용은 [고급 사용자 가이드](../advanced/index.md){.internal-link target=_blank}에서 확인할 수 있습니다.

## 세부사항 { #details }

첫 번째 `"/static"`은 이 "하위 애플리케이션"이 "마운트"될 하위 경로를 가리킵니다. 따라서 `"/static"`으로 시작하는 모든 경로는 이 애플리케이션이 처리합니다.

`directory="static"`은 정적 파일이 들어 있는 디렉터리의 이름을 나타냅니다.

`name="static"`은 **FastAPI**에서 내부적으로 사용할 수 있는 이름을 제공합니다.

이 모든 매개변수는 "`static`"과 다를 수 있으며, 여러분의 애플리케이션 요구 사항 및 구체적인 세부 정보에 맞게 조정하세요.

## 추가 정보 { #more-info }

자세한 내용과 옵션은 <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette의 정적 파일 문서</a>를 확인하세요.
