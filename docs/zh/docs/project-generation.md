# 项目生成 - 模板

项目生成器一般都会提供很多初始设置、安全措施、数据库，甚至还准备好了第一个 API 端点，能帮助您快速上手。

项目生成器的设置通常都很主观，您可以按需更新或修改，但对于您的项目来说，它是非常好的起点。

## 全栈 FastAPI + PostgreSQL

GitHub：<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### 全栈 FastAPI + PostgreSQL - 功能

* 完整的 **Docker** 集成（基于 Docker）
* Docker Swarm 开发模式
* **Docker Compose** 本地开发集成与优化
* **生产可用**的 Python 网络服务器，使用 Uvicorn 或 Gunicorn
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> 后端：
* * **速度快**：可与 **NodeJS** 和 **Go** 比肩的极高性能（归功于 Starlette 和 Pydantic）
    * **直观**：强大的编辑器支持，处处皆可<abbr title="也叫自动完成、智能感知">自动补全</abbr>，减少调试时间
    * **简单**：易学、易用，阅读文档所需时间更短
    * **简短**：代码重复最小化，每次参数声明都可以实现多个功能
    * **健壮**： 生产级别的代码，还有自动交互文档
    * **基于标准**：完全兼容并基于 API 开放标准：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 和 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**更多功能**</a>包括自动验证、序列化、交互文档、OAuth2 JWT 令牌身份验证等
* **安全密码**，默认使用密码哈希
* **JWT 令牌**身份验证
* **SQLAlchemy** 模型（独立于 Flask 扩展，可直接用于 Celery Worker）
* 基础的用户模型（可按需修改或删除）
* **Alembic** 迁移
* **CORS**（跨域资源共享）
* **Celery** Worker 可从后端其它部分有选择地导入并使用模型和代码
* REST 后端测试基于 Pytest，并与 Docker 集成，可独立于数据库实现完整的 API 交互测试。因为是在 Docker 中运行，每次都可从头构建新的数据存储（使用 ElasticSearch、MongoDB、CouchDB 等数据库，仅测试 API 运行）
* Python 与 **Jupyter Kernels** 集成，用于远程或 Docker 容器内部开发，使用 Atom Hydrogen 或 Visual Studio Code 的 Jupyter 插件
* **Vue** 前端：
    * 由 Vue CLI 生成
    * **JWT 身份验证**处理
    * 登录视图
    * 登录后显示主仪表盘视图
    * 主仪表盘支持用户创建与编辑
    * 用户信息编辑
    * **Vuex**
    * **Vue-router**
    * **Vuetify** 美化组件
    * **TypeScript**
    * 基于 **Nginx** 的 Docker 服务器（优化了 Vue-router 配置）
    * Docker 多阶段构建，无需保存或提交编译的代码
    * 在构建时运行前端测试（可禁用）
    * 尽量模块化，开箱即用，但仍可使用 Vue CLI 重新生成或创建所需项目，或复用所需内容
* 使用 **PGAdmin** 管理 PostgreSQL 数据库，可轻松替换为 PHPMyAdmin 或 MySQL
* 使用 **Flower** 监控 Celery 任务
* 使用 **Traefik** 处理前后端负载平衡，可把前后端放在同一个域下，按路径分隔，但在不同容器中提供服务
* Traefik 集成，包括自动生成 Let's Encrypt **HTTPS** 凭证
* GitLab **CI**（持续集成），包括前后端测试

## 全栈 FastAPI + Couchbase

GitHub：<a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **警告** ⚠️

如果您想从头开始创建新项目，建议使用以下备选方案。

例如，项目生成器<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">全栈 FastAPI + PostgreSQL </a>会更适用，这个项目的维护积极，用的人也多，还包括了所有新功能和改进内容。

当然，您也可以放心使用这个基于 Couchbase 的生成器，它也能正常使用。就算用它生成项目也没有任何问题（为了更好地满足需求，您可以自行更新这个项目）。

详见资源仓库中的文档。

## 全栈 FastAPI + MongoDB

……敬请期待，得看我有没有时间做这个项目。😅 🎉

## FastAPI + spaCy 机器学习模型

GitHub：<a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### FastAPI + spaCy 机器学习模型 - 功能

* 集成 **spaCy** NER 模型
* 内置 **Azure 认知搜索**请求格式
* **生产可用**的 Python 网络服务器，使用 Uvicorn 与 Gunicorn
* 内置 **Azure DevOps** Kubernetes (AKS) CI/CD 开发
* **多语**支持，可在项目设置时选择 spaCy 内置的语言
* 不仅局限于 spaCy，可**轻松扩展**至其它模型框架（Pytorch、TensorFlow）
