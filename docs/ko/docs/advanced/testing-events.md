# 이벤트 테스트: 라이프스팬 및 시작 - 종료 { #testing-events-lifespan-and-startup-shutdown }

테스트에서 `lifespan`을 실행해야 하는 경우, `with` 문과 함께 `TestClient`를 사용할 수 있습니다:

{* ../../docs_src/app_testing/tutorial004_py39.py hl[9:15,18,27:28,30:32,41:43] *}


["공식 Starlette 문서 사이트에서 테스트에서 라이프스팬 실행하기."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)에 대한 자세한 내용을 더 읽을 수 있습니다.

더 이상 권장되지 않는 `startup` 및 `shutdown` 이벤트의 경우, 다음과 같이 `TestClient`를 사용할 수 있습니다:

{* ../../docs_src/app_testing/tutorial003_py39.py hl[9:12,20:24] *}
