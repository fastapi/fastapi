# 项目生成器 - 模版

您可以使用一个项目生成器来开启您的项目，因为它已经包含了一些最初的配置、安全性、数据库和一些API端点。

一个项目生成器总是有着非常主观的设置，您应该更新和调整它以满足自己的需求，但它可能是您项目的很好的起点。

## 全栈 FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### 全栈 FastAPI PostgreSQL - 特性

* 完整的 **Docker** 集成 (基于Docker)。
* Docker Swarm 模式部署。
* **Docker Compose** 集成和优化本地开发。
* 使用 Uvicorn 和 Gunicorn 的 **生产就绪** Python Web 服务器。
* Python <a href="https://github。com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> 后端：
    * **快速**: 非常高效的性能，与 **NodeJS** 和 **Go** 相当(感谢 Starlette 和 Pydantic)。
    * **直观**: 良好的编辑器支持。全局自动补全。缩短调试时间。
    * **易用**: 易于使用和学习。减少阅读文档的时间。
    * **简短**: 尽量减少代码重复。每个参数声明有多个特性。
    * **稳定**: 可用于生产级别的代码并自动生成可交互的接口文档。
    * **基于标准**: 基于(并且完全兼容)关于API的开放标准: <a href="https://github。com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 和 <a href="https://json-schema。org/" class="external-link" target="_blank">JSON Schema</a>。
    * <a href="https://fastapi。tiangolo。com/features/" class="external-link" target="_blank">**许多其他特性**</a>， 包括自动表单验证、序列化、交互式文档、OAuth2 JWT令牌认证等。
* 默认**安全密码**哈希。
* **JWT token** 认证。
* **SQLAlchemy** 模型 (独立于 Flask 扩展， 因此它们可以直接用于 Celery workers)。
* 基础的用户模型 (根据需要进行更改和删除)。
* **Alembic** 迁移。
* **CORS** (跨域资源共享)。
* 可以选择性地从后端导入和使用模型和代码的 **Celery** worker。
* 基于 **Pytest** 的REST 后端测试，与Docker集成，因此您可以独立于数据库测试全部 API 交互。由于它在Docker中运行，所以每次它可以从头开始构建一个新的数据存储(因此您可以使用 ElasticSearch，MongoDB，CouchDB 或任何您想要的，只是测试 API 是否正常工作)。
* 与扩展项像 Atom Hydrogen 或 Visual Studio Code Jupyter 的 **Jupyter内核** 进行轻松的Python集成远程或在Docker开发。
* **Vue** 前端:
    - Vue CLI生成。
    - **JWT认证** 处理。
    - 登录视图。
    - 登录后主仪表板视图。
    - 具有用户创建和编辑的主要仪表板。
    - 自我用户编辑。
    - **Vuex**。
    - **Vue-router**。
    - **Vuetify** 美化套件。
    - **TypeScript**。
    - 基于**Nginx**的Docker服务器 (可以很好的与 Vue-router 一起工作)。
    - Docker多段式构建，所以您无需保存或提交已编译的代码。 
    - 前端测试在构建时运行(也可以禁用)。 
    - 尽可能模块化，因此它可以直接使用，但是您也可以使用Vue CLI重新生成或按需创建，并复用您想要的内容。
* **PGAdmin** 用于管理PostgreSQL 数据库， 您也可以改为使用 PHPMyAdmin 和 MySQL。
* **Flower** 监控Celery。
* 前端和后端使用 **Traefik** 负载均衡，这样您可以将两者放在同一个域下，通过路径分离但由不同的容器提供服务。
* Traefik 集成，包括自动生成 Let's Encrypt **HTTPS** 证书。
* GitLab **CI**(持续集成)，包括前端和后端测试。

## 全栈FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **警告** ⚠️

如果您从头开始启动一个新项目，请查看这里的替代方案。

例如，项目生成器<a href="https://github。com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a> 可能是更好的选择，因为它正在活跃地维护和使用。并且包含了所有新的功能和改进。

如果您仍然想使用基于Couchbase的生成器，它可能仍然可以很好地工作，并且如果您已经有一个生成的项目适合您的需求也是可以的。

您可以在库的文档中阅读更多关于它的信息。

## **全栈 FastAPI + MongoDB**

……敬请期待，得看我有没有时间做这个项目。😅 🎉

## spaCy 和 FastAPI 的机器学习模型

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### spaCy和FastAPI的机器学习模型 - 特性

* **spaCy** NER模型集成。
* 内置**Azure Cognitive Search**请求格式。
* 使用 Uvicorn 和 Gunicorn 的 **生产就绪** Python Web 服务器。
* **Azure DevOps** Kubernetes (AKS) CI/CD 部署内置。
* **多语言** 在项目设置期间轻松选择其中一个 spaCy's 内置语言。
* 易于扩展到其他模型框架(Pytorch， Tensorflow)，不仅仅是spaCy。
