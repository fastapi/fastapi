# Release Notes

## Latest Changes

* 🐛 Fix copier to handle string vars with spaces in quotes. PR [#631](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/631) by [@estebanx64](https://github.com/estebanx64).
* ⬆ Bump tiangolo/issue-manager from 0.2.0 to 0.5.0. PR [#591](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/591) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✨ Upgrade items router with new SQLModel models, simplified logic, and new FastAPI Annotated dependencies. PR [#560](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/560) by [@tiangolo](https://github.com/tiangolo).
* ✨ Adopt SQLModel, create models, start using it. PR [#559](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/559) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade Python version and dependencies. PR [#558](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/558) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add missing dotenv variables. PR [#554](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/554) by [@tiangolo](https://github.com/tiangolo).

### Features

* ✅ Add tests to raise coverage to at least 90% and fix recover password logic. PR [#632](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/632) by [@estebanx64](https://github.com/estebanx64).
* ⚙️ Add Prettier and ESLint config with pre-commit. PR [#640](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/640) by [@alejsdev](https://github.com/alejsdev).
* 👷 Add coverage with Smokeshow to CI and badge. PR [#638](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/638) by [@estebanx64](https://github.com/estebanx64).
* ✨ Migrate to TanStack Query (React Query) and TanStack Router. PR [#637](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/637) by [@alejsdev](https://github.com/alejsdev).
* ✅ Add setup and teardown database for tests. PR [#626](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/626) by [@estebanx64](https://github.com/estebanx64).
* ✨ Update new-frontend client. PR [#625](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/625) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add password reset functionality. PR [#624](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/624) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add private/public routing. PR [#621](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/621) by [@alejsdev](https://github.com/alejsdev).
* 🔧 Add VS Code debug configs. PR [#620](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/620) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add `Not Found` page. PR [#595](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/595) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add new pages, components, panels, modals, and theme; refactor and improvements in existing components. PR [#593](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/593) by [@alejsdev](https://github.com/alejsdev).
* ✨ Support delete own account and other tweaks. PR [#614](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/614) by [@alejsdev](https://github.com/alejsdev).
* ✨ Restructure folders, allow editing of users/items, and implement other refactors and improvements. PR [#603](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/603) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add Copier, migrate from Cookiecutter, in a way that supports using the project as is, forking or cloning it. PR [#612](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/612) by [@tiangolo](https://github.com/tiangolo).
* ➕ Replace black, isort, flake8, autoflake with ruff and upgrade mypy. PR [#610](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/610) by [@tiangolo](https://github.com/tiangolo).
* ♻ Refactor items and services endpoints to return count and data, and add CI tests. PR [#599](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/599) by [@estebanx64](https://github.com/estebanx64).
* ✨ Add support for updating items and upgrade SQLModel to 0.0.16 (which supports model object updates). PR [#601](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/601) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add dark mode to new-frontend and conditional sidebar items. PR [#600](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/600) by [@alejsdev](https://github.com/alejsdev).
* ✨ Migrate to RouterProvider and other refactors . PR [#598](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/598) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add delete_user; refactor delete_item. PR [#594](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/594) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add state store to new frontend. PR [#592](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/592) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add form validation to Admin, Items and Login. PR [#616](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/616) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add Sidebar to new frontend. PR [#587](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/587) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add Login to new frontend. PR [#585](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/585) by [@alejsdev](https://github.com/alejsdev).
* ✨ Include schemas in generated frontend client. PR [#584](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/584) by [@alejsdev](https://github.com/alejsdev).
* ✨ Regenerate frontend client with recent changes. PR [#575](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/575) by [@alejsdev](https://github.com/alejsdev).
* ♻️ Refactor API in `utils.py`. PR [#573](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/573) by [@alejsdev](https://github.com/alejsdev).
* ✨ Update code for login API. PR [#571](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/571) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add client in frontend and client generation. PR [#569](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/569) by [@alejsdev](https://github.com/alejsdev).
* 🐳 Set up Docker config for new-frontend. PR [#564](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/564) by [@alejsdev](https://github.com/alejsdev).
* ✨ Set up new frontend with Vite, TypeScript and React. PR [#563](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/563) by [@alejsdev](https://github.com/alejsdev).
* 📌 Add NodeJS version management and instructions. PR [#551](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/551) by [@alejsdev](https://github.com/alejsdev).
* Add consistent errors for env vars not set. PR [#200](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/200).
* Upgrade Traefik to version 2, keeping in sync with DockerSwarm.rocks. PR [#199](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/199).
* Run tests with `TestClient`. PR [#160](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/160).

### Fixes

* 🐛  Add `onClose` to `SidebarItems`. PR [#589](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/589) by [@alejsdev](https://github.com/alejsdev).
* 🐛 Fix positional argument bug in `init_db.py`. PR [#562](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/562) by [@alejsdev](https://github.com/alejsdev).
* 📌 Fix flower Docker image, pin version. PR [#396](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/396) by [@sanggusti](https://github.com/sanggusti).
* 🐛 Fix Celery worker command. PR [#443](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/443) by [@bechtold](https://github.com/bechtold).
* 🐛 Fix Poetry installation in Dockerfile and upgrade Python version and packages to fix Docker build. PR [#480](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/480) by [@little7Li](https://github.com/little7Li).

### Refactors

* ♻ Move project source files to top level from src, update Sentry dependency. PR [#630](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/630) by [@estebanx64](https://github.com/estebanx64).
* ♻ Refactor Python folder tree. PR [#629](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/629) by [@estebanx64](https://github.com/estebanx64).
* ♻️ Refactor old CRUD utils and tests. PR [#622](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/622) by [@alejsdev](https://github.com/alejsdev).
* 🔧 Update .env to allow local debug for the backend. PR [#618](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/618) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor and update CORS, remove trailing slash from new Pydantic v2. PR [#617](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/617) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Format files with pre-commit and Ruff. PR [#611](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/611) by [@tiangolo](https://github.com/tiangolo).
* 🚚 Refactor and simplify backend file structure. PR [#609](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/609) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Clean up old files no longer relevant. PR [#608](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/608) by [@tiangolo](https://github.com/tiangolo).
* ♻ Re-structure Docker Compose files, discard Docker Swarm specific logic. PR [#607](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/607) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor update endpoints and regenerate client for new-frontend. PR [#602](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/602) by [@alejsdev](https://github.com/alejsdev).
* ✨ Add Layout to App. PR [#588](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/588) by [@alejsdev](https://github.com/alejsdev).
* ♻️ Re-enable user update path operations for frontend client generation. PR [#574](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/574) by [@alejsdev](https://github.com/alejsdev).
* ♻️ Remove type ignores and add `response_model`. PR [#572](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/572) by [@alejsdev](https://github.com/alejsdev).
* ♻️ Refactor Users API and dependencies. PR [#561](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/561) by [@alejsdev](https://github.com/alejsdev).
* ♻️ Refactor frontend Docker build setup, use plain NodeJS, use custom Nginx config, fix build for old Vue. PR [#555](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/555) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor project generation, discard cookiecutter, use plain git/clone/fork. PR [#553](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/553) by [@tiangolo](https://github.com/tiangolo).
* Refactor backend:
    * Simplify configs for tools and format to better support editor integration.
    * Add mypy configurations and plugins.
    * Add types to all the codebase.
    * Update types for SQLAlchemy models with plugin.
    * Update and refactor CRUD utils.
    * Refactor DB sessions to use dependencies with `yield`.
    * Refactor dependencies, security, CRUD, models, schemas, etc. To simplify code and improve autocompletion.
    * Change from PyJWT to Python-JOSE as it supports additional use cases.
    * Fix JWT tokens using user email/ID as the subject in `sub`.
    * PR [#158](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/158).
* Simplify `docker-compose.*.yml` files, refactor deployment to reduce config files. PR [#153](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/153).
* Simplify env var files, merge to a single `.env` file. PR [#151](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/151).

### Upgrades

* ⬆ Upgrade code to support pydantic V2. PR [#615](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/615) by [@estebanx64](https://github.com/estebanx64).

### Docs

* 📝 Refactor README into separate README.md files for backend, frontend, deployment, development. PR [#639](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/639) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update README. PR [#628](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/628) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action latest-changes and move release notes to independent file. PR [#619](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/619) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update internal README and referred files. PR [#613](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/613) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update README with in construction notice. PR [#552](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/552) by [@tiangolo](https://github.com/tiangolo).
* Add docs about reporting test coverage in HTML. PR [#161](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/161).
* Add docs about removing the frontend, for an API-only app. PR [#156](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/156).

### Internal

* 👷 Add dependabot. PR [#547](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/547) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix latest-changes GitHub Action token, strike 2. PR [#546](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/546) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix latest-changes GitHub Action token config. PR [#545](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/545) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add latest-changes GitHub Action. PR [#544](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/544) by [@tiangolo](https://github.com/tiangolo).
* Update issue-manager. PR [#211](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/211).
* Add [GitHub Sponsors](https://github.com/sponsors/tiangolo) button. PR [#201](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/201).
* Simplify scripts and development, update docs and configs. PR [#155](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/155).

## 0.5.0

* Make the Traefik public network a fixed default of `traefik-public` as done in DockerSwarm.rocks, to simplify development and iteration of the project generator. PR [#150](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/150).
* Update to PostgreSQL 12. PR [#148](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/148). by [@RCheese](https://github.com/RCheese).
* Use Poetry for package management. Initial PR [#144](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/144) by [@RCheese](https://github.com/RCheese).
* Fix Windows line endings for shell scripts after project generation with Cookiecutter hooks. PR [#149](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/149).
* Upgrade Vue CLI to version 4. PR [#120](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/120) by [@br3ndonland](https://github.com/br3ndonland).
* Remove duplicate `login` tag. PR [#135](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/135) by [@Nonameentered](https://github.com/Nonameentered).
* Fix showing email in dashboard when there's no user's full name. PR [#129](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/129) by [@rlonka](https://github.com/rlonka).
* Format code with Black and Flake8. PR [#121](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/121) by [@br3ndonland](https://github.com/br3ndonland).
* Simplify SQLAlchemy Base class. PR [#117](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/117) by [@airibarne](https://github.com/airibarne).
* Update CRUD utils for users, handling password hashing. PR [#106](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/106) by [@mocsar](https://github.com/mocsar).
* Use `.` instead of `source` for interoperability. PR [#98](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/98) by [@gucharbon](https://github.com/gucharbon).
* Use Pydantic's `BaseSettings` for settings/configs and env vars. PR [#87](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/87) by [@StephenBrown2](https://github.com/StephenBrown2).
* Remove `package-lock.json` to let everyone lock their own versions (depending on OS, etc).
* Simplify Traefik service labels PR [#139](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/139).
* Add email validation. PR [#40](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/40) by [@kedod](https://github.com/kedod).
* Fix typo in README. PR [#83](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/83) by [@ashears](https://github.com/ashears).
* Fix typo in README. PR [#80](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/80) by [@abjoker](https://github.com/abjoker).
* Fix function name `read_item` and response code. PR [#74](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/74) by [@jcaguirre89](https://github.com/jcaguirre89).
* Fix typo in comment. PR [#70](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/70) by [@daniel-butler](https://github.com/daniel-butler).
* Fix Flower Docker configuration. PR [#37](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/37) by [@dmontagu](https://github.com/dmontagu).
* Add new CRUD utils based on DB and Pydantic models. Initial PR [#23](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/23) by [@ebreton](https://github.com/ebreton).
* Add normal user testing Pytest fixture. PR [#20](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/20) by [@ebreton](https://github.com/ebreton).

## 0.4.0

* Fix security on resetting a password. Receive token as body, not query. PR [#34](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/34).

* Fix security on resetting a password. Receive it as body, not query. PR [#33](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/33) by [@dmontagu](https://github.com/dmontagu).

* Fix SQLAlchemy class lookup on initialization. PR [#29](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/29) by [@ebreton](https://github.com/ebreton).

* Fix SQLAlchemy operation errors on database restart. PR [#32](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/32) by [@ebreton](https://github.com/ebreton).

* Fix locations of scripts in generated README. PR [#19](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/19) by [@ebreton](https://github.com/ebreton).

* Forward arguments from script to `pytest` inside container. PR [#17](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/17) by [@ebreton](https://github.com/ebreton).

* Update development scripts.

* Read Alembic configs from env vars. PR <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/9" target="_blank">#9</a> by <a href="https://github.com/ebreton" target="_blank">@ebreton</a>.

* Create DB Item objects from all Pydantic model's fields.

* Update Jupyter Lab installation and util script/environment variable for local development.

## 0.3.0

* PR <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/14" target="_blank">#14</a>:
    * Update CRUD utils to use types better.
    * Simplify Pydantic model names, from `UserInCreate` to `UserCreate`, etc.
    * Upgrade packages.
    * Add new generic "Items" models, crud utils, endpoints, and tests. To facilitate re-using them to create new functionality. As they are simple and generic (not like Users), it's easier to copy-paste and adapt them to each use case.
    * Update endpoints/*path operations* to simplify code and use new utilities, prefix and tags in `include_router`.
    * Update testing utils.
    * Update linting rules, relax vulture to reduce false positives.
    * Update migrations to include new Items.
    * Update project README.md with tips about how to start with backend.

* Upgrade Python to 3.7 as Celery is now compatible too. PR <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/10" target="_blank">#10</a> by <a href="https://github.com/ebreton" target="_blank">@ebreton</a>.

## 0.2.2

* Fix frontend hijacking /docs in development. Using latest https://github.com/tiangolo/node-frontend with custom Nginx configs in frontend. <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/6" target="_blank">PR #6</a>.

## 0.2.1

* Fix documentation for *path operation* to get user by ID. <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/4" target="_blank">PR #4</a> by <a href="https://github.com/mpclarkson" target="_blank">@mpclarkson</a> in FastAPI.

* Set `/start-reload.sh` as a command override for development by default.

* Update generated README.

## 0.2.0

**<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/2" target="_blank">PR #2</a>**:

* Simplify and update backend `Dockerfile`s.
* Refactor and simplify backend code, improve naming, imports, modules and "namespaces".
* Improve and simplify Vuex integration with TypeScript accessors.
* Standardize frontend components layout, buttons order, etc.
* Add local development scripts (to develop this project generator itself).
* Add logs to startup modules to detect errors early.
* Improve FastAPI dependency utilities, to simplify and reduce code (to require a superuser).

## 0.1.2

* Fix path operation to update self-user, set parameters as body payload.

## 0.1.1

Several bug fixes since initial publication, including:

* Order of path operations for users.
* Frontend sending login data in the correct format.
* Add https://localhost variants to CORS.
