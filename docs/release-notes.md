## Next

* Add section about <a href="https://fastapi.tiangolo.com/help-fastapi/" target="_blank">helping and getting help with **FastAPI**</a>.

* Add note about <a href="https://fastapi.tiangolo.com/tutorial/path-params/#order-matters" target="_blank">path operations order in docs</a>.

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
