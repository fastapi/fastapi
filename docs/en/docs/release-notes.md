# Release Notes

## Latest Changes

* 🌐 Add Chinese translation for Tutorial - Request - Files. PR [#3244](https://github.com/tiangolo/fastapi/pull/3244) by [@jaystone776](https://github.com/jaystone776).

## 0.65.2

### Security fixes

* 🔒 Check Content-Type request header before assuming JSON. Initial PR [#2118](https://github.com/tiangolo/fastapi/pull/2118) by [@patrickkwang](https://github.com/patrickkwang).

This change fixes a [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery) security vulnerability when using cookies for authentication in path operations with JSON payloads sent by browsers.

In versions lower than `0.65.2`, FastAPI would try to read the request payload as JSON even if the `content-type` header sent was not set to `application/json` or a compatible JSON media type (e.g. `application/geo+json`).

So, a request with a content type of `text/plain` containing JSON data would be accepted and the JSON data would be extracted.

But requests with content type `text/plain` are exempt from [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) preflights, for being considered [Simple requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests). So, the browser would execute them right away including cookies, and the text content could be a JSON string that would be parsed and accepted by the FastAPI application.

See [CVE-2021-32677](https://github.com/tiangolo/fastapi/security/advisories/GHSA-8h2j-cgx8-6xv7) for more details.

Thanks to [Dima Boger](https://twitter.com/b0g3r) for the security report! 🙇🔒

### Internal

* 🔧 Update sponsors badge, course bundle. PR [#3340](https://github.com/tiangolo/fastapi/pull/3340) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new gold sponsor Jina 🎉. PR [#3291](https://github.com/tiangolo/fastapi/pull/3291) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new banner sponsor badge for FastAPI courses bundle. PR [#3288](https://github.com/tiangolo/fastapi/pull/3288) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade Issue Manager GitHub Action. PR [#3236](https://github.com/tiangolo/fastapi/pull/3236) by [@tiangolo](https://github.com/tiangolo).

## 0.65.1

### Security fixes

* 📌 Upgrade pydantic pin, to handle security vulnerability [CVE-2021-29510](https://github.com/samuelcolvin/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh). PR [#3213](https://github.com/tiangolo/fastapi/pull/3213) by [@tiangolo](https://github.com/tiangolo).

## 0.65.0

### Breaking Changes - Upgrade

* ⬆️  Upgrade Starlette to `0.14.2`, including internal `UJSONResponse` migrated from Starlette. This includes several bug fixes and features from Starlette. PR [#2335](https://github.com/tiangolo/fastapi/pull/2335) by [@hanneskuettner](https://github.com/hanneskuettner).

### Translations

* 🌐 Initialize new language Polish for translations. PR [#3170](https://github.com/tiangolo/fastapi/pull/3170) by [@neternefer](https://github.com/neternefer).

### Internal

* 👷 Add GitHub Action cache to speed up CI installs. PR [#3204](https://github.com/tiangolo/fastapi/pull/3204) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade setup-python GitHub Action to v2. PR [#3203](https://github.com/tiangolo/fastapi/pull/3203) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix docs script to generate a new translation language with `overrides` boilerplate. PR [#3202](https://github.com/tiangolo/fastapi/pull/3202) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add new Deta banner badge with new sponsorship tier 🙇. PR [#3194](https://github.com/tiangolo/fastapi/pull/3194) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#3189](https://github.com/tiangolo/fastapi/pull/3189) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔊 Update FastAPI People to allow better debugging. PR [#3188](https://github.com/tiangolo/fastapi/pull/3188) by [@tiangolo](https://github.com/tiangolo).

## 0.64.0

### Features

* ✨ Add support for adding multiple `examples` in request bodies and path, query, cookie, and header params. New docs: [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#body-with-multiple-examples). Initial PR [#1267](https://github.com/tiangolo/fastapi/pull/1267) by [@austinorr](https://github.com/austinorr).

### Fixes

* 📌 Pin SQLAlchemy range for tests, as it doesn't use SemVer. PR [#3001](https://github.com/tiangolo/fastapi/pull/3001) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Add newly required type annotations for mypy. PR [#2882](https://github.com/tiangolo/fastapi/pull/2882) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Remove internal "type: ignore", now unnecessary. PR [#2424](https://github.com/tiangolo/fastapi/pull/2424) by [@AsakuraMizu](https://github.com/AsakuraMizu).

### Docs

* 📝 Add link to article in Russian "FastAPI: знакомимся с фреймворком". PR [#2564](https://github.com/tiangolo/fastapi/pull/2564) by [@trkohler](https://github.com/trkohler).
* 📝 Add external link to blog post "Authenticate Your FastAPI App with Auth0". PR [#2172](https://github.com/tiangolo/fastapi/pull/2172) by [@dompatmore](https://github.com/dompatmore).
* 📝 Fix broken link to article: Machine learning model serving in Python using FastAPI and Streamlit. PR [#2557](https://github.com/tiangolo/fastapi/pull/2557) by [@davidefiocco](https://github.com/davidefiocco).
* 📝 Add FastAPI Medium Article: Deploy a dockerized FastAPI application to AWS. PR [#2515](https://github.com/tiangolo/fastapi/pull/2515) by [@vjanz](https://github.com/vjanz).
* ✏ Fix typo in Tutorial - Handling Errors. PR [#2486](https://github.com/tiangolo/fastapi/pull/2486) by [@johnthagen](https://github.com/johnthagen).
* ✏ Fix typo in Security OAuth2 scopes. PR [#2407](https://github.com/tiangolo/fastapi/pull/2407) by [@jugmac00](https://github.com/jugmac00).
* ✏ Fix typo/clarify docs for SQL (Relational) Databases. PR [#2393](https://github.com/tiangolo/fastapi/pull/2393) by [@kangni](https://github.com/kangni).
* 📝 Add external link to "FastAPI for Flask Users". PR [#2280](https://github.com/tiangolo/fastapi/pull/2280) by [@amitness](https://github.com/amitness).

### Translations

* 🌐 Fix Chinese translation of Tutorial - Query Parameters, remove obsolete content. PR [#3051](https://github.com/tiangolo/fastapi/pull/3051) by [@louis70109](https://github.com/louis70109).
* 🌐 Add French translation for Tutorial - Background Tasks. PR [#3098](https://github.com/tiangolo/fastapi/pull/3098) by [@Smlep](https://github.com/Smlep).
* 🌐 Fix Korean translation for docs/ko/docs/index.md. PR [#3159](https://github.com/tiangolo/fastapi/pull/3159) by [@SueNaEunYang](https://github.com/SueNaEunYang).
* 🌐 Add Korean translation for Tutorial - Query Parameters. PR [#2390](https://github.com/tiangolo/fastapi/pull/2390) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add French translation for FastAPI People. PR [#2232](https://github.com/tiangolo/fastapi/pull/2232) by [@JulianMaurin](https://github.com/JulianMaurin).
* 🌐 Add Korean translation for Tutorial - Path Parameters. PR [#2355](https://github.com/tiangolo/fastapi/pull/2355) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add French translation for Features. PR [#2157](https://github.com/tiangolo/fastapi/pull/2157) by [@Jefidev](https://github.com/Jefidev).
* 👥 Update FastAPI People. PR [#3031](https://github.com/tiangolo/fastapi/pull/3031) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🌐 Add Chinese translation for Tutorial - Debugging. PR [#2737](https://github.com/tiangolo/fastapi/pull/2737) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Chinese translation for Tutorial - Security - OAuth2 with Password (and hashing), Bearer with JWT tokens. PR [#2642](https://github.com/tiangolo/fastapi/pull/2642) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Korean translation for Tutorial - Header Parameters. PR [#2589](https://github.com/tiangolo/fastapi/pull/2589) by [@mode9](https://github.com/mode9).
* 🌐 Add Chinese translation for Tutorial - Metadata and Docs URLs. PR [#2559](https://github.com/tiangolo/fastapi/pull/2559) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Korean translation for Tutorial - First Steps. PR [#2323](https://github.com/tiangolo/fastapi/pull/2323) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Chinese translation for Tutorial - CORS (Cross-Origin Resource Sharing). PR [#2540](https://github.com/tiangolo/fastapi/pull/2540) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Chinese translation for Tutorial - Middleware. PR [#2334](https://github.com/tiangolo/fastapi/pull/2334) by [@lpdswing](https://github.com/lpdswing).
* 🌐 Add Korean translation for Tutorial - Intro. PR [#2317](https://github.com/tiangolo/fastapi/pull/2317) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Chinese translation for Tutorial - Bigger Applications - Multiple Files. PR [#2453](https://github.com/tiangolo/fastapi/pull/2453) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Security - Security Intro. PR [#2443](https://github.com/tiangolo/fastapi/pull/2443) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Header Parameters. PR [#2412](https://github.com/tiangolo/fastapi/pull/2412) by [@maoyibo](https://github.com/maoyibo).
* 🌐 Add Chinese translation for Tutorial - Extra Data Types. PR [#2410](https://github.com/tiangolo/fastapi/pull/2410) by [@maoyibo](https://github.com/maoyibo).
* 🌐 Add Japanese translation for Deployment - Docker. PR [#2312](https://github.com/tiangolo/fastapi/pull/2312) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Deployment - Versions. PR [#2310](https://github.com/tiangolo/fastapi/pull/2310) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Cookie Parameters. PR [#2261](https://github.com/tiangolo/fastapi/pull/2261) by [@alicrazy1947](https://github.com/alicrazy1947).
* 🌐 Add Japanese translation for Tutorial - Static files. PR [#2260](https://github.com/tiangolo/fastapi/pull/2260) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Testing. PR [#2259](https://github.com/tiangolo/fastapi/pull/2259) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Debugging. PR [#2256](https://github.com/tiangolo/fastapi/pull/2256) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Middleware. PR [#2255](https://github.com/tiangolo/fastapi/pull/2255) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Concurrency and async / await. PR [#2058](https://github.com/tiangolo/fastapi/pull/2058) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Security - Simple OAuth2 with Password and Bearer. PR [#2514](https://github.com/tiangolo/fastapi/pull/2514) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Japanese translation for Deployment - Deta. PR [#2314](https://github.com/tiangolo/fastapi/pull/2314) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Security - Get Current User. PR [#2474](https://github.com/tiangolo/fastapi/pull/2474) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Japanese translation for Deployment - Manually. PR [#2313](https://github.com/tiangolo/fastapi/pull/2313) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Deployment - Intro. PR [#2309](https://github.com/tiangolo/fastapi/pull/2309) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for FastAPI People. PR [#2254](https://github.com/tiangolo/fastapi/pull/2254) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Advanced - Path Operation Advanced Configuration. PR [#2124](https://github.com/tiangolo/fastapi/pull/2124) by [@Attsun1031](https://github.com/Attsun1031).
* 🌐 Add Japanese translation for External Links. PR [#2070](https://github.com/tiangolo/fastapi/pull/2070) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Body - Updates. PR [#1956](https://github.com/tiangolo/fastapi/pull/1956) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for Tutorial - Form Data. PR [#1943](https://github.com/tiangolo/fastapi/pull/1943) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for Tutorial - Cookie Parameters. PR [#1933](https://github.com/tiangolo/fastapi/pull/1933) by [@SwftAlpc](https://github.com/SwftAlpc).

### Internal

* 🔧 Update top banner, point to newsletter. PR [#3003](https://github.com/tiangolo/fastapi/pull/3003) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Disable sponsor WeTransfer. PR [#3002](https://github.com/tiangolo/fastapi/pull/3002) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2880](https://github.com/tiangolo/fastapi/pull/2880) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 👥 Update FastAPI People. PR [#2739](https://github.com/tiangolo/fastapi/pull/2739) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Add new Gold Sponsor Talk Python 🎉. PR [#2673](https://github.com/tiangolo/fastapi/pull/2673) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Gold Sponsor vim.so 🎉. PR [#2669](https://github.com/tiangolo/fastapi/pull/2669) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add FastAPI user survey banner. PR [#2623](https://github.com/tiangolo/fastapi/pull/2623) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Bronze Sponsor(s) 🥉🎉. PR [#2622](https://github.com/tiangolo/fastapi/pull/2622) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update social links: add Discord, fix GitHub. PR [#2621](https://github.com/tiangolo/fastapi/pull/2621) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update FastAPI People GitHub Sponsors order. PR [#2620](https://github.com/tiangolo/fastapi/pull/2620) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update InvestSuite sponsor data. PR [#2608](https://github.com/tiangolo/fastapi/pull/2608) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2590](https://github.com/tiangolo/fastapi/pull/2590) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.63.0

### Features

* ✨ Improve type annotations, add support for mypy --strict, internally and for external packages. PR [#2547](https://github.com/tiangolo/fastapi/pull/2547) by [@tiangolo](https://github.com/tiangolo).

### Breaking changes

* ⬆️ Upgrade Uvicorn when installing `fastapi[all]` to the latest version including `uvloop`, the new range is `uvicorn[standard] >=0.12.0,<0.14.0`. PR [#2548](https://github.com/tiangolo/fastapi/pull/2548) by [@tiangolo](https://github.com/tiangolo).

### Fixes

* 🐛 PR [#2547](https://github.com/tiangolo/fastapi/pull/2547) (read above) also fixes some false-positive mypy errors with `callbacks` parameters and when using the `OAuth2` class.

### Docs

* 📝 Update Uvicorn installation instructions to use uvicorn[standard] (includes uvloop). PR [#2543](https://github.com/tiangolo/fastapi/pull/2543) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update title for Deta tutorial. PR [#2466](https://github.com/tiangolo/fastapi/pull/2466) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2454](https://github.com/tiangolo/fastapi/pull/2454) by [@github-actions[bot]](https://github.com/apps/github-actions).

### Translations

* 🌐 Add docs lang selector widget. PR [#2542](https://github.com/tiangolo/fastapi/pull/2542) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Add Chinese translation for Tutorial - Response Status Code. PR [#2442](https://github.com/tiangolo/fastapi/pull/2442) by [@waynerv](https://github.com/waynerv).
* 🌐 Start translation of the documentation for the Albanian language. PR [#2516](https://github.com/tiangolo/fastapi/pull/2516) by [@vjanz](https://github.com/vjanz).
* 🌐 Add Chinese translation for Tutorial - Extra Models. PR [#2416](https://github.com/tiangolo/fastapi/pull/2416) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Response Model. PR [#2414](https://github.com/tiangolo/fastapi/pull/2414) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Schema Extra Example. PR [#2411](https://github.com/tiangolo/fastapi/pull/2411) by [@maoyibo](https://github.com/maoyibo).
* 🌐 Add Korean translation for Index. PR [#2192](https://github.com/tiangolo/fastapi/pull/2192) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Japanese translation for Advanced User Guide - Additional Status Codes. PR [#2145](https://github.com/tiangolo/fastapi/pull/2145) by [@Attsun1031](https://github.com/Attsun1031).

### Internal

* 🐛 Fix docs overrides directory for translations. PR [#2541](https://github.com/tiangolo/fastapi/pull/2541) by [@tiangolo](https://github.com/tiangolo).
* ➖ Remove Typer as a docs building dependency (covered by typer-cli) to fix pip resolver conflicts. PR [#2539](https://github.com/tiangolo/fastapi/pull/2539) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add newsletter: FastAPI and friends. PR [#2509](https://github.com/tiangolo/fastapi/pull/2509) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add new Gold Sponsor: InvestSuite 🎉. PR [#2508](https://github.com/tiangolo/fastapi/pull/2508) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add issue template configs. PR [#2476](https://github.com/tiangolo/fastapi/pull/2476) by [@tiangolo](https://github.com/tiangolo).

## 0.62.0

### Features

* ✨ Add support for shared/top-level parameters (dependencies, tags, etc). PR [#2434](https://github.com/tiangolo/fastapi/pull/2434) by [@tiangolo](https://github.com/tiangolo).

Up to now, for several options, the only way to apply them to a group of *path operations* was in `include_router`. That works well, but the call to `app.include_router()` or `router.include_router()` is normally done in another file.

That means that, for example, to apply authentication to all the *path operations* in a router it would end up being done in a different file, instead of keeping related logic together.

Setting options in `include_router` still makes sense in some cases, for example, to override or increase configurations from a third party router included in an app. But in a router that is part of a bigger application, it would probably make more sense to add those settings when creating the `APIRouter`.

**In `FastAPI`**

This allows setting the (mostly new) parameters (additionally to the already existing parameters):

* `default_response_class`: updated to handle defaults in `APIRouter` and `include_router`.
* `dependencies`: to include ✨ top-level dependencies ✨ that apply to the whole application. E.g. to add global authentication.
* `callbacks`: OpenAPI callbacks that apply to all the *path operations*.
* `deprecated`: to mark all the *path operations* as deprecated. 🤷
* `include_in_schema`: to allow excluding all the *path operations* from the OpenAPI schema.
* `responses`: OpenAPI responses that apply to all the *path operations*.

For example:

```Python
from fastapi import FastAPI, Depends


async def some_dependency():
    return


app = FastAPI(dependencies=[Depends(some_dependency)])
```

**In `APIRouter`**

This allows setting the (mostly new) parameters (additionally to the already existing parameters):

* `default_response_class`: updated to handle defaults in `APIRouter` and `include_router`. For example, it's not needed to set it explicitly when [creating callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
* `dependencies`: to include ✨ router-level dependencies ✨ that apply to all the *path operations* in a router. Up to now, this was only possible with `include_router`.
* `callbacks`: OpenAPI callbacks that apply to all the *path operations* in this router.
* `deprecated`: to mark all the *path operations* in a router as deprecated.
* `include_in_schema`: to allow excluding all the *path operations* in a router from the OpenAPI schema.
* `responses`: OpenAPI responses that apply to all the *path operations* in a router.
* `prefix`: to set the path prefix for a router. Up to now, this was only possible when calling `include_router`.
* `tags`: OpenAPI tags to apply to all the *path operations* in this router.

For example:

```Python
from fastapi import APIRouter, Depends


async def some_dependency():
    return


router = APIRouter(prefix="/users", dependencies=[Depends(some_dependency)])
```

**In `include_router`**

Most of these settings are now supported in `APIRouter`, which normally lives closer to the related code, so it is recommended to use `APIRouter` when possible.

But `include_router` is still useful to, for example, adding options (like `dependencies`, `prefix`, and `tags`) when including a third party router, or a generic router that is shared between several projects.

This PR allows setting the (mostly new) parameters (additionally to the already existing parameters):

* `default_response_class`: updated to handle defaults in `APIRouter` and `FastAPI`.
* `deprecated`: to mark all the *path operations* in a router as deprecated in OpenAPI.
* `include_in_schema`: to allow disabling all the *path operations* from showing in the OpenAPI schema.
* `callbacks`: OpenAPI callbacks that apply to all the *path operations* in this router.

Note: all the previous parameters are still there, so it's still possible to declare `dependencies` in `include_router`.

### Breaking Changes

* PR [#2434](https://github.com/tiangolo/fastapi/pull/2434) includes several improvements that shouldn't affect normal use cases, but could affect in advanced scenarios:
    * If you are testing the generated OpenAPI (you shouldn't, FastAPI already tests it extensively for you): the order for `tags` in `include_router` and *path operations* was updated for consistency, but it's a simple order change.
    * If you have advanced custom logic to access each route's `route.response_class`, or the `router.default_response_class`, or the `app.default_response_class`: the default value for `response_class` in `APIRoute` and for `default_response_class` in `APIRouter` and `FastAPI` is now a `DefaultPlaceholder` used internally to handle and solve default values and overrides. The actual response class inside the `DefaultPlaceholder` is available at `route.response_class.value`.

### Docs

* PR [#2434](https://github.com/tiangolo/fastapi/pull/2434) (above) includes new or updated docs:
    * <a href="https://fastapi.tiangolo.com/advanced/openapi-callbacks/" class="external-link" target="_blank">Advanced User Guide - OpenAPI Callbacks</a>.
    * <a href="https://fastapi.tiangolo.com/tutorial/bigger-applications/" class="external-link" target="_blank">Tutorial - Bigger Applications</a>.
    * <a href="https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/" class="external-link" target="_blank">Tutorial - Dependencies - Dependencies in path operation decorators</a>.
    * <a href="https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/" class="external-link" target="_blank">Tutorial - Dependencies - Global Dependencies</a>.

* 📝 Add FastAPI monitoring blog post to External Links. PR [#2324](https://github.com/tiangolo/fastapi/pull/2324) by [@louisguitton](https://github.com/louisguitton).
* ✏️ Fix typo in Deta tutorial. PR [#2320](https://github.com/tiangolo/fastapi/pull/2320) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add Discord chat. PR [#2322](https://github.com/tiangolo/fastapi/pull/2322) by [@tiangolo](https://github.com/tiangolo).
* 📝 Fix image links for sponsors. PR [#2304](https://github.com/tiangolo/fastapi/pull/2304) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Japanese translation for Advanced - Custom Response. PR [#2193](https://github.com/tiangolo/fastapi/pull/2193) by [@Attsun1031](https://github.com/Attsun1031).
* 🌐 Add Chinese translation for Benchmarks. PR [#2119](https://github.com/tiangolo/fastapi/pull/2119) by [@spaceack](https://github.com/spaceack).
* 🌐 Add Chinese translation for Tutorial - Body - Nested Models. PR [#1609](https://github.com/tiangolo/fastapi/pull/1609) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Advanced - Custom Response. PR [#1459](https://github.com/tiangolo/fastapi/pull/1459) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* 🌐 Add Chinese translation for Advanced - Return a Response Directly. PR [#1452](https://github.com/tiangolo/fastapi/pull/1452) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* 🌐 Add Chinese translation for Advanced - Additional Status Codes. PR [#1451](https://github.com/tiangolo/fastapi/pull/1451) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* 🌐 Add Chinese translation for Advanced - Path Operation Advanced Configuration. PR [#1447](https://github.com/tiangolo/fastapi/pull/1447) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* 🌐 Add Chinese translation for Advanced User Guide - Intro. PR [#1445](https://github.com/tiangolo/fastapi/pull/1445) by [@RunningIkkyu](https://github.com/RunningIkkyu).

### Internal

* 🔧 Update TestDriven link to course in sponsors section. PR [#2435](https://github.com/tiangolo/fastapi/pull/2435) by [@tiangolo](https://github.com/tiangolo).
* 🍱 Update sponsor logos. PR [#2418](https://github.com/tiangolo/fastapi/pull/2418) by [@tiangolo](https://github.com/tiangolo).
* 💚 Fix disabling install of Material for MkDocs Insiders in forks, strike 1 ⚾. PR [#2340](https://github.com/tiangolo/fastapi/pull/2340) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix disabling Material for MkDocs Insiders install in forks. PR [#2339](https://github.com/tiangolo/fastapi/pull/2339) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add silver sponsor WeTransfer. PR [#2338](https://github.com/tiangolo/fastapi/pull/2338) by [@tiangolo](https://github.com/tiangolo).
* ✨ Set up and enable Material for MkDocs Insiders for the docs. PR [#2325](https://github.com/tiangolo/fastapi/pull/2325) by [@tiangolo](https://github.com/tiangolo).

## 0.61.2

### Fixes

* 📌 Relax Swagger UI version pin. PR [#2089](https://github.com/tiangolo/fastapi/pull/2089) by [@jmriebold](https://github.com/jmriebold).
* 🐛 Fix bug overriding custom HTTPException and RequestValidationError from exception_handlers. PR [#1924](https://github.com/tiangolo/fastapi/pull/1924) by [@uriyyo](https://github.com/uriyyo).
* ✏️ Fix typo on dependencies utils and cleanup unused variable. PR [#1912](https://github.com/tiangolo/fastapi/pull/1912) by [@Kludex](https://github.com/Kludex).

### Docs

* ✏️  Fix typo in Tutorial - Path Parameters. PR [#2231](https://github.com/tiangolo/fastapi/pull/2231) by [@mariacamilagl](https://github.com/mariacamilagl).
* ✏ Fix a stylistic error in docs. PR [#2206](https://github.com/tiangolo/fastapi/pull/2206) by [@ddobrinskiy](https://github.com/ddobrinskiy).
* ✏ Fix capitalizaiton typo in docs. PR [#2204](https://github.com/tiangolo/fastapi/pull/2204) by [@imba-tjd](https://github.com/imba-tjd).
* ✏ Fix typo in docs. PR [#2179](https://github.com/tiangolo/fastapi/pull/2179) by [@ammarasmro](https://github.com/ammarasmro).
* 📝 Update/fix links in docs to use HTTPS. PR [#2165](https://github.com/tiangolo/fastapi/pull/2165) by [@imba-tjd](https://github.com/imba-tjd).
* ✏ Fix typos and add rewording in docs. PR [#2159](https://github.com/tiangolo/fastapi/pull/2159) by [@nukopy](https://github.com/nukopy).
* 📝 Fix code consistency in examples for Tutorial - User Guide - Path Parameters. PR [#2158](https://github.com/tiangolo/fastapi/pull/2158) by [@nukopy](https://github.com/nukopy).
* 📝 Fix renamed parameter `content_type` typo. PR [#2135](https://github.com/tiangolo/fastapi/pull/2135) by [@TeoZosa](https://github.com/TeoZosa).
* ✏ Fix minor typos in docs. PR [#2122](https://github.com/tiangolo/fastapi/pull/2122) by [@TeoZosa](https://github.com/TeoZosa).
* ✏ Fix typos in docs and source examples. PR [#2102](https://github.com/tiangolo/fastapi/pull/2102) by [@AdrianDeAnda](https://github.com/AdrianDeAnda).
* ✏ Fix incorrect Celery URLs in docs. PR [#2100](https://github.com/tiangolo/fastapi/pull/2100) by [@CircleOnCircles](https://github.com/CircleOnCircles).
* 📝 Simplify intro to Python Types, all currently supported Python versions include type hints 🎉. PR [#2085](https://github.com/tiangolo/fastapi/pull/2085) by [@ninjaaron](https://github.com/ninjaaron).
* 📝 Fix example code with sets in Tutorial - Body - Nested Models 3. PR [#2054](https://github.com/tiangolo/fastapi/pull/2054) by [@hitrust](https://github.com/hitrust).
* 📝 Fix example code with sets in Tutorial - Body - Nested Models 2. PR [#2053](https://github.com/tiangolo/fastapi/pull/2053) by [@hitrust](https://github.com/hitrust).
* 📝 Fix example code with sets in Tutorial - Body - Nested Models. PR [#2052](https://github.com/tiangolo/fastapi/pull/2052) by [@hitrust](https://github.com/hitrust).
* ✏ Fix typo in Benchmarks. PR [#1995](https://github.com/tiangolo/fastapi/pull/1995) by [@AlejoAsd](https://github.com/AlejoAsd).
* 📝 Add note in CORS tutorial about allow_origins with ["*"] and allow_credentials. PR [#1895](https://github.com/tiangolo/fastapi/pull/1895) by [@dsmurrell](https://github.com/dsmurrell).
* 📝 Add deployment to Deta, the first gold sponsor 🎉. PR [#2303](https://github.com/tiangolo/fastapi/pull/2303) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2282](https://github.com/tiangolo/fastapi/pull/2282) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ✏️ Fix uppercase in Tutorial - Query parameters. PR [#2245](https://github.com/tiangolo/fastapi/pull/2245) by [@mariacamilagl](https://github.com/mariacamilagl).
* 📝 Add articles to External Links. PR [#2247](https://github.com/tiangolo/fastapi/pull/2247) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typo in Spanish tutorial index. PR [#2020](https://github.com/tiangolo/fastapi/pull/2020) by [@aviloncho](https://github.com/aviloncho).

### Translations

* 🌐 Add Japanese translation for Advanced Tutorial - Response Directly. PR [#2191](https://github.com/tiangolo/fastapi/pull/2191) by [@Attsun1031](https://github.com/Attsun1031).
* 📝 Add Japanese translation for Tutorial - Security - First Steps. PR [#2153](https://github.com/tiangolo/fastapi/pull/2153) by [@komtaki](https://github.com/komtaki).
* 🌐 Add Japanese translation for Tutorial - Query Parameters and String Validations. PR [#1901](https://github.com/tiangolo/fastapi/pull/1901) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Portuguese translation for External Links. PR [#1443](https://github.com/tiangolo/fastapi/pull/1443) by [@Serrones](https://github.com/Serrones).
* 🌐 Add Japanese translation for Tutorial - CORS. PR [#2125](https://github.com/tiangolo/fastapi/pull/2125) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Contributing. PR [#2067](https://github.com/tiangolo/fastapi/pull/2067) by [@komtaki](https://github.com/komtaki).
* 🌐 Add Japanese translation for Project Generation. PR [#2050](https://github.com/tiangolo/fastapi/pull/2050) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Alternatives. PR [#2043](https://github.com/tiangolo/fastapi/pull/2043) by [@Attsun1031](https://github.com/Attsun1031).
* 🌐 Add Japanese translation for History Design and Future. PR [#2002](https://github.com/tiangolo/fastapi/pull/2002) by [@komtaki](https://github.com/komtaki).
* 🌐 Add Japanese translation for Benchmarks. PR [#1992](https://github.com/tiangolo/fastapi/pull/1992) by [@komtaki](https://github.com/komtaki).
* 🌐 Add Japanese translation for Tutorial - Header Parameters. PR [#1935](https://github.com/tiangolo/fastapi/pull/1935) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Portuguese translation for Tutorial - First Steps. PR [#1861](https://github.com/tiangolo/fastapi/pull/1861) by [@jessicapaz](https://github.com/jessicapaz).
* 🌐 Add Portuguese translation for Python Types. PR [#1796](https://github.com/tiangolo/fastapi/pull/1796) by [@izaguerreiro](https://github.com/izaguerreiro).
* 🌐 Add Japanese translation for Help FastAPI. PR [#1692](https://github.com/tiangolo/fastapi/pull/1692) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Body. PR [#1683](https://github.com/tiangolo/fastapi/pull/1683) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Query Params. PR [#1674](https://github.com/tiangolo/fastapi/pull/1674) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for tutorial/path-params.md. PR [#1671](https://github.com/tiangolo/fastapi/pull/1671) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for tutorial/first-steps.md. PR [#1658](https://github.com/tiangolo/fastapi/pull/1658) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for tutorial/index.md. PR [#1656](https://github.com/tiangolo/fastapi/pull/1656) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add translation to Portuguese for Project Generation. PR [#1602](https://github.com/tiangolo/fastapi/pull/1602) by [@Serrones](https://github.com/Serrones).
* 🌐 Add Japanese translation for Features. PR [#1625](https://github.com/tiangolo/fastapi/pull/1625) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Initialize new language Korean for translations. PR [#2018](https://github.com/tiangolo/fastapi/pull/2018) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Portuguese translation of Deployment. PR [#1374](https://github.com/tiangolo/fastapi/pull/1374) by [@Serrones](https://github.com/Serrones).

### Internal

* 🔥 Cleanup after upgrade for Docs Previews GitHub Action. PR [#2248](https://github.com/tiangolo/fastapi/pull/2248) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix CI docs preview, unzip docs. PR [#2246](https://github.com/tiangolo/fastapi/pull/2246) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add instant docs deploy previews for PRs from forks. PR [#2244](https://github.com/tiangolo/fastapi/pull/2244) by [@tiangolo](https://github.com/tiangolo).
* ⚡️ Build docs for languages in parallel in subprocesses to speed up CI. PR [#2242](https://github.com/tiangolo/fastapi/pull/2242) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix docs order generation for partial translations. PR [#2238](https://github.com/tiangolo/fastapi/pull/2238) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2202](https://github.com/tiangolo/fastapi/pull/2202) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ♻️ Update FastAPI People GitHub Action to send the PR as github-actions. PR [#2201](https://github.com/tiangolo/fastapi/pull/2201) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update FastAPI People GitHub Action config, run monthly. PR [#2199](https://github.com/tiangolo/fastapi/pull/2199) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix FastAPI People GitHub Action Docker dependency, strike 1 ⚾. PR [#2198](https://github.com/tiangolo/fastapi/pull/2198) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix FastAPI People GitHub Action Docker dependencies. PR [#2197](https://github.com/tiangolo/fastapi/pull/2197) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix FastAPI People GitHub Action when there's nothing to change. PR [#2196](https://github.com/tiangolo/fastapi/pull/2196) by [@tiangolo](https://github.com/tiangolo).
* 👥 Add new section FastAPI People. PR [#2195](https://github.com/tiangolo/fastapi/pull/2195) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade GitHub Action Latest Changes. PR [#2190](https://github.com/tiangolo/fastapi/pull/2190) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade GitHub Action Label Approved. PR [#2189](https://github.com/tiangolo/fastapi/pull/2189) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update GitHub Action Label Approved, run at 12:00. PR [#2185](https://github.com/tiangolo/fastapi/pull/2185) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade GitHub Action Latest Changes. PR [#2184](https://github.com/tiangolo/fastapi/pull/2184) by [@tiangolo](https://github.com/tiangolo).
* 👷 Set GitHub Action Label Approved to run daily, not every minute. PR [#2163](https://github.com/tiangolo/fastapi/pull/2163) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove pr-approvals GitHub Action as it's not compatible with forks. Use the new one. PR [#2162](https://github.com/tiangolo/fastapi/pull/2162) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action Latest Changes. PR [#2160](https://github.com/tiangolo/fastapi/pull/2160).
* 👷 Add GitHub Action Label Approved. PR [#2161](https://github.com/tiangolo/fastapi/pull/2161).

## 0.61.1

### Fixes

* Fix issues using `jsonable_encoder` with SQLAlchemy models directly. PR [#1987](https://github.com/tiangolo/fastapi/pull/1987).

### Docs

* Fix typo in NoSQL docs. PR [#1980](https://github.com/tiangolo/fastapi/pull/1980) by [@facundojmaero](https://github.com/facundojmaero).

### Translations

* Add translation for [main page to Japanese](https://fastapi.tiangolo.com/ja/) PR [#1571](https://github.com/tiangolo/fastapi/pull/1571) by [@ryuckel](https://github.com/ryuckel).
* Initialize French translations. PR [#1975](https://github.com/tiangolo/fastapi/pull/1975) by [@JulianMaurin-BM](https://github.com/JulianMaurin-BM).
* Initialize Turkish translations. PR [#1905](https://github.com/tiangolo/fastapi/pull/1905) by [@ycd](https://github.com/ycd).

### Internal

* Improve docs maintainability by updating `hl_lines` syntax to use ranges. PR [#1863](https://github.com/tiangolo/fastapi/pull/1863) by [@la-mar](https://github.com/la-mar).

## 0.61.0

### Features

* Add support for injecting `HTTPConnection` (as `Request` and `WebSocket`). Useful for sharing app state in dependencies. PR [#1827](https://github.com/tiangolo/fastapi/pull/1827) by [@nsidnev](https://github.com/nsidnev).
* Export `WebSocketDisconnect` and add example handling WebSocket disconnections to docs. PR [#1822](https://github.com/tiangolo/fastapi/pull/1822) by [@rkbeatss](https://github.com/rkbeatss).

### Breaking Changes

* Require Pydantic > `1.0.0`.
    * Remove support for deprecated Pydantic `0.32.2`. This improves maintainability and allows new features.
    * In `FastAPI` and `APIRouter`:
        * Remove *path operation decorators* related/deprecated parameter `response_model_skip_defaults` (use `response_model_exclude_unset` instead).
        * Change *path operation decorators* parameter default for `response_model_exclude` from `set()` to `None` (as is in Pydantic).
    * In `encoders.jsonable_encoder`:
        * Remove deprecated `skip_defaults`, use instead `exclude_unset`.
        * Set default of `exclude` from `set()` to `None` (as is in Pydantic).
    * PR [#1862](https://github.com/tiangolo/fastapi/pull/1862).
* In `encoders.jsonable_encoder` remove parameter `sqlalchemy_safe`.
    * It was an early hack to allow returning SQLAlchemy models, but it was never documented, and the recommended way is using Pydantic's `orm_mode` as described in the tutorial: [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/).
    * PR [#1864](https://github.com/tiangolo/fastapi/pull/1864).

### Docs

* Add link to the course by TestDriven.io: [Test-Driven Development with FastAPI and Docker](https://testdriven.io/courses/tdd-fastapi/). PR [#1860](https://github.com/tiangolo/fastapi/pull/1860).
* Fix empty log message in docs example about handling errors. PR [#1815](https://github.com/tiangolo/fastapi/pull/1815) by [@manlix](https://github.com/manlix).
* Reword text to reduce ambiguity while not being gender-specific. PR [#1824](https://github.com/tiangolo/fastapi/pull/1824) by [@Mause](https://github.com/Mause).

### Internal

* Add Flake8 linting. Original PR [#1774](https://github.com/tiangolo/fastapi/pull/1774) by [@MashhadiNima](https://github.com/MashhadiNima).
* Disable Gitter bot, as it's currently broken, and Gitter's response doesn't show the problem. PR [#1853](https://github.com/tiangolo/fastapi/pull/1853).

## 0.60.2

* Fix typo in docs for query parameters. PR [#1832](https://github.com/tiangolo/fastapi/pull/1832) by [@ycd](https://github.com/ycd).
* Add docs about [Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/). PR [#1619](https://github.com/tiangolo/fastapi/pull/1619) by [@empicano](https://github.com/empicano).
* Raise an exception when using form data (`Form`, `File`) without having `python-multipart` installed.
    * Up to now the application would run, and raise an exception only when receiving a request with form data, the new behavior, raising early, will prevent from deploying applications with broken dependencies.
    * It also detects if the correct package `python-multipart` is installed instead of the incorrect `multipart` (both importable as `multipart`).
    * PR [#1851](https://github.com/tiangolo/fastapi/pull/1851) based on original PR [#1627](https://github.com/tiangolo/fastapi/pull/1627) by [@chrisngyn](https://github.com/chrisngyn), [@YKo20010](https://github.com/YKo20010), [@kx-chen](https://github.com/kx-chen).
* Re-enable Gitter releases bot. PR [#1831](https://github.com/tiangolo/fastapi/pull/1831).
* Add link to async SQL databases tutorial from main SQL tutorial. PR [#1813](https://github.com/tiangolo/fastapi/pull/1813) by [@short2strings](https://github.com/short2strings).
* Fix typo in tutorial about behind a proxy. PR [#1807](https://github.com/tiangolo/fastapi/pull/1807) by [@toidi](https://github.com/toidi).
* Fix typo in Portuguese docs. PR [#1795](https://github.com/tiangolo/fastapi/pull/1795) by [@izaguerreiro](https://github.com/izaguerreiro).
* Add translations setup for Ukrainian. PR [#1830](https://github.com/tiangolo/fastapi/pull/1830).
* Add external link [Build And Host Fast Data Science Applications Using FastAPI](https://towardsdatascience.com/build-and-host-fast-data-science-applications-using-fastapi-823be8a1d6a0). PR [#1786](https://github.com/tiangolo/fastapi/pull/1786) by [@Kludex](https://github.com/Kludex).
* Fix encoding of Pydantic models that inherit from others models with custom `json_encoders`. PR [#1769](https://github.com/tiangolo/fastapi/pull/1769) by [@henrybetts](https://github.com/henrybetts).
* Simplify and improve `jsonable_encoder`. PR [#1754](https://github.com/tiangolo/fastapi/pull/1754) by [@MashhadiNima](https://github.com/MashhadiNima).
* Simplify internal code syntax in several points. PR [#1753](https://github.com/tiangolo/fastapi/pull/1753) by [@uriyyo](https://github.com/uriyyo).
* Improve internal typing, declare `Optional` parameters. PR [#1731](https://github.com/tiangolo/fastapi/pull/1731) by [@MashhadiNima](https://github.com/MashhadiNima).
* Add external link [Deploy FastAPI on Azure App Service](https://www.tutlinks.com/deploy-fastapi-on-azure/) to docs. PR [#1726](https://github.com/tiangolo/fastapi/pull/1726) by [@windson](https://github.com/windson).
* Add link to Starlette docs about WebSocket testing. PR [#1717](https://github.com/tiangolo/fastapi/pull/1717) by [@hellocoldworld](https://github.com/hellocoldworld).
* Refactor generating dependant, merge for loops. PR [#1714](https://github.com/tiangolo/fastapi/pull/1714) by [@Bloodielie](https://github.com/Bloodielie).
* Update example for templates with Jinja to include HTML media type. PR [#1690](https://github.com/tiangolo/fastapi/pull/1690) by [@frafra](https://github.com/frafra).
* Fix typos in docs for security. PR [#1678](https://github.com/tiangolo/fastapi/pull/1678) by [@nilslindemann](https://github.com/nilslindemann).
* Fix typos in docs for dependencies. PR [#1675](https://github.com/tiangolo/fastapi/pull/1675) by [@nilslindemann](https://github.com/nilslindemann).
* Fix type annotation for `**extra` parameters in `FastAPI`. PR [#1659](https://github.com/tiangolo/fastapi/pull/1659) by [@bharel](https://github.com/bharel).
* Bump MkDocs Material to fix docs in browsers with dark mode. PR [#1789](https://github.com/tiangolo/fastapi/pull/1789) by [@adriencaccia](https://github.com/adriencaccia).
* Remove docs preview comment from each commit. PR [#1826](https://github.com/tiangolo/fastapi/pull/1826).
* Update GitHub context extraction for Gitter notification bot. PR [#1766](https://github.com/tiangolo/fastapi/pull/1766).

## 0.60.1

* Add debugging logs for GitHub actions to introspect GitHub hidden context. PR [#1764](https://github.com/tiangolo/fastapi/pull/1764).
* Use OS preference theme for online docs. PR [#1760](https://github.com/tiangolo/fastapi/pull/1760) by [@adriencaccia](https://github.com/adriencaccia).
* Upgrade Starlette to version `0.13.6` to handle a vulnerability when using static files in Windows. PR [#1759](https://github.com/tiangolo/fastapi/pull/1759) by [@jamesag26](https://github.com/jamesag26).
* Pin Swagger UI temporarily, waiting for a fix for [swagger-api/swagger-ui#6249](https://github.com/swagger-api/swagger-ui/issues/6249). PR [#1763](https://github.com/tiangolo/fastapi/pull/1763).
* Update GitHub Actions, use commit from PR for docs preview, not commit from pre-merge. PR [#1761](https://github.com/tiangolo/fastapi/pull/1761).
* Update GitHub Actions, refactor Gitter bot. PR [#1746](https://github.com/tiangolo/fastapi/pull/1746).

## 0.60.0

* Add GitHub Action to watch for missing preview docs and trigger a preview deploy. PR [#1740](https://github.com/tiangolo/fastapi/pull/1740).
* Add custom GitHub Action to get artifact with docs preview. PR [#1739](https://github.com/tiangolo/fastapi/pull/1739).
* Add new GitHub Actions to preview docs from PRs. PR [#1738](https://github.com/tiangolo/fastapi/pull/1738).
* Add XML test coverage to support GitHub Actions. PR [#1737](https://github.com/tiangolo/fastapi/pull/1737).
* Update badges and remove Travis now that GitHub Actions is the main CI. PR [#1736](https://github.com/tiangolo/fastapi/pull/1736).
* Add GitHub Actions for CI, move from Travis. PR [#1735](https://github.com/tiangolo/fastapi/pull/1735).
* Add support for adding OpenAPI schema for GET requests with a body. PR [#1626](https://github.com/tiangolo/fastapi/pull/1626) by [@victorphoenix3](https://github.com/victorphoenix3).

## 0.59.0

* Fix typo in docstring for OAuth2 utils. PR [#1621](https://github.com/tiangolo/fastapi/pull/1621) by [@tomarv2](https://github.com/tomarv2).
* Update JWT docs to use Python-jose instead of PyJWT. Initial PR [#1610](https://github.com/tiangolo/fastapi/pull/1610) by [@asheux](https://github.com/asheux).
* Fix/re-enable search bar in docs. PR [#1703](https://github.com/tiangolo/fastapi/pull/1703).
* Auto-generate a "server" in OpenAPI `servers` when there's a `root_path` instead of prefixing all the `paths`:
    * Add a new parameter for `FastAPI` classes: `root_path_in_servers` to disable the auto-generation of `servers`.
    * New docs about `root_path` and `servers` in [Additional Servers](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).
    * Update OAuth2 examples to use a relative URL for `tokenUrl="token"` to make sure those examples keep working as-is even when behind a reverse proxy.
    * Initial PR [#1596](https://github.com/tiangolo/fastapi/pull/1596) by [@rkbeatss](https://github.com/rkbeatss).
* Fix typo/link in External Links. PR [#1702](https://github.com/tiangolo/fastapi/pull/1702).
* Update handling of [External Links](https://fastapi.tiangolo.com/external-links/) to use a data file and allow translating the headers without becoming obsolete quickly when new links are added. PR [#https://github.com/tiangolo/fastapi/pull/1701](https://github.com/tiangolo/fastapi/pull/1701).
* Add external link [Machine learning model serving in Python using FastAPI and Streamlit](https://davidefiocco.github.io/2020/06/27/streamlit-fastapi-ml-serving.html) to docs. PR [#1669](https://github.com/tiangolo/fastapi/pull/1669) by [@davidefiocco](https://github.com/davidefiocco).
* Add note in docs on order in Pydantic Unions. PR [#1591](https://github.com/tiangolo/fastapi/pull/1591) by [@kbanc](https://github.com/kbanc).
* Improve support for tests in editor. PR [#1699](https://github.com/tiangolo/fastapi/pull/1699).
* Pin dependencies. PR [#1697](https://github.com/tiangolo/fastapi/pull/1697).
* Update isort to version 5.x.x. PR [#1670](https://github.com/tiangolo/fastapi/pull/1670) by [@asheux](https://github.com/asheux).

## 0.58.1

* Add link in docs to Pydantic data types. PR [#1612](https://github.com/tiangolo/fastapi/pull/1612) by [@tayoogunbiyi](https://github.com/tayoogunbiyi).
* Fix link in warning logs for `openapi_prefix`. PR [#1611](https://github.com/tiangolo/fastapi/pull/1611) by [@bavaria95](https://github.com/bavaria95).
* Fix bad link in docs. PR [#1603](https://github.com/tiangolo/fastapi/pull/1603) by [@molto0504](https://github.com/molto0504).
* Add Vim temporary files to `.gitignore` for contributors using Vim. PR [#1590](https://github.com/tiangolo/fastapi/pull/1590) by [@asheux](https://github.com/asheux).
* Fix typo in docs for sub-applications. PR [#1578](https://github.com/tiangolo/fastapi/pull/1578) by [@schlpbch](https://github.com/schlpbch).
* Use `Optional` in all the examples in the docs. Original PR [#1574](https://github.com/tiangolo/fastapi/pull/1574) by [@chrisngyn](https://github.com/chrisngyn), [@kx-chen](https://github.com/kx-chen), [@YKo20010](https://github.com/YKo20010). Updated and merged PR [#1644](https://github.com/tiangolo/fastapi/pull/1644).
* Update tests and handling of `response_model_by_alias`. PR [#1642](https://github.com/tiangolo/fastapi/pull/1642).
* Add translation to Chinese for [Body - Fields - 请求体 - 字段](https://fastapi.tiangolo.com/zh/tutorial/body-fields/). PR [#1569](https://github.com/tiangolo/fastapi/pull/1569) by [@waynerv](https://github.com/waynerv).
* Update Chinese translation of main page. PR [#1564](https://github.com/tiangolo/fastapi/pull/1564) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Body - Multiple Parameters - 请求体 - 多个参数](https://fastapi.tiangolo.com/zh/tutorial/body-multiple-params/). PR [#1532](https://github.com/tiangolo/fastapi/pull/1532) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Path Parameters and Numeric Validations - 路径参数和数值校验](https://fastapi.tiangolo.com/zh/tutorial/path-params-numeric-validations/). PR [#1506](https://github.com/tiangolo/fastapi/pull/1506) by [@waynerv](https://github.com/waynerv).
* Add GitHub action to auto-label approved PRs (mainly for translations). PR [#1638](https://github.com/tiangolo/fastapi/pull/1638).

## 0.58.0

* Deep merge OpenAPI responses to preserve all the additional metadata. PR [#1577](https://github.com/tiangolo/fastapi/pull/1577).
* Mention in docs that only main app events are run (not sub-apps). PR [#1554](https://github.com/tiangolo/fastapi/pull/1554) by [@amacfie](https://github.com/amacfie).
* Fix body validation error response, do not include body variable when it is not embedded. PR [#1553](https://github.com/tiangolo/fastapi/pull/1553) by [@amacfie](https://github.com/amacfie).
* Fix testing OAuth2 security scopes when using dependency overrides. PR [#1549](https://github.com/tiangolo/fastapi/pull/1549) by [@amacfie](https://github.com/amacfie).
* Fix Model for JSON Schema keyword `not` as a JSON Schema instead of a list. PR [#1548](https://github.com/tiangolo/fastapi/pull/1548) by [@v-do](https://github.com/v-do).
* Add support for OpenAPI `servers`. PR [#1547](https://github.com/tiangolo/fastapi/pull/1547) by [@mikaello](https://github.com/mikaello).

## 0.57.0

* Remove broken link from "External Links". PR [#1565](https://github.com/tiangolo/fastapi/pull/1565) by [@victorphoenix3](https://github.com/victorphoenix3).
* Update/fix docs for [WebSockets with dependencies](https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others). Original PR [#1540](https://github.com/tiangolo/fastapi/pull/1540) by [@ChihSeanHsu](https://github.com/ChihSeanHsu).
* Add support for Python's `http.HTTPStatus` in `status_code` parameters. PR [#1534](https://github.com/tiangolo/fastapi/pull/1534) by [@retnikt](https://github.com/retnikt).
* When using Pydantic models with `__root__`, use the internal value in `jsonable_encoder`. PR [#1524](https://github.com/tiangolo/fastapi/pull/1524) by [@patrickkwang](https://github.com/patrickkwang).
* Update docs for path parameters. PR [#1521](https://github.com/tiangolo/fastapi/pull/1521) by [@yankeexe](https://github.com/yankeexe).
* Update docs for first steps, links and rewording. PR [#1518](https://github.com/tiangolo/fastapi/pull/1518) by [@yankeexe](https://github.com/yankeexe).
* Enable `showCommonExtensions` in Swagger UI to show additional validations like `maxLength`, etc. PR [#1466](https://github.com/tiangolo/fastapi/pull/1466) by [@TiewKH](https://github.com/TiewKH).
* Make `OAuth2PasswordRequestFormStrict` importable directly from `fastapi.security`. PR [#1462](https://github.com/tiangolo/fastapi/pull/1462) by [@RichardHoekstra](https://github.com/RichardHoekstra).
* Add docs about [Default response class](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). PR [#1455](https://github.com/tiangolo/fastapi/pull/1455) by [@TezRomacH](https://github.com/TezRomacH).
* Add note in docs about additional parameters `response_model_exclude_defaults` and `response_model_exclude_none` in [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter). PR [#1427](https://github.com/tiangolo/fastapi/pull/1427) by [@wshayes](https://github.com/wshayes).
* Add note about [PyCharm Pydantic plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin) to docs. PR [#1420](https://github.com/tiangolo/fastapi/pull/1420) by [@koxudaxi](https://github.com/koxudaxi).
* Update and clarify testing function name. PR [#1395](https://github.com/tiangolo/fastapi/pull/1395) by [@chenl](https://github.com/chenl).
* Fix duplicated headers created by indirect dependencies that use the request directly. PR [#1386](https://github.com/tiangolo/fastapi/pull/1386) by [@obataku](https://github.com/obataku) from tests by [@scottsmith2gmail](https://github.com/scottsmith2gmail).
* Upgrade Starlette version to `0.13.4`. PR [#1361](https://github.com/tiangolo/fastapi/pull/1361) by [@rushton](https://github.com/rushton).
* Improve error handling and feedback for requests with invalid JSON. PR [#1354](https://github.com/tiangolo/fastapi/pull/1354) by [@aviramha](https://github.com/aviramha).
* Add support for declaring metadata for tags in OpenAPI. New docs at [Tutorial - Metadata and Docs URLs - Metadata for tags](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). PR [#1348](https://github.com/tiangolo/fastapi/pull/1348) by [@thomas-maschler](https://github.com/thomas-maschler).
* Add basic setup for Russian translations. PR [#1566](https://github.com/tiangolo/fastapi/pull/1566).
* Remove obsolete Chinese articles after adding official community translations. PR [#1510](https://github.com/tiangolo/fastapi/pull/1510) by [@waynerv](https://github.com/waynerv).
* Add `__repr__` for *path operation function* parameter helpers (like `Query`, `Depends`, etc) to simplify debugging. PR [#1560](https://github.com/tiangolo/fastapi/pull/1560) by [@rkbeatss](https://github.com/rkbeatss) and [@victorphoenix3](https://github.com/victorphoenix3).

## 0.56.1

* Add link to advanced docs from tutorial. PR [#1512](https://github.com/tiangolo/fastapi/pull/1512) by [@kx-chen](https://github.com/kx-chen).
* Remove internal unnecessary f-strings. PR [#1526](https://github.com/tiangolo/fastapi/pull/1526) by [@kotamatsuoka](https://github.com/kotamatsuoka).
* Add translation to Chinese for [Query Parameters and String Validations - 查询参数和字符串校验](https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/). PR [#1500](https://github.com/tiangolo/fastapi/pull/1500) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Request Body - 请求体](https://fastapi.tiangolo.com/zh/tutorial/body/). PR [#1492](https://github.com/tiangolo/fastapi/pull/1492) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Help FastAPI - Get Help - 帮助 FastAPI - 获取帮助](https://fastapi.tiangolo.com/zh/help-fastapi/). PR [#1465](https://github.com/tiangolo/fastapi/pull/1465) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Query Parameters - 查询参数](https://fastapi.tiangolo.com/zh/tutorial/query-params/). PR [#1454](https://github.com/tiangolo/fastapi/pull/1454) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Contributing - 开发 - 贡献](https://fastapi.tiangolo.com/zh/contributing/). PR [#1460](https://github.com/tiangolo/fastapi/pull/1460) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Path Parameters - 路径参数](https://fastapi.tiangolo.com/zh/tutorial/path-params/). PR [#1453](https://github.com/tiangolo/fastapi/pull/1453) by [@waynerv](https://github.com/waynerv).
* Add official Microsoft project generator for [serving spaCy with FastAPI and Azure Cognitive Skills](https://github.com/microsoft/cookiecutter-spacy-fastapi) to [Project Generators](https://fastapi.tiangolo.com/project-generation/). PR [#1390](https://github.com/tiangolo/fastapi/pull/1390) by [@kabirkhan](https://github.com/kabirkhan).
* Update docs in [Python Types Intro](https://fastapi.tiangolo.com/python-types/) to include info about `Optional`. Original PR [#1377](https://github.com/tiangolo/fastapi/pull/1377) by [@yaegassy](https://github.com/yaegassy).
* Fix support for callable class dependencies with `yield`. PR [#1365](https://github.com/tiangolo/fastapi/pull/1365) by [@mrosales](https://github.com/mrosales).
* Fix/remove incorrect error logging when a client sends invalid payloads. PR [#1351](https://github.com/tiangolo/fastapi/pull/1351) by [@dbanty](https://github.com/dbanty).
* Add translation to Chinese for [First Steps - 第一步](https://fastapi.tiangolo.com/zh/tutorial/first-steps/). PR [#1323](https://github.com/tiangolo/fastapi/pull/1323) by [@waynerv](https://github.com/waynerv).
* Fix generating OpenAPI for apps using callbacks with routers including Pydantic models. PR [#1322](https://github.com/tiangolo/fastapi/pull/1322) by [@nsidnev](https://github.com/nsidnev).
* Optimize internal regex performance in `get_path_param_names()`. PR [#1243](https://github.com/tiangolo/fastapi/pull/1243) by [@heckad](https://github.com/heckad).
* Remove `*,` from functions in docs where it's not needed. PR [#1239](https://github.com/tiangolo/fastapi/pull/1239) by [@pankaj-giri](https://github.com/pankaj-giri).
* Start translations for Italian. PR [#1557](https://github.com/tiangolo/fastapi/pull/1557) by [@csr](https://github.com/csr).

## 0.56.0

* Add support for ASGI `root_path`:
    * Use `root_path` internally for mounted applications, so that OpenAPI and the docs UI works automatically without extra configurations and parameters.
    * Add new `root_path` parameter for `FastAPI` applications to provide it in cases where it can be set with the command line (e.g. for Uvicorn and Hypercorn, with the parameter `--root-path`).
    * Deprecate `openapi_prefix` parameter in favor of the new `root_path` parameter.
    * Add new/updated docs for [Sub Applications - Mounts](https://fastapi.tiangolo.com/advanced/sub-applications/), without `openapi_prefix` (as it is now handled automatically).
    * Add new/updated docs for [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/), including how to setup a local testing proxy with Traefik and using `root_path`.
    * Update docs for [Extending OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/) with the new `openapi_prefix` parameter passed (internally generated from `root_path`).
    * Original PR [#1199](https://github.com/tiangolo/fastapi/pull/1199) by [@iksteen](https://github.com/iksteen).
* Update new issue templates and docs: [Help FastAPI - Get Help](https://fastapi.tiangolo.com/help-fastapi/). PR [#1531](https://github.com/tiangolo/fastapi/pull/1531).
* Update GitHub action issue-manager. PR [#1520](https://github.com/tiangolo/fastapi/pull/1520).
* Add new links:
    * **English articles**:
        * [Real-time Notifications with Python and Postgres](https://wuilly.com/2019/10/real-time-notifications-with-python-and-postgres/) by [Guillermo Cruz](https://wuilly.com/).
        * [Microservice in Python using FastAPI](https://dev.to/paurakhsharma/microservice-in-python-using-fastapi-24cc)  by [Paurakh Sharma Humagain](https://twitter.com/PaurakhSharma).
        * [Build simple API service with Python FastAPI — Part 1](https://dev.to/cuongld2/build-simple-api-service-with-python-fastapi-part-1-581o) by [cuongld2](https://dev.to/cuongld2).
        * [FastAPI + Zeit.co = 🚀](https://paulsec.github.io/posts/fastapi_plus_zeit_serverless_fu/) by [Paul Sec](https://twitter.com/PaulWebSec).
        * [Build a web API from scratch with FastAPI - the workshop](https://dev.to/tiangolo/build-a-web-api-from-scratch-with-fastapi-the-workshop-2ehe) by [Sebastián Ramírez (tiangolo)](https://twitter.com/tiangolo).
        * [Build a Secure Twilio Webhook with Python and FastAPI](https://www.twilio.com/blog/build-secure-twilio-webhook-python-fastapi)  by [Twilio](https://www.twilio.com).
        * [Using FastAPI with Django](https://www.stavros.io/posts/fastapi-with-django/)  by [Stavros Korokithakis](https://twitter.com/Stavros).
        * [Introducing Dispatch](https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072) by [Netflix](https://netflixtechblog.com/).
    * **Podcasts**:
        * [Build The Next Generation Of Python Web Applications With FastAPI - Episode 259 - interview to Sebastían Ramírez (tiangolo)](https://www.pythonpodcast.com/fastapi-web-application-framework-episode-259/) by [Podcast.`__init__`](https://www.pythonpodcast.com/).
    * **Talks**:
        * [PyConBY 2020: Serve ML models easily with FastAPI](https://www.youtube.com/watch?v=z9K5pwb0rt8) by [Sebastián Ramírez (tiangolo)](https://twitter.com/tiangolo).
        * [[VIRTUAL] Py.Amsterdam's flying Software Circus: Intro to FastAPI](https://www.youtube.com/watch?v=PnpTY1f4k2U) by [Sebastián Ramírez (tiangolo)](https://twitter.com/tiangolo).
    * PR [#1467](https://github.com/tiangolo/fastapi/pull/1467).
* Add translation to Chinese for [Python Types Intro - Python 类型提示简介](https://fastapi.tiangolo.com/zh/python-types/). PR [#1197](https://github.com/tiangolo/fastapi/pull/1197) by [@waynerv](https://github.com/waynerv).

## 0.55.1

* Fix handling of enums with their own schema in path parameters. To support [samuelcolvin/pydantic#1432](https://github.com/samuelcolvin/pydantic/pull/1432) in FastAPI. PR [#1463](https://github.com/tiangolo/fastapi/pull/1463).

## 0.55.0

* Allow enums to allow them to have their own schemas in OpenAPI. To support [samuelcolvin/pydantic#1432](https://github.com/samuelcolvin/pydantic/pull/1432) in FastAPI. PR [#1461](https://github.com/tiangolo/fastapi/pull/1461).
* Add links for funding through [GitHub sponsors](https://github.com/sponsors/tiangolo). PR [#1425](https://github.com/tiangolo/fastapi/pull/1425).
* Update issue template for for questions. PR [#1344](https://github.com/tiangolo/fastapi/pull/1344) by [@retnikt](https://github.com/retnikt).
* Update warning about storing passwords in docs. PR [#1336](https://github.com/tiangolo/fastapi/pull/1336) by [@skorokithakis](https://github.com/skorokithakis).
* Fix typo. PR [#1326](https://github.com/tiangolo/fastapi/pull/1326) by [@chenl](https://github.com/chenl).
* Add translation to Portuguese for [Alternatives, Inspiration and Comparisons - Alternativas, Inspiração e Comparações](https://fastapi.tiangolo.com/pt/alternatives/). PR [#1325](https://github.com/tiangolo/fastapi/pull/1325) by [@Serrones](https://github.com/Serrones).
* Fix 2 typos in docs. PR [#1324](https://github.com/tiangolo/fastapi/pull/1324) by [@waynerv](https://github.com/waynerv).
* Update CORS docs, fix correct default of `max_age=600`. PR [#1301](https://github.com/tiangolo/fastapi/pull/1301) by [@derekbekoe](https://github.com/derekbekoe).
* Add translation of [main page to Portuguese](https://fastapi.tiangolo.com/pt/). PR [#1300](https://github.com/tiangolo/fastapi/pull/1300) by [@Serrones](https://github.com/Serrones).
* Re-word and clarify docs for extra info in fields. PR [#1299](https://github.com/tiangolo/fastapi/pull/1299) by [@chris-allnutt](https://github.com/chris-allnutt).
* Make sure the `*` in short features in the docs is consistent (after `.`) in all languages. PR [#1424](https://github.com/tiangolo/fastapi/pull/1424).
* Update order of execution for `get_db` in SQLAlchemy tutorial. PR [#1293](https://github.com/tiangolo/fastapi/pull/1293) by [@bcb](https://github.com/bcb).
* Fix typos in Async docs. PR [#1423](https://github.com/tiangolo/fastapi/pull/1423).

## 0.54.2

* Add translation to Spanish for [Concurrency and async / await - Concurrencia y async / await](https://fastapi.tiangolo.com/es/async/). PR [#1290](https://github.com/tiangolo/fastapi/pull/1290) by [@alvaropernas](https://github.com/alvaropernas).
* Remove obsolete vote link. PR [#1289](https://github.com/tiangolo/fastapi/pull/1289) by [@donhui](https://github.com/donhui).
* Allow disabling docs UIs by just disabling OpenAPI with `openapi_url=None`. New example in docs: [Advanced: Conditional OpenAPI](https://fastapi.tiangolo.com/advanced/conditional-openapi/). PR [#1421](https://github.com/tiangolo/fastapi/pull/1421).
* Add translation to Portuguese for [Benchmarks - Comparações](https://fastapi.tiangolo.com/pt/benchmarks/). PR [#1274](https://github.com/tiangolo/fastapi/pull/1274) by [@Serrones](https://github.com/Serrones).
* Add translation to Portuguese for [Tutorial - User Guide - Intro - Tutorial - Guia de Usuário - Introdução](https://fastapi.tiangolo.com/pt/tutorial/). PR [#1259](https://github.com/tiangolo/fastapi/pull/1259) by [@marcosmmb](https://github.com/marcosmmb).
* Allow using Unicode in MkDocs for translations. PR [#1419](https://github.com/tiangolo/fastapi/pull/1419).
* Add translation to Spanish for [Advanced User Guide - Intro - Guía de Usuario Avanzada - Introducción](https://fastapi.tiangolo.com/es/advanced/). PR [#1250](https://github.com/tiangolo/fastapi/pull/1250) by [@jfunez](https://github.com/jfunez).
* Add translation to Portuguese for [History, Design and Future - História, Design e Futuro](https://fastapi.tiangolo.com/pt/history-design-future/). PR [#1249](https://github.com/tiangolo/fastapi/pull/1249) by [@marcosmmb](https://github.com/marcosmmb).
* Add translation to Portuguese for [Features - Recursos](https://fastapi.tiangolo.com/pt/features/). PR [#1248](https://github.com/tiangolo/fastapi/pull/1248) by [@marcosmmb](https://github.com/marcosmmb).
* Add translation to Spanish for [Tutorial - User Guide - Intro - Tutorial - Guía de Usuario - Introducción](https://fastapi.tiangolo.com/es/tutorial/). PR [#1244](https://github.com/tiangolo/fastapi/pull/1244) by [@MartinEliasQ](https://github.com/MartinEliasQ).
* Add translation to Chinese for [Deployment - 部署](https://fastapi.tiangolo.com/zh/deployment/). PR [#1203](https://github.com/tiangolo/fastapi/pull/1203) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* Add translation to Chinese for [Tutorial - User Guide - Intro - 教程 - 用户指南 - 简介](https://fastapi.tiangolo.com/zh/tutorial/). PR [#1202](https://github.com/tiangolo/fastapi/pull/1202) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Features - 特性](https://fastapi.tiangolo.com/zh/features/). PR [#1192](https://github.com/tiangolo/fastapi/pull/1192) by [@Dustyposa](https://github.com/Dustyposa).
* Add translation for [main page to Chinese](https://fastapi.tiangolo.com/zh/) PR [#1191](https://github.com/tiangolo/fastapi/pull/1191) by [@waynerv](https://github.com/waynerv).
* Update docs for project generation. PR [#1287](https://github.com/tiangolo/fastapi/pull/1287).
* Add Spanish translation for [Introducción a los Tipos de Python (Python Types Intro)](https://fastapi.tiangolo.com/es/python-types/). PR [#1237](https://github.com/tiangolo/fastapi/pull/1237) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add Spanish translation for [Características (Features)](https://fastapi.tiangolo.com/es/features/). PR [#1220](https://github.com/tiangolo/fastapi/pull/1220) by [@mariacamilagl](https://github.com/mariacamilagl).

## 0.54.1

* Update database test setup. PR [#1226](https://github.com/tiangolo/fastapi/pull/1226).
* Improve test debugging by showing response text in failing tests. PR [#1222](https://github.com/tiangolo/fastapi/pull/1222) by [@samuelcolvin](https://github.com/samuelcolvin).

## 0.54.0

* Fix grammatical mistakes in async docs. PR [#1188](https://github.com/tiangolo/fastapi/pull/1188) by [@mickeypash](https://github.com/mickeypash).
* Add support for `response_model_exclude_defaults` and `response_model_exclude_none`:
    * Deprecate the parameter `include_none` in `jsonable_encoder` and add the inverted `exclude_none`, to keep in sync with Pydantic.
    * PR [#1166](https://github.com/tiangolo/fastapi/pull/1166) by [@voegtlel](https://github.com/voegtlel).
* Add example about [Testing a Database](https://fastapi.tiangolo.com/advanced/testing-database/). Initial PR [#1144](https://github.com/tiangolo/fastapi/pull/1144) by [@duganchen](https://github.com/duganchen).
* Update docs for [Development - Contributing: Translations](https://fastapi.tiangolo.com/contributing/#translations) including note about reviewing translation PRs. [#1215](https://github.com/tiangolo/fastapi/pull/1215).
* Update log style in README.md for GitHub Markdown compatibility. PR [#1200](https://github.com/tiangolo/fastapi/pull/1200) by [#geekgao](https://github.com/geekgao).
* Add Python venv `env` to `.gitignore`. PR [#1212](https://github.com/tiangolo/fastapi/pull/1212) by [@cassiobotaro](https://github.com/cassiobotaro).
* Start Portuguese translations. PR [#1210](https://github.com/tiangolo/fastapi/pull/1210) by [@cassiobotaro](https://github.com/cassiobotaro).
* Update docs for Pydantic's `Settings` using a dependency with `@lru_cache()`. PR [#1214](https://github.com/tiangolo/fastapi/pull/1214).
* Add first translation to Spanish [FastAPI](https://fastapi.tiangolo.com/es/). PR [#1201](https://github.com/tiangolo/fastapi/pull/1201) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add docs about [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/). Initial PR [1118](https://github.com/tiangolo/fastapi/pull/1118) by [@alexmitelman](https://github.com/alexmitelman).

## 0.53.2

* Fix automatic embedding of body fields for dependencies and sub-dependencies. Original PR [#1079](https://github.com/tiangolo/fastapi/pull/1079) by [@Toad2186](https://github.com/Toad2186).
* Fix dependency overrides in WebSocket testing. PR [#1122](https://github.com/tiangolo/fastapi/pull/1122) by [@amitlissack](https://github.com/amitlissack).
* Fix docs script to ensure languages are always sorted. PR [#1189](https://github.com/tiangolo/fastapi/pull/1189).
* Start translations for Chinese. PR [#1187](https://github.com/tiangolo/fastapi/pull/1187) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* Add docs for [Schema Extra - Example](https://fastapi.tiangolo.com/tutorial/schema-extra-example/). PR [#1185](https://github.com/tiangolo/fastapi/pull/1185).

## 0.53.1

* Fix included example after translations refactor. PR [#1182](https://github.com/tiangolo/fastapi/pull/1182).
* Add docs example for `example` in `Field`. Docs at [Body - Fields: JSON Schema extras](https://fastapi.tiangolo.com/tutorial/body-fields/#json-schema-extras). PR [#1106](https://github.com/tiangolo/fastapi/pull/1106) by [@JohnPaton](https://github.com/JohnPaton).
* Fix using recursive models in `response_model`. PR [#1164](https://github.com/tiangolo/fastapi/pull/1164) by [@voegtlel](https://github.com/voegtlel).
* Add docs for [Pycharm Debugging](https://fastapi.tiangolo.com/tutorial/debugging/). PR [#1096](https://github.com/tiangolo/fastapi/pull/1096) by [@youngquan](https://github.com/youngquan).
* Fix typo in docs. PR [#1148](https://github.com/tiangolo/fastapi/pull/1148) by [@PLNech](https://github.com/PLNech).
* Update Windows development environment instructions. PR [#1179](https://github.com/tiangolo/fastapi/pull/1179).

## 0.53.0

* Update test coverage badge. PR [#1175](https://github.com/tiangolo/fastapi/pull/1175).
* Add `orjson` to `pip install fastapi[all]`. PR [#1161](https://github.com/tiangolo/fastapi/pull/1161) by [@michael0liver](https://github.com/michael0liver).
* Fix included example for `GZipMiddleware`. PR [#1138](https://github.com/tiangolo/fastapi/pull/1138) by [@arimbr](https://github.com/arimbr).
* Fix class name in docstring for `OAuth2PasswordRequestFormStrict`. PR [#1126](https://github.com/tiangolo/fastapi/pull/1126) by [@adg-mh](https://github.com/adg-mh).
* Clarify function name in example in docs. PR [#1121](https://github.com/tiangolo/fastapi/pull/1121) by [@tmsick](https://github.com/tmsick).
* Add external link [Apache Kafka producer and consumer with FastAPI and aiokafka](https://iwpnd.pw/articles/2020-03/apache-kafka-fastapi-geostream) to docs. PR [#1112](https://github.com/tiangolo/fastapi/pull/1112) by [@iwpnd](https://github.com/iwpnd).
* Fix serialization when using `by_alias` or `exclude_unset` and returning data with Pydantic models. PR [#1074](https://github.com/tiangolo/fastapi/pull/1074) by [@juhovh-aiven](https://github.com/juhovh-aiven).
* Add Gitter chat to docs. PR [#1061](https://github.com/tiangolo/fastapi/pull/1061) by [@aakashnand](https://github.com/aakashnand).
* Update and simplify translations docs. PR [#1171](https://github.com/tiangolo/fastapi/pull/1171).
* Update development of FastAPI docs, set address to `127.0.0.1` to improve Windows support. PR [#1169](https://github.com/tiangolo/fastapi/pull/1169) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add support for docs translations. New docs: [Development - Contributing: Docs: Translations](https://fastapi.tiangolo.com/contributing/#translations). PR [#1168](https://github.com/tiangolo/fastapi/pull/1168).
* Update terminal styles in docs and add note about [**Typer**, the FastAPI of CLIs](https://typer.tiangolo.com/). PR [#1139](https://github.com/tiangolo/fastapi/pull/1139).

## 0.52.0

* Add new high-performance JSON response class using `orjson`. New docs: [Custom Response - HTML, Stream, File, others: `ORJSONResponse`](https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse). PR [#1065](https://github.com/tiangolo/fastapi/pull/1065).

## 0.51.0

* Re-export utils from Starlette:
    * This allows using things like `from fastapi.responses import JSONResponse` instead of `from starlette.responses import JSONResponse`.
    * It's mainly syntax sugar, a convenience for developer experience.
    * Now `Request`, `Response`, `WebSocket`, `status` can be imported directly from `fastapi` as in `from fastapi import Response`. This is because those are frequently used, to use the request directly, to set headers and cookies, to get status codes, etc.
    * Documentation changes in many places, but new docs and noticeable improvements:
        * [Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
        * [Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/).
        * [Including WSGI - Flask, Django, others](https://fastapi.tiangolo.com/advanced/wsgi/).
    * PR [#1064](https://github.com/tiangolo/fastapi/pull/1064).

## 0.50.0

* Add link to Release Notes from docs about pinning versions for deployment. PR [#1058](https://github.com/tiangolo/fastapi/pull/1058).
* Upgrade code to use the latest version of Starlette, including:
    * Several bug fixes.
    * Optional redirects of slashes, with or without ending in `/`.
    * Events for routers, `"startup"`, and `"shutdown"`.
    * PR [#1057](https://github.com/tiangolo/fastapi/pull/1057).
* Add docs about pinning FastAPI versions for deployment: [Deployment: FastAPI versions](https://fastapi.tiangolo.com/deployment/#fastapi-versions). PR [#1056](https://github.com/tiangolo/fastapi/pull/1056).

## 0.49.2

* Fix links in release notes. PR [#1052](https://github.com/tiangolo/fastapi/pull/1052) by [@sattosan](https://github.com/sattosan).
* Fix typo in release notes. PR [#1051](https://github.com/tiangolo/fastapi/pull/1051) by [@sattosan](https://github.com/sattosan).
* Refactor/clarify `serialize_response` parameter name to avoid confusion. PR [#1031](https://github.com/tiangolo/fastapi/pull/1031) by [@patrickmckenna](https://github.com/patrickmckenna).
* Refactor calling each a path operation's handler function in an isolated function, to simplify profiling. PR [#1027](https://github.com/tiangolo/fastapi/pull/1027) by [@sm-Fifteen](https://github.com/sm-Fifteen).
* Add missing dependencies for testing. PR [#1026](https://github.com/tiangolo/fastapi/pull/1026) by [@sm-Fifteen](https://github.com/sm-Fifteen).
* Fix accepting valid types for response models, including Python types like `List[int]`. PR [#1017](https://github.com/tiangolo/fastapi/pull/1017) by [@patrickmckenna](https://github.com/patrickmckenna).
* Fix format in SQL tutorial. PR [#1015](https://github.com/tiangolo/fastapi/pull/1015) by [@vegarsti](https://github.com/vegarsti).

## 0.49.1

* Fix path operation duplicated parameters when used in dependencies and the path operation function. PR [#994](https://github.com/tiangolo/fastapi/pull/994) by [@merowinger92](https://github.com/merowinger92).
* Update Netlify previews deployment GitHub action as the fix is already merged and there's a new release. PR [#1047](https://github.com/tiangolo/fastapi/pull/1047).
* Move mypy configurations to config file. PR [#987](https://github.com/tiangolo/fastapi/pull/987) by [@hukkinj1](https://github.com/hukkinj1).
* Temporary fix to Netlify previews not deployable from PRs from forks. PR [#1046](https://github.com/tiangolo/fastapi/pull/1046) by [@mariacamilagl](https://github.com/mariacamilagl).

## 0.49.0

* Fix encoding of `pathlib` paths in `jsonable_encoder`. PR [#978](https://github.com/tiangolo/fastapi/pull/978) by [@patrickmckenna](https://github.com/patrickmckenna).
* Add articles to [External Links](https://fastapi.tiangolo.com/external-links/): [PythonのWeb frameworkのパフォーマンス比較 (Django, Flask, responder, FastAPI, japronto)](https://qiita.com/bee2/items/0ad260ab9835a2087dae) and [[FastAPI] Python製のASGI Web フレームワーク FastAPIに入門する](https://qiita.com/bee2/items/75d9c0d7ba20e7a4a0e9). PR [#974](https://github.com/tiangolo/fastapi/pull/974) by [@tokusumi](https://github.com/tokusumi).
* Fix broken links in docs. PR [#949](https://github.com/tiangolo/fastapi/pull/949) by [@tsotnikov](https://github.com/tsotnikov).
* Fix small typos. PR [#941](https://github.com/tiangolo/fastapi/pull/941) by [@NikitaKolesov](https://github.com/NikitaKolesov).
* Update and clarify docs for dependencies with `yield`. PR [#986](https://github.com/tiangolo/fastapi/pull/986).
* Add Mermaid JS support for diagrams in docs. Add first diagrams to [Dependencies: First Steps](https://fastapi.tiangolo.com/tutorial/dependencies/) and [Dependencies with `yield` and `HTTPException`](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception). PR [#985](https://github.com/tiangolo/fastapi/pull/985).
* Update CI to run docs deployment in GitHub actions. PR [#983](https://github.com/tiangolo/fastapi/pull/983).
* Allow `callable`s in *path operation functions*, like functions modified with `functools.partial`. PR [#977](https://github.com/tiangolo/fastapi/pull/977).

## 0.48.0

* Run linters first in tests to error out faster. PR [#948](https://github.com/tiangolo/fastapi/pull/948).
* Log warning about `email-validator` only when used. PR [#946](https://github.com/tiangolo/fastapi/pull/946).
* Simplify [Peewee docs](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/) with double dependency with `yield`. PR [#947](https://github.com/tiangolo/fastapi/pull/947).
* Add article [External Links](https://fastapi.tiangolo.com/external-links/): [Create and Deploy FastAPI app to Heroku](https://www.tutlinks.com/create-and-deploy-fastapi-app-to-heroku/). PR [#942](https://github.com/tiangolo/fastapi/pull/942) by [@windson](https://github.com/windson).
* Update description of Sanic, as it is now ASGI too. PR [#932](https://github.com/tiangolo/fastapi/pull/932) by [@raphaelauv](https://github.com/raphaelauv).
* Fix typo in main page. PR [#920](https://github.com/tiangolo/fastapi/pull/920) by [@mMarzeta](https://github.com/mMarzeta).
* Fix parsing of possibly invalid bodies. PR [#918](https://github.com/tiangolo/fastapi/pull/918) by [@dmontagu](https://github.com/dmontagu).
* Fix typo [#916](https://github.com/tiangolo/fastapi/pull/916) by [@adursun](https://github.com/adursun).
* Allow `Any` type for enums in OpenAPI. PR [#906](https://github.com/tiangolo/fastapi/pull/906) by [@songzhi](https://github.com/songzhi).
* Add article to [External Links](https://fastapi.tiangolo.com/external-links/): [How to continuously deploy a FastAPI to AWS Lambda with AWS SAM](https://iwpnd.pw/articles/2020-01/deploy-fastapi-to-aws-lambda). PR [#901](https://github.com/tiangolo/fastapi/pull/901) by [@iwpnd](https://github.com/iwpnd).
* Add note about using Body parameters without Pydantic. PR [#900](https://github.com/tiangolo/fastapi/pull/900) by [@pawamoy](https://github.com/pawamoy).
* Fix Pydantic field clone logic. PR [#899](https://github.com/tiangolo/fastapi/pull/899) by [@deuce2367](https://github.com/deuce2367).
* Fix link in middleware docs. PR [#893](https://github.com/tiangolo/fastapi/pull/893) by [@linchiwei123](https://github.com/linchiwei123).
* Rename default API title from "Fast API" to "FastAPI" for consistency. PR [#890](https://github.com/tiangolo/fastapi/pull/890).

## 0.47.1

* Fix model filtering in `response_model`, cloning sub-models. PR [#889](https://github.com/tiangolo/fastapi/pull/889).
* Fix FastAPI serialization of Pydantic models using ORM mode blocking the event loop. PR [#888](https://github.com/tiangolo/fastapi/pull/888).

## 0.47.0

* Refactor documentation to make a simpler and shorter [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/) and an additional [Advanced User Guide](https://fastapi.tiangolo.com/advanced/) with all the additional docs. PR [#887](https://github.com/tiangolo/fastapi/pull/887).
* Tweak external links, Markdown format, typos. PR [#881](https://github.com/tiangolo/fastapi/pull/881).
* Fix bug in tutorial handling HTTP Basic Auth `username` and `password`. PR [#865](https://github.com/tiangolo/fastapi/pull/865) by [@isaevpd](https://github.com/isaevpd).
* Fix handling form *path operation* parameters declared with pure classes like `list`, `tuple`, etc. PR [#856](https://github.com/tiangolo/fastapi/pull/856) by [@nsidnev](https://github.com/nsidnev).
* Add request `body` to `RequestValidationError`, new docs: [Use the `RequestValidationError` body](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body). Initial PR [#853](https://github.com/tiangolo/fastapi/pull/853) by [@aviramha](https://github.com/aviramha).
* Update [External Links](https://fastapi.tiangolo.com/external-links/) with new links and dynamic GitHub projects with `fastapi` topic. PR [#850](https://github.com/tiangolo/fastapi/pull/850).
* Fix Peewee `contextvars` handling in docs: [SQL (Relational) Databases with Peewee](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/). PR [#879](https://github.com/tiangolo/fastapi/pull/879).
* Setup development environment with Python's Venv and Flit, instead of requiring the extra Pipenv duplicating dependencies. Updated docs: [Development - Contributing](https://fastapi.tiangolo.com/contributing/). PR [#877](https://github.com/tiangolo/fastapi/pull/877).
* Update docs for [HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/) to improve security against timing attacks. Initial PR [#807](https://github.com/tiangolo/fastapi/pull/807) by [@zwass](https://github.com/zwass).

## 0.46.0

* Fix typos and tweak configs. PR [#837](https://github.com/tiangolo/fastapi/pull/837).
* Add link to Chinese article in [External Links](https://fastapi.tiangolo.com/external-links/). PR [810](https://github.com/tiangolo/fastapi/pull/810) by [@wxq0309](https://github.com/wxq0309).
* Implement `OAuth2AuthorizationCodeBearer` class. PR [#797](https://github.com/tiangolo/fastapi/pull/797) by [@kuwv](https://github.com/kuwv).
* Update example upgrade in docs main page. PR [#795](https://github.com/tiangolo/fastapi/pull/795) by [@cdeil](https://github.com/cdeil).
* Fix callback handling for sub-routers. PR [#792](https://github.com/tiangolo/fastapi/pull/792) by [@jekirl](https://github.com/jekirl).
* Fix typos. PR [#784](https://github.com/tiangolo/fastapi/pull/784) by [@kkinder](https://github.com/kkinder).
* Add 4 Japanese articles to [External Links](https://fastapi.tiangolo.com/external-links/). PR [#783](https://github.com/tiangolo/fastapi/pull/783) by [@HymanZHAN](https://github.com/HymanZHAN).
* Add support for subtypes of main types in `jsonable_encoder`, e.g. asyncpg's UUIDs. PR [#756](https://github.com/tiangolo/fastapi/pull/756) by [@RmStorm](https://github.com/RmStorm).
* Fix usage of Pydantic's `HttpUrl` in docs. PR [#832](https://github.com/tiangolo/fastapi/pull/832) by [@Dustyposa](https://github.com/Dustyposa).
* Fix Twitter links in docs. PR [#813](https://github.com/tiangolo/fastapi/pull/813) by [@justindujardin](https://github.com/justindujardin).
* Add docs for correctly [using FastAPI with Peewee ORM](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/). Including how to overwrite parts of Peewee to correctly handle async threads. PR [#789](https://github.com/tiangolo/fastapi/pull/789).

## 0.45.0

* Add support for OpenAPI Callbacks:
    * New docs: [OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
    * Refactor generation of `operationId`s to be valid Python names (also valid variables in most languages).
    * Add `default_response_class` parameter to `APIRouter`.
    * Original PR [#722](https://github.com/tiangolo/fastapi/pull/722) by [@booooh](https://github.com/booooh).
* Refactor logging to use the same logger everywhere, update log strings and levels. PR [#781](https://github.com/tiangolo/fastapi/pull/781).
* Add article to [External Links](https://fastapi.tiangolo.com/external-links/): [Почему Вы должны попробовать FastAPI?](https://habr.com/ru/post/478620/). PR [#766](https://github.com/tiangolo/fastapi/pull/766) by [@prostomarkeloff](https://github.com/prostomarkeloff).
* Remove gender bias in docs for handling errors. PR [#780](https://github.com/tiangolo/fastapi/pull/780). Original idea in PR [#761](https://github.com/tiangolo/fastapi/pull/761) by [@classywhetten](https://github.com/classywhetten).
* Rename docs and references to `body-schema` to `body-fields` to keep in line with Pydantic. PR [#746](https://github.com/tiangolo/fastapi/pull/746) by [@prostomarkeloff](https://github.com/prostomarkeloff).

## 0.44.1

* Add GitHub social preview images to git. PR [#752](https://github.com/tiangolo/fastapi/pull/752).
* Update PyPI "trove classifiers". PR [#751](https://github.com/tiangolo/fastapi/pull/751).
* Add full support for Python 3.8. Enable Python 3.8 in full in Travis. PR [749](https://github.com/tiangolo/fastapi/pull/749).
* Update "new issue" templates. PR [#749](https://github.com/tiangolo/fastapi/pull/749).
* Fix serialization of errors for exotic Pydantic types. PR [#748](https://github.com/tiangolo/fastapi/pull/748) by [@dmontagu](https://github.com/dmontagu).

## 0.44.0

* Add GitHub action [Issue Manager](https://github.com/tiangolo/issue-manager). PR [#742](https://github.com/tiangolo/fastapi/pull/742).
* Fix typos in docs. PR [734](https://github.com/tiangolo/fastapi/pull/734) by [@bundabrg](https://github.com/bundabrg).
* Fix usage of `custom_encoder` in `jsonable_encoder`. PR [#715](https://github.com/tiangolo/fastapi/pull/715) by [@matrixise](https://github.com/matrixise).
* Fix invalid XML example. PR [710](https://github.com/tiangolo/fastapi/pull/710) by [@OcasoProtal](https://github.com/OcasoProtal).
* Fix typos and update wording in deployment docs. PR [#700](https://github.com/tiangolo/fastapi/pull/700) by [@marier-nico](https://github.com/tiangolo/fastapi/pull/700).
* Add note about dependencies in `APIRouter` docs. PR [#698](https://github.com/tiangolo/fastapi/pull/698) by [@marier-nico](https://github.com/marier-nico).
* Add support for async class methods as dependencies [#681](https://github.com/tiangolo/fastapi/pull/681) by [@frankie567](https://github.com/frankie567).
* Add FastAPI with Swagger UI cheatsheet to external links. PR [#671](https://github.com/tiangolo/fastapi/pull/671) by [@euri10](https://github.com/euri10).
* Fix typo in HTTP protocol in CORS example. PR [#647](https://github.com/tiangolo/fastapi/pull/647) by [@forestmonster](https://github.com/forestmonster).
* Add support for Pydantic versions `1.0.0` and above, with temporary (deprecated) backwards compatibility for Pydantic `0.32.2`. PR [#646](https://github.com/tiangolo/fastapi/pull/646) by [@dmontagu](https://github.com/dmontagu).

## 0.43.0

* Update docs to reduce gender bias. PR [#645](https://github.com/tiangolo/fastapi/pull/645) by [@ticosax](https://github.com/ticosax).
* Add docs about [overriding the `operationId` for all the *path operations*](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid) based on their function name. PR [#642](https://github.com/tiangolo/fastapi/pull/642) by [@SKalt](https://github.com/SKalt).
* Fix validators in models generating an incorrect key order. PR [#637](https://github.com/tiangolo/fastapi/pull/637) by [@jaddison](https://github.com/jaddison).
* Generate correct OpenAPI docs for responses with no content. PR [#621](https://github.com/tiangolo/fastapi/pull/621) by [@brotskydotcom](https://github.com/brotskydotcom).
* Remove `$` from Bash code blocks in docs for consistency. PR [#613](https://github.com/tiangolo/fastapi/pull/613) by [@nstapelbroek](https://github.com/nstapelbroek).
* Add docs for [self-serving docs' (Swagger UI) static assets](https://fastapi.tiangolo.com/advanced/extending-openapi/#self-hosting-javascript-and-css-for-docs), e.g. to use the docs offline, or without Internet. Initial PR [#557](https://github.com/tiangolo/fastapi/pull/557) by [@svalouch](https://github.com/svalouch).
* Fix `black` linting after upgrade. PR [#682](https://github.com/tiangolo/fastapi/pull/682) by [@frankie567](https://github.com/frankie567).

## 0.42.0

* Add dependencies with `yield`, a.k.a. exit steps, context managers, cleanup, teardown, ...
    * This allows adding extra code after a dependency is done. It can be used, for example, to close database connections.
    * Dependencies with `yield` can be normal or `async`, **FastAPI** will run normal dependencies in a threadpool.
    * They can be combined with normal dependencies.
    * It's possible to have arbitrary trees/levels of dependencies with `yield` and exit steps are handled in the correct order automatically.
    * It works by default in Python 3.7 or above. For Python 3.6, it requires the extra backport dependencies:
        * `async-exit-stack`
        * `async-generator`
    * New docs at [Dependencies with `yield`](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
    * Updated database docs [SQL (Relational) Databases: Main **FastAPI** app](https://fastapi.tiangolo.com/tutorial/sql-databases/#main-fastapi-app).
    * PR [#595](https://github.com/tiangolo/fastapi/pull/595).
* Fix `sitemap.xml` in website. PR [#598](https://github.com/tiangolo/fastapi/pull/598) by [@samuelcolvin](https://github.com/samuelcolvin).

## 0.41.0

* Upgrade required Starlette to `0.12.9`, the new range is `>=0.12.9,<=0.12.9`.
    * Add `State` to FastAPI apps at `app.state`.
    * PR [#593](https://github.com/tiangolo/fastapi/pull/593).
* Improve handling of custom classes for `Request`s and `APIRoute`s.
    * This helps to more easily solve use cases like:
        * Reading a body before and/or after a request (equivalent to a middleware).
        * Run middleware-like code only for a subset of *path operations*.
        * Process a request before passing it to a *path operation function*. E.g. decompressing, deserializing, etc.
        * Processing a response after being generated by *path operation functions* but before returning it. E.g. adding custom headers, logging, adding extra metadata.
    * New docs section: [Custom Request and APIRoute class](https://fastapi.tiangolo.com/advanced/custom-request-and-route/).
    * PR [#589](https://github.com/tiangolo/fastapi/pull/589) by [@dmontagu](https://github.com/dmontagu).
* Fix preserving custom route class in routers when including other sub-routers. PR [#538](https://github.com/tiangolo/fastapi/pull/538) by [@dmontagu](https://github.com/dmontagu).

## 0.40.0

* Add notes to docs about installing `python-multipart` when using forms. PR [#574](https://github.com/tiangolo/fastapi/pull/574) by [@sliptonic](https://github.com/sliptonic).
* Generate OpenAPI schemas in alphabetical order. PR [#554](https://github.com/tiangolo/fastapi/pull/554) by [@dmontagu](https://github.com/dmontagu).
* Add support for truncating docstrings from *path operation functions*.
    * New docs at [Advanced description from docstring](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#advanced-description-from-docstring).
    * PR [#556](https://github.com/tiangolo/fastapi/pull/556) by [@svalouch](https://github.com/svalouch).
* Fix `DOCTYPE` in HTML files generated for Swagger UI and ReDoc. PR [#537](https://github.com/tiangolo/fastapi/pull/537) by [@Trim21](https://github.com/Trim21).
* Fix handling `4XX` responses overriding default `422` validation error responses. PR [#517](https://github.com/tiangolo/fastapi/pull/517) by [@tsouvarev](https://github.com/tsouvarev).
* Fix typo in documentation for [Simple HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#simple-http-basic-auth). PR [#514](https://github.com/tiangolo/fastapi/pull/514) by [@prostomarkeloff](https://github.com/prostomarkeloff).
* Fix incorrect documentation example in [first steps](https://fastapi.tiangolo.com/tutorial/first-steps/). PR [#511](https://github.com/tiangolo/fastapi/pull/511) by [@IgnatovFedor](https://github.com/IgnatovFedor).
* Add support for Swagger UI [initOauth](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/oauth2.md) settings with the parameter `swagger_ui_init_oauth`. PR [#499](https://github.com/tiangolo/fastapi/pull/499) by [@zamiramir](https://github.com/zamiramir).

## 0.39.0

* Allow path parameters to have default values (e.g. `None`) and discard them instead of raising an error.
    * This allows declaring a parameter like `user_id: str = None` that can be taken from a query parameter, but the same *path operation* can be included in a router with a path `/users/{user_id}`, in which case will be taken from the path and will be required.
    * PR [#464](https://github.com/tiangolo/fastapi/pull/464) by [@jonathanunderwood](https://github.com/jonathanunderwood).
* Add support for setting a `default_response_class` in the `FastAPI` instance or in `include_router`. Initial PR [#467](https://github.com/tiangolo/fastapi/pull/467) by [@toppk](https://github.com/toppk).
* Add support for type annotations using strings and `from __future__ import annotations`. PR [#451](https://github.com/tiangolo/fastapi/pull/451) by [@dmontagu](https://github.com/dmontagu).

## 0.38.1

* Fix incorrect `Request` class import. PR [#493](https://github.com/tiangolo/fastapi/pull/493) by [@kamalgill](https://github.com/kamalgill).

## 0.38.0

* Add recent articles to [External Links](https://fastapi.tiangolo.com/external-links/) and recent opinions. PR [#490](https://github.com/tiangolo/fastapi/pull/490).
* Upgrade support range for Starlette to include `0.12.8`. The new range is `>=0.11.1,<=0.12.8"`. PR [#477](https://github.com/tiangolo/fastapi/pull/477) by [@dmontagu](https://github.com/dmontagu).
* Upgrade support to Pydantic version 0.32.2 and update internal code to use it (breaking change). PR [#463](https://github.com/tiangolo/fastapi/pull/463) by [@dmontagu](https://github.com/dmontagu).

## 0.37.0

* Add support for custom route classes for advanced use cases. PR [#468](https://github.com/tiangolo/fastapi/pull/468) by [@dmontagu](https://github.com/dmontagu).
* Allow disabling Google fonts in ReDoc. PR [#481](https://github.com/tiangolo/fastapi/pull/481) by [@b1-luettje](https://github.com/b1-luettje).
* Fix security issue: when returning a sub-class of a response model and using `skip_defaults` it could leak information. PR [#485](https://github.com/tiangolo/fastapi/pull/485) by [@dmontagu](https://github.com/dmontagu).
* Enable tests for Python 3.8-dev. PR [#465](https://github.com/tiangolo/fastapi/pull/465) by [@Jamim](https://github.com/Jamim).
* Add support and tests for Pydantic dataclasses in `response_model`. PR [#454](https://github.com/tiangolo/fastapi/pull/454) by [@dconathan](https://github.com/dconathan).
* Fix typo in OAuth2 JWT tutorial. PR [#447](https://github.com/tiangolo/fastapi/pull/447) by [@pablogamboa](https://github.com/pablogamboa).
* Use the `media_type` parameter in `Body()` params to set the media type in OpenAPI for `requestBody`. PR [#439](https://github.com/tiangolo/fastapi/pull/439) by [@divums](https://github.com/divums).
* Add article [Deploying a scikit-learn model with ONNX and FastAPI](https://medium.com/@nico.axtmann95/deploying-a-scikit-learn-model-with-onnx-und-fastapi-1af398268915) by [https://www.linkedin.com/in/nico-axtmann](Nico Axtmann). PR [#438](https://github.com/tiangolo/fastapi/pull/438) by [@naxty](https://github.com/naxty).
* Allow setting custom `422` (validation error) response/schema in OpenAPI.
    * And use media type from response class instead of fixed `application/json` (the default).
    * PR [#437](https://github.com/tiangolo/fastapi/pull/437) by [@divums](https://github.com/divums).
* Fix using `"default"` extra response with status codes at the same time. PR [#489](https://github.com/tiangolo/fastapi/pull/489).
* Allow additional responses to use status code ranges (like `5XX` and `4XX`) and `"default"`. PR [#435](https://github.com/tiangolo/fastapi/pull/435) by [@divums](https://github.com/divums).

## 0.36.0

* Fix implementation for `skip_defaults` when returning a Pydantic model. PR [#422](https://github.com/tiangolo/fastapi/pull/422) by [@dmontagu](https://github.com/dmontagu).
* Fix OpenAPI generation when using the same dependency in multiple places for the same *path operation*. PR [#417](https://github.com/tiangolo/fastapi/pull/417) by [@dmontagu](https://github.com/dmontagu).
* Allow having empty paths in *path operations* used with `include_router` and a `prefix`.
    * This allows having a router for `/cats` and all its *path operations*, while having one of them for `/cats`.
    * Now it doesn't have to be only `/cats/` (with a trailing slash).
    * To use it, declare the path in the *path operation* as the empty string (`""`).
    * PR [#415](https://github.com/tiangolo/fastapi/pull/415) by [@vitalik](https://github.com/vitalik).
* Fix mypy error after merging PR #415. PR [#462](https://github.com/tiangolo/fastapi/pull/462).

## 0.35.0

* Fix typo in routing `assert`. PR [#419](https://github.com/tiangolo/fastapi/pull/419) by [@pablogamboa](https://github.com/pablogamboa).
* Fix typo in docs. PR [#411](https://github.com/tiangolo/fastapi/pull/411) by [@bronsen](https://github.com/bronsen).
* Fix parsing a body type declared with `Union`. PR [#400](https://github.com/tiangolo/fastapi/pull/400) by [@koxudaxi](https://github.com/koxudaxi).

## 0.34.0

* Upgrade Starlette supported range to include the latest `0.12.7`. The new range is `0.11.1,<=0.12.7`. PR [#367](https://github.com/tiangolo/fastapi/pull/367) by [@dedsm](https://github.com/dedsm).

* Add test for OpenAPI schema with duplicate models from PR [#333](https://github.com/tiangolo/fastapi/pull/333) by [@dmontagu](https://github.com/dmontagu). PR [#385](https://github.com/tiangolo/fastapi/pull/385).

## 0.33.0

* Upgrade Pydantic version to `0.30.0`. PR [#384](https://github.com/tiangolo/fastapi/pull/384) by [@jekirl](https://github.com/jekirl).

## 0.32.0

* Fix typo in docs for features. PR [#380](https://github.com/tiangolo/fastapi/pull/380) by [@MartinoMensio](https://github.com/MartinoMensio).

* Fix source code `limit` for example in [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/). PR [#366](https://github.com/tiangolo/fastapi/pull/366) by [@Smashman](https://github.com/Smashman).

* Update wording in docs about [OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/). PR [#371](https://github.com/tiangolo/fastapi/pull/371) by [@cjw296](https://github.com/cjw296).

* Update docs for `Enum`s to inherit from `str` and improve Swagger UI rendering. PR [#351](https://github.com/tiangolo/fastapi/pull/351).

* Fix regression, add Swagger UI deep linking again. PR [#350](https://github.com/tiangolo/fastapi/pull/350).

* Add test for having path templates in `prefix` of `.include_router`. PR [#349](https://github.com/tiangolo/fastapi/pull/349).

* Add note to docs: [Include the same router multiple times with different `prefix`](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-the-same-router-multiple-times-with-different-prefix). PR [#348](https://github.com/tiangolo/fastapi/pull/348).

* Fix OpenAPI/JSON Schema generation for two functions with the same name (in different modules) with the same composite bodies.
    * Composite bodies' IDs are now based on path, not only on route name, as the auto-generated name uses the function names, that can be duplicated in different modules.
    * The same new ID generation applies to response models.
    * This also changes the generated title for those models.
    * Only composite bodies and response models are affected because those are generated dynamically, they don't have a module (a Python file).
    * This also adds the possibility of using `.include_router()` with the same `APIRouter` *multiple*  times, with different prefixes, e.g. `/api/v2` and `/api/latest`, and it will now work correctly.
    * PR [#347](https://github.com/tiangolo/fastapi/pull/347).

## 0.31.0

* Upgrade Pydantic supported version to `0.29.0`.
    * New supported version range is `"pydantic >=0.28,<=0.29.0"`.
    * This adds support for Pydantic [Generic Models](https://pydantic-docs.helpmanual.io/#generic-models), kudos to [@dmontagu](https://github.com/dmontagu).
    * PR [#344](https://github.com/tiangolo/fastapi/pull/344).

## 0.30.1

* Add section in docs about [External Links and Articles](https://fastapi.tiangolo.com/external-links/). PR [#341](https://github.com/tiangolo/fastapi/pull/341).

* Remove `Pipfile.lock` from the repository as it is only used by FastAPI contributors (developers of FastAPI itself). See the PR for more details. PR [#340](https://github.com/tiangolo/fastapi/pull/340).

* Update section about [Help FastAPI - Get Help](https://fastapi.tiangolo.com/help-fastapi/). PR [#339](https://github.com/tiangolo/fastapi/pull/339).

* Refine internal type declarations to improve/remove Mypy errors in users' code. PR [#338](https://github.com/tiangolo/fastapi/pull/338).

* Update and clarify [SQL tutorial with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/). PR [#331](https://github.com/tiangolo/fastapi/pull/331) by [@mariacamilagl](https://github.com/mariacamilagl).

* Add SQLite [online viewers to the docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#interact-with-the-database-directly). PR [#330](https://github.com/tiangolo/fastapi/pull/330) by [@cyrilbois](https://github.com/cyrilbois).

## 0.30.0

* Add support for Pydantic's ORM mode:
    * Updated documentation about SQL with SQLAlchemy, using Pydantic models with ORM mode, SQLAlchemy models with relations, separation of files, simplification of code and other changes. New docs: [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/).
    * The new support for ORM mode fixes issues/adds features related to ORMs with lazy-loading, hybrid properties, dynamic/getters (using `@property` decorators) and several other use cases.
    * This applies to ORMs like SQLAlchemy, Peewee, Tortoise ORM, GINO ORM and virtually any other.
    * If your *path operations* return an arbitrary object with attributes (e.g. `my_item.name` instead of `my_item["name"]`) AND you use a `response_model`, make sure to update the Pydantic models with `orm_mode = True` as described in the docs (link above).
    * New documentation about receiving plain `dict`s as request bodies: [Bodies of arbitrary `dict`s](https://fastapi.tiangolo.com/tutorial/body-nested-models/#bodies-of-arbitrary-dicts).
    * New documentation about returning arbitrary `dict`s in responses: [Response with arbitrary `dict`](https://fastapi.tiangolo.com/tutorial/extra-models/#response-with-arbitrary-dict).
    * **Technical Details**:
        * When declaring a `response_model` it is used directly to generate the response content, from whatever was returned from the *path operation function*.
        * Before this, the return content was first passed through `jsonable_encoder` to ensure it was a "jsonable" object, like a `dict`, instead of an arbitrary object with attributes (like an ORM model). That's why you should make sure to update your Pydantic models for objects with attributes to use `orm_mode = True`.
        * If you don't have a `response_model`, the return object will still be passed through `jsonable_encoder` first.
        * When a `response_model` is declared, the same `response_model` type declaration won't be used as is, it will be "cloned" to create an new one (a cloned Pydantic `Field` with all the submodels cloned as well).
        * This avoids/fixes a potential security issue: as the returned object is passed directly to Pydantic, if the returned object was a subclass of the `response_model` (e.g. you return a `UserInDB` that inherits from `User` but contains extra fields, like `hashed_password`, and `User` is used in the `response_model`), it would still pass the validation (because `UserInDB` is a subclass of `User`) and the object would be returned as-is, including the `hashed_password`. To fix this, the declared `response_model` is cloned, if it is a Pydantic model class (or contains Pydantic model classes in it, e.g. in a `List[Item]`), the Pydantic model class(es) will be a different one (the "cloned" one). So, an object that is a subclass won't simply pass the validation and returned as-is, because it is no longer a sub-class of the cloned `response_model`. Instead, a new Pydantic model object will be created with the contents of the returned object. So, it will be a new object (made with the data from the returned one), and will be filtered by the cloned `response_model`, containing only the declared fields as normally.
    * PR [#322](https://github.com/tiangolo/fastapi/pull/322).

* Remove/clean unused RegEx code in routing. PR [#314](https://github.com/tiangolo/fastapi/pull/314) by [@dmontagu](https://github.com/dmontagu).

* Use default response status code descriptions for additional responses. PR [#313](https://github.com/tiangolo/fastapi/pull/313) by [@duxiaoyao](https://github.com/duxiaoyao).

* Upgrade Pydantic support to `0.28`. PR [#320](https://github.com/tiangolo/fastapi/pull/320) by [@jekirl](https://github.com/jekirl).

## 0.29.1

* Fix handling an empty-body request with a required body param. PR [#311](https://github.com/tiangolo/fastapi/pull/311).

* Fix broken link in docs: [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/). PR [#306](https://github.com/tiangolo/fastapi/pull/306) by [@dmontagu](https://github.com/dmontagu).

* Fix docs discrepancy in docs for [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/). PR [#288](https://github.com/tiangolo/fastapi/pull/288) by [@awiddersheim](https://github.com/awiddersheim).

## 0.29.0

* Add support for declaring a `Response` parameter:
    * This allows declaring:
        * [Response Cookies](https://fastapi.tiangolo.com/advanced/response-cookies/).
        * [Response Headers](https://fastapi.tiangolo.com/advanced/response-headers/).
        * An HTTP Status Code different than the default: [Response - Change Status Code](https://fastapi.tiangolo.com/advanced/response-change-status-code/).
    * All of this while still being able to return arbitrary objects (`dict`, DB model, etc).
    * Update attribution to Hug, for inspiring the `response` parameter pattern.
    * PR [#294](https://github.com/tiangolo/fastapi/pull/294).

## 0.28.0

* Implement dependency cache per request.
    * This avoids calling each dependency multiple times for the same request.
    * This is useful while calling external services, performing costly computation, etc.
    * This also means that if a dependency was declared as a *path operation decorator* dependency, possibly at the router level (with `.include_router()`) and then it is declared again in a specific *path operation*, the dependency will be called only once.
    * The cache can be disabled per dependency declaration, using `use_cache=False` as in `Depends(your_dependency, use_cache=False)`.
    * Updated docs at: [Using the same dependency multiple times](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times).
    * PR [#292](https://github.com/tiangolo/fastapi/pull/292).

* Implement dependency overrides for testing.
    * This allows using overrides/mocks of dependencies during tests.
    * New docs: [Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
    * PR [#291](https://github.com/tiangolo/fastapi/pull/291).

## 0.27.2

* Fix path and query parameters receiving `dict` as a valid type. It should be mapped to a body payload. PR [#287](https://github.com/tiangolo/fastapi/pull/287). Updated docs at: [Query parameter list / multiple values with defaults: Using `list`](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#using-list).

## 0.27.1

* Fix `auto_error=False` handling in `HTTPBearer` security scheme. Do not `raise` when there's an incorrect `Authorization` header if `auto_error=False`. PR [#282](https://github.com/tiangolo/fastapi/pull/282).

* Fix type declaration of `HTTPException`. PR [#279](https://github.com/tiangolo/fastapi/pull/279).

## 0.27.0

* Fix broken link in docs about OAuth 2.0 with scopes. PR [#275](https://github.com/tiangolo/fastapi/pull/275) by [@dmontagu](https://github.com/dmontagu).

* Refactor param extraction using Pydantic `Field`:
    * Large refactor, improvement, and simplification of param extraction from *path operations*.
    * Fix/add support for list *query parameters* with list defaults. New documentation: [Query parameter list / multiple values with defaults](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values-with-defaults).
    * Add support for enumerations in *path operation* parameters. New documentation: [Path Parameters: Predefined values](https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values).
    * Add support for type annotations using `Optional` as in `param: Optional[str] = None`. New documentation: [Optional type declarations](https://fastapi.tiangolo.com/tutorial/query-params/#optional-type-declarations).
    * PR [#278](https://github.com/tiangolo/fastapi/pull/278).

## 0.26.0

* Separate error handling for validation errors.
    * This will allow developers to customize the exception handlers.
    * Document better how to handle exceptions and use error handlers.
    * Include `RequestValidationError` and `WebSocketRequestValidationError` (this last one will be useful once [encode/starlette#527](https://github.com/encode/starlette/pull/527) or equivalent is merged).
    * New documentation about exceptions handlers:
        * [Install custom exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers).
        * [Override the default exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers).
        * [Re-use **FastAPI's** exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers).
    * PR [#273](https://github.com/tiangolo/fastapi/pull/273).

* Fix support for *paths* in *path parameters* without needing explicit `Path(...)`.
    * PR [#256](https://github.com/tiangolo/fastapi/pull/256).
    * Documented in PR [#272](https://github.com/tiangolo/fastapi/pull/272) by [@wshayes](https://github.com/wshayes).
    * New documentation at: [Path Parameters containing paths](https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-containing-paths).

* Update docs for testing FastAPI. Include using `POST`, sending JSON, testing headers, etc. New documentation: [Testing](https://fastapi.tiangolo.com/tutorial/testing/#testing-extended-example). PR [#271](https://github.com/tiangolo/fastapi/pull/271).

* Fix type declaration of `response_model` to allow generic Python types as `List[Model]`. Mainly to fix `mypy` for users. PR [#266](https://github.com/tiangolo/fastapi/pull/266).

## 0.25.0

* Add support for Pydantic's `include`, `exclude`, `by_alias`.
    * Update documentation: [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
    * Add docs for: [Body - updates](https://fastapi.tiangolo.com/tutorial/body-updates/), using Pydantic's `skip_defaults`.
    * Add method consistency tests.
    * PR [#264](https://github.com/tiangolo/fastapi/pull/264).

* Add `CONTRIBUTING.md` file to GitHub, to help new contributors. PR [#255](https://github.com/tiangolo/fastapi/pull/255) by [@wshayes](https://github.com/wshayes).

* Add support for Pydantic's `skip_defaults`:
    * There's a new *path operation decorator* parameter `response_model_skip_defaults`.
        * The name of the parameter will most probably change in a future version to `response_skip_defaults`, `model_skip_defaults` or something similar.
    * New [documentation section about using `response_model_skip_defaults`](https://fastapi.tiangolo.com/tutorial/response-model/#response-model-encoding-parameters).
    * PR [#248](https://github.com/tiangolo/fastapi/pull/248) by [@wshayes](https://github.com/wshayes).

## 0.24.0

* Add support for WebSockets with dependencies and parameters.
    * Support included for:
        * `Depends`
        * `Security`
        * `Cookie`
        * `Header`
        * `Path`
        * `Query`
        * ...as these are compatible with the WebSockets protocol (e.g. `Body` is not).
    * [Updated documentation for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).
    * PR [#178](https://github.com/tiangolo/fastapi/pull/178) by [@jekirl](https://github.com/jekirl).

* Upgrade the compatible version of Pydantic to `0.26.0`.
    * This includes JSON Schema support for IP address and network objects, bug fixes, and other features.
    * PR [#247](https://github.com/tiangolo/fastapi/pull/247) by [@euri10](https://github.com/euri10).

## 0.23.0

* Upgrade the compatible version of Starlette to `0.12.0`.
    * This includes support for ASGI 3 (the latest version of the standard).
    * It's now possible to use [Starlette's `StreamingResponse`](https://www.starlette.io/responses/#streamingresponse) with iterators, like [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) objects (as those returned by `open()`).
    * It's now possible to use the low level utility `iterate_in_threadpool` from `starlette.concurrency` (for advanced scenarios).
    * PR [#243](https://github.com/tiangolo/fastapi/pull/243).

* Add OAuth2 redirect page for Swagger UI. This allows having delegated authentication in the Swagger UI docs. For this to work, you need to add `{your_origin}/docs/oauth2-redirect` to the allowed callbacks in your OAuth2 provider (in Auth0, Facebook, Google, etc).
    * For example, during development, it could be `http://localhost:8000/docs/oauth2-redirect`.
    * Have in mind that this callback URL is independent of whichever one is used by your frontend. You might also have another callback at `https://yourdomain.com/login/callback`.
    * This is only to allow delegated authentication in the API docs with Swagger UI.
    * PR [#198](https://github.com/tiangolo/fastapi/pull/198) by [@steinitzu](https://github.com/steinitzu).

* Make Swagger UI and ReDoc route handlers (*path operations*) be `async` functions instead of lambdas to improve performance. PR [#241](https://github.com/tiangolo/fastapi/pull/241) by [@Trim21](https://github.com/Trim21).

* Make Swagger UI and ReDoc URLs parameterizable, allowing to host and serve local versions of them and have offline docs. PR [#112](https://github.com/tiangolo/fastapi/pull/112) by [@euri10](https://github.com/euri10).

## 0.22.0

* Add support for `dependencies` parameter:
    * A parameter in *path operation decorators*, for dependencies that should be executed but the return value is not important or not used in the *path operation function*.
    * A parameter in the `.include_router()` method of FastAPI applications and routers, to include dependencies that should be executed in each *path operation* in a router.
        * This is useful, for example, to require authentication or permissions in specific group of *path operations*.
        * Different `dependencies` can be applied to different routers.
    * These `dependencies` are run before the normal parameter dependencies. And normal dependencies are run too. They can be combined.
    * Dependencies declared in a router are executed first, then the ones defined in *path operation decorators*, and then the ones declared in normal parameters. They are all combined and executed.
    * All this also supports using `Security` with `scopes` in those `dependencies` parameters, for more advanced OAuth 2.0 security scenarios with scopes.
    * New documentation about [dependencies in *path operation decorators*](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
    * New documentation about [dependencies in the `include_router()` method](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-prefix-tags-responses-and-dependencies).
    * PR [#235](https://github.com/tiangolo/fastapi/pull/235).

* Fix OpenAPI documentation of Starlette URL convertors. Specially useful when using `path` convertors, to take a whole path as a parameter, like `/some/url/{p:path}`. PR [#234](https://github.com/tiangolo/fastapi/pull/234) by [@euri10](https://github.com/euri10).

* Make default parameter utilities exported from `fastapi` be functions instead of classes (the new functions return instances of those classes). To be able to override the return types and fix `mypy` errors in FastAPI's users' code. Applies to `Path`, `Query`, `Header`, `Cookie`, `Body`, `Form`, `File`, `Depends`, and `Security`. PR [#226](https://github.com/tiangolo/fastapi/pull/226) and PR [#231](https://github.com/tiangolo/fastapi/pull/231).

* Separate development scripts `test.sh`, `lint.sh`, and `format.sh`. PR [#232](https://github.com/tiangolo/fastapi/pull/232).

* Re-enable `black` formatting checks for Python 3.7. PR [#229](https://github.com/tiangolo/fastapi/pull/229) by [@zamiramir](https://github.com/zamiramir).

## 0.21.0

* On body parsing errors, raise `from` previous exception, to allow better introspection in logging code. PR [#192](https://github.com/tiangolo/fastapi/pull/195) by [@ricardomomm](https://github.com/ricardomomm).

* Use Python logger named "`fastapi`" instead of root logger. PR [#222](https://github.com/tiangolo/fastapi/pull/222) by [@euri10](https://github.com/euri10).

* Upgrade Pydantic to version 0.25. PR [#225](https://github.com/tiangolo/fastapi/pull/225) by [@euri10](https://github.com/euri10).

* Fix typo in routing. PR [#221](https://github.com/tiangolo/fastapi/pull/221) by [@djlambert](https://github.com/djlambert).

## 0.20.1

* Add typing information to package including file `py.typed`. PR [#209](https://github.com/tiangolo/fastapi/pull/209) by [@meadsteve](https://github.com/meadsteve).

* Add FastAPI bot for Gitter. To automatically announce new releases. PR [#189](https://github.com/tiangolo/fastapi/pull/189).

## 0.20.0

* Upgrade OAuth2:
    * Upgrade Password flow using Bearer tokens to use the correct HTTP status code 401 `UNAUTHORIZED`, with `WWW-Authenticate` headers.
    * Update, simplify, and improve all the [security docs](https://fastapi.tiangolo.com/advanced/security/).
    * Add new `scope_str` to `SecurityScopes` and update docs: [OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).
    * Update docs, images, tests.
    * PR [#188](https://github.com/tiangolo/fastapi/pull/188).

* Include [Hypercorn](https://gitlab.com/pgjones/hypercorn) as an alternative ASGI server in the docs. PR [#187](https://github.com/tiangolo/fastapi/pull/187).

* Add docs for [Static Files](https://fastapi.tiangolo.com/tutorial/static-files/) and [Templates](https://fastapi.tiangolo.com/advanced/templates/). PR [#186](https://github.com/tiangolo/fastapi/pull/186).

* Add docs for handling [Response Cookies](https://fastapi.tiangolo.com/advanced/response-cookies/) and [Response Headers](https://fastapi.tiangolo.com/advanced/response-headers/). PR [#185](https://github.com/tiangolo/fastapi/pull/185).

* Fix typos in docs. PR [#176](https://github.com/tiangolo/fastapi/pull/176) by [@chdsbd](https://github.com/chdsbd).

## 0.19.0

* Rename *path operation decorator* parameter `content_type` to `response_class`. PR [#183](https://github.com/tiangolo/fastapi/pull/183).

* Add docs:
    * How to use the `jsonable_encoder` in [JSON compatible encoder](https://fastapi.tiangolo.com/tutorial/encoder/).
    * How to [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/).
    * Update how to use a [Custom Response Class](https://fastapi.tiangolo.com/advanced/custom-response/).
    * PR [#184](https://github.com/tiangolo/fastapi/pull/184).

## 0.18.0

* Add docs for [HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/custom-response/). PR [#177](https://github.com/tiangolo/fastapi/pull/177).

* Upgrade HTTP Basic Auth handling with automatic headers (automatic browser login prompt). PR [#175](https://github.com/tiangolo/fastapi/pull/175).

* Update dependencies for security. PR [#174](https://github.com/tiangolo/fastapi/pull/174).

* Add docs for [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). PR [#173](https://github.com/tiangolo/fastapi/pull/173).

## 0.17.0

* Make Flit publish from CI. PR [#170](https://github.com/tiangolo/fastapi/pull/170).

* Add documentation about handling [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/). PR [#169](https://github.com/tiangolo/fastapi/pull/169).

* By default, encode by alias. This allows using Pydantic `alias` parameters working by default. PR [#168](https://github.com/tiangolo/fastapi/pull/168).

## 0.16.0

* Upgrade *path operation* `docstring` parsing to support proper Markdown descriptions. New documentation at [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#description-from-docstring). PR [#163](https://github.com/tiangolo/fastapi/pull/163).

* Refactor internal usage of Pydantic to use correct data types. PR [#164](https://github.com/tiangolo/fastapi/pull/164).

* Upgrade Pydantic to version `0.23`. PR [#160](https://github.com/tiangolo/fastapi/pull/160) by [@euri10](https://github.com/euri10).

* Fix typo in Tutorial about Extra Models. PR [#159](https://github.com/tiangolo/fastapi/pull/159) by [@danielmichaels](https://github.com/danielmichaels).

* Fix [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) URL examples in docs. PR [#157](https://github.com/tiangolo/fastapi/pull/157) by [@hayata-yamamoto](https://github.com/hayata-yamamoto).

## 0.15.0

* Add support for multiple file uploads (as a single form field). New docs at: [Multiple file uploads](https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads). PR [#158](https://github.com/tiangolo/fastapi/pull/158).

* Add docs for: [Additional Status Codes](https://fastapi.tiangolo.com/advanced/additional-status-codes/). PR [#156](https://github.com/tiangolo/fastapi/pull/156).

## 0.14.0

* Improve automatically generated names of *path operations* in OpenAPI (in API docs). A function `read_items` instead of having a generated name "Read Items Get" will have "Read Items". PR [#155](https://github.com/tiangolo/fastapi/pull/155).

* Add docs for: [Testing **FastAPI**](https://fastapi.tiangolo.com/tutorial/testing/). PR [#151](https://github.com/tiangolo/fastapi/pull/151).

* Update `/docs` Swagger UI to enable deep linking. This allows sharing the URL pointing directly to the *path operation* documentation in the docs. PR [#148](https://github.com/tiangolo/fastapi/pull/148) by [@wshayes](https://github.com/wshayes).

* Update development dependencies, `Pipfile.lock`. PR [#150](https://github.com/tiangolo/fastapi/pull/150).

* Include Falcon and Hug in: [Alternatives, Inspiration and Comparisons](https://fastapi.tiangolo.com/alternatives/).

## 0.13.0

* Improve/upgrade OAuth2 scopes support with `SecurityScopes`:
    * `SecurityScopes` can be declared as a parameter like `Request`, to get the scopes of all super-dependencies/dependants.
    * Improve `Security` handling, merging scopes when declaring `SecurityScopes`.
    * Allow using `SecurityBase` (like `OAuth2`) classes with `Depends` and still document them. `Security` now is needed only to declare `scopes`.
    * Updated docs about: [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
    * New docs about: [OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).
    * PR [#141](https://github.com/tiangolo/fastapi/pull/141).

## 0.12.1

* Fix bug: handling additional `responses` in `APIRouter.include_router()`. PR [#140](https://github.com/tiangolo/fastapi/pull/140).

* Fix typo in SQL tutorial. PR [#138](https://github.com/tiangolo/fastapi/pull/138) by [@mostaphaRoudsari](https://github.com/mostaphaRoudsari).

* Fix typos in section about nested models and OAuth2 with JWT. PR [#127](https://github.com/tiangolo/fastapi/pull/127) by [@mmcloud](https://github.com/mmcloud).

## 0.12.0

* Add additional `responses` parameter to *path operation decorators* to extend responses in OpenAPI (and API docs).
    * It also allows extending existing responses generated from `response_model`, declare other media types (like images), etc.
    * The new documentation is here: [Additional Responses](https://fastapi.tiangolo.com/advanced/additional-responses/).
    * `responses` can also be added to `.include_router()`, the updated docs are here: [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#add-some-custom-tags-and-responses).
    * PR [#97](https://github.com/tiangolo/fastapi/pull/97) originally initiated by [@barsi](https://github.com/barsi).
* Update `scripts/test-cov-html.sh` to allow passing extra parameters like `-vv`, for development.

## 0.11.0

* Add `auto_error` parameter to security utility functions. Allowing them to be optional. Also allowing to have multiple alternative security schemes that are then checked in a single dependency instead of each one verifying and returning the error to the client automatically when not satisfied. PR [#134](https://github.com/tiangolo/fastapi/pull/134).

* Update [SQL Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-middleware-to-handle-sessions) to close database sessions even when there are exceptions. PR [#89](https://github.com/tiangolo/fastapi/pull/89) by [@alexiri](https://github.com/alexiri).

* Fix duplicate dependency in `pyproject.toml`. PR [#128](https://github.com/tiangolo/fastapi/pull/128) by [@zxalif](https://github.com/zxalif).

## 0.10.3

* Add Gitter chat, badge, links, etc. [https://gitter.im/tiangolo/fastapi](https://gitter.im/tiangolo/fastapi) . PR [#117](https://github.com/tiangolo/fastapi/pull/117).

* Add docs about [Extending OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/). PR [#126](https://github.com/tiangolo/fastapi/pull/126).

* Make Travis run Ubuntu Xenial (newer version) and Python 3.7 instead of Python 3.7-dev. PR [#92](https://github.com/tiangolo/fastapi/pull/92) by [@blueyed](https://github.com/blueyed).

* Fix duplicated param variable creation. PR [#123](https://github.com/tiangolo/fastapi/pull/123) by [@yihuang](https://github.com/yihuang).

* Add note in [Response Model docs](https://fastapi.tiangolo.com/tutorial/response-model/) about why using a function parameter instead of a function return type annotation. PR [#109](https://github.com/tiangolo/fastapi/pull/109) by [@JHSaunders](https://github.com/JHSaunders).

* Fix event docs (startup/shutdown) function name. PR [#105](https://github.com/tiangolo/fastapi/pull/105) by [@stratosgear](https://github.com/stratosgear).

## 0.10.2

* Fix OpenAPI (JSON Schema) for declarations of Python `Union` (JSON Schema `additionalProperties`). PR [#121](https://github.com/tiangolo/fastapi/pull/121).

* Update [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) with a note on Celery.

* Document response models using unions and lists, updated at: [Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/). PR [#108](https://github.com/tiangolo/fastapi/pull/108).

## 0.10.1

* Add docs and tests for [encode/databases](https://github.com/encode/databases). New docs at: [Async SQL (Relational) Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/). PR [#107](https://github.com/tiangolo/fastapi/pull/107).

## 0.10.0

* Add support for Background Tasks in *path operation functions* and dependencies. New documentation about [Background Tasks is here](https://fastapi.tiangolo.com/tutorial/background-tasks/). PR [#103](https://github.com/tiangolo/fastapi/pull/103).

* Add support for `.websocket_route()` in `APIRouter`. PR [#100](https://github.com/tiangolo/fastapi/pull/100) by [@euri10](https://github.com/euri10).

* New docs section about [Events: startup - shutdown](https://fastapi.tiangolo.com/advanced/events/). PR [#99](https://github.com/tiangolo/fastapi/pull/99).

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

* Add docs for using [WebSockets with **FastAPI**](https://fastapi.tiangolo.com/advanced/websockets/). PR [#62](https://github.com/tiangolo/fastapi/pull/62).

## 0.6.3

* Add Favicons to docs. PR [#53](https://github.com/tiangolo/fastapi/pull/53).

## 0.6.2

* Introduce new project generator based on FastAPI and PostgreSQL: [https://github.com/tiangolo/full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Update [SQL tutorial with SQLAlchemy, using `Depends` to improve editor support and reduce code repetition](https://fastapi.tiangolo.com/tutorial/sql-databases/). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Improve middleware naming in tutorial for SQL with SQLAlchemy [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/).

## 0.6.1

* Add docs for GraphQL: [https://fastapi.tiangolo.com/advanced/graphql/](https://fastapi.tiangolo.com/advanced/graphql/). PR [#48](https://github.com/tiangolo/fastapi/pull/48).

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

* Add [documentation to use Starlette `Request` object](https://fastapi.tiangolo.com/advanced/using-request-directly/) directly. Check [#25](https://github.com/tiangolo/fastapi/pull/25) by [@euri10](https://github.com/euri10).

* Add issue templates to simplify reporting bugs, getting help, etc: [#34](https://github.com/tiangolo/fastapi/pull/34).

* Update example for the SQLAlchemy tutorial at [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/) using middleware and database session attached to request.

## 0.4.0

* Add `openapi_prefix`, support for reverse proxy and mounting sub-applications. See the docs at [https://fastapi.tiangolo.com/advanced/sub-applications-proxy/](https://fastapi.tiangolo.com/advanced/sub-applications-proxy/): [#26](https://github.com/tiangolo/fastapi/pull/26) by [@kabirkhan](https://github.com/kabirkhan).

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
