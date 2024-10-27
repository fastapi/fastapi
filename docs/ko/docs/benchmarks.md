# 벤치마크

독립적인 TechEmpower 벤치마크에 따르면 **FastAPI** 애플리케이션이 Uvicorn을 사용하여 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">가장 빠른 Python 프레임워크 중 하나</a>로 실행되며, Starlette와 Uvicorn 자체(내부적으로 FastAPI가 사용하는 도구)보다 조금 아래에 위치합니다.

그러나 벤치마크와 비교를 확인할 때 다음 사항을 염두에 두어야 합니다.

## 벤치마크와 속도

벤치마크를 확인할 때, 일반적으로 여러 가지 유형의 도구가 동등한 것으로 비교되는 것을 볼 수 있습니다.

특히, Uvicorn, Starlette, FastAPI가 함께 비교되는 경우가 많습니다(다른 여러 도구와 함께).

도구가 해결하는 문제가 단순할수록 성능이 더 좋아집니다. 그리고 대부분의 벤치마크는 도구가 제공하는 추가 기능을 테스트하지 않습니다.

계층 구조는 다음과 같습니다:

* **Uvicorn**: ASGI 서버
    * **Starlette**: (Uvicorn 사용) 웹 마이크로 프레임워크
        * **FastAPI**: (Starlette 사용) API 구축을 위한 데이터 검증 등 여러 추가 기능이 포함된 API 마이크로 프레임워크

* **Uvicorn**:
    * 서버 자체 외에는 많은 추가 코드가 없기 때문에 최고의 성능을 발휘합니다.
    * 직접 Uvicorn으로 응용 프로그램을 작성하지는 않을 것입니다. 즉, 사용자의 코드에는 적어도 Starlette(또는 **FastAPI**)에서 제공하는 모든 코드가 포함되어야 합니다. 그렇게 하면 최종 응용 프로그램은 프레임워크를 사용하고 앱 코드와 버그를 최소화하는 것과 동일한 오버헤드를 갖게 됩니다.
    * Uvicorn을 비교할 때는 Daphne, Hypercorn, uWSGI 등의 응용 프로그램 서버와 비교하세요.
* **Starlette**:
    * Uvicorn 다음으로 좋은 성능을 발휘합니다. 사실 Starlette는 Uvicorn을 사용하여 실행됩니다. 따라서 더 많은 코드를 실행해야 하기 때문에 Uvicorn보다 "느려질" 수밖에 없습니다.
    * 하지만 경로 기반 라우팅 등 간단한 웹 응용 프로그램을 구축할 수 있는 도구를 제공합니다.
    * Starlette를 비교할 때는 Sanic, Flask, Django 등의 웹 프레임워크(또는 마이크로 프레임워크)와 비교하세요.
* **FastAPI**:
    * Starlette가 Uvicorn을 사용하므로 Uvicorn보다 빨라질 수 없는 것과 마찬가지로, **FastAPI**는 Starlette를 사용하므로 더 빠를 수 없습니다.
    * FastAPI는 Starlette에 추가적으로 더 많은 기능을 제공합니다. API를 구축할 때 거의 항상 필요한 데이터 검증 및 직렬화와 같은 기능들이 포함되어 있습니다. 그리고 이를 사용하면 문서 자동화 기능도 제공됩니다(문서 자동화는 응용 프로그램 실행 시 오버헤드를 추가하지 않고 시작 시 생성됩니다).
    * FastAPI를 사용하지 않고 직접 Starlette(또는 Sanic, Flask, Responder 등)를 사용했다면 데이터 검증 및 직렬화를 직접 구현해야 합니다. 따라서 최종 응용 프로그램은 FastAPI를 사용한 것과 동일한 오버헤드를 가지게 될 것입니다. 많은 경우 데이터 검증 및 직렬화가 응용 프로그램에서 작성된 코드 중 가장 많은 부분을 차지합니다.
    * 따라서 FastAPI를 사용함으로써 개발 시간, 버그, 코드 라인을 줄일 수 있으며, FastAPI를 사용하지 않았을 때와 동일하거나 더 나은 성능을 얻을 수 있습니다(코드에서 모두 구현해야 하기 때문에).
    * FastAPI를 비교할 때는 Flask-apispec, NestJS, Molten 등 데이터 검증, 직렬화 및 문서화가 통합된 자동 데이터 검증, 직렬화 및 문서화를 제공하는 웹 응용 프로그램 프레임워크(또는 도구 집합)와 비교하세요.
