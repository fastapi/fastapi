## Next release

* Use Python logger named "`fastapi`" instead of root logger. PR [#222](https://github.com/tiangolo/fastapi/pull/222) by [@euri10](https://github.com/euri10).

* Upgrade Pydantic to version 0.25. PR [#225](https://github.com/tiangolo/fastapi/pull/225) by [@euri10](https://github.com/euri10).

* Fix typo in routing. PR [#221](https://github.com/tiangolo/fastapi/pull/221) by [@djlambert](https://github.com/djlambert).

## 0.20.1

* Add typing information to package including file `py.typed`. PR [#209](https://github.com/tiangolo/fastapi/pull/209) by [@meadsteve](https://github.com/meadsteve).

* Add FastAPI bot for Gitter. To automatically announce new releases. PR [#189](https://github.com/tiangolo/fastapi/pull/189).

## 0.20.0

* Upgrade OAuth2:
    * Upgrade Password flow using Bearer tokens to use the correct HTTP status code 401 `UNAUTHORIZED`, with `WWW-Authenticate` headers.
    * Update, simplify, and improve all the [security docs](https://fastapi.tiangolo.com/tutorial/security/intro/).
    * Add new `scope_str` to `SecurityScopes` and update docs: [OAuth2 scopes](https://fastapi.tiangolo.com/tutorial/security/oauth2-scopes/).
    * Update docs, images, tests.
    * PR [#188](https://github.com/tiangolo/fastapi/pull/188).

* Include [Hypercorn](https://gitlab.com/pgjones/hypercorn) as an alternative ASGI server in the docs. PR [#187](https://github.com/tiangolo/fastapi/pull/187).

* Add docs for [Static Files](https://fastapi.tiangolo.com/tutorial/static-files/) and [Templates](https://fastapi.tiangolo.com/tutorial/templates/). PR [#186](https://github.com/tiangolo/fastapi/pull/186).

* Add docs for handling [Response Cookies](https://fastapi.tiangolo.com/tutorial/response-cookies/) and [Response Headers](https://fastapi.tiangolo.com/tutorial/response-headers/). PR [#185](https://github.com/tiangolo/fastapi/pull/185).

* Fix typos in docs. PR [#176](https://github.com/tiangolo/fastapi/pull/176) by [@chdsbd](https://github.com/chdsbd).

## 0.19.0

* Rename _path operation decorator_ parameter `content_type` to `response_class`. PR [#183](https://github.com/tiangolo/fastapi/pull/183).

* Add docs:
    * How to use the `jsonable_encoder` in [JSON compatible encoder](https://fastapi.tiangolo.com/tutorial/encoder/).
    * How to [Return a Response directly](https://fastapi.tiangolo.com/tutorial/response-directly/).
    * Update how to use a [Custom Response Class](https://fastapi.tiangolo.com/tutorial/custom-response/).
    * PR [#184](https://github.com/tiangolo/fastapi/pull/184).

## 0.18.0

* Add docs for [HTTP Basic Auth](https://fastapi.tiangolo.com/tutorial/custom-response/). PR [#177](https://github.com/tiangolo/fastapi/pull/177).

* Upgrade HTTP Basic Auth handling with automatic headers (automatic browser login prompt). PR [#175](https://github.com/tiangolo/fastapi/pull/175).

* Update dependencies for security. PR [#174](https://github.com/tiangolo/fastapi/pull/174).

* Add docs for [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). PR [#173](https://github.com/tiangolo/fastapi/pull/173).

## 0.17.0

* Make Flit publish from CI. PR [#170](https://github.com/tiangolo/fastapi/pull/170).

* Add documentation about handling [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/). PR [#169](https://github.com/tiangolo/fastapi/pull/169).

* By default, encode by alias. This allows using Pydantic `alias` parameters working by default. PR [#168](https://github.com/tiangolo/fastapi/pull/168).

## 0.16.0

* Upgrade _path operation_ `doctsring` parsing to support proper Markdown descriptions. New documentation at [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#description-from-docstring). PR [#163](https://github.com/tiangolo/fastapi/pull/163).

* Refactor internal usage of Pydantic to use correct data types. PR [#164](https://github.com/tiangolo/fastapi/pull/164).

* Upgrade Pydantic to version `0.23`. PR [#160](https://github.com/tiangolo/fastapi/pull/160) by [@euri10](https://github.com/euri10).

* Fix typo in Tutorial about Extra Models. PR [#159](https://github.com/tiangolo/fastapi/pull/159) by [@danielmichaels](https://github.com/danielmichaels).

* Fix [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) URL examples in docs. PR [#157](https://github.com/tiangolo/fastapi/pull/157) by [@hayata-yamamoto](https://github.com/hayata-yamamoto).

## 0.15.0

* Add support for multiple file uploads (as a single form field). New docs at: [Multiple file uploads](https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads). PR [#158](https://github.com/tiangolo/fastapi/pull/158).

* Add docs for: [Additional Status Codes](https://fastapi.tiangolo.com/tutorial/additional-status-codes/). PR [#156](https://github.com/tiangolo/fastapi/pull/156).

## 0.14.0

* Improve automatically generated names of path operations in OpenAPI (in API docs). A function `read_items` instead of having a generated name "Read Items Get" will have "Read Items". PR [#155](https://github.com/tiangolo/fastapi/pull/155).

* Add docs for: [Testing **FastAPI**](https://fastapi.tiangolo.com/tutorial/testing/). PR [#151](https://github.com/tiangolo/fastapi/pull/151).

* Update `/docs` Swagger UI to enable deep linking. This allows sharing the URL pointing directly to the path operation documentation in the docs. PR [#148](https://github.com/tiangolo/fastapi/pull/148) by [@wshayes](https://github.com/wshayes).

* Update development dependencies, `Pipfile.lock`. PR [#150](https://github.com/tiangolo/fastapi/pull/150).

* Include Falcon and Hug in: [Alternatives, Inspiration and Comparisons](https://fastapi.tiangolo.com/alternatives/).

## 0.13.0

* Improve/upgrade OAuth2 scopes support with `SecurityScopes`:
    * `SecurityScopes` can be declared as a parameter like `Request`, to get the scopes of all super-dependencies/dependants.
    * Improve `Security` handling, merging scopes when declaring `SecurityScopes`.
    * Allow using `SecurityBase` (like `OAuth2`) classes with `Depends` and still document them. `Security` now is needed only to declare `scopes`.
    * Updated docs about: [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
    * New docs about: [OAuth2 scopes](https://fastapi.tiangolo.com/tutorial/security/oauth2-scopes/).
    * PR [#141](https://github.com/tiangolo/fastapi/pull/141).

## 0.12.1

* Fix bug: handling additional `responses` in `APIRouter.include_router()`. PR [#140](https://github.com/tiangolo/fastapi/pull/140).

* Fix typo in SQL tutorial. PR [#138](https://github.com/tiangolo/fastapi/pull/138) by [@mostaphaRoudsari](https://github.com/mostaphaRoudsari).

* Fix typos in section about nested models and OAuth2 with JWT. PR [#127](https://github.com/tiangolo/fastapi/pull/127) by [@mmcloud](https://github.com/mmcloud).

## 0.12.0

* Add additional `responses` parameter to _path operation decorators_ to extend responses in OpenAPI (and API docs).
    * It also allows extending existing responses generated from `response_model`, declare other media types (like images), etc.
    * The new documentation is here: [Additional Responses](https://fastapi.tiangolo.com/tutorial/additional-responses/).
    * `responses` can also be added to `.include_router()`, the updated docs are here: [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#add-some-custom-tags-and-responses).
    * PR [#97](https://github.com/tiangolo/fastapi/pull/97) originally initiated by [@barsi](https://github.com/barsi).
* Update `scripts/test-cov-html.sh` to allow passing extra parameters like `-vv`, for development.

## 0.11.0

* Add `auto_error` parameter to security utility functions. Allowing them to be optional. Also allowing to have multiple alternative security schemes that are then checked in a single dependency instead of each one verifying and returning the error to the client automatically when not satisfied. PR [#134](https://github.com/tiangolo/fastapi/pull/134).

* Update [SQL Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-middleware-to-handle-sessions) to close database sessions even when there are exceptions. PR [#89](https://github.com/tiangolo/fastapi/pull/89) by [@alexiri](https://github.com/alexiri).

* Fix duplicate dependency in `pyproject.toml`. PR [#128](https://github.com/tiangolo/fastapi/pull/128) by [@zxalif](https://github.com/zxalif).

## 0.10.3

* Add Gitter chat, badge, links, etc. [https://gitter.im/tiangolo/fastapi](https://gitter.im/tiangolo/fastapi) . PR [#117](https://github.com/tiangolo/fastapi/pull/117).

* Add docs about [Extending OpenAPI](https://fastapi.tiangolo.com/tutorial/extending-openapi/). PR [#126](https://github.com/tiangolo/fastapi/pull/126).

* Make Travis run Ubuntu Xenial (newer version) and Python 3.7 instead of Python 3.7-dev. PR [#92](https://github.com/tiangolo/fastapi/pull/92) by [@blueyed](https://github.com/blueyed).

* Fix duplicated param variable creation. PR [#123](https://github.com/tiangolo/fastapi/pull/123) by [@yihuang](https://github.com/yihuang).

* Add note in [Response Model docs](https://fastapi.tiangolo.com/tutorial/response-model/) about why using a function parameter instead of a function return type annotation. PR [#109](https://github.com/tiangolo/fastapi/pull/109) by [@JHSaunders](https://github.com/JHSaunders).

* Fix event docs (startup/shutdown) function name. PR [#105](https://github.com/tiangolo/fastapi/pull/105) by [@stratosgear](https://github.com/stratosgear).

## 0.10.2

* Fix OpenAPI (JSON Schema) for declarations of Python `Union` (JSON Schema `additionalProperties`). PR [#121](https://github.com/tiangolo/fastapi/pull/121).

* Update [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) with a note on Celery.

* Document response models using unions and lists, updated at: [Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/). PR [#108](https://github.com/tiangolo/fastapi/pull/108).

## 0.10.1

* Add docs and tests for [encode/databases](https://github.com/encode/databases). New docs at: [Async SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/async-sql-databases/). PR [#107](https://github.com/tiangolo/fastapi/pull/107).

## 0.10.0

* Add support for Background Tasks in _path operation functions_ and dependencies. New documentation about [Background Tasks is here](https://fastapi.tiangolo.com/tutorial/background-tasks/). PR [#103](https://github.com/tiangolo/fastapi/pull/103).

* Add support for `.websocket_route()` in `APIRouter`. PR [#100](https://github.com/tiangolo/fastapi/pull/100) by [@euri10](https://github.com/euri10).

* New docs section about [Events: startup - shutdown](https://fastapi.tiangolo.com/tutorial/events/). PR [#99](https://github.com/tiangolo/fastapi/pull/99).

## 0.9.1

* Document receiving [Multiple values with the same query parameter](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values) and [Duplicate headers](https://fastapi.tiangolo.com/tutorial/header-params/#duplicate-headers). PR [#95](https://github.com/tiangolo/fastapi/pull/95).

## 0.9.0

* Upgrade compatible Pydantic version to `0.21.0`. PR [#90](https://github.com/tiangolo/fastapi/pull/90).

* Add documentation for: [Application Configuration](https://fastapi.tiangolo.com/tutorial/application-configuration/).

* Fix typo in docs. PR [#76](https://github.com/tiangolo/fastapi/pull/76) by [@matthewhegarty](https://github.com/matthewhegarty).

* Fix link in "Deployment" to "Bigger Applications".

## 0.8.0

* Make development scripts executable. PR [#76](https://github.com/tiangolo/fastapi/pull/76) by [@euri10](https://github.com/euri10).

* Add support for adding `tags` in `app.include_router()`. PR [#55](https://github.com/tiangolo/fastapi/pull/55) by [@euri10](https://github.com/euri10). Documentation updated in the section: [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

* Update docs related to Uvicorn to use new `--reload` option from version `0.5.x`. PR [#74](https://github.com/tiangolo/fastapi/pull/74).

* Update `isort` imports and scripts to be compatible with newer versions. PR [#75](https://github.com/tiangolo/fastapi/pull/75).

## 0.7.1

* Update [technical details about `async def` handling](https://fastapi.tiangolo.com/async/#path-operation-functions) with respect to previous frameworks. PR [#64](https://github.com/tiangolo/fastapi/pull/64) by [@haizaar](https://github.com/haizaar).

* Add [deployment documentation for Docker in Raspberry Pi](https://fastapi.tiangolo.com/deployment/#raspberry-pi-and-other-architectures) and other architectures.

* Trigger Docker images build on Travis CI automatically. PR [#65](https://github.com/tiangolo/fastapi/pull/65).

## 0.7.0

* Add support for `UploadFile` in `File` parameter annotations.
    * This includes a file-like interface.
    * Here's the updated documentation for declaring [`File` parameters with `UploadFile`](https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile).
    * And here's the updated documentation for using [`Form` parameters mixed with `File` parameters, supporting `bytes` and `UploadFile`](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/) at the same time.
    * PR [#63](https://github.com/tiangolo/fastapi/pull/63).

## 0.6.4

* Add [technical details about `async def` handling to docs](https://fastapi.tiangolo.com/async/#very-technical-details). PR [#61](https://github.com/tiangolo/fastapi/pull/61).

* Add docs for [Debugging FastAPI applications in editors](https://fastapi.tiangolo.com/tutorial/debugging/).

* Clarify [Bigger Applications deployed with Docker](https://fastapi.tiangolo.com/deployment/#bigger-applications).

* Fix typos in docs.

* Add section about [History, Design and Future](https://fastapi.tiangolo.com/history-design-future/).

* Add docs for using [WebSockets with **FastAPI**](https://fastapi.tiangolo.com/tutorial/websockets/). PR [#62](https://github.com/tiangolo/fastapi/pull/62).

## 0.6.3

* Add Favicons to docs. PR [#53](https://github.com/tiangolo/fastapi/pull/53).

## 0.6.2

* Introduce new project generator based on FastAPI and PostgreSQL: [https://github.com/tiangolo/full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Update [SQL tutorial with SQLAlchemy, using `Depends` to improve editor support and reduce code repetition](https://fastapi.tiangolo.com/tutorial/sql-databases/). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Improve middleware naming in tutorial for SQL with SQLAlchemy [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/).

## 0.6.1

* Add docs for GraphQL: [https://fastapi.tiangolo.com/tutorial/graphql/](https://fastapi.tiangolo.com/tutorial/graphql/). PR [#48](https://github.com/tiangolo/fastapi/pull/48).

## 0.6.0

* Update SQL with SQLAlchemy tutorial at [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/) using the new official `request.state`. PR [#45](https://github.com/tiangolo/fastapi/pull/45).

* Upgrade Starlette to version `0.11.1` and add required compatibility changes. PR [#44](https://github.com/tiangolo/fastapi/pull/44).

## 0.5.1

* Add section about [helping and getting help with **FastAPI**](https://fastapi.tiangolo.com/help-fastapi/).

* Add note about [path operations order in docs](https://fastapi.tiangolo.com/tutorial/path-params/#order-matters).

* Update [section about error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/) with more information and make relation with Starlette error handling utilities more explicit. PR [#41](https://github.com/tiangolo/fastapi/pull/41).

* Add <a href="" target="_blank">Development - Contributing section to the docs</a>. PR [#42](https://github.com/tiangolo/fastapi/pull/42).

## 0.5.0

* Add new `HTTPException` with support for custom headers. With new documentation for handling errors at: [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/). PR [#35](https://github.com/tiangolo/fastapi/pull/35).

* Add [documentation to use Starlette `Request` object](https://fastapi.tiangolo.com/tutorial/using-request-directly/) directly. Check [#25](https://github.com/tiangolo/fastapi/pull/25) by [@euri10](https://github.com/euri10).

* Add issue templates to simplify reporting bugs, getting help, etc: [#34](https://github.com/tiangolo/fastapi/pull/34).

* Update example for the SQLAlchemy tutorial at [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/) using middleware and database session attached to request.

## 0.4.0

* Add `openapi_prefix`, support for reverse proxy and mounting sub-applications. See the docs at [https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/](https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/): [#26](https://github.com/tiangolo/fastapi/pull/26) by [@kabirkhan](https://github.com/kabirkhan).

* Update [docs/tutorial for SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/) including note about _DB Browser for SQLite_.

## 0.3.0

* Fix/add SQLAlchemy support, including ORM, and update [docs for SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/): [#30](https://github.com/tiangolo/fastapi/pull/30).

## 0.2.1

* Fix `jsonable_encoder` for Pydantic models with `Config` but without `json_encoders`: [#29](https://github.com/tiangolo/fastapi/pull/29).

## 0.2.0

* Fix typos in Security section: [#24](https://github.com/tiangolo/fastapi/pull/24) by [@kkinder](https://github.com/kkinder).

* Add support for Pydantic custom JSON encoders: [#21](https://github.com/tiangolo/fastapi/pull/21) by [@euri10](https://github.com/euri10).

## 0.1.19

* Upgrade Starlette version to the current latest `0.10.1`: [#17](https://github.com/tiangolo/fastapi/pull/17) by [@euri10](https://github.com/euri10).
