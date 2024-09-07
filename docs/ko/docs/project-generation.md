# Full Stack FastAPI 템플릿

템플릿, 일반적으로 특정 설정과 함께 제공되는 것은, 유연하고 사용자 정의가 가능하게 디자인 되었습니다. 이 특성들은 당신이 프로젝트의 요구사항에 맞춰 수정과 적용을 하게 해주고, 템플릿이 완벽한 시작점이 되게 해줍니다. 🏁

이 템플릿은 많은 초기 설정, 보안, 데이터베이스 및 일부 API 엔드포인트가 이미 준비되어 있으므로 시작하는 데 사용할 수 있습니다.

GitHub 저장소: <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI 템플릿</a>

## Full Stack FastAPI 템플릿 - 기술 스택과 기능들

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) Python 백엔드 API를 위한.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) Python SQL 데이터 상호작용을 위한 (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), FastAPI에 의해 사용되는, 데이터 검증과 설정관리를 위해.
    - 💾 [PostgreSQL](https://www.postgresql.org) SQL 데이터베이스.
- 🚀 [React](https://react.dev) 프론트엔드를 위한.
    - 💃 TypeScript, hooks, Vite 및 기타 현대적인 프론트엔드 스택을 사용합니다.
    - 🎨 [Chakra UI](https://chakra-ui.com) 프론트엔드 컴포넌트를 위한.
    - 🤖 자동으로 생성된 프론트엔드 클라이언트.
    - 🧪 종단간 테스팅을 위한 Playwright.
    - 🦇 다크 모드 지원.
- 🐋 [Docker Compose](https://www.docker.com) 개발 및 프로덕션을 위한.
- 🔒 기본으로 지원되는 안전한 비밀번호 해싱.
- 🔑 JWT 토큰 인증.
- 📫 이메일 기반 비밀번호 복구.
- ✅ [Pytest]를 이용한 테스트(https://pytest.org).
- 📞 [Traefik](https://traefik.io) 리버스 프록시 / 로드 밸런서.
- 🚢 Docker Compose를 이용한 배포 지침, 자동 HTTPS 인증서를 처리하기 위한 프론트엔드 Traefik 프록시 설정 방법을 포함하는.
- 🏭 GitHub Actions를 기반으로 한 CI (지속적인 통합) 및 CD (지속적인 배포).
