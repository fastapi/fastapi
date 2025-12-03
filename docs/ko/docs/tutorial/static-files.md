# 정적 파일

'StaticFiles'를 사용하여 디렉토리에서 정적 파일을 자동으로 제공할 수 있습니다.

## `StaticFiles` 사용

* `StaticFiles` 임포트합니다.
* 특정 경로에 `StaticFiles()` 인스턴스를 "마운트" 합니다.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | 기술적 세부사항

`from starlette.staticfiles import StaticFiles` 를 사용할 수도 있습니다.

**FastAPI**는 단지 개발자인, 당신에게 편의를 제공하기 위해 `fastapi.static files` 와 동일한 `starlett.static files`를 제공합니다. 하지만 사실 이것은 Starlett에서 직접 온 것입니다.

///

### "마운팅" 이란

"마운팅"은 특정 경로에 완전히 "독립적인" 애플리케이션을 추가하는 것을 의미하는데, 그 후 모든 하위 경로에 대해서도 적용됩니다.

마운트된 응용 프로그램은 완전히 독립적이기 때문에 `APIRouter`를 사용하는 것과는 다릅니다. OpenAPI 및 응용 프로그램의 문서는 마운트된 응용 프로그램 등에서 어떤 것도 포함하지 않습니다.

자세한 내용은 **숙련된 사용자 안내서**에서 확인할 수 있습니다.

## 세부사항

첫 번째 `"/static"`은 이 "하위 응용 프로그램"이 "마운트"될 하위 경로를 가리킵니다. 따라서 `"/static"`으로 시작하는 모든 경로는 `"/static"`으로 처리됩니다.

`'directory="static"`은 정적 파일이 들어 있는 디렉토리의 이름을 나타냅니다.

`name="static"`은 **FastAPI**에서 내부적으로 사용할 수 있는 이름을 제공합니다.

이 모든 매개변수는 "`static`"과 다를 수 있으며, 사용자 응용 프로그램의 요구 사항 및 구체적인 세부 정보에 따라 매개변수를 조정할 수 있습니다.


## 추가 정보

자세한 내용과 선택 사항을 보려면 <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette의 정적 파일에 관한 문서</a>를 확인하십시오.
