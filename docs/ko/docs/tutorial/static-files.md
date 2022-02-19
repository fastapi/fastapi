# 정적 파일

'StaticFiles'을 사용하는 디렉터리로부터 자동으로 정적 파일을 서비스할 수 있습니다.

## `StaticFiles` 사용하기

* `StaticFiles` 가져오기
* 특정 경로 안에 `StaticFiles()` 인스턴스를 "마운트"

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! 기술 세부사항
    `from starlette.staticfiles import StaticFiles`를 이용할 수도 있습니다. 

    **FastAPI**는 개발자인 당신에게 편의를 제공하기 위해 `starlette.staticfiles`와 동일한 `fastapi.staticfiles`를 제공합니다. 실제로는 Starlette으로부터 직접 온 것입니다. 

### "마운팅"이란

"마운팅"은 특정 경로에 완전히 "독립된" 애플리케이션을 추가하여 모든 하위 경로를 처리하는 것을 의미합니다.

이는 마운트된 애플리케이션이 완전히 독립적이기 때문에 APIRouter를 사용하는 것과는 다릅니다. 메인 애플리케이션의 OpenAPI 및 문서에는 마운트된 응용 프로그램 등의 항목이 포함되지 않습니다.

자세한 내용은 **사용자 안내서 고급편**에서 확인할 수 있습니다.


## 세부사항

첫 번째 `"/static"`은 이 "서브 애플리케이션"이 "탑재"될 하위 경로를 나타냅니다. 따라서 "/static"로 시작하는 모든 경로는 이 경로에 의해 처리됩니다.

`directory="static"`은 정적 파일이 들어 있는 디렉터리의 이름을 나타냅니다.

`name="static"`은 **FastAPI** 내부에서 쓰게 될 이름을 뜻합니다.

이러한 모든 매개변수는 "`static`"과 다를 수 있으므로, 응용 프로그램의 요구 사항과 특정 세부 사항에 따라 변경하시기 바랍니다.

## 추가 정보

더 자세한 세부사항과 옵션은 <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>에서 확인하시기 바랍니다.
