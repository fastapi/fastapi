# 基准测试 { #benchmarks }

第三方机构 TechEmpower 的基准测试表明，在 Uvicorn 下运行的 **FastAPI** 应用是 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">目前可用的最快的 Python 框架之一</a>，仅次于 Starlette 和 Uvicorn 本身（FastAPI 内部使用）。

但是在查看基准测试和对比时，请记住以下几点。

## 基准测试与速度 { #benchmarks-and-speed }

当你查看基准测试时，常见的情况是把几种不同类型的工具等效地做比较。

具体来说，会把 Uvicorn、Starlette 和 FastAPI 放在一起比较（以及许多其他工具）。

工具解决的问题越简单，它获得的性能就越好。而且大多数基准测试并不会测试该工具提供的附加功能。

层级结构如下：

* **Uvicorn**：ASGI 服务器
    * **Starlette**：（使用 Uvicorn）Web 微框架
        * **FastAPI**：（使用 Starlette）用于构建 API 的 API 微框架，带有多个附加功能，比如数据校验等。

* **Uvicorn**:
    * 性能会最好，因为除了服务器本身外，它没有太多额外代码。
    * 你不会直接用 Uvicorn 来编写应用。这意味着你的代码至少必须包含或多或少、至少 Starlette（或 **FastAPI**）提供的全部代码。如果你那样做了，你最终的应用会有与使用框架并最小化你的应用代码和 bug 相同的额外开销。
    * 如果你要对比 Uvicorn，请把它与 Daphne、Hypercorn、uWSGI 等应用服务器进行比较。
* **Starlette**:
    * 会有仅次于 Uvicorn 的性能。事实上，Starlette 使用 Uvicorn 运行。所以，它很可能只能因为要执行更多代码而比 Uvicorn“更慢”。
    * 但它为你提供了构建简单 Web 应用的工具，比如基于路径的路由等。
    * 如果你要对比 Starlette，请把它与 Sanic、Flask、Django 等 Web 框架（或微框架）进行比较。
* **FastAPI**:
    * 就像 Starlette 使用 Uvicorn 因而不可能比它更快一样，**FastAPI** 使用 Starlette，所以也不可能比它更快。
    * FastAPI 在 Starlette 之上提供了更多功能。这些是在构建 API 时几乎总会需要的功能，比如数据校验和序列化。并且使用它，你可以免费获得自动文档（自动文档甚至不会给运行中的应用增加额外开销，它是在启动时生成的）。
    * 如果你不使用 FastAPI 而是直接使用 Starlette（或其他工具，比如 Sanic、Flask、Responder 等），你就必须自己实现所有数据校验和序列化。因此，你最终的应用仍然会有与使用 FastAPI 构建时相同的额外开销。而且在很多情况下，这些数据校验和序列化会是应用中编写代码最多的部分。
    * 因此，通过使用 FastAPI，你可以节省开发时间、减少 bug、减少代码行数，并且你很可能会获得与不使用它时相同的性能（甚至更好）（因为否则你就必须在自己的代码中把这些都实现一遍）。
    * 如果你要对比 FastAPI，请把它与提供数据校验、序列化和文档的 Web 应用框架（或工具集）进行比较，比如 Flask-apispec、NestJS、Molten 等——那些集成了自动数据校验、序列化和文档的框架。
