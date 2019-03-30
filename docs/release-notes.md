## Next release

* Fix duplicated param variable creation. PR <a href="https://github.com/tiangolo/fastapi/pull/123" target="_blank">#123</a> by <a href="https://github.com/yihuang" target="_blank">@yihuang</a>.

* Add docs about <a href="https://fastapi.tiangolo.com/tutorial/extending-openapi/" target="_blank">Extending OpenAPI</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/126" target="_blank">#126</a>.

* Add Gitter chat, badge, links, etc. <a href="https://gitter.im/tiangolo/fastapi" target="_blank">https://gitter.im/tiangolo/fastapi
</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/117" target="_blank">#117</a>.

* Add note in <a href="https://fastapi.tiangolo.com/tutorial/response-model/" target="_blank">Response Model docs</a> about why using a function parameter instead of a function return type annotation. PR <a href="https://github.com/tiangolo/fastapi/pull/109" target="_blank">#109</a> by <a href="https://github.com/JHSaunders" target="_blank">@JHSaunders</a>.

* Fix event docs (startup/shutdown) function name. PR <a href="https://github.com/tiangolo/fastapi/pull/105" target="_blank">#105</a> by <a href="https://github.com/stratosgear" target="_blank">@stratosgear</a>.

## 0.10.2

* Fix OpenAPI (JSON Schema) for declarations of Python `Union` (JSON Schema `additionalProperties`). PR <a href="https://github.com/tiangolo/fastapi/pull/121" target="_blank">#121</a>.

* Update <a href="https://fastapi.tiangolo.com/tutorial/background-tasks/" target="_blank">Background Tasks</a> with a note on Celery.

* Document response models using unions and lists, updated at: <a href="https://fastapi.tiangolo.com/tutorial/extra-models/" target="_blank">Extra Models</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/108" target="_blank">#108</a>.

## 0.10.1

* Add docs and tests for <a href="https://github.com/encode/databases" target="_blank">encode/databases</a>. New docs at: <a href="https://fastapi.tiangolo.com/tutorial/async-sql-databases/" target="_blank">Async SQL (Relational) Databases</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/107" target="_blank">#107</a>.

## 0.10.0

* Add support for Background Tasks in *path operation functions* and dependencies. New documentation about <a href="https://fastapi.tiangolo.com/tutorial/background-tasks/" target="_blank">Background Tasks is here</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/103" target="_blank">#103</a>.

* Add support for `.websocket_route()` in `APIRouter`. PR <a href="https://github.com/tiangolo/fastapi/pull/100" target="_blank">#100</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>.

* New docs section about <a href="https://fastapi.tiangolo.com/tutorial/events/" target="_blank">Events: startup - shutdown</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/99" target="_blank">#99</a>.

## 0.9.1

* Document receiving <a href="https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values" target="_blank">Multiple values with the same query parameter</a> and <a href="https://fastapi.tiangolo.com/tutorial/header-params/#duplicate-headers" target="_blank">Duplicate headers</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/95" target="_blank">#95</a>.

## 0.9.0

* Upgrade compatible Pydantic version to `0.21.0`. PR <a href="https://github.com/tiangolo/fastapi/pull/90" target="_blank">#90</a>.

* Add documentation for: <a href="https://fastapi.tiangolo.com/tutorial/application-configuration/" target="_blank">Application Configuration</a>.

* Fix typo in docs. PR <a href="https://github.com/tiangolo/fastapi/pull/76" target="_blank">#76</a> by <a href="https://github.com/matthewhegarty" target="_blank">@matthewhegarty</a>.

* Fix link in "Deployment" to "Bigger Applications".

## 0.8.0

* Make development scripts executable. PR <a href="https://github.com/tiangolo/fastapi/pull/76" target="_blank">#76</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>.

* Add support for adding `tags` in `app.include_router()`. PR <a href="https://github.com/tiangolo/fastapi/pull/55" target="_blank">#55</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>. Documentation updated in the section: <a href="https://fastapi.tiangolo.com/tutorial/bigger-applications/" target="_blank">Bigger Applications</a>.

* Update docs related to Uvicorn to use new `--reload` option from version `0.5.x`. PR <a href="https://github.com/tiangolo/fastapi/pull/74" target="_blank">#74</a>.

* Update `isort` imports and scripts to be compatible with newer versions. PR <a href="https://github.com/tiangolo/fastapi/pull/75" target="_blank">#75</a>.

## 0.7.1

* Update <a href="https://fastapi.tiangolo.com/async/#path-operation-functions" target="_blank">technical details about `async def` handling</a> with respect to previous frameworks. PR <a href="https://github.com/tiangolo/fastapi/pull/64" target="_blank">#64</a> by <a href="https://github.com/haizaar" target="_blank">@haizaar</a>.

* Add <a href="https://fastapi.tiangolo.com/deployment/#raspberry-pi-and-other-architectures" target="_blank">deployment documentation for Docker in Raspberry Pi</a> and other architectures.

* Trigger Docker images build on Travis CI automatically. PR <a href="https://github.com/tiangolo/fastapi/pull/65" target="_blank">#65</a>.

## 0.7.0

* Add support for `UploadFile` in `File` parameter annotations.
    * This includes a file-like interface.
    * Here's the updated documentation for declaring <a href="https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile" target="_blank"> `File` parameters with `UploadFile`</a>.
    * And here's the updated documentation for using <a href="https://fastapi.tiangolo.com/tutorial/request-forms-and-files/" target="_blank">`Form` parameters mixed with `File` parameters, supporting `bytes` and `UploadFile`</a> at the same time.
    * PR <a href="https://github.com/tiangolo/fastapi/pull/63" target="_blank">#63</a>.

## 0.6.4

* Add <a href="https://fastapi.tiangolo.com/async/#very-technical-details" target="_blank">technical details about `async def` handling to docs</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/61" target="_blank">#61</a>.

* Add docs for <a href="https://fastapi.tiangolo.com/tutorial/debugging/" target="_blank">Debugging FastAPI applications in editors</a>.

* Clarify <a href="https://fastapi.tiangolo.com/deployment/#bigger-applications" target="_blank">Bigger Applications deployed with Docker</a>.

* Fix typos in docs.

* Add section about <a href="https://fastapi.tiangolo.com/history-design-future/" target="_blank">History, Design and Future</a>.

* Add docs for using <a href="https://fastapi.tiangolo.com/tutorial/websockets/" target="_blank">WebSockets with **FastAPI**</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/62" target="_blank">#62</a>.

## 0.6.3

* Add Favicons to docs. PR <a href="https://github.com/tiangolo/fastapi/pull/53" target="_blank">#53</a>.

## 0.6.2

* Introduce new project generator based on FastAPI and PostgreSQL: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/52" target="_blank">#52</a>.

* Update <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">SQL tutorial with SQLAlchemy, using `Depends` to improve editor support and reduce code repetition</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/52" target="_blank">#52</a>.

* Improve middleware naming in tutorial for SQL with SQLAlchemy <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">https://fastapi.tiangolo.com/tutorial/sql-databases/</a>.

## 0.6.1

* Add docs for GraphQL: <a href="https://fastapi.tiangolo.com/tutorial/graphql/" target="_blank">https://fastapi.tiangolo.com/tutorial/graphql/</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/48" target="_blank">#48</a>.

## 0.6.0

* Update SQL with SQLAlchemy tutorial at <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">https://fastapi.tiangolo.com/tutorial/sql-databases/</a> using the new official `request.state`. PR <a href="https://github.com/tiangolo/fastapi/pull/45" target="_blank">#45</a>.

* Upgrade Starlette to version `0.11.1` and add required compatibility changes. PR <a href="https://github.com/tiangolo/fastapi/pull/44" target="_blank">#44</a>.

## 0.5.1

* Add section about <a href="https://fastapi.tiangolo.com/help-fastapi/" target="_blank">helping and getting help with **FastAPI**</a>.

* Add note about <a href="https://fastapi.tiangolo.com/tutorial/path-params/#order-matters" target="_blank">path operations order in docs</a>.

* Update <a href="https://fastapi.tiangolo.com/tutorial/handling-errors/" target="_blank">section about error handling</a> with more information and make relation with Starlette error handling utilities more explicit. PR <a href="https://github.com/tiangolo/fastapi/pull/41" target="_blank">#41</a>.

* Add <a href="" target="_blank">Development - Contributing section to the docs</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/42" target="_blank">#42</a>.

## 0.5.0

* Add new `HTTPException` with support for custom headers. With new documentation for handling errors at: <a href="https://fastapi.tiangolo.com/tutorial/handling-errors/" target="_blank">https://fastapi.tiangolo.com/tutorial/handling-errors/</a>. PR <a href="https://github.com/tiangolo/fastapi/pull/35" target="_blank">#35</a>.

* Add <a href="https://fastapi.tiangolo.com/tutorial/using-request-directly/" target="_blank">documentation to use Starlette `Request` object</a> directly. Check <a href="https://github.com/tiangolo/fastapi/pull/25" target="_blank">#25</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>.

* Add issue templates to simplify reporting bugs, getting help, etc: <a href="https://github.com/tiangolo/fastapi/pull/34" target="_blank">#34</a>.

* Update example for the SQLAlchemy tutorial at <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">https://fastapi.tiangolo.com/tutorial/sql-databases/</a> using middleware and database session attached to request.

## 0.4.0

* Add `openapi_prefix`, support for reverse proxy and mounting sub-applications. See the docs at <a href="https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/" target="_blank">https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/</a>: <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank">#26</a> by <a href="https://github.com/kabirkhan" target="_blank">@kabirkhan</a>.

* Update <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">docs/tutorial for SQLAlchemy</a> including note about *DB Browser for SQLite*.

## 0.3.0

* Fix/add SQLAlchemy support, including ORM, and update <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">docs for SQLAlchemy</a>: <a href="https://github.com/tiangolo/fastapi/pull/30" target="_blank">#30</a>.

## 0.2.1

* Fix `jsonable_encoder` for Pydantic models with `Config` but without `json_encoders`: <a href="https://github.com/tiangolo/fastapi/pull/29" target="_blank">#29</a>.

## 0.2.0

* Fix typos in Security section: <a href="https://github.com/tiangolo/fastapi/pull/24" target="_blank">#24</a> by <a href="https://github.com/kkinder" target="_blank">@kkinder</a>.

* Add support for Pydantic custom JSON encoders: <a href="https://github.com/tiangolo/fastapi/pull/21" target="_blank">#21</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>.

## 0.1.19

* Upgrade Starlette version to the current latest `0.10.1`: <a href="https://github.com/tiangolo/fastapi/pull/17" target="_blank">#17</a> by <a href="https://github.com/euri10" target="_blank">@euri10</a>.
