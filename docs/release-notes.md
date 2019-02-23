## Next

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

* Add `openapi_prefix`, support for reverse proxy and mounting sub-applicaitons. See the docs at <a href="https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/" target="_blank">https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/</a>: <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank">#26</a> by <a href="https://github.com/kabirkhan" target="_blank">@kabirkhan</a>.

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
