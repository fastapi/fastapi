# Geração de Projeto - Modelo

Você pode usar um gerador de projeto para começar, pois inclui muito da configuração inicial, segurança, banco de dados e primeiros endpoints da API já feitos para você.

Um gerador de projeto sempre terá uma configuração muito opinativa que você deve atualizar e adaptar às suas próprias necessidades, mas pode ser um bom ponto de partida para o seu projeto.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank"> https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Recursos

- Integração completa do **Docker** (baseado em Docker).
- Implantação do modo Docker Swarm.
- Integração e otimização do **Docker Compose** para desenvolvimento local.
- **Pronto para produção** Servidor da web Python usando Uvicorn e Gunicorn.
- Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank"> **FastAPI** </a> backend:
  - **Rápido**: Desempenho muito alto, a par de **NodeJS** e **Go** (graças a Starlette e Pydantic).
  - **Intuitivo**: Ótimo suporte ao editor. <abbr title="também conhecido como autocompletar, autocompletar, IntelliSense">Completar</abbr> em todos os lugares. Menos tempo de depuração.
  - **Fácil**: Projetado para ser fácil de usar e aprender. Menos tempo lendo documentos.
  - **Curto**: Minimize a duplicação de código. Vários recursos de cada declaração de parâmetro.
  - **Robusto**: Obtenha código pronto para produção. Com documentação interativa automática.
  - **Baseado em padrões**: baseado em (e totalmente compatível com) os padrões abertos para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> e <a href="http://json-schema.org/" class="external-link" target="_blank">Esquema JSON</a>.
  - <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank"> **Muitos outros recursos** </a> incluindo validação automática, serialização, interativo documentação, autenticação com tokens OAuth2 JWT, etc.
- **Senha segura** hash por padrão.
- Autenticação **token JWT**.
- Modelos **SQLAlchemy** (independentes das extensões Flask, para que possam ser usados ​​diretamente com os trabalhadores do Celery).
- Modelos iniciais básicos para usuários (modifique e remova conforme necessário).
- Migrações de **Alembic**.
- **CORS** (Compartilhamento de recursos de origem cruzada).
- **Celery** que pode importar e usar modelos e código do resto do back-end de maneira seletiva.
- Testes de backend REST baseados em **Pytest**, integrado ao Docker, para que você possa testar a interação completa da API, independente do banco de dados. Conforme é executado no Docker, ele pode construir um novo armazenamento de dados a cada vez (então você pode usar ElasticSearch, MongoDB, CouchDB ou o que quiser e apenas testar se a API funciona).
- Fácil integração do Python com **Jupyter Kernels** para desenvolvimento remoto ou no Docker com extensões como Atom Hydrogen ou Visual Studio Code Jupyter.
- Interface **Vue**:
  - Gerado com Vue CLI.
  - Tratamento de **Autenticação JWT**.
  - Visualização de login.
  - Após o login, visualização do painel principal.
  - Painel principal com criação e edição do usuário.
  - Edição de usuário próprio.
  - **Vuex**.
  - **Vue-router**.
  - **Vuetify** para belos componentes de design de materiais.
  - **TypeScript**.
  - Servidor Docker baseado em **Nginx** (configurado para funcionar bem com o roteador Vue).
  - Construção de vários estágios do Docker, para que você não precise salvar ou confirmar o código compilado.
  - Os testes de front-end foram executados em tempo de construção (também podem ser desabilitados).
  - Feito da forma mais modular possível, por isso funciona fora da caixa, mas você pode gerar novamente com o Vue CLI ou criá-lo conforme necessário e reutilizar o que quiser.
- **PGAdmin** para banco de dados PostgreSQL, você pode modificá-lo para usar PHPMyAdmin e MySQL facilmente.
- **Flor** para monitoramento de trabalhos de celery.
- Balanceamento de carga entre front-end e back-end com **Traefik**, para que você possa ter ambos no mesmo domínio, separados por caminho, mas atendidos por contêineres diferentes.
- Integração do Traefik, incluindo a geração automática de certificados Let's Encrypt **HTTPS**.
- GitLab **CI** (integração contínua), incluindo testes de front-end e back-end.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank"> https://github.com/tiangolo/full- stack-fastapi-couchbase </a>

⚠️ **AVISO** ⚠️

Se você está começando um novo projeto do zero, verifique as alternativas aqui.

Por exemplo, o gerador de projeto <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank"> Full Stack FastAPI PostgreSQL </a> pode ser uma alternativa melhor, pois é ativamente mantido e usado. E inclui todos os novos recursos e melhorias.

Você ainda está livre para usar o gerador baseado em Couchbase se quiser, provavelmente ainda funcionará bem e, se você já tiver um projeto gerado com ele, também está bem (e provavelmente já o atualizou para atender às suas necessidades).

Você pode ler mais sobre isso na documentação do repo.

## Full Stack FastAPI MongoDB

... pode vir mais tarde, dependendo da minha disponibilidade de tempo e outros fatores. 😅 🎉

## Modelos de aprendizado de máquina com spaCy e FastAPI

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank"> https://github.com/microsoft/cookiecutter-spacy- fastapi </a>

### Modelos de aprendizado de máquina com spaCy e FastAPI - Recursos

- **SpaCy** Integração do modelo NER.
- Formato de solicitação **Azure Cognitive Search** integrado.
- **Pronto para produção** Servidor da web Python usando Uvicorn e Gunicorn.
- **Azure DevOps** Implantação de CI/CD do Kubernetes (AKS) integrada.
- **Multilíngue** Escolha facilmente um dos idiomas integrados do spaCy durante a configuração do projeto.
- **Facilmente extensível** a outras estruturas de modelo (Pytorch, Tensorflow), não apenas spaCy.
