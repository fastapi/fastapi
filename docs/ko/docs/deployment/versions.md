# FastAPI 버전들에 대하여 { #about-fastapi-versions }

**FastAPI**는 이미 많은 애플리케이션과 시스템에서 프로덕션으로 사용되고 있습니다. 그리고 테스트 커버리지는 100%로 유지됩니다. 하지만 개발은 여전히 빠르게 진행되고 있습니다.

새로운 기능이 자주 추가되고, 버그가 규칙적으로 수정되며, 코드는 계속해서 지속적으로 개선되고 있습니다.

그래서 현재 버전이 아직 `0.x.x`인 것입니다. 이는 각 버전이 잠재적으로 하위 호환성이 깨지는 변경을 포함할 수 있음을 반영합니다. 이는 <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a> 관례를 따릅니다.

지금 바로 **FastAPI**로 프로덕션 애플리케이션을 만들 수 있습니다(그리고 아마도 한동안 그렇게 해오셨을 것입니다). 다만 나머지 코드와 함께 올바르게 동작하는 버전을 사용하고 있는지 확인하기만 하면 됩니다.

## `fastapi` 버전을 고정하기 { #pin-your-fastapi-version }

가장 먼저 해야 할 일은 여러분의 애플리케이션에서 올바르게 동작하는 것으로 알고 있는 **FastAPI**의 최신 구체 버전에 맞춰 사용 중인 버전을 "고정(pin)"하는 것입니다.

예를 들어, 앱에서 `0.112.0` 버전을 사용하고 있다고 가정해 보겠습니다.

`requirements.txt` 파일을 사용한다면 다음과 같이 버전을 지정할 수 있습니다:

```txt
fastapi[standard]==0.112.0
```

이는 정확히 `0.112.0` 버전을 사용한다는 의미입니다.

또는 다음과 같이 고정할 수도 있습니다:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

이는 `0.112.0` 이상이면서 `0.113.0` 미만의 버전을 사용한다는 의미입니다. 예를 들어 `0.112.2` 버전도 허용됩니다.

`uv`, Poetry, Pipenv 등 다른 도구로 설치를 관리한다면, 모두 패키지의 특정 버전을 정의할 수 있는 방법을 제공합니다.

## 이용 가능한 버전들 { #available-versions }

사용 가능한 버전(예: 현재 최신 버전이 무엇인지 확인하기 위해)은 [Release Notes](../release-notes.md){.internal-link target=_blank}에서 확인할 수 있습니다.

## 버전들에 대해 { #about-versions }

Semantic Versioning 관례에 따르면, `1.0.0` 미만의 어떤 버전이든 잠재적으로 하위 호환성이 깨지는 변경을 추가할 수 있습니다.

FastAPI는 또한 "PATCH" 버전 변경은 버그 수정과 하위 호환성이 깨지지 않는 변경을 위한 것이라는 관례를 따릅니다.

/// tip | 팁

"PATCH"는 마지막 숫자입니다. 예를 들어 `0.2.3`에서 PATCH 버전은 `3`입니다.

///

따라서 다음과 같이 버전을 고정할 수 있어야 합니다:

```txt
fastapi>=0.45.0,<0.46.0
```

하위 호환성이 깨지는 변경과 새로운 기능은 "MINOR" 버전에 추가됩니다.

/// tip | 팁

"MINOR"는 가운데 숫자입니다. 예를 들어 `0.2.3`에서 MINOR 버전은 `2`입니다.

///

## FastAPI 버전 업그레이드하기 { #upgrading-the-fastapi-versions }

앱에 테스트를 추가해야 합니다.

**FastAPI**에서는 매우 쉽습니다(Starlette 덕분에). 문서를 확인해 보세요: [Testing](../tutorial/testing.md){.internal-link target=_blank}

테스트를 갖춘 뒤에는 **FastAPI** 버전을 더 최신 버전으로 업그레이드하고, 테스트를 실행하여 모든 코드가 올바르게 동작하는지 확인하세요.

모든 것이 동작하거나 필요한 변경을 한 뒤 모든 테스트가 통과한다면, `fastapi`를 그 새로운 최신 버전으로 고정할 수 있습니다.

## Starlette에 대해 { #about-starlette }

`starlette`의 버전은 고정하지 않는 것이 좋습니다.

서로 다른 **FastAPI** 버전은 Starlette의 특정한 더 새로운 버전을 사용하게 됩니다.

따라서 **FastAPI**가 올바른 Starlette 버전을 사용하도록 그냥 두면 됩니다.

## Pydantic에 대해 { #about-pydantic }

Pydantic은 자체 테스트에 **FastAPI**에 대한 테스트도 포함하고 있으므로, Pydantic의 새 버전(`1.0.0` 초과)은 항상 FastAPI와 호환됩니다.

여러분에게 맞는 `1.0.0` 초과의 어떤 Pydantic 버전으로든 고정할 수 있습니다.

예를 들어:

```txt
pydantic>=2.7.0,<3.0.0
```
