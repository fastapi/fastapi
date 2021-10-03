# 프로젝트 생성 - 템플릿

당신은 프로젝트 생성기를 사용하여 시작할 수 있으며, 생성기에는 초기설정, 보안, 데이터베이스 및 초기 API 엔드포인트 등이 설정 되어있습니다.

프로젝트 생성기를 사용하기 위해서는 항상 당신의 필요에 맞게 업데이트하고 또 설정해야 하는 부분이 있지만, 이것은 프로젝트를 시작하기에 좋은 역할을 해줄 것입니다.

## 풀 스택 FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### 전체 스택 FastAPI PostgreSQL - 기능

* 전체 **Docker**를 통합합니다. (Docker 기반).
* **Docker Swarm Mode**를 배포합니다.
* **Docker**는 지역 개발을 위한 통합 및 최적화 시킵니다.
* Uvicorn 및 Gunicorn을 사용한 Python 웹 서버를 준비합니다.
* 파이썬 <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank"> **FastAPI**</a> 백엔드:

  * **빠르다**: **NodeJS**와 **GO** 수준의 매우 빠른 성능 (Starlette 와 Pydantic로 인해서)
  * **직관적**: 훌륭한 편집자 지원. 어느 환경에서나 디버깅 시간 단축.
  * **쉽다**: 쉽게 사용하고 배울 수 있도록 설계 문서 읽는 시간 단축
  * **짧다**: 코드의 중복 최소화. 매개변수 한 개의 다중 기능 가능.
  * **강력**: 프로덕션에 바로 사용할 수 있는 코드를 제공. 자동 대화형 문서를 사용.
  * **표준 기반**: API에 대한 개방형 표준 기반. <a href="https://github.com/OAI/OpenAPI-Specification" class="외부 링크" target="_blank">OpenAPI</a> 및 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON 스키마</a>를 기반으로 완전한 호환 가능.
  * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**기타 기능**</a>: 자동 유효성 검사, 직렬화, 대화형 문서, OAuth2 JWT 토큰을 사용한 인증 등을 포함한 여러 기능.
* **암호 보안** 해싱은 기본적으로 수행됩니다.

* **JWT 토큰** 인증 기능을 가집니다.
* **SQLlchemy 모델**을 통해 플라스크 확장과 별개로 셀러리 작업자와 함께 직접 사용할 수 있습니다.
* 사용자를 위한 기본 시작 모델을 가지며, 필요에 따라 수정 및 제거가 가능합니다.
* **Alembic migrations** 특징을 가집니다.
* **CORS** (Cross Origin Resource Sharing) 특징을 가집니다.
* 셀러리 작업자를 통해 나머지 백엔드에서 모델과 코드를 선택적으로 가져와 사용할 수 있습니다.
* Docker와 통합된 Pytest 기반 REST 백엔드 테스트를 통해 데이터베이스에서 독립적으로 전체 API 상호 작용을 테스트 할 수 있습니다. Docker에서 실행되므로 매번 처음부터 새로운 데이터 저장소를 구축할 수 있습니다. 따라서 Elastic Search, MonogoDB, CouchDB 등의 원하는 것을 사용할 수 있으며, API가 작동하는지 테스트 해볼 수 있습니다.
* Atom Hydrogen 또는 Visual Studio Code Jupyter과 같은 확장 기능을 갖춘 원격 또는 Docker개발을 위해 Jupyter Kernels 과 Python을 쉽게 통합할 수 있다.
* **Vue** 프런트엔드:
  * Vue CLI를 사용하여 생성됨.
  * **JWT 인증** 처리.
  * 로그인 보기.
  * 로그인 후 기본 대시보드 보기.
  * 사용자 생성 및 에디션이 포함된 기본 대시보드.
  * 셀프 사용자 에디션.
  * **Vuex.**
  * **Vue-router.**
  * 아름다운 재료 디자인 구성 요소를 확인.
  * **TypeScript**.
  * **Nginx** 기반의 도커 서버 (Vue-router와 원활하게 작동하도록 구성)
  * 도커 다단계 빌딩으로 컴파일된 코드를 저장하거나 커밋할 필요 없음.
  * 프런트엔드 테스트는 빌드 시간에 실행 (사용 불가능으로 설정 가능)
  * 가능한 한 모듈식으로 제작되어 즉시 사용할 수 있지만, Vue CLI를 사용하여 다시 생성하거나 필요에 따라 생성하고 원하는 것을 다시 사용할 수 있음.
* **PGADmin for PostgreSQL 데이터베이스**는 PHPmyAdmin 및 MySQL을 쉽게 사용하도록 수정할 수 있습니다.
* 셀러리 작업 감시를 위한 Flower을 가집니다.
* **HTTPS** 인증서 자동 생성을 암호화하는 트레이픽을 통합합니다.
* 프런트엔드 및 백엔드 테스트 포함한 GitLab **CI**(연속 통합)을 가집니다.

## 풀 스택 FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank"> https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠**경고**⚠

새 프로젝트를 처음 시작하는 경우, 이곳에서 대안을 확인하십시오.

예를 들어 프로젝트 생성기 풀 스택 <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a>은 적극적으로 유지 관리 및 사용되므로 더 나은 대안이 될 수 있습니다. 그리고 이곳에서 모든 새로운 기능과 향상된 기능을 확인할 수 있습니다.

원하는 경우 Couchbase 생성기를 자유롭게 사용할 수 있습니다. 아마 여전히 잘 작동할 것이며, 이미 생성된 프로젝트가 있는 경우에도 괜찮습니다. (아마도 필요에 맞게 업데이트 했을 것입니다.)

이에 대한 자세한 내용은 repo 문서를 참조하십시오.

## 풀 스택 FastAPI MongoDB

아직 공개되지 않았습니다. 추후에 업데이트 하겠습니다.😅 🎉

## spaCy and FastAPI를 지원하는 머신러닝 모델

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### spaCy and FastAPI를 지원하는 머신러닝 모델 - 기능

* **spaCy** NER 모델 통합.
* **Azure 인지 검색** 요청이 내장됨.
* Uvicorn 및 Gunicorn을 사용한 Python 웹 서버를 준비합니다.
* **Azure DevOps Kubernetes (AKS) CI/CD** 배포가 기본 제공됩니다.
* 다국어 프로젝트 설정에서 spaCy의 기본 제공 언어 중 하나를 쉽게 선택할 수 있습니다.
* spaCy뿐 아니라 다른 프레임워크(Pytorch, Tensorflow 등) 로도 쉽게 확장 가능합니다.