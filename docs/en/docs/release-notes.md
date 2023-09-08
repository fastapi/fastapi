# Release Notes

## Latest Changes


## 0.103.1

### Fixes

* 📌 Pin AnyIO to < 4.0.0 to handle an incompatibility while upgrading to Starlette 0.31.1. PR [#10194](https://github.com/tiangolo/fastapi/pull/10194) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix validation parameter name in docs, from `regex` to `pattern`. PR [#10085](https://github.com/tiangolo/fastapi/pull/10085) by [@pablodorrio](https://github.com/pablodorrio).
* ✏️ Fix indent format in `docs/en/docs/deployment/server-workers.md`. PR [#10066](https://github.com/tiangolo/fastapi/pull/10066) by [@tamtam-fitness](https://github.com/tamtam-fitness).
* ✏️ Fix Pydantic examples in tutorial for Python types. PR [#9961](https://github.com/tiangolo/fastapi/pull/9961) by [@rahulsalgare](https://github.com/rahulsalgare).
* ✏️ Fix link to Pydantic docs in `docs/en/docs/tutorial/extra-data-types.md`. PR [#10155](https://github.com/tiangolo/fastapi/pull/10155) by [@hasnatsajid](https://github.com/hasnatsajid).
* ✏️ Fix typo in `docs/en/docs/tutorial/handling-errors.md`. PR [#10170](https://github.com/tiangolo/fastapi/pull/10170) by [@poupapaa](https://github.com/poupapaa).
* ✏️ Fix typo in `docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#10172](https://github.com/tiangolo/fastapi/pull/10172) by [@ragul-kachiappan](https://github.com/ragul-kachiappan).

### Translations

* 🌐 Remove duplicate line in translation for `docs/pt/docs/tutorial/path-params.md`. PR [#10126](https://github.com/tiangolo/fastapi/pull/10126) by [@LecoOliveira](https://github.com/LecoOliveira).
* 🌐 Add Yoruba translation for `docs/yo/docs/index.md`. PR [#10033](https://github.com/tiangolo/fastapi/pull/10033) by [@AfolabiOlaoluwa](https://github.com/AfolabiOlaoluwa).
* 🌐 Add Ukrainian translation for `docs/uk/docs/python-types.md`. PR [#10080](https://github.com/tiangolo/fastapi/pull/10080) by [@rostik1410](https://github.com/rostik1410).
* 🌐 Add Vietnamese translations for `docs/vi/docs/tutorial/first-steps.md` and `docs/vi/docs/tutorial/index.md`. PR [#10088](https://github.com/tiangolo/fastapi/pull/10088) by [@magiskboy](https://github.com/magiskboy).
* 🌐 Add Ukrainian translation for `docs/uk/docs/alternatives.md`. PR [#10060](https://github.com/tiangolo/fastapi/pull/10060) by [@whysage](https://github.com/whysage).
* 🌐 Add Ukrainian translation for `docs/uk/docs/tutorial/index.md`. PR [#10079](https://github.com/tiangolo/fastapi/pull/10079) by [@rostik1410](https://github.com/rostik1410).
* ✏️ Fix typos in `docs/en/docs/how-to/separate-openapi-schemas.md` and `docs/en/docs/tutorial/schema-extra-example.md`. PR [#10189](https://github.com/tiangolo/fastapi/pull/10189) by [@xzmeng](https://github.com/xzmeng).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/generate-clients.md`. PR [#9883](https://github.com/tiangolo/fastapi/pull/9883) by [@funny-cat-happy](https://github.com/funny-cat-happy).

### Refactors

* ✏️ Fix typos in comment in `fastapi/applications.py`. PR [#10045](https://github.com/tiangolo/fastapi/pull/10045) by [@AhsanSheraz](https://github.com/AhsanSheraz).
* ✅ Add missing test for OpenAPI examples, it was missing in coverage. PR [#10188](https://github.com/tiangolo/fastapi/pull/10188) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 👥 Update FastAPI People. PR [#10186](https://github.com/tiangolo/fastapi/pull/10186) by [@tiangolo](https://github.com/tiangolo).

## 0.103.0

### Features

* ✨ Add support for `openapi_examples` in all FastAPI parameters. PR [#10152](https://github.com/tiangolo/fastapi/pull/10152) by [@tiangolo](https://github.com/tiangolo).
    * New docs: [OpenAPI-specific examples](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#openapi-specific-examples).

### Docs

* 📝 Add note to docs about Separate Input and Output Schemas with FastAPI version. PR [#10150](https://github.com/tiangolo/fastapi/pull/10150) by [@tiangolo](https://github.com/tiangolo).

## 0.102.0

### Features

* ✨ Add support for disabling the separation of input and output JSON Schemas in OpenAPI with Pydantic v2 with `separate_input_output_schemas=False`. PR [#10145](https://github.com/tiangolo/fastapi/pull/10145) by [@tiangolo](https://github.com/tiangolo).
    * New docs [Separate OpenAPI Schemas for Input and Output or Not](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas/).
    * This PR also includes a new setup (internal tools) for generating screenshots for the docs.

### Refactors

* ♻️ Refactor tests for new Pydantic 2.2.1. PR [#10115](https://github.com/tiangolo/fastapi/pull/10115) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Add new docs section, How To - Recipes, move docs that don't have to be read by everyone to How To. PR [#10114](https://github.com/tiangolo/fastapi/pull/10114) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update Advanced docs, add links to sponsor courses. PR [#10113](https://github.com/tiangolo/fastapi/pull/10113) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for generating clients. PR [#10112](https://github.com/tiangolo/fastapi/pull/10112) by [@tiangolo](https://github.com/tiangolo).
* 📝 Tweak MkDocs and add redirects. PR [#10111](https://github.com/tiangolo/fastapi/pull/10111) by [@tiangolo](https://github.com/tiangolo).
* 📝 Restructure docs for cloud providers, include links to sponsors. PR [#10110](https://github.com/tiangolo/fastapi/pull/10110) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Update sponsors, add Speakeasy. PR [#10098](https://github.com/tiangolo/fastapi/pull/10098) by [@tiangolo](https://github.com/tiangolo).

## 0.101.1

### Fixes

* ✨ Add `ResponseValidationError` printable details, to show up in server error logs. PR [#10078](https://github.com/tiangolo/fastapi/pull/10078) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* ✏️ Fix typo in deprecation warnings in `fastapi/params.py`. PR [#9854](https://github.com/tiangolo/fastapi/pull/9854) by [@russbiggs](https://github.com/russbiggs).
* ✏️ Fix typos in comments on internal code in `fastapi/concurrency.py` and `fastapi/routing.py`. PR [#9590](https://github.com/tiangolo/fastapi/pull/9590) by [@ElliottLarsen](https://github.com/ElliottLarsen).

### Docs

* ✏️ Fix typo in release notes. PR [#9835](https://github.com/tiangolo/fastapi/pull/9835) by [@francisbergin](https://github.com/francisbergin).
* 📝 Add external article: Build an SMS Spam Classifier Serverless Database with FaunaDB and FastAPI. PR [#9847](https://github.com/tiangolo/fastapi/pull/9847) by [@adejumoridwan](https://github.com/adejumoridwan).
* 📝 Fix typo in `docs/en/docs/contributing.md`. PR [#9878](https://github.com/tiangolo/fastapi/pull/9878) by [@VicenteMerino](https://github.com/VicenteMerino).
* 📝 Fix code highlighting in `docs/en/docs/tutorial/bigger-applications.md`. PR [#9806](https://github.com/tiangolo/fastapi/pull/9806) by [@theonlykingpin](https://github.com/theonlykingpin).

### Translations

* 🌐 Add Japanese translation for `docs/ja/docs/deployment/concepts.md`. PR [#10062](https://github.com/tiangolo/fastapi/pull/10062) by [@tamtam-fitness](https://github.com/tamtam-fitness).
* 🌐 Add Japanese translation for `docs/ja/docs/deployment/server-workers.md`. PR [#10064](https://github.com/tiangolo/fastapi/pull/10064) by [@tamtam-fitness](https://github.com/tamtam-fitness).
* 🌐 Update Japanese translation for `docs/ja/docs/deployment/docker.md`. PR [#10073](https://github.com/tiangolo/fastapi/pull/10073) by [@tamtam-fitness](https://github.com/tamtam-fitness).
* 🌐 Add Ukrainian translation for `docs/uk/docs/fastapi-people.md`. PR [#10059](https://github.com/tiangolo/fastapi/pull/10059) by [@rostik1410](https://github.com/rostik1410).
* 🌐 Add Ukrainian translation for `docs/uk/docs/tutorial/cookie-params.md`. PR [#10032](https://github.com/tiangolo/fastapi/pull/10032) by [@rostik1410](https://github.com/rostik1410).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/docker.md`. PR [#9971](https://github.com/tiangolo/fastapi/pull/9971) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Vietnamese translation for `docs/vi/docs/python-types.md`. PR [#10047](https://github.com/tiangolo/fastapi/pull/10047) by [@magiskboy](https://github.com/magiskboy).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/dependencies/global-dependencies.md`. PR [#9970](https://github.com/tiangolo/fastapi/pull/9970) by [@dudyaosuplayer](https://github.com/dudyaosuplayer).
* 🌐 Add Urdu translation for `docs/ur/docs/benchmarks.md`. PR [#9974](https://github.com/tiangolo/fastapi/pull/9974) by [@AhsanSheraz](https://github.com/AhsanSheraz).

### Internal

* 🔧 Add sponsor Porter. PR [#10051](https://github.com/tiangolo/fastapi/pull/10051) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add Jina back as bronze sponsor. PR [#10050](https://github.com/tiangolo/fastapi/pull/10050) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump mypy from 1.4.0 to 1.4.1. PR [#9756](https://github.com/tiangolo/fastapi/pull/9756) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mkdocs-material from 9.1.17 to 9.1.21. PR [#9960](https://github.com/tiangolo/fastapi/pull/9960) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.101.0

### Features

* ✨ Enable Pydantic's serialization mode for responses, add support for Pydantic's `computed_field`, better OpenAPI for response models, proper required attributes, better generated clients. PR [#10011](https://github.com/tiangolo/fastapi/pull/10011) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* ✅ Fix tests for compatibility with pydantic 2.1.1. PR [#9943](https://github.com/tiangolo/fastapi/pull/9943) by [@dmontagu](https://github.com/dmontagu).
* ✅ Fix test error in Windows for `jsonable_encoder`. PR [#9840](https://github.com/tiangolo/fastapi/pull/9840) by [@iudeen](https://github.com/iudeen).

### Upgrades

* 📌 Do not allow Pydantic 2.1.0 that breaks (require 2.1.1). PR [#10012](https://github.com/tiangolo/fastapi/pull/10012) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/security/index.md`. PR [#9963](https://github.com/tiangolo/fastapi/pull/9963) by [@eVery1337](https://github.com/eVery1337).
* 🌐 Remove Vietnamese note about missing translation. PR [#9957](https://github.com/tiangolo/fastapi/pull/9957) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 👷 Add GitHub Actions step dump context to debug external failures. PR [#10008](https://github.com/tiangolo/fastapi/pull/10008) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Restore MkDocs Material pin after the fix. PR [#10001](https://github.com/tiangolo/fastapi/pull/10001) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update the Question template to ask for the Pydantic version. PR [#10000](https://github.com/tiangolo/fastapi/pull/10000) by [@tiangolo](https://github.com/tiangolo).
* 📍 Update MkDocs Material dependencies. PR [#9986](https://github.com/tiangolo/fastapi/pull/9986) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#9999](https://github.com/tiangolo/fastapi/pull/9999) by [@tiangolo](https://github.com/tiangolo).
* 🐳 Update Dockerfile with compatibility versions, to upgrade later. PR [#9998](https://github.com/tiangolo/fastapi/pull/9998) by [@tiangolo](https://github.com/tiangolo).
* ➕ Add pydantic-settings to FastAPI People dependencies. PR [#9988](https://github.com/tiangolo/fastapi/pull/9988) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Update FastAPI People logic with new Pydantic. PR [#9985](https://github.com/tiangolo/fastapi/pull/9985) by [@tiangolo](https://github.com/tiangolo).
* 🍱 Update sponsors, Fern badge. PR [#9982](https://github.com/tiangolo/fastapi/pull/9982) by [@tiangolo](https://github.com/tiangolo).
* 👷 Deploy docs to Cloudflare Pages. PR [#9978](https://github.com/tiangolo/fastapi/pull/9978) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsor Fern. PR [#9979](https://github.com/tiangolo/fastapi/pull/9979) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update CI debug mode with Tmate. PR [#9977](https://github.com/tiangolo/fastapi/pull/9977) by [@tiangolo](https://github.com/tiangolo).

## 0.100.1

### Fixes

* 🐛 Replace `MultHostUrl` to `AnyUrl` for compatibility with older versions of Pydantic v1. PR [#9852](https://github.com/tiangolo/fastapi/pull/9852) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Update links for self-hosted Swagger UI, point to v5, for OpenAPI 31.0. PR [#9834](https://github.com/tiangolo/fastapi/pull/9834) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Ukrainian translation for `docs/uk/docs/tutorial/body.md`. PR [#4574](https://github.com/tiangolo/fastapi/pull/4574) by [@ss-o-furda](https://github.com/ss-o-furda).
* 🌐 Add Vietnamese translation for `docs/vi/docs/features.md` and `docs/vi/docs/index.md`. PR [#3006](https://github.com/tiangolo/fastapi/pull/3006) by [@magiskboy](https://github.com/magiskboy).
* 🌐 Add Korean translation for `docs/ko/docs/async.md`. PR [#4179](https://github.com/tiangolo/fastapi/pull/4179) by [@NinaHwang](https://github.com/NinaHwang).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/background-tasks.md`. PR [#9812](https://github.com/tiangolo/fastapi/pull/9812) by [@wdh99](https://github.com/wdh99).
* 🌐 Add French translation for `docs/fr/docs/tutorial/query-params-str-validations.md`. PR [#4075](https://github.com/tiangolo/fastapi/pull/4075) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for `docs/fr/docs/tutorial/index.md`. PR [#2234](https://github.com/tiangolo/fastapi/pull/2234) by [@JulianMaurin](https://github.com/JulianMaurin).
* 🌐 Add French translation for `docs/fr/docs/contributing.md`. PR [#2132](https://github.com/tiangolo/fastapi/pull/2132) by [@JulianMaurin](https://github.com/JulianMaurin).
* 🌐 Add French translation for `docs/fr/docs/benchmarks.md`. PR [#2155](https://github.com/tiangolo/fastapi/pull/2155) by [@clemsau](https://github.com/clemsau).
* 🌐 Update Chinese translations with new source files. PR [#9738](https://github.com/tiangolo/fastapi/pull/9738) by [@mahone3297](https://github.com/mahone3297).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/request-forms.md`. PR [#9841](https://github.com/tiangolo/fastapi/pull/9841) by [@dedkot01](https://github.com/dedkot01).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/handling-errors.md`. PR [#9485](https://github.com/tiangolo/fastapi/pull/9485) by [@Creat55](https://github.com/Creat55).

### Internal

* 🔧 Update sponsors, add Fern. PR [#9956](https://github.com/tiangolo/fastapi/pull/9956) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update FastAPI People token. PR [#9844](https://github.com/tiangolo/fastapi/pull/9844) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#9775](https://github.com/tiangolo/fastapi/pull/9775) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update MkDocs Material token. PR [#9843](https://github.com/tiangolo/fastapi/pull/9843) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update token for latest changes. PR [#9842](https://github.com/tiangolo/fastapi/pull/9842) by [@tiangolo](https://github.com/tiangolo).

## 0.100.0

✨ Support for **Pydantic v2** ✨

Pydantic version 2 has the **core** re-written in **Rust** and includes a lot of improvements and features, for example:

* Improved **correctness** in corner cases.
* **Safer** types.
* Better **performance** and **less energy** consumption.
* Better **extensibility**.
* etc.

...all this while keeping the **same Python API**. In most of the cases, for simple models, you can simply upgrade the Pydantic version and get all the benefits. 🚀

In some cases, for pure data validation and processing, you can get performance improvements of **20x** or more. This means 2,000% or more. 🤯

When you use **FastAPI**, there's a lot more going on, processing the request and response, handling dependencies, executing **your own code**, and particularly, **waiting for the network**. But you will probably still get some nice performance improvements just from the upgrade.

The focus of this release is **compatibility** with Pydantic v1 and v2, to make sure your current apps keep working. Later there will be more focus on refactors, correctness, code improvements, and then **performance** improvements. Some third-party early beta testers that ran benchmarks on the beta releases of FastAPI reported improvements of **2x - 3x**. Which is not bad for just doing `pip install --upgrade fastapi pydantic`. This was not an official benchmark and I didn't check it myself, but it's a good sign.

### Migration

Check out the [Pydantic migration guide](https://docs.pydantic.dev/2.0/migration/).

For the things that need changes in your Pydantic models, the Pydantic team built [`bump-pydantic`](https://github.com/pydantic/bump-pydantic).

A command line tool that will **process your code** and update most of the things **automatically** for you. Make sure you have your code in git first, and review each of the changes to make sure everything is correct before committing the changes.

### Pydantic v1

**This version of FastAPI still supports Pydantic v1**. And although Pydantic v1 will be deprecated at some point, it will still be supported for a while.

This means that you can install the new Pydantic v2, and if something fails, you can install Pydantic v1 while you fix any problems you might have, but having the latest FastAPI.

There are **tests for both Pydantic v1 and v2**, and test **coverage** is kept at **100%**.

### Changes

* There are **new parameter** fields supported by Pydantic `Field()` for:

    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
    * `Body()`
    * `Form()`
    * `File()`

* The new parameter fields are:

    * `default_factory`
    * `alias_priority`
    * `validation_alias`
    * `serialization_alias`
    * `discriminator`
    * `strict`
    * `multiple_of`
    * `allow_inf_nan`
    * `max_digits`
    * `decimal_places`
    * `json_schema_extra`

...you can read about them in the Pydantic docs.

* The parameter `regex` has been deprecated and replaced by `pattern`.
    * You can read more about it in the docs for [Query Parameters and String Validations: Add regular expressions](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#add-regular-expressions).
* New Pydantic models use an improved and simplified attribute `model_config` that takes a simple dict instead of an internal class `Config` for their configuration.
    * You can read more about it in the docs for [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/).
* The attribute `schema_extra` for the internal class `Config` has been replaced by the key `json_schema_extra` in the new `model_config` dict.
    * You can read more about it in the docs for [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/).
* When you install `"fastapi[all]"` it now also includes:
    * <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - for settings management.
    * <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - for extra types to be used with Pydantic.
* Now Pydantic Settings is an additional optional package (included in `"fastapi[all]"`). To use settings you should now import `from pydantic_settings import BaseSettings` instead of importing from `pydantic` directly.
    * You can read more about it in the docs for [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/).

* PR [#9816](https://github.com/tiangolo/fastapi/pull/9816) by [@tiangolo](https://github.com/tiangolo), included all the work done (in multiple PRs) on the beta branch (`main-pv2`).

## 0.99.1

### Fixes

* 🐛 Fix JSON Schema accepting bools as valid JSON Schemas, e.g. `additionalProperties: false`. PR [#9781](https://github.com/tiangolo/fastapi/pull/9781) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update source examples to use new JSON Schema examples field. PR [#9776](https://github.com/tiangolo/fastapi/pull/9776) by [@tiangolo](https://github.com/tiangolo).

## 0.99.0

### Features

* ✨ Add support for OpenAPI 3.1.0. PR [#9770](https://github.com/tiangolo/fastapi/pull/9770) by [@tiangolo](https://github.com/tiangolo).
    * New support for documenting **webhooks**, read the new docs here: <a href="https://fastapi.tiangolo.com/advanced/openapi-webhooks/" class="external-link" target="_blank">Advanced User Guide: OpenAPI Webhooks</a>.
    * Upgrade OpenAPI 3.1.0, this uses JSON Schema 2020-12.
    * Upgrade Swagger UI to version 5.x.x, that supports OpenAPI 3.1.0.
    * Updated `examples` field in `Query()`, `Cookie()`, `Body()`, etc. based on the latest JSON Schema and OpenAPI. Now it takes a list of examples and they are included directly in the JSON Schema, not outside. Read more about it (including the historical technical details) in the updated docs: <a href="https://fastapi.tiangolo.com/tutorial/schema-extra-example/" class="external-link" target="_blank">Tutorial: Declare Request Example Data</a>.

* ✨ Add support for `deque` objects and children in `jsonable_encoder`. PR [#9433](https://github.com/tiangolo/fastapi/pull/9433) by [@cranium](https://github.com/cranium).

### Docs

* 📝 Fix form for the FastAPI and friends newsletter. PR [#9749](https://github.com/tiangolo/fastapi/pull/9749) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Persian translation for `docs/fa/docs/advanced/sub-applications.md`. PR [#9692](https://github.com/tiangolo/fastapi/pull/9692) by [@mojtabapaso](https://github.com/mojtabapaso).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/response-model.md`. PR [#9675](https://github.com/tiangolo/fastapi/pull/9675) by [@glsglsgls](https://github.com/glsglsgls).

### Internal

* 🔨 Enable linenums in MkDocs Material during local live development to simplify highlighting code. PR [#9769](https://github.com/tiangolo/fastapi/pull/9769) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Update httpx requirement from <0.24.0,>=0.23.0 to >=0.23.0,<0.25.0. PR [#9724](https://github.com/tiangolo/fastapi/pull/9724) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mkdocs-material from 9.1.16 to 9.1.17. PR [#9746](https://github.com/tiangolo/fastapi/pull/9746) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Remove missing translation dummy pages, no longer necessary. PR [#9751](https://github.com/tiangolo/fastapi/pull/9751) by [@tiangolo](https://github.com/tiangolo).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#9259](https://github.com/tiangolo/fastapi/pull/9259) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ✨ Add Material for MkDocs Insiders features and cards. PR [#9748](https://github.com/tiangolo/fastapi/pull/9748) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove languages without translations. PR [#9743](https://github.com/tiangolo/fastapi/pull/9743) by [@tiangolo](https://github.com/tiangolo).
* ✨ Refactor docs for building scripts, use MkDocs hooks, simplify (remove) configs for languages. PR [#9742](https://github.com/tiangolo/fastapi/pull/9742) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Add MkDocs hook that renames sections based on the first index file. PR [#9737](https://github.com/tiangolo/fastapi/pull/9737) by [@tiangolo](https://github.com/tiangolo).
* 👷 Make cron jobs run only on main repo, not on forks, to avoid error notifications from missing tokens. PR [#9735](https://github.com/tiangolo/fastapi/pull/9735) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update MkDocs for other languages. PR [#9734](https://github.com/tiangolo/fastapi/pull/9734) by [@tiangolo](https://github.com/tiangolo).
* 👷 Refactor Docs CI, run in multiple workers with a dynamic matrix to optimize speed. PR [#9732](https://github.com/tiangolo/fastapi/pull/9732) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove old internal GitHub Action watch-previews that is no longer needed. PR [#9730](https://github.com/tiangolo/fastapi/pull/9730) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade MkDocs and MkDocs Material. PR [#9729](https://github.com/tiangolo/fastapi/pull/9729) by [@tiangolo](https://github.com/tiangolo).
* 👷 Build and deploy docs only on docs changes. PR [#9728](https://github.com/tiangolo/fastapi/pull/9728) by [@tiangolo](https://github.com/tiangolo).

## 0.98.0

### Features

* ✨ Allow disabling `redirect_slashes` at the FastAPI app level. PR [#3432](https://github.com/tiangolo/fastapi/pull/3432) by [@cyberlis](https://github.com/cyberlis).

### Docs

* 📝 Update docs on Pydantic using ujson internally. PR [#5804](https://github.com/tiangolo/fastapi/pull/5804) by [@mvasilkov](https://github.com/mvasilkov).
* ✏ Rewording in `docs/en/docs/tutorial/debugging.md`. PR [#9581](https://github.com/tiangolo/fastapi/pull/9581) by [@ivan-abc](https://github.com/ivan-abc).
* 📝 Add german blog post (Domain-driven Design mit Python und FastAPI). PR [#9261](https://github.com/tiangolo/fastapi/pull/9261) by [@msander](https://github.com/msander).
* ✏️ Tweak wording in `docs/en/docs/tutorial/security/index.md`. PR [#9561](https://github.com/tiangolo/fastapi/pull/9561) by [@jyothish-mohan](https://github.com/jyothish-mohan).
* 📝 Update `Annotated` notes in `docs/en/docs/tutorial/schema-extra-example.md`. PR [#9620](https://github.com/tiangolo/fastapi/pull/9620) by [@Alexandrhub](https://github.com/Alexandrhub).
* ✏️ Fix typo `Annotation` -> `Annotated` in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9625](https://github.com/tiangolo/fastapi/pull/9625) by [@mccricardo](https://github.com/mccricardo).
* 📝 Use in memory database for testing SQL in docs. PR [#1223](https://github.com/tiangolo/fastapi/pull/1223) by [@HarshaLaxman](https://github.com/HarshaLaxman).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/metadata.md`. PR [#9681](https://github.com/tiangolo/fastapi/pull/9681) by [@TabarakoAkula](https://github.com/TabarakoAkula).
* 🌐 Fix typo in Spanish translation for `docs/es/docs/tutorial/first-steps.md`. PR [#9571](https://github.com/tiangolo/fastapi/pull/9571) by [@lilidl-nft](https://github.com/lilidl-nft).
* 🌐 Add Russian translation for `docs/tutorial/path-operation-configuration.md`. PR [#9696](https://github.com/tiangolo/fastapi/pull/9696) by [@TabarakoAkula](https://github.com/TabarakoAkula).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/security/index.md`. PR [#9666](https://github.com/tiangolo/fastapi/pull/9666) by [@lordqyxz](https://github.com/lordqyxz).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/settings.md`. PR [#9652](https://github.com/tiangolo/fastapi/pull/9652) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/websockets.md`. PR [#9651](https://github.com/tiangolo/fastapi/pull/9651) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/testing.md`. PR [#9641](https://github.com/tiangolo/fastapi/pull/9641) by [@wdh99](https://github.com/wdh99).
* 🌐 Add Russian translation for `docs/tutorial/extra-models.md`. PR [#9619](https://github.com/tiangolo/fastapi/pull/9619) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Russian translation for `docs/tutorial/cors.md`. PR [#9608](https://github.com/tiangolo/fastapi/pull/9608) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Polish translation for `docs/pl/docs/features.md`. PR [#5348](https://github.com/tiangolo/fastapi/pull/5348) by [@mbroton](https://github.com/mbroton).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-nested-models.md`. PR [#9605](https://github.com/tiangolo/fastapi/pull/9605) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* ⬆ Bump ruff from 0.0.272 to 0.0.275. PR [#9721](https://github.com/tiangolo/fastapi/pull/9721) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update uvicorn[standard] requirement from <0.21.0,>=0.12.0 to >=0.12.0,<0.23.0. PR [#9463](https://github.com/tiangolo/fastapi/pull/9463) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mypy from 1.3.0 to 1.4.0. PR [#9719](https://github.com/tiangolo/fastapi/pull/9719) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update pre-commit requirement from <3.0.0,>=2.17.0 to >=2.17.0,<4.0.0. PR [#9251](https://github.com/tiangolo/fastapi/pull/9251) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.8.5 to 1.8.6. PR [#9482](https://github.com/tiangolo/fastapi/pull/9482) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✏️ Fix tooltips for light/dark theme toggler in docs. PR [#9588](https://github.com/tiangolo/fastapi/pull/9588) by [@pankaj1707k](https://github.com/pankaj1707k).
* 🔧 Set minimal hatchling version needed to build the package. PR [#9240](https://github.com/tiangolo/fastapi/pull/9240) by [@mgorny](https://github.com/mgorny).
* 📝 Add repo link to PyPI. PR [#9559](https://github.com/tiangolo/fastapi/pull/9559) by [@JacobCoffee](https://github.com/JacobCoffee).
* ✏️ Fix typos in data for tests. PR [#4958](https://github.com/tiangolo/fastapi/pull/4958) by [@ryanrussell](https://github.com/ryanrussell).
* 🔧 Update sponsors, add Flint. PR [#9699](https://github.com/tiangolo/fastapi/pull/9699) by [@tiangolo](https://github.com/tiangolo).
* 👷 Lint in CI only once, only with one version of Python, run tests with all of them. PR [#9686](https://github.com/tiangolo/fastapi/pull/9686) by [@tiangolo](https://github.com/tiangolo).

## 0.97.0

### Features

* ✨ Add support for `dependencies` in WebSocket routes. PR [#4534](https://github.com/tiangolo/fastapi/pull/4534) by [@paulo-raca](https://github.com/paulo-raca).
* ✨ Add exception handler for `WebSocketRequestValidationError` (which also allows to override it). PR [#6030](https://github.com/tiangolo/fastapi/pull/6030) by [@kristjanvalur](https://github.com/kristjanvalur).

### Refactors

* ⬆️ Upgrade and fully migrate to Ruff, remove isort, includes a couple of tweaks suggested by the new version of Ruff. PR [#9660](https://github.com/tiangolo/fastapi/pull/9660) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Update internal type annotations and upgrade mypy. PR [#9658](https://github.com/tiangolo/fastapi/pull/9658) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Simplify `AsyncExitStackMiddleware` as without Python 3.6 `AsyncExitStack` is always available. PR [#9657](https://github.com/tiangolo/fastapi/pull/9657) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* ⬆️ Upgrade Black. PR [#9661](https://github.com/tiangolo/fastapi/pull/9661) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 💚 Update CI cache to fix installs when dependencies change. PR [#9659](https://github.com/tiangolo/fastapi/pull/9659) by [@tiangolo](https://github.com/tiangolo).
* ⬇️ Separate requirements for development into their own requirements.txt files, they shouldn't be extras. PR [#9655](https://github.com/tiangolo/fastapi/pull/9655) by [@tiangolo](https://github.com/tiangolo).

## 0.96.1

### Fixes

* 🐛 Fix `HTTPException` header type annotations. PR [#9648](https://github.com/tiangolo/fastapi/pull/9648) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix OpenAPI model fields int validations, `gte` to `ge`. PR [#9635](https://github.com/tiangolo/fastapi/pull/9635) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* 📌 Update minimum version of Pydantic to >=1.7.4. This fixes an issue when trying to use an old version of Pydantic. PR [#9567](https://github.com/tiangolo/fastapi/pull/9567) by [@Kludex](https://github.com/Kludex).

### Refactors

* ♻ Remove `media_type` from `ORJSONResponse` as it's inherited from the parent class. PR [#5805](https://github.com/tiangolo/fastapi/pull/5805) by [@Kludex](https://github.com/Kludex).
* ♻ Instantiate `HTTPException` only when needed, optimization refactor. PR [#5356](https://github.com/tiangolo/fastapi/pull/5356) by [@pawamoy](https://github.com/pawamoy).

### Docs

* 🔥 Remove link to Pydantic's benchmark, as it was removed there. PR [#5811](https://github.com/tiangolo/fastapi/pull/5811) by [@Kludex](https://github.com/Kludex).

### Translations

* 🌐 Fix spelling in Indonesian translation of `docs/id/docs/tutorial/index.md`. PR [#5635](https://github.com/tiangolo/fastapi/pull/5635) by [@purwowd](https://github.com/purwowd).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/index.md`. PR [#5896](https://github.com/tiangolo/fastapi/pull/5896) by [@Wilidon](https://github.com/Wilidon).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/response-change-status-code.md` and `docs/zh/docs/advanced/response-headers.md`. PR [#9544](https://github.com/tiangolo/fastapi/pull/9544) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/schema-extra-example.md`. PR [#9621](https://github.com/tiangolo/fastapi/pull/9621) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* 🔧 Add sponsor Platform.sh. PR [#9650](https://github.com/tiangolo/fastapi/pull/9650) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add custom token to Smokeshow and Preview Docs for download-artifact, to prevent API rate limits. PR [#9646](https://github.com/tiangolo/fastapi/pull/9646) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add custom tokens for GitHub Actions to avoid rate limits. PR [#9647](https://github.com/tiangolo/fastapi/pull/9647) by [@tiangolo](https://github.com/tiangolo).

## 0.96.0

### Features

* ⚡ Update `create_cloned_field` to use a global cache and improve startup performance. PR [#4645](https://github.com/tiangolo/fastapi/pull/4645) by [@madkinsz](https://github.com/madkinsz) and previous original PR by [@huonw](https://github.com/huonw).

### Docs

* 📝 Update Deta deployment tutorial for compatibility with Deta Space. PR [#6004](https://github.com/tiangolo/fastapi/pull/6004) by [@mikBighne98](https://github.com/mikBighne98).
* ✏️ Fix typo in Deta deployment tutorial. PR [#9501](https://github.com/tiangolo/fastapi/pull/9501) by [@lemonyte](https://github.com/lemonyte).

### Translations

* 🌐 Add Russian translation for `docs/tutorial/body.md`. PR [#3885](https://github.com/tiangolo/fastapi/pull/3885) by [@solomein-sv](https://github.com/solomein-sv).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/static-files.md`. PR [#9580](https://github.com/tiangolo/fastapi/pull/9580) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/query-params.md`. PR [#9584](https://github.com/tiangolo/fastapi/pull/9584) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/first-steps.md`. PR [#9471](https://github.com/tiangolo/fastapi/pull/9471) by [@AGolicyn](https://github.com/AGolicyn).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/debugging.md`. PR [#9579](https://github.com/tiangolo/fastapi/pull/9579) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/path-params.md`. PR [#9519](https://github.com/tiangolo/fastapi/pull/9519) by [@AGolicyn](https://github.com/AGolicyn).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/static-files.md`. PR [#9436](https://github.com/tiangolo/fastapi/pull/9436) by [@wdh99](https://github.com/wdh99).
* 🌐 Update Spanish translation including new illustrations in `docs/es/docs/async.md`. PR [#9483](https://github.com/tiangolo/fastapi/pull/9483) by [@andresbermeoq](https://github.com/andresbermeoq).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/path-params-numeric-validations.md`. PR [#9563](https://github.com/tiangolo/fastapi/pull/9563) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/concepts.md`. PR [#9577](https://github.com/tiangolo/fastapi/pull/9577) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-multiple-params.md`. PR [#9586](https://github.com/tiangolo/fastapi/pull/9586) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* 👥 Update FastAPI People. PR [#9602](https://github.com/tiangolo/fastapi/pull/9602) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Update sponsors, remove InvestSuite. PR [#9612](https://github.com/tiangolo/fastapi/pull/9612) by [@tiangolo](https://github.com/tiangolo).

## 0.95.2

* ⬆️ Upgrade Starlette version to `>=0.27.0` for a security release. PR [#9541](https://github.com/tiangolo/fastapi/pull/9541) by [@tiangolo](https://github.com/tiangolo). Details on [Starlette's security advisory](https://github.com/encode/starlette/security/advisories/GHSA-v5gw-mw7f-84px).

### Translations

* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/events.md`. PR [#9326](https://github.com/tiangolo/fastapi/pull/9326) by [@oandersonmagalhaes](https://github.com/oandersonmagalhaes).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/manually.md`. PR [#9417](https://github.com/tiangolo/fastapi/pull/9417) by [@Xewus](https://github.com/Xewus).
* 🌐 Add setup for translations to Lao. PR [#9396](https://github.com/tiangolo/fastapi/pull/9396) by [@TheBrown](https://github.com/TheBrown).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/testing.md`. PR [#9403](https://github.com/tiangolo/fastapi/pull/9403) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/https.md`. PR [#9428](https://github.com/tiangolo/fastapi/pull/9428) by [@Xewus](https://github.com/Xewus).
* ✏ Fix command to install requirements in Windows. PR [#9445](https://github.com/tiangolo/fastapi/pull/9445) by [@MariiaRomanuik](https://github.com/MariiaRomanuik).
* 🌐 Add French translation for `docs/fr/docs/advanced/response-directly.md`. PR [#9415](https://github.com/tiangolo/fastapi/pull/9415) by [@axel584](https://github.com/axel584).
* 🌐 Initiate Czech translation setup. PR [#9288](https://github.com/tiangolo/fastapi/pull/9288) by [@3p1463k](https://github.com/3p1463k).
* ✏ Fix typo in Portuguese docs for `docs/pt/docs/index.md`. PR [#9337](https://github.com/tiangolo/fastapi/pull/9337) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/response-status-code.md`. PR [#9370](https://github.com/tiangolo/fastapi/pull/9370) by [@nadia3373](https://github.com/nadia3373).

### Internal

* 🐛 Fix `flask.escape` warning for internal tests. PR [#9468](https://github.com/tiangolo/fastapi/pull/9468) by [@samuelcolvin](https://github.com/samuelcolvin).
* ✅ Refactor 2 tests, for consistency and simplification. PR [#9504](https://github.com/tiangolo/fastapi/pull/9504) by [@tiangolo](https://github.com/tiangolo).
* ✅ Refactor OpenAPI tests, prepare for Pydantic v2. PR [#9503](https://github.com/tiangolo/fastapi/pull/9503) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump dawidd6/action-download-artifact from 2.26.0 to 2.27.0. PR [#9394](https://github.com/tiangolo/fastapi/pull/9394) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 💚 Disable setup-python pip cache in CI. PR [#9438](https://github.com/tiangolo/fastapi/pull/9438) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.6.4 to 1.8.5. PR [#9346](https://github.com/tiangolo/fastapi/pull/9346) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.95.1

### Fixes

* 🐛 Fix using `Annotated` in routers or path operations decorated multiple times. PR [#9315](https://github.com/tiangolo/fastapi/pull/9315) by [@sharonyogev](https://github.com/sharonyogev).

### Docs

* 🌐 🔠 📄 🐢 Translate docs to Emoji 🥳 🎉 💥 🤯 🤯. PR [#5385](https://github.com/tiangolo/fastapi/pull/5385) by [@LeeeeT](https://github.com/LeeeeT).
* 📝 Add notification message warning about old versions of FastAPI not supporting `Annotated`. PR [#9298](https://github.com/tiangolo/fastapi/pull/9298) by [@grdworkin](https://github.com/grdworkin).
* 📝 Fix typo in `docs/en/docs/advanced/behind-a-proxy.md`. PR [#5681](https://github.com/tiangolo/fastapi/pull/5681) by [@Leommjr](https://github.com/Leommjr).
* ✏ Fix wrong import from typing module in Persian translations for `docs/fa/docs/index.md`. PR [#6083](https://github.com/tiangolo/fastapi/pull/6083) by [@Kimiaattaei](https://github.com/Kimiaattaei).
* ✏️ Fix format, remove unnecessary asterisks in `docs/en/docs/help-fastapi.md`. PR [#9249](https://github.com/tiangolo/fastapi/pull/9249) by [@armgabrielyan](https://github.com/armgabrielyan).
* ✏ Fix typo in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9272](https://github.com/tiangolo/fastapi/pull/9272) by [@nicornk](https://github.com/nicornk).
* ✏ Fix typo/bug in inline code example in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9273](https://github.com/tiangolo/fastapi/pull/9273) by [@tim-habitat](https://github.com/tim-habitat).
* ✏ Fix typo in `docs/en/docs/tutorial/path-params-numeric-validations.md`. PR [#9282](https://github.com/tiangolo/fastapi/pull/9282) by [@aadarsh977](https://github.com/aadarsh977).
* ✏ Fix typo: 'wll' to 'will' in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9380](https://github.com/tiangolo/fastapi/pull/9380) by [@dasstyxx](https://github.com/dasstyxx).

### Translations

* 🌐 Add French translation for `docs/fr/docs/advanced/index.md`. PR [#5673](https://github.com/tiangolo/fastapi/pull/5673) by [@axel584](https://github.com/axel584).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/body-nested-models.md`. PR [#4053](https://github.com/tiangolo/fastapi/pull/4053) by [@luccasmmg](https://github.com/luccasmmg).
* 🌐 Add Russian translation for `docs/ru/docs/alternatives.md`. PR [#5994](https://github.com/tiangolo/fastapi/pull/5994) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/extra-models.md`. PR [#5912](https://github.com/tiangolo/fastapi/pull/5912) by [@LorhanSohaky](https://github.com/LorhanSohaky).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/path-operation-configuration.md`. PR [#5936](https://github.com/tiangolo/fastapi/pull/5936) by [@LorhanSohaky](https://github.com/LorhanSohaky).
* 🌐 Add Russian translation for `docs/ru/docs/contributing.md`. PR [#6002](https://github.com/tiangolo/fastapi/pull/6002) by [@stigsanek](https://github.com/stigsanek).
* 🌐 Add Korean translation for `docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#9176](https://github.com/tiangolo/fastapi/pull/9176) by [@sehwan505](https://github.com/sehwan505).
* 🌐 Add Russian translation for `docs/ru/docs/project-generation.md`. PR [#9243](https://github.com/tiangolo/fastapi/pull/9243) by [@Xewus](https://github.com/Xewus).
* 🌐 Add French translation for `docs/fr/docs/index.md`. PR [#9265](https://github.com/tiangolo/fastapi/pull/9265) by [@frabc](https://github.com/frabc).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/query-params-str-validations.md`. PR [#9267](https://github.com/tiangolo/fastapi/pull/9267) by [@dedkot01](https://github.com/dedkot01).
* 🌐 Add Russian translation for `docs/ru/docs/benchmarks.md`. PR [#9271](https://github.com/tiangolo/fastapi/pull/9271) by [@Xewus](https://github.com/Xewus).

### Internal

* 🔧 Update sponsors: remove Jina. PR [#9388](https://github.com/tiangolo/fastapi/pull/9388) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add databento, remove Ines's course and StriveWorks. PR [#9351](https://github.com/tiangolo/fastapi/pull/9351) by [@tiangolo](https://github.com/tiangolo).

## 0.95.0

### Highlights

This release adds support for dependencies and parameters using `Annotated` and recommends its usage. ✨

This has **several benefits**, one of the main ones is that now the parameters of your functions with `Annotated` would **not be affected** at all.

If you call those functions in **other places in your code**, the actual **default values** will be kept, your editor will help you notice missing **required arguments**, Python will require you to pass required arguments at **runtime**, you will be able to **use the same functions** for different things and with different libraries (e.g. **Typer** will soon support `Annotated` too, then you could use the same function for an API and a CLI), etc.

Because `Annotated` is **standard Python**, you still get all the **benefits** from editors and tools, like **autocompletion**, **inline errors**, etc.

One of the **biggest benefits** is that now you can create `Annotated` dependencies that are then shared by multiple *path operation functions*, this will allow you to **reduce** a lot of **code duplication** in your codebase, while keeping all the support from editors and tools.

For example, you could have code like this:

```Python
def get_current_user(token: str):
    # authenticate user
    return User()


@app.get("/items/")
def read_items(user: User = Depends(get_current_user)):
    ...


@app.post("/items/")
def create_item(*, user: User = Depends(get_current_user), item: Item):
    ...


@app.get("/items/{item_id}")
def read_item(*, user: User = Depends(get_current_user), item_id: int):
    ...


@app.delete("/items/{item_id}")
def delete_item(*, user: User = Depends(get_current_user), item_id: int):
    ...
```

There's a bit of code duplication for the dependency:

```Python
user: User = Depends(get_current_user)
```

...the bigger the codebase, the more noticeable it is.

Now you can create an annotated dependency once, like this:

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]
```

And then you can reuse this `Annotated` dependency:

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/items/")
def read_items(user: CurrentUser):
    ...


@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    ...


@app.get("/items/{item_id}")
def read_item(user: CurrentUser, item_id: int):
    ...


@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    ...
```

...and `CurrentUser` has all the typing information as `User`, so your editor will work as expected (autocompletion and everything), and **FastAPI** will be able to understand the dependency defined in `Annotated`. 😎

Roughly **all the docs** have been rewritten to use `Annotated` as the main way to declare **parameters** and **dependencies**. All the **examples** in the docs now include a version with `Annotated` and a version without it, for each of the specific Python versions (when there are small differences/improvements in more recent versions). There were around 23K new lines added between docs, examples, and tests. 🚀

The key updated docs are:

* Python Types Intro:
    * [Type Hints with Metadata Annotations](https://fastapi.tiangolo.com/python-types/#type-hints-with-metadata-annotations).
* Tutorial:
    * [Query Parameters and String Validations - Additional validation](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#additional-validation)
        * [Advantages of `Annotated`](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#advantages-of-annotated)
    * [Path Parameters and Numeric Validations - Order the parameters as you need, tricks](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#order-the-parameters-as-you-need-tricks)
        * [Better with `Annotated`](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#better-with-annotated)
    * [Dependencies - First Steps - Share `Annotated` dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies)

Special thanks to [@nzig](https://github.com/nzig) for the core implementation and to [@adriangb](https://github.com/adriangb) for the inspiration and idea with [Xpresso](https://github.com/adriangb/xpresso)! 🚀

### Features

* ✨Add support for PEP-593 `Annotated` for specifying dependencies and parameters. PR [#4871](https://github.com/tiangolo/fastapi/pull/4871) by [@nzig](https://github.com/nzig).

### Docs

* 📝 Tweak tip recommending `Annotated` in docs. PR [#9270](https://github.com/tiangolo/fastapi/pull/9270) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update order of examples, latest Python version first, and simplify version tab names. PR [#9269](https://github.com/tiangolo/fastapi/pull/9269) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update all docs to use `Annotated` as the main recommendation, with new examples and tests. PR [#9268](https://github.com/tiangolo/fastapi/pull/9268) by [@tiangolo](https://github.com/tiangolo).

## 0.94.1

### Fixes

* 🎨 Fix types for lifespan, upgrade Starlette to 0.26.1. PR [#9245](https://github.com/tiangolo/fastapi/pull/9245) by [@tiangolo](https://github.com/tiangolo).

## 0.94.0

### Upgrades

* ⬆ Upgrade python-multipart to support 0.0.6. PR [#9212](https://github.com/tiangolo/fastapi/pull/9212) by [@musicinmybrain](https://github.com/musicinmybrain).
* ⬆️ Upgrade Starlette version, support new `lifespan` with state. PR [#9239](https://github.com/tiangolo/fastapi/pull/9239) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update Sentry link in docs. PR [#9218](https://github.com/tiangolo/fastapi/pull/9218) by [@smeubank](https://github.com/smeubank).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/history-design-future.md`. PR [#5986](https://github.com/tiangolo/fastapi/pull/5986) by [@Xewus](https://github.com/Xewus).

### Internal

* ➕ Add `pydantic` to PyPI classifiers. PR [#5914](https://github.com/tiangolo/fastapi/pull/5914) by [@yezz123](https://github.com/yezz123).
* ⬆ Bump black from 22.10.0 to 23.1.0. PR [#5953](https://github.com/tiangolo/fastapi/pull/5953) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump types-ujson from 5.6.0.0 to 5.7.0.1. PR [#6027](https://github.com/tiangolo/fastapi/pull/6027) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.3 to 2.26.0. PR [#6034](https://github.com/tiangolo/fastapi/pull/6034) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5709](https://github.com/tiangolo/fastapi/pull/5709) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.93.0

### Features

* ✨ Add support for `lifespan` async context managers (superseding `startup` and `shutdown` events). Initial PR [#2944](https://github.com/tiangolo/fastapi/pull/2944) by [@uSpike](https://github.com/uSpike).

Now, instead of using independent `startup` and `shutdown` events, you can define that logic in a single function with `yield` decorated with `@asynccontextmanager` (an async context manager).

For example:

```Python
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

**Note**: This is the recommended way going forward, instead of using `startup` and `shutdown` events.

Read more about it in the new docs: [Advanced User Guide: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

### Docs

* ✏ Fix formatting in `docs/en/docs/tutorial/metadata.md` for `ReDoc`. PR [#6005](https://github.com/tiangolo/fastapi/pull/6005) by [@eykamp](https://github.com/eykamp).

### Translations

* 🌐 Tamil translations - initial setup. PR [#5564](https://github.com/tiangolo/fastapi/pull/5564) by [@gusty1g](https://github.com/gusty1g).
* 🌐 Add French translation for `docs/fr/docs/advanced/path-operation-advanced-configuration.md`. PR [#9221](https://github.com/tiangolo/fastapi/pull/9221) by [@axel584](https://github.com/axel584).
* 🌐 Add French translation for `docs/tutorial/debugging.md`. PR [#9175](https://github.com/tiangolo/fastapi/pull/9175) by [@frabc](https://github.com/frabc).
* 🌐 Initiate Armenian translation setup. PR [#5844](https://github.com/tiangolo/fastapi/pull/5844) by [@har8](https://github.com/har8).
* 🌐 Add French translation for `deployment/manually.md`. PR [#3693](https://github.com/tiangolo/fastapi/pull/3693) by [@rjNemo](https://github.com/rjNemo).

### Internal

* 👷 Update translation bot messages. PR [#9206](https://github.com/tiangolo/fastapi/pull/9206) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update translations bot to use Discussions, and notify when a PR is done. PR [#9183](https://github.com/tiangolo/fastapi/pull/9183) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors-badges. PR [#9182](https://github.com/tiangolo/fastapi/pull/9182) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#9181](https://github.com/tiangolo/fastapi/pull/9181) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔊 Log GraphQL errors in FastAPI People, because it returns 200, with a payload with an error. PR [#9171](https://github.com/tiangolo/fastapi/pull/9171) by [@tiangolo](https://github.com/tiangolo).
* 💚 Fix/workaround GitHub Actions in Docker with git for FastAPI People. PR [#9169](https://github.com/tiangolo/fastapi/pull/9169) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor FastAPI Experts to use only discussions now that questions are migrated. PR [#9165](https://github.com/tiangolo/fastapi/pull/9165) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade analytics. PR [#6025](https://github.com/tiangolo/fastapi/pull/6025) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade and re-enable installing Typer-CLI. PR [#6008](https://github.com/tiangolo/fastapi/pull/6008) by [@tiangolo](https://github.com/tiangolo).

## 0.92.0

🚨 This is a security fix. Please upgrade as soon as possible.

### Upgrades

* ⬆️ Upgrade Starlette to 0.25.0. PR [#5996](https://github.com/tiangolo/fastapi/pull/5996) by [@tiangolo](https://github.com/tiangolo).
    * This solves a vulnerability that could allow denial of service attacks by using many small multipart fields/files (parts), consuming high CPU and memory.
    * Only applications using forms (e.g. file uploads) could be affected.
    * For most cases, upgrading won't have any breaking changes.

## 0.91.0

### Upgrades

* ⬆️ Upgrade Starlette version to `0.24.0` and refactor internals for compatibility. PR [#5985](https://github.com/tiangolo/fastapi/pull/5985) by [@tiangolo](https://github.com/tiangolo).
    * This can solve nuanced errors when using middlewares. Before Starlette `0.24.0`, a new instance of each middleware class would be created when a new middleware was added. That normally was not a problem, unless the middleware class expected to be created only once, with only one instance, that happened in some cases. This upgrade would solve those cases (thanks [@adriangb](https://github.com/adriangb)! Starlette PR [#2017](https://github.com/encode/starlette/pull/2017)). Now the middleware class instances are created once, right before the first request (the first time the app is called).
    * If you depended on that previous behavior, you might need to update your code. As always, make sure your tests pass before merging the upgrade.

## 0.90.1

### Upgrades

* ⬆️ Upgrade Starlette range to allow 0.23.1. PR [#5980](https://github.com/tiangolo/fastapi/pull/5980) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏ Tweak wording to clarify `docs/en/docs/project-generation.md`. PR [#5930](https://github.com/tiangolo/fastapi/pull/5930) by [@chandra-deb](https://github.com/chandra-deb).
* ✏ Update Pydantic GitHub URLs. PR [#5952](https://github.com/tiangolo/fastapi/pull/5952) by [@yezz123](https://github.com/yezz123).
* 📝 Add opinion from Cisco. PR [#5981](https://github.com/tiangolo/fastapi/pull/5981) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/cookie-params.md`. PR [#5890](https://github.com/tiangolo/fastapi/pull/5890) by [@bnzone](https://github.com/bnzone).

### Internal

* ✏ Update `zip-docs.sh` internal script, remove extra space. PR [#5931](https://github.com/tiangolo/fastapi/pull/5931) by [@JuanPerdomo00](https://github.com/JuanPerdomo00).

## 0.90.0

### Upgrades

* ⬆️ Bump Starlette from 0.22.0 to 0.23.0. Initial PR [#5739](https://github.com/tiangolo/fastapi/pull/5739) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Add article "Tortoise ORM / FastAPI 整合快速筆記" to External Links. PR [#5496](https://github.com/tiangolo/fastapi/pull/5496) by [@Leon0824](https://github.com/Leon0824).
* 👥 Update FastAPI People. PR [#5954](https://github.com/tiangolo/fastapi/pull/5954) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 📝 Micro-tweak help docs. PR [#5960](https://github.com/tiangolo/fastapi/pull/5960) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update new issue chooser to direct to GitHub Discussions. PR [#5948](https://github.com/tiangolo/fastapi/pull/5948) by [@tiangolo](https://github.com/tiangolo).
* 📝 Recommend GitHub Discussions for questions. PR [#5944](https://github.com/tiangolo/fastapi/pull/5944) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-fields.md`. PR [#5898](https://github.com/tiangolo/fastapi/pull/5898) by [@simatheone](https://github.com/simatheone).
* 🌐 Add Russian translation for `docs/ru/docs/help-fastapi.md`. PR [#5970](https://github.com/tiangolo/fastapi/pull/5970) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/static-files.md`. PR [#5858](https://github.com/tiangolo/fastapi/pull/5858) by [@batlopes](https://github.com/batlopes).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/encoder.md`. PR [#5525](https://github.com/tiangolo/fastapi/pull/5525) by [@felipebpl](https://github.com/felipebpl).
* 🌐 Add Russian translation for `docs/ru/docs/contributing.md`. PR [#5870](https://github.com/tiangolo/fastapi/pull/5870) by [@Xewus](https://github.com/Xewus).

### Internal

* ⬆️ Upgrade Ubuntu version for docs workflow. PR [#5971](https://github.com/tiangolo/fastapi/pull/5971) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors badges. PR [#5943](https://github.com/tiangolo/fastapi/pull/5943) by [@tiangolo](https://github.com/tiangolo).
* ✨ Compute FastAPI Experts including GitHub Discussions. PR [#5941](https://github.com/tiangolo/fastapi/pull/5941) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade isort and update pre-commit. PR [#5940](https://github.com/tiangolo/fastapi/pull/5940) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add template for questions in Discussions. PR [#5920](https://github.com/tiangolo/fastapi/pull/5920) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Sponsor Budget Insight to Powens. PR [#5916](https://github.com/tiangolo/fastapi/pull/5916) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update GitHub Sponsors badge data. PR [#5915](https://github.com/tiangolo/fastapi/pull/5915) by [@tiangolo](https://github.com/tiangolo).

## 0.89.1

### Fixes

* 🐛 Ignore Response classes on return annotation. PR [#5855](https://github.com/tiangolo/fastapi/pull/5855) by [@Kludex](https://github.com/Kludex). See the new docs in the PR below.

### Docs

* 📝 Update docs and examples for Response Model with Return Type Annotations, and update runtime error. PR [#5873](https://github.com/tiangolo/fastapi/pull/5873) by [@tiangolo](https://github.com/tiangolo). New docs at [Response Model - Return Type: Other Return Type Annotations](https://fastapi.tiangolo.com/tutorial/response-model/#other-return-type-annotations).
* 📝 Add External Link: FastAPI lambda container: serverless simplified. PR [#5784](https://github.com/tiangolo/fastapi/pull/5784) by [@rafrasenberg](https://github.com/rafrasenberg).

### Translations

* 🌐 Add Turkish translation for `docs/tr/docs/tutorial/first_steps.md`. PR [#5691](https://github.com/tiangolo/fastapi/pull/5691) by [@Kadermiyanyedi](https://github.com/Kadermiyanyedi).

## 0.89.0

### Features

* ✨ Add support for function return type annotations to declare the `response_model`. Initial PR [#1436](https://github.com/tiangolo/fastapi/pull/1436) by [@uriyyo](https://github.com/uriyyo).

Now you can declare the return type / `response_model` in the function return type annotation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
```

FastAPI will use the return type annotation to perform:

* Data validation
* Automatic documentation
    * It could power automatic client generators
* **Data filtering**

Before this version it was only supported via the `response_model` parameter.

Read more about it in the new docs: [Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/).

### Docs

* 📝 Add External Link: Authorization on FastAPI with Casbin. PR [#5712](https://github.com/tiangolo/fastapi/pull/5712) by [@Xhy-5000](https://github.com/Xhy-5000).
* ✏ Fix typo in `docs/en/docs/async.md`. PR [#5785](https://github.com/tiangolo/fastapi/pull/5785) by [@Kingdageek](https://github.com/Kingdageek).
* ✏ Fix typo in `docs/en/docs/deployment/concepts.md`. PR [#5824](https://github.com/tiangolo/fastapi/pull/5824) by [@kelbyfaessler](https://github.com/kelbyfaessler).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/fastapi-people.md`. PR [#5577](https://github.com/tiangolo/fastapi/pull/5577) by [@Xewus](https://github.com/Xewus).
* 🌐 Fix typo in Chinese translation for `docs/zh/docs/benchmarks.md`. PR [#4269](https://github.com/tiangolo/fastapi/pull/4269) by [@15027668g](https://github.com/15027668g).
* 🌐 Add Korean translation for `docs/tutorial/cors.md`. PR [#3764](https://github.com/tiangolo/fastapi/pull/3764) by [@NinaHwang](https://github.com/NinaHwang).

### Internal

* ⬆ Update coverage[toml] requirement from <7.0,>=6.5.0 to >=6.5.0,<8.0. PR [#5801](https://github.com/tiangolo/fastapi/pull/5801) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update uvicorn[standard] requirement from <0.19.0,>=0.12.0 to >=0.12.0,<0.21.0 for development. PR [#5795](https://github.com/tiangolo/fastapi/pull/5795) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.2 to 2.24.3. PR [#5842](https://github.com/tiangolo/fastapi/pull/5842) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI People. PR [#5825](https://github.com/tiangolo/fastapi/pull/5825) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ⬆ Bump types-ujson from 5.5.0 to 5.6.0.0. PR [#5735](https://github.com/tiangolo/fastapi/pull/5735) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.5.2 to 1.6.4. PR [#5750](https://github.com/tiangolo/fastapi/pull/5750) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add GitHub Action gate/check. PR [#5492](https://github.com/tiangolo/fastapi/pull/5492) by [@webknjaz](https://github.com/webknjaz).
* 🔧 Update sponsors, add Svix. PR [#5848](https://github.com/tiangolo/fastapi/pull/5848) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Remove Doist sponsor. PR [#5847](https://github.com/tiangolo/fastapi/pull/5847) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Update sqlalchemy requirement from <=1.4.41,>=1.3.18 to >=1.3.18,<1.4.43. PR [#5540](https://github.com/tiangolo/fastapi/pull/5540) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump nwtgck/actions-netlify from 1.2.4 to 2.0.0. PR [#5757](https://github.com/tiangolo/fastapi/pull/5757) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Refactor CI artifact upload/download for docs previews. PR [#5793](https://github.com/tiangolo/fastapi/pull/5793) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.5.1 to 1.5.2. PR [#5714](https://github.com/tiangolo/fastapi/pull/5714) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI People. PR [#5722](https://github.com/tiangolo/fastapi/pull/5722) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Update sponsors, disable course bundle. PR [#5713](https://github.com/tiangolo/fastapi/pull/5713) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Update typer[all] requirement from <0.7.0,>=0.6.1 to >=0.6.1,<0.8.0. PR [#5639](https://github.com/tiangolo/fastapi/pull/5639) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.88.0

### Upgrades

* ⬆ Bump Starlette to version `0.22.0` to fix bad encoding for query parameters in new `TestClient`. PR [#5659](https://github.com/tiangolo/fastapi/pull/5659) by [@azogue](https://github.com/azogue).

### Docs

* ✏️ Fix typo in docs for `docs/en/docs/advanced/middleware.md`. PR [#5376](https://github.com/tiangolo/fastapi/pull/5376) by [@rifatrakib](https://github.com/rifatrakib).

### Translations

* 🌐 Add Portuguese translation for `docs/pt/docs/deployment/docker.md`. PR [#5663](https://github.com/tiangolo/fastapi/pull/5663) by [@ayr-ton](https://github.com/ayr-ton).

### Internal

* 👷 Tweak build-docs to improve CI performance. PR [#5699](https://github.com/tiangolo/fastapi/pull/5699) by [@tiangolo](https://github.com/tiangolo).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5566](https://github.com/tiangolo/fastapi/pull/5566) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆️ Upgrade Ruff. PR [#5698](https://github.com/tiangolo/fastapi/pull/5698) by [@tiangolo](https://github.com/tiangolo).
* 👷 Remove pip cache for Smokeshow as it depends on a requirements.txt. PR [#5700](https://github.com/tiangolo/fastapi/pull/5700) by [@tiangolo](https://github.com/tiangolo).
* 💚 Fix pip cache for Smokeshow. PR [#5697](https://github.com/tiangolo/fastapi/pull/5697) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix and tweak CI cache handling. PR [#5696](https://github.com/tiangolo/fastapi/pull/5696) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `setup-python` action in tests to use new caching feature. PR [#5680](https://github.com/tiangolo/fastapi/pull/5680) by [@madkinsz](https://github.com/madkinsz).
* ⬆ Bump black from 22.8.0 to 22.10.0. PR [#5569](https://github.com/tiangolo/fastapi/pull/5569) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.87.0

Highlights of this release:

* [Upgraded Starlette](https://github.com/encode/starlette/releases/tag/0.21.0)
    * Now the `TestClient` is based on HTTPX instead of Requests. 🚀
    * There are some possible **breaking changes** in the `TestClient` usage, but [@Kludex](https://github.com/Kludex) built [bump-testclient](https://github.com/Kludex/bump-testclient) to help you automatize migrating your tests. Make sure you are using Git and that you can undo any unnecessary changes (false positive changes, etc) before using `bump-testclient`.
* New [WebSocketException (and docs)](https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others), re-exported from Starlette.
* Upgraded and relaxed dependencies for package extras `all` (including new Uvicorn version), when you install `"fastapi[all]"`.
* New docs about how to [**Help Maintain FastAPI**](https://fastapi.tiangolo.com/help-fastapi/#help-maintain-fastapi).

### Features

* ⬆️ Upgrade and relax dependencies for extras "all". PR [#5634](https://github.com/tiangolo/fastapi/pull/5634) by [@tiangolo](https://github.com/tiangolo).
* ✨ Re-export Starlette's `WebSocketException` and add it to docs. PR [#5629](https://github.com/tiangolo/fastapi/pull/5629) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update references to Requests for tests to HTTPX, and add HTTPX to extras. PR [#5628](https://github.com/tiangolo/fastapi/pull/5628) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Upgrade Starlette to `0.21.0`, including the new [`TestClient` based on HTTPX](https://github.com/encode/starlette/releases/tag/0.21.0). PR [#5471](https://github.com/tiangolo/fastapi/pull/5471) by [@pawelrubin](https://github.com/pawelrubin).

### Docs

* ✏️ Tweak Help FastAPI from PR review after merging. PR [#5633](https://github.com/tiangolo/fastapi/pull/5633) by [@tiangolo](https://github.com/tiangolo).
* ✏️  Clarify docs on CORS. PR [#5627](https://github.com/tiangolo/fastapi/pull/5627) by [@paxcodes](https://github.com/paxcodes).
* 📝 Update Help FastAPI: Help Maintain FastAPI. PR [#5632](https://github.com/tiangolo/fastapi/pull/5632) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Fix highlight lines for Japanese translation for `docs/tutorial/query-params.md`. PR [#2969](https://github.com/tiangolo/fastapi/pull/2969) by [@ftnext](https://github.com/ftnext).
* 🌐 Add French translation for `docs/fr/docs/advanced/additional-status-code.md`. PR [#5477](https://github.com/tiangolo/fastapi/pull/5477) by [@axel584](https://github.com/axel584).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/request-forms-and-files.md`. PR [#5579](https://github.com/tiangolo/fastapi/pull/5579) by [@batlopes](https://github.com/batlopes).
* 🌐 Add Japanese translation for `docs/ja/docs/advanced/websockets.md`. PR [#4983](https://github.com/tiangolo/fastapi/pull/4983) by [@xryuseix](https://github.com/xryuseix).

### Internal

* ✨ Use Ruff for linting. PR [#5630](https://github.com/tiangolo/fastapi/pull/5630) by [@tiangolo](https://github.com/tiangolo).
* 🛠 Add Arabic issue number to Notify Translations GitHub Action. PR [#5610](https://github.com/tiangolo/fastapi/pull/5610) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.1 to 2.24.2. PR [#5609](https://github.com/tiangolo/fastapi/pull/5609) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.0 to 2.24.1. PR [#5603](https://github.com/tiangolo/fastapi/pull/5603) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 📝 Update coverage badge to use Samuel Colvin's Smokeshow. PR [#5585](https://github.com/tiangolo/fastapi/pull/5585) by [@tiangolo](https://github.com/tiangolo).

## 0.86.0

### Features

* ⬆ Add Python 3.11 to the officially supported versions. PR [#5587](https://github.com/tiangolo/fastapi/pull/5587) by [@tiangolo](https://github.com/tiangolo).
* ✅ Enable tests for Python 3.11. PR [#4881](https://github.com/tiangolo/fastapi/pull/4881) by [@tiangolo](https://github.com/tiangolo).

### Fixes

* 🐛 Close FormData (uploaded files) after the request is done. PR [#5465](https://github.com/tiangolo/fastapi/pull/5465) by [@adriangb](https://github.com/adriangb).

### Docs

* ✏ Fix typo in `docs/en/docs/tutorial/security/oauth2-jwt.md`. PR [#5584](https://github.com/tiangolo/fastapi/pull/5584) by [@vivekashok1221](https://github.com/vivekashok1221).

### Translations

* 🌐 Update wording in Chinese translation for `docs/zh/docs/python-types.md`. PR [#5416](https://github.com/tiangolo/fastapi/pull/5416) by [@supercaizehua](https://github.com/supercaizehua).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/index.md`. PR [#5336](https://github.com/tiangolo/fastapi/pull/5336) by [@Xewus](https://github.com/Xewus).
* 🌐 Update Chinese translation for `docs/tutorial/security/oauth2-jwt.md`. PR [#3846](https://github.com/tiangolo/fastapi/pull/3846) by [@jaystone776](https://github.com/jaystone776).

### Internal

* 👷 Update FastAPI People to exclude bots: pre-commit-ci, dependabot. PR [#5586](https://github.com/tiangolo/fastapi/pull/5586) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Format OpenAPI JSON in `test_starlette_exception.py`. PR [#5379](https://github.com/tiangolo/fastapi/pull/5379) by [@iudeen](https://github.com/iudeen).
* 👷 Switch from Codecov to Smokeshow plus pytest-cov to pure coverage for internal tests. PR [#5583](https://github.com/tiangolo/fastapi/pull/5583) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#5571](https://github.com/tiangolo/fastapi/pull/5571) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.85.2

### Docs

* ✏ Fix grammar and add helpful links to dependencies in `docs/en/docs/async.md`. PR [#5432](https://github.com/tiangolo/fastapi/pull/5432) by [@pamelafox](https://github.com/pamelafox).
* ✏ Fix broken link in `alternatives.md`. PR [#5455](https://github.com/tiangolo/fastapi/pull/5455) by [@su-shubham](https://github.com/su-shubham).
* ✏ Fix typo in docs about contributing, for compatibility with `pip` in Zsh. PR [#5523](https://github.com/tiangolo/fastapi/pull/5523) by [@zhangbo2012](https://github.com/zhangbo2012).
* 📝 Fix typo in docs with examples for Python 3.10 instead of 3.9. PR [#5545](https://github.com/tiangolo/fastapi/pull/5545) by [@feliciss](https://github.com/feliciss).

### Translations

* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/request-forms.md`. PR [#4934](https://github.com/tiangolo/fastapi/pull/4934) by [@batlopes](https://github.com/batlopes).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#4971](https://github.com/tiangolo/fastapi/pull/4971) by [@Zssaer](https://github.com/Zssaer).
* 🌐 Add French translation for `deployment/deta.md`. PR [#3692](https://github.com/tiangolo/fastapi/pull/3692) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/query-params-str-validations.md`. PR [#5255](https://github.com/tiangolo/fastapi/pull/5255) by [@hjlarry](https://github.com/hjlarry).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/sql-databases.md`. PR [#4999](https://github.com/tiangolo/fastapi/pull/4999) by [@Zssaer](https://github.com/Zssaer).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/wsgi.md`. PR [#4505](https://github.com/tiangolo/fastapi/pull/4505) by [@ASpathfinder](https://github.com/ASpathfinder).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/body-multiple-params.md`. PR [#4111](https://github.com/tiangolo/fastapi/pull/4111) by [@lbmendes](https://github.com/lbmendes).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/path-params-numeric-validations.md`. PR [#4099](https://github.com/tiangolo/fastapi/pull/4099) by [@lbmendes](https://github.com/lbmendes).
* 🌐 Add French translation for `deployment/versions.md`. PR [#3690](https://github.com/tiangolo/fastapi/pull/3690) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Add French translation for `docs/fr/docs/help-fastapi.md`. PR [#2233](https://github.com/tiangolo/fastapi/pull/2233) by [@JulianMaurin](https://github.com/JulianMaurin).
* 🌐 Fix typo in Chinese translation for `docs/zh/docs/tutorial/security/first-steps.md`. PR [#5530](https://github.com/tiangolo/fastapi/pull/5530) by [@yuki1sntSnow](https://github.com/yuki1sntSnow).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/response-status-code.md`. PR [#4922](https://github.com/tiangolo/fastapi/pull/4922) by [@batlopes](https://github.com/batlopes).
* 🔧 Add config for Tamil translations. PR [#5563](https://github.com/tiangolo/fastapi/pull/5563) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump internal dependency mypy from 0.971 to 0.982. PR [#5541](https://github.com/tiangolo/fastapi/pull/5541) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump nwtgck/actions-netlify from 1.2.3 to 1.2.4. PR [#5507](https://github.com/tiangolo/fastapi/pull/5507) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump internal dependency types-ujson from 5.4.0 to 5.5.0. PR [#5537](https://github.com/tiangolo/fastapi/pull/5537) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.23.0 to 2.24.0. PR [#5508](https://github.com/tiangolo/fastapi/pull/5508) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update internal dependency pytest-cov requirement from <4.0.0,>=2.12.0 to >=2.12.0,<5.0.0. PR [#5539](https://github.com/tiangolo/fastapi/pull/5539) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5536](https://github.com/tiangolo/fastapi/pull/5536) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🐛 Fix internal Trio test warnings. PR [#5547](https://github.com/tiangolo/fastapi/pull/5547) by [@samuelcolvin](https://github.com/samuelcolvin).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5408](https://github.com/tiangolo/fastapi/pull/5408) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆️ Upgrade Typer to include Rich in scripts for docs. PR [#5502](https://github.com/tiangolo/fastapi/pull/5502) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix calling `mkdocs` for languages as a subprocess to fix/enable MkDocs Material search plugin. PR [#5501](https://github.com/tiangolo/fastapi/pull/5501) by [@tiangolo](https://github.com/tiangolo).

## 0.85.1

### Fixes

* 🐛 Fix support for strings in OpenAPI status codes: `default`, `1XX`, `2XX`, `3XX`, `4XX`, `5XX`. PR [#5187](https://github.com/tiangolo/fastapi/pull/5187) by [@JarroVGIT](https://github.com/JarroVGIT).

### Docs

* 📝 Add WayScript x FastAPI Tutorial to External Links section. PR [#5407](https://github.com/tiangolo/fastapi/pull/5407) by [@moneeka](https://github.com/moneeka).

### Internal

* 👥 Update FastAPI People. PR [#5447](https://github.com/tiangolo/fastapi/pull/5447) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Disable Material for MkDocs search plugin. PR [#5495](https://github.com/tiangolo/fastapi/pull/5495) by [@tiangolo](https://github.com/tiangolo).
* 🔇 Ignore Trio warning in tests for CI. PR [#5483](https://github.com/tiangolo/fastapi/pull/5483) by [@samuelcolvin](https://github.com/samuelcolvin).

## 0.85.0

### Features

* ⬆ Upgrade version required of Starlette from `0.19.1` to `0.20.4`. Initial PR [#4820](https://github.com/tiangolo/fastapi/pull/4820) by [@Kludex](https://github.com/Kludex).
    * This includes several bug fixes in Starlette.
* ⬆️ Upgrade Uvicorn max version in public extras: all. From `>=0.12.0,<0.18.0` to `>=0.12.0,<0.19.0`. PR [#5401](https://github.com/tiangolo/fastapi/pull/5401) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆️ Upgrade dependencies for doc and dev internal extras: Typer, Uvicorn. PR [#5400](https://github.com/tiangolo/fastapi/pull/5400) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade test dependencies: Black, HTTPX, databases, types-ujson. PR [#5399](https://github.com/tiangolo/fastapi/pull/5399) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade mypy and tweak internal type annotations. PR [#5398](https://github.com/tiangolo/fastapi/pull/5398) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update test dependencies, upgrade Pytest, move dependencies from dev to test. PR [#5396](https://github.com/tiangolo/fastapi/pull/5396) by [@tiangolo](https://github.com/tiangolo).

## 0.84.0

### Breaking Changes

This version of FastAPI drops support for Python 3.6. 🔥 Please upgrade to a supported version of Python (3.7 or above), Python 3.6 reached the end-of-life a long time ago. 😅☠

* 🔧 Update package metadata, drop support for Python 3.6, move build internals from Flit to Hatch. PR [#5240](https://github.com/tiangolo/fastapi/pull/5240) by [@ofek](https://github.com/ofek).

## 0.83.0

🚨 This is probably the last release (or one of the last releases) to support Python 3.6. 🔥

Python 3.6 reached the [end-of-life and is no longer supported by Python](https://www.python.org/downloads/release/python-3615/) since around a year ago.

You hopefully updated to a supported version of Python a while ago. If you haven't, you really should.

### Features

* ✨ Add support in `jsonable_encoder` for include and exclude with dataclasses. PR [#4923](https://github.com/tiangolo/fastapi/pull/4923) by [@DCsunset](https://github.com/DCsunset).

### Fixes

* 🐛 Fix `RuntimeError` raised when `HTTPException` has a status code with no content. PR [#5365](https://github.com/tiangolo/fastapi/pull/5365) by [@iudeen](https://github.com/iudeen).
* 🐛 Fix empty reponse body when default `status_code` is empty but the a `Response` parameter with `response.status_code` is set. PR [#5360](https://github.com/tiangolo/fastapi/pull/5360) by [@tmeckel](https://github.com/tmeckel).

### Docs

* 📝 Update `SECURITY.md`. PR [#5377](https://github.com/tiangolo/fastapi/pull/5377) by [@Kludex](https://github.com/Kludex).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5352](https://github.com/tiangolo/fastapi/pull/5352) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.82.0

🚨 This is probably the last release (or one of the last releases) to support Python 3.6. 🔥

Python 3.6 reached the [end-of-life and is no longer supported by Python](https://www.python.org/downloads/release/python-3615/) since around a year ago.

You hopefully updated to a supported version of Python a while ago. If you haven't, you really should.

### Features

* ✨ Export `WebSocketState` in `fastapi.websockets`. PR [#4376](https://github.com/tiangolo/fastapi/pull/4376) by [@matiuszka](https://github.com/matiuszka).
* ✨ Support Python internal description on Pydantic model's docstring. PR [#3032](https://github.com/tiangolo/fastapi/pull/3032) by [@Kludex](https://github.com/Kludex).
* ✨ Update `ORJSONResponse` to support non `str` keys and serializing Numpy arrays. PR [#3892](https://github.com/tiangolo/fastapi/pull/3892) by [@baby5](https://github.com/baby5).

### Fixes

* 🐛 Allow exit code for dependencies with `yield` to always execute, by removing capacity limiter for them, to e.g. allow closing DB connections without deadlocks. PR [#5122](https://github.com/tiangolo/fastapi/pull/5122) by [@adriangb](https://github.com/adriangb).
* 🐛 Fix FastAPI People GitHub Action: set HTTPX timeout for GraphQL query request. PR [#5222](https://github.com/tiangolo/fastapi/pull/5222) by [@iudeen](https://github.com/iudeen).
* 🐛 Make sure a parameter defined as required is kept required in OpenAPI even if defined as optional in another dependency. PR [#4319](https://github.com/tiangolo/fastapi/pull/4319) by [@cd17822](https://github.com/cd17822).
* 🐛 Fix support for path parameters in WebSockets. PR [#3879](https://github.com/tiangolo/fastapi/pull/3879) by [@davidbrochart](https://github.com/davidbrochart).

### Docs

* ✏ Update Hypercorn link, now pointing to GitHub. PR [#5346](https://github.com/tiangolo/fastapi/pull/5346) by [@baconfield](https://github.com/baconfield).
* ✏ Tweak wording in `docs/en/docs/advanced/dataclasses.md`. PR [#3698](https://github.com/tiangolo/fastapi/pull/3698) by [@pfackeldey](https://github.com/pfackeldey).
* 📝 Add note about Python 3.10 `X | Y` operator in explanation about Response Models. PR [#5307](https://github.com/tiangolo/fastapi/pull/5307) by [@MendyLanda](https://github.com/MendyLanda).
* 📝 Add link to New Relic article: "How to monitor FastAPI application performance using Python agent". PR [#5260](https://github.com/tiangolo/fastapi/pull/5260) by [@sjyothi54](https://github.com/sjyothi54).
* 📝 Update docs for `ORJSONResponse` with details about improving performance. PR [#2615](https://github.com/tiangolo/fastapi/pull/2615) by [@falkben](https://github.com/falkben).
* 📝 Add docs for creating a custom Response class. PR [#5331](https://github.com/tiangolo/fastapi/pull/5331) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add tip about using alias for form data fields. PR [#5329](https://github.com/tiangolo/fastapi/pull/5329) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/features.md`. PR [#5315](https://github.com/tiangolo/fastapi/pull/5315) by [@Xewus](https://github.com/Xewus).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/request-files.md`. PR [#4529](https://github.com/tiangolo/fastapi/pull/4529) by [@ASpathfinder](https://github.com/ASpathfinder).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/encoder.md`. PR [#4969](https://github.com/tiangolo/fastapi/pull/4969) by [@Zssaer](https://github.com/Zssaer).
* 🌐 Fix MkDocs file line for Portuguese translation of `background-task.md`. PR [#5242](https://github.com/tiangolo/fastapi/pull/5242) by [@ComicShrimp](https://github.com/ComicShrimp).

### Internal

* 👥 Update FastAPI People. PR [#5347](https://github.com/tiangolo/fastapi/pull/5347) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ⬆ Bump dawidd6/action-download-artifact from 2.22.0 to 2.23.0. PR [#5321](https://github.com/tiangolo/fastapi/pull/5321) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5318](https://github.com/tiangolo/fastapi/pull/5318) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ✏ Fix a small code highlight line error. PR [#5256](https://github.com/tiangolo/fastapi/pull/5256) by [@hjlarry](https://github.com/hjlarry).
* ♻ Internal small refactor, move `operation_id` parameter position in delete method for consistency with the code. PR [#4474](https://github.com/tiangolo/fastapi/pull/4474) by [@hiel](https://github.com/hiel).
* 🔧 Update sponsors, disable ImgWhale. PR [#5338](https://github.com/tiangolo/fastapi/pull/5338) by [@tiangolo](https://github.com/tiangolo).

## 0.81.0

### Features

* ✨ Add ReDoc `<noscript>` warning when JS is disabled. PR [#5074](https://github.com/tiangolo/fastapi/pull/5074) by [@evroon](https://github.com/evroon).
* ✨ Add support for `FrozenSet` in parameters (e.g. query). PR [#2938](https://github.com/tiangolo/fastapi/pull/2938) by [@juntatalor](https://github.com/juntatalor).
* ✨ Allow custom middlewares to raise `HTTPException`s and propagate them. PR [#2036](https://github.com/tiangolo/fastapi/pull/2036) by [@ghandic](https://github.com/ghandic).
* ✨ Preserve `json.JSONDecodeError` information when handling invalid JSON in request body, to support custom exception handlers that use its information. PR [#4057](https://github.com/tiangolo/fastapi/pull/4057) by [@UKnowWhoIm](https://github.com/UKnowWhoIm).

### Fixes

* 🐛 Fix `jsonable_encoder` for dataclasses with pydantic-compatible fields. PR [#3607](https://github.com/tiangolo/fastapi/pull/3607) by [@himbeles](https://github.com/himbeles).
* 🐛 Fix support for extending `openapi_extras` with parameter lists. PR [#4267](https://github.com/tiangolo/fastapi/pull/4267) by [@orilevari](https://github.com/orilevari).

### Docs

* ✏ Fix a simple typo in `docs/en/docs/python-types.md`. PR [#5193](https://github.com/tiangolo/fastapi/pull/5193) by [@GlitchingCore](https://github.com/GlitchingCore).
* ✏ Fix typos in `tests/test_schema_extra_examples.py`. PR [#5126](https://github.com/tiangolo/fastapi/pull/5126) by [@supraaxdd](https://github.com/supraaxdd).
* ✏ Fix typos in `docs/en/docs/tutorial/path-params-numeric-validations.md`. PR [#5142](https://github.com/tiangolo/fastapi/pull/5142) by [@invisibleroads](https://github.com/invisibleroads).
* 📝 Add step about upgrading pip in the venv to avoid errors when installing dependencies `docs/en/docs/contributing.md`. PR [#5181](https://github.com/tiangolo/fastapi/pull/5181) by [@edisnake](https://github.com/edisnake).
* ✏ Reword and clarify text in tutorial `docs/en/docs/tutorial/body-nested-models.md`. PR [#5169](https://github.com/tiangolo/fastapi/pull/5169) by [@papb](https://github.com/papb).
* ✏ Fix minor typo in `docs/en/docs/features.md`. PR [#5206](https://github.com/tiangolo/fastapi/pull/5206) by [@OtherBarry](https://github.com/OtherBarry).
* ✏ Fix minor typos in `docs/en/docs/async.md`. PR [#5125](https://github.com/tiangolo/fastapi/pull/5125) by [@Ksenofanex](https://github.com/Ksenofanex).
* 📝 Add external link to docs: "Fastapi, Docker(Docker compose) and Postgres". PR [#5033](https://github.com/tiangolo/fastapi/pull/5033) by [@krishnardt](https://github.com/krishnardt).
* 📝 Simplify example for docs for Additional Responses, remove unnecessary `else`. PR [#4693](https://github.com/tiangolo/fastapi/pull/4693) by [@adriangb](https://github.com/adriangb).
* 📝 Update docs, compare enums with identity instead of equality. PR [#4905](https://github.com/tiangolo/fastapi/pull/4905) by [@MicaelJarniac](https://github.com/MicaelJarniac).
* ✏ Fix typo in `docs/en/docs/python-types.md`. PR [#4886](https://github.com/tiangolo/fastapi/pull/4886) by [@MicaelJarniac](https://github.com/MicaelJarniac).
* 🎨 Fix syntax highlighting in docs for OpenAPI Callbacks. PR [#4368](https://github.com/tiangolo/fastapi/pull/4368) by [@xncbf](https://github.com/xncbf).
* ✏ Reword confusing sentence in docs file `typo-fix-path-params-numeric-validations.md`. PR [#3219](https://github.com/tiangolo/fastapi/pull/3219) by [@ccrenfroe](https://github.com/ccrenfroe).
* 📝 Update docs for handling HTTP Basic Auth with `secrets.compare_digest()` to account for non-ASCII characters. PR [#3536](https://github.com/tiangolo/fastapi/pull/3536) by [@lewoudar](https://github.com/lewoudar).
* 📝 Update docs for testing, fix examples with relative imports. PR [#5302](https://github.com/tiangolo/fastapi/pull/5302) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/index.md`. PR [#5289](https://github.com/tiangolo/fastapi/pull/5289) by [@impocode](https://github.com/impocode).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/versions.md`. PR [#4985](https://github.com/tiangolo/fastapi/pull/4985) by [@emp7yhead](https://github.com/emp7yhead).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/header-params.md`. PR [#4921](https://github.com/tiangolo/fastapi/pull/4921) by [@batlopes](https://github.com/batlopes).
* 🌐 Update `ko/mkdocs.yml` for a missing link. PR [#5020](https://github.com/tiangolo/fastapi/pull/5020) by [@dalinaum](https://github.com/dalinaum).

### Internal

* ⬆ Bump dawidd6/action-download-artifact from 2.21.1 to 2.22.0. PR [#5258](https://github.com/tiangolo/fastapi/pull/5258) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5196](https://github.com/tiangolo/fastapi/pull/5196) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔥 Delete duplicated tests in `tests/test_tutorial/test_sql_databases/test_sql_databases.py`. PR [#5040](https://github.com/tiangolo/fastapi/pull/5040) by [@raccoonyy](https://github.com/raccoonyy).
* ♻ Simplify internal RegEx in `fastapi/utils.py`. PR [#5057](https://github.com/tiangolo/fastapi/pull/5057) by [@pylounge](https://github.com/pylounge).
* 🔧 Fix Type hint of `auto_error` which does not need to be `Optional[bool]`. PR [#4933](https://github.com/tiangolo/fastapi/pull/4933) by [@DavidKimDY](https://github.com/DavidKimDY).
* 🔧 Update mypy config, use `strict = true` instead of manual configs. PR [#4605](https://github.com/tiangolo/fastapi/pull/4605) by [@michaeloliverx](https://github.com/michaeloliverx).
* ♻ Change a `dict()` for `{}` in `fastapi/utils.py`. PR [#3138](https://github.com/tiangolo/fastapi/pull/3138) by [@ShahriyarR](https://github.com/ShahriyarR).
* ♻ Move internal variable for errors in `jsonable_encoder` to put related code closer. PR [#4560](https://github.com/tiangolo/fastapi/pull/4560) by [@GuilleQP](https://github.com/GuilleQP).
* ♻ Simplify conditional assignment in `fastapi/dependencies/utils.py`. PR [#4597](https://github.com/tiangolo/fastapi/pull/4597) by [@cikay](https://github.com/cikay).
* ⬆ Upgrade version pin accepted for Flake8, for internal code, to `flake8 >=3.8.3,<6.0.0`. PR [#4097](https://github.com/tiangolo/fastapi/pull/4097) by [@jamescurtin](https://github.com/jamescurtin).
* 🍱 Update Jina banner, fix typo. PR [#5301](https://github.com/tiangolo/fastapi/pull/5301) by [@tiangolo](https://github.com/tiangolo).

## 0.80.0

### Breaking Changes - Fixes

* 🐛 Fix `response_model` not invalidating `None`. PR [#2725](https://github.com/tiangolo/fastapi/pull/2725) by [@hukkin](https://github.com/hukkin).

If you are using `response_model` with some type that doesn't include `None` but the function is returning `None`, it will now raise an internal server error, because you are returning invalid data that violates the contract in `response_model`. Before this release it would allow breaking that contract returning `None`.

For example, if you have an app like this:

```Python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None

app = FastAPI()

@app.get("/items/invalidnone", response_model=Item)
def get_invalid_none():
    return None
```

...calling the path `/items/invalidnone` will raise an error, because `None` is not a valid type for the `response_model` declared with `Item`.

You could also be implicitly returning `None` without realizing, for example:

```Python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None

app = FastAPI()

@app.get("/items/invalidnone", response_model=Item)
def get_invalid_none():
    if flag:
        return {"name": "foo"}
    # if flag is False, at this point the function will implicitly return None
```

If you have *path operations* using `response_model` that need to be allowed to return `None`, make it explicit in `response_model` using `Union[Something, None]`:

```Python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None

app = FastAPI()

@app.get("/items/invalidnone", response_model=Union[Item, None])
def get_invalid_none():
    return None
```

This way the data will be correctly validated, you won't have an internal server error, and the documentation will also reflect that this *path operation* could return `None` (or `null` in JSON).

### Fixes

* ⬆ Upgrade Swagger UI copy of `oauth2-redirect.html` to include fixes for flavors of authorization code flows in Swagger UI. PR [#3439](https://github.com/tiangolo/fastapi/pull/3439) initial PR by [@koonpeng](https://github.com/koonpeng).
* ♻ Strip empty whitespace from description extracted from docstrings. PR [#2821](https://github.com/tiangolo/fastapi/pull/2821) by [@and-semakin](https://github.com/and-semakin).
* 🐛 Fix cached dependencies when using a dependency in `Security()` and other places (e.g. `Depends()`) with different OAuth2 scopes. PR [#2945](https://github.com/tiangolo/fastapi/pull/2945) by [@laggardkernel](https://github.com/laggardkernel).
* 🎨 Update type annotations for `response_model`, allow things like `Union[str, None]`. PR [#5294](https://github.com/tiangolo/fastapi/pull/5294) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Fix typos in German translation for `docs/de/docs/features.md`. PR [#4533](https://github.com/tiangolo/fastapi/pull/4533) by [@0xflotus](https://github.com/0xflotus).
* 🌐 Add missing navigator for `encoder.md` in Korean translation. PR [#5238](https://github.com/tiangolo/fastapi/pull/5238) by [@joonas-yoon](https://github.com/joonas-yoon).
* (Empty PR merge by accident) [#4913](https://github.com/tiangolo/fastapi/pull/4913).

## 0.79.1

### Fixes

* 🐛 Fix `jsonable_encoder` using `include` and `exclude` parameters for non-Pydantic objects. PR [#2606](https://github.com/tiangolo/fastapi/pull/2606) by [@xaviml](https://github.com/xaviml).
* 🐛 Fix edge case with repeated aliases names not shown in OpenAPI. PR [#2351](https://github.com/tiangolo/fastapi/pull/2351) by [@klaa97](https://github.com/klaa97).
* 📝 Add misc dependency installs to tutorial docs. PR [#2126](https://github.com/tiangolo/fastapi/pull/2126) by [@TeoZosa](https://github.com/TeoZosa).

### Docs

* 📝 Add note giving credit for illustrations to [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot/). PR [#5284](https://github.com/tiangolo/fastapi/pull/5284) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typo in `python-types.md`. PR [#5116](https://github.com/tiangolo/fastapi/pull/5116) by [@Kludex](https://github.com/Kludex).
* ✏ Fix typo in `docs/en/docs/python-types.md`. PR [#5007](https://github.com/tiangolo/fastapi/pull/5007) by [@atiabbz](https://github.com/atiabbz).
* 📝 Remove unneeded Django/Flask references from async topic intro. PR [#5280](https://github.com/tiangolo/fastapi/pull/5280) by [@carltongibson](https://github.com/carltongibson).
* ✨ Add illustrations for Concurrent burgers and Parallel burgers. PR [#5277](https://github.com/tiangolo/fastapi/pull/5277) by [@tiangolo](https://github.com/tiangolo). Updated docs at: [Concurrency and Burgers](https://fastapi.tiangolo.com/async/#concurrency-and-burgers).

### Translations

* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/query-params.md`. PR [#4775](https://github.com/tiangolo/fastapi/pull/4775) by [@batlopes](https://github.com/batlopes).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/security/first-steps.md`. PR [#4954](https://github.com/tiangolo/fastapi/pull/4954) by [@FLAIR7](https://github.com/FLAIR7).
* 🌐 Add translation for `docs/zh/docs/advanced/response-cookies.md`. PR [#4638](https://github.com/tiangolo/fastapi/pull/4638) by [@zhangbo2012](https://github.com/zhangbo2012).
* 🌐  Add French translation for `docs/fr/docs/deployment/index.md`. PR [#3689](https://github.com/tiangolo/fastapi/pull/3689) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Add Portuguese translation for `tutorial/handling-errors.md`. PR [#4769](https://github.com/tiangolo/fastapi/pull/4769) by [@frnsimoes](https://github.com/frnsimoes).
* 🌐 Add French translation for `docs/fr/docs/history-design-future.md`. PR [#3451](https://github.com/tiangolo/fastapi/pull/3451) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/background-tasks.md`. PR [#4854](https://github.com/tiangolo/fastapi/pull/4854) by [@AdmiralDesu](https://github.com/AdmiralDesu).
* 🌐 Add Chinese translation for `docs/tutorial/security/first-steps.md`. PR [#3841](https://github.com/tiangolo/fastapi/pull/3841) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Japanese translation for `docs/ja/docs/advanced/nosql-databases.md`. PR [#4205](https://github.com/tiangolo/fastapi/pull/4205) by [@sUeharaE4](https://github.com/sUeharaE4).
* 🌐 Add Indonesian translation for `docs/id/docs/tutorial/index.md`. PR [#4705](https://github.com/tiangolo/fastapi/pull/4705) by [@bas-baskara](https://github.com/bas-baskara).
* 🌐 Add Persian translation for `docs/fa/docs/index.md` and tweak right-to-left CSS. PR [#2395](https://github.com/tiangolo/fastapi/pull/2395) by [@mohsen-mahmoodi](https://github.com/mohsen-mahmoodi).

### Internal

* 🔧 Update Jina sponsorship. PR [#5283](https://github.com/tiangolo/fastapi/pull/5283) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Jina sponsorship. PR [#5272](https://github.com/tiangolo/fastapi/pull/5272) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, Striveworks badge. PR [#5179](https://github.com/tiangolo/fastapi/pull/5179) by [@tiangolo](https://github.com/tiangolo).

## 0.79.0

### Fixes - Breaking Changes

* 🐛 Fix removing body from status codes that do not support it. PR [#5145](https://github.com/tiangolo/fastapi/pull/5145) by [@tiangolo](https://github.com/tiangolo).
    * Setting `status_code` to `204`, `304`, or any code below `200` (1xx) will remove the body from the response.
    * This fixes an error in Uvicorn that otherwise would be thrown: `RuntimeError: Response content longer than Content-Length`.
    * This removes `fastapi.openapi.constants.STATUS_CODES_WITH_NO_BODY`, it is replaced by a function in utils.

### Translations

* 🌐 Start of Hebrew translation. PR [#5050](https://github.com/tiangolo/fastapi/pull/5050) by [@itay-raveh](https://github.com/itay-raveh).
* 🔧 Add config for Swedish translations notification. PR [#5147](https://github.com/tiangolo/fastapi/pull/5147) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Start of Swedish translation. PR [#5062](https://github.com/tiangolo/fastapi/pull/5062) by [@MrRawbin](https://github.com/MrRawbin).
* 🌐 Add Japanese translation for `docs/ja/docs/advanced/index.md`. PR [#5043](https://github.com/tiangolo/fastapi/pull/5043) by [@wakabame](https://github.com/wakabame).
* 🌐🇵🇱 Add Polish translation for `docs/pl/docs/tutorial/first-steps.md`. PR [#5024](https://github.com/tiangolo/fastapi/pull/5024) by [@Valaraucoo](https://github.com/Valaraucoo).

### Internal

* 🔧 Update translations notification for Hebrew. PR [#5158](https://github.com/tiangolo/fastapi/pull/5158) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Dependabot commit message. PR [#5156](https://github.com/tiangolo/fastapi/pull/5156) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/upload-artifact from 2 to 3. PR [#5148](https://github.com/tiangolo/fastapi/pull/5148) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/cache from 2 to 3. PR [#5149](https://github.com/tiangolo/fastapi/pull/5149) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update sponsors badge configs. PR [#5155](https://github.com/tiangolo/fastapi/pull/5155) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#5154](https://github.com/tiangolo/fastapi/pull/5154) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Jina sponsor badges. PR [#5151](https://github.com/tiangolo/fastapi/pull/5151) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/checkout from 2 to 3. PR [#5133](https://github.com/tiangolo/fastapi/pull/5133) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5030](https://github.com/tiangolo/fastapi/pull/5030) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump nwtgck/actions-netlify from 1.1.5 to 1.2.3. PR [#5132](https://github.com/tiangolo/fastapi/pull/5132) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump codecov/codecov-action from 2 to 3. PR [#5131](https://github.com/tiangolo/fastapi/pull/5131) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.9.0 to 2.21.1. PR [#5130](https://github.com/tiangolo/fastapi/pull/5130) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 2 to 4. PR [#5129](https://github.com/tiangolo/fastapi/pull/5129) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add Dependabot. PR [#5128](https://github.com/tiangolo/fastapi/pull/5128) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Move from `Optional[X]` to `Union[X, None]` for internal utils. PR [#5124](https://github.com/tiangolo/fastapi/pull/5124) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, remove Dropbase, add Doist. PR [#5096](https://github.com/tiangolo/fastapi/pull/5096) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, remove Classiq, add ImgWhale. PR [#5079](https://github.com/tiangolo/fastapi/pull/5079) by [@tiangolo](https://github.com/tiangolo).

## 0.78.0

### Features

* ✨ Add support for omitting `...` as default value when declaring required parameters with:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

New docs at [Tutorial - Query Parameters and String Validations - Make it required](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#make-it-required). PR [#4906](https://github.com/tiangolo/fastapi/pull/4906) by [@tiangolo](https://github.com/tiangolo).

Up to now, declaring a required parameter while adding additional validation or metadata needed using `...` (Ellipsis).

For example:

```Python
from fastapi import Cookie, FastAPI, Header, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
def main(
    item_id: int = Path(default=..., gt=0),
    query: str = Query(default=..., max_length=10),
    session: str = Cookie(default=..., min_length=3),
    x_trace: str = Header(default=..., title="Tracing header"),
):
    return {"message": "Hello World"}
```

...all these parameters are required because the default value is `...` (Ellipsis).

But now it's possible and supported to just omit the default value, as would be done with Pydantic fields, and the parameters would still be required.

✨ For example, this is now supported:

```Python
from fastapi import Cookie, FastAPI, Header, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
def main(
    item_id: int = Path(gt=0),
    query: str = Query(max_length=10),
    session: str = Cookie(min_length=3),
    x_trace: str = Header(title="Tracing header"),
):
    return {"message": "Hello World"}
```

To declare parameters as optional (not required), you can set a default value as always, for example using `None`:

```Python
from typing import Union
from fastapi import Cookie, FastAPI, Header, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
def main(
    item_id: int = Path(gt=0),
    query: Union[str, None] = Query(default=None, max_length=10),
    session: Union[str, None] = Cookie(default=None, min_length=3),
    x_trace: Union[str, None] = Header(default=None, title="Tracing header"),
):
    return {"message": "Hello World"}
```

### Docs

* 📝 Add docs recommending `Union` over `Optional` and migrate source examples. New docs at [Python Types Intro - Using `Union` or `Optional`](https://fastapi.tiangolo.com/python-types/#using-union-or-optional). PR [#4908](https://github.com/tiangolo/fastapi/pull/4908) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Fix default value as set in tutorial for Path Operations Advanced Configurations. PR [#4899](https://github.com/tiangolo/fastapi/pull/4899) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add documentation for redefined path operations. PR [#4864](https://github.com/tiangolo/fastapi/pull/4864) by [@madkinsz](https://github.com/madkinsz).
* 📝 Updates links for Celery documentation. PR [#4736](https://github.com/tiangolo/fastapi/pull/4736) by [@sammyzord](https://github.com/sammyzord).
* ✏ Fix example code with sets in tutorial for body nested models. PR [#3030](https://github.com/tiangolo/fastapi/pull/3030) by [@hitrust](https://github.com/hitrust).
* ✏ Fix links to Pydantic docs. PR [#4670](https://github.com/tiangolo/fastapi/pull/4670) by [@kinuax](https://github.com/kinuax).
* 📝 Update docs about Swagger UI self-hosting with newer source links. PR [#4813](https://github.com/tiangolo/fastapi/pull/4813) by [@Kastakin](https://github.com/Kastakin).
* 📝 Add link to external article: Building the Poll App From Django Tutorial With FastAPI And React. PR [#4778](https://github.com/tiangolo/fastapi/pull/4778) by [@jbrocher](https://github.com/jbrocher).
* 📝 Add OpenAPI warning to "Body - Fields" docs with extra schema extensions. PR [#4846](https://github.com/tiangolo/fastapi/pull/4846) by [@ml-evs](https://github.com/ml-evs).

### Translations

* 🌐 Fix code examples in Japanese translation for `docs/ja/docs/tutorial/testing.md`. PR [#4623](https://github.com/tiangolo/fastapi/pull/4623) by [@hirotoKirimaru](https://github.com/hirotoKirimaru).

### Internal

* ♻ Refactor dict value extraction to minimize key lookups `fastapi/utils.py`. PR [#3139](https://github.com/tiangolo/fastapi/pull/3139) by [@ShahriyarR](https://github.com/ShahriyarR).
* ✅ Add tests for required nonable parameters and body fields. PR [#4907](https://github.com/tiangolo/fastapi/pull/4907) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix installing Material for MkDocs Insiders in CI. PR [#4897](https://github.com/tiangolo/fastapi/pull/4897) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add pre-commit CI instead of custom GitHub Action. PR [#4896](https://github.com/tiangolo/fastapi/pull/4896) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add pre-commit GitHub Action workflow. PR [#4895](https://github.com/tiangolo/fastapi/pull/4895) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add dark mode auto switch to docs based on OS preference. PR [#4869](https://github.com/tiangolo/fastapi/pull/4869) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🔥 Remove un-used old pending tests, already covered in other places. PR [#4891](https://github.com/tiangolo/fastapi/pull/4891) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add Python formatting hooks to pre-commit. PR [#4890](https://github.com/tiangolo/fastapi/pull/4890) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add pre-commit with first config and first formatting pass. PR [#4888](https://github.com/tiangolo/fastapi/pull/4888) by [@tiangolo](https://github.com/tiangolo).
* 👷 Disable CI installing Material for MkDocs in forks. PR [#4410](https://github.com/tiangolo/fastapi/pull/4410) by [@dolfinus](https://github.com/dolfinus).

## 0.77.1

### Upgrades

* ⬆ Upgrade Starlette from 0.19.0 to 0.19.1. PR [#4819](https://github.com/tiangolo/fastapi/pull/4819) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Add link to german article: REST-API Programmieren mittels Python und dem FastAPI Modul. PR [#4624](https://github.com/tiangolo/fastapi/pull/4624) by [@fschuermeyer](https://github.com/fschuermeyer).
* 📝 Add external link: PyCharm Guide to FastAPI. PR [#4512](https://github.com/tiangolo/fastapi/pull/4512) by [@mukulmantosh](https://github.com/mukulmantosh).
* 📝 Add external link to article: Building an API with FastAPI and Supabase and Deploying on Deta. PR [#4440](https://github.com/tiangolo/fastapi/pull/4440) by [@aUnicornDev](https://github.com/aUnicornDev).
* ✏ Fix small typo in `docs/en/docs/tutorial/security/first-steps.md`. PR [#4515](https://github.com/tiangolo/fastapi/pull/4515) by [@KikoIlievski](https://github.com/KikoIlievski).

### Translations

* 🌐 Add Polish translation for `docs/pl/docs/tutorial/index.md`. PR [#4516](https://github.com/tiangolo/fastapi/pull/4516) by [@MKaczkow](https://github.com/MKaczkow).
* ✏ Fix typo in deployment. PR [#4629](https://github.com/tiangolo/fastapi/pull/4629) by [@raisulislam541](https://github.com/raisulislam541).
* 🌐 Add Portuguese translation for `docs/pt/docs/help-fastapi.md`. PR [#4583](https://github.com/tiangolo/fastapi/pull/4583) by [@mateusjs](https://github.com/mateusjs).

### Internal

* 🔧 Add notifications in issue for Uzbek translations. PR [#4884](https://github.com/tiangolo/fastapi/pull/4884) by [@tiangolo](https://github.com/tiangolo).

## 0.77.0

### Upgrades

* ⬆ Upgrade Starlette from 0.18.0 to 0.19.0. PR [#4488](https://github.com/tiangolo/fastapi/pull/4488) by [@Kludex](https://github.com/Kludex).
    * When creating an explicit `JSONResponse` the `content` argument is now required.

### Docs

* 📝 Add external link to article: Seamless FastAPI Configuration with ConfZ. PR [#4414](https://github.com/tiangolo/fastapi/pull/4414) by [@silvanmelchior](https://github.com/silvanmelchior).
* 📝 Add external link to article: 5 Advanced Features of FastAPI You Should Try. PR [#4436](https://github.com/tiangolo/fastapi/pull/4436) by [@kaustubhgupta](https://github.com/kaustubhgupta).
* ✏ Reword to improve legibility of docs about `TestClient`. PR [#4389](https://github.com/tiangolo/fastapi/pull/4389) by [@rgilton](https://github.com/rgilton).
* 📝 Add external link to blog post about Kafka, FastAPI, and Ably. PR [#4044](https://github.com/tiangolo/fastapi/pull/4044) by [@Ugbot](https://github.com/Ugbot).
* ✏ Fix typo in `docs/en/docs/tutorial/sql-databases.md`. PR [#4875](https://github.com/tiangolo/fastapi/pull/4875) by [@wpyoga](https://github.com/wpyoga).
* ✏ Fix typo in `docs/en/docs/async.md`. PR [#4726](https://github.com/tiangolo/fastapi/pull/4726) by [@Prezu](https://github.com/Prezu).

### Translations

* 🌐 Update source example highlights for `docs/zh/docs/tutorial/query-params-str-validations.md`. PR [#4237](https://github.com/tiangolo/fastapi/pull/4237) by [@caimaoy](https://github.com/caimaoy).
* 🌐 Remove translation docs references to aiofiles as it's no longer needed since AnyIO. PR [#3594](https://github.com/tiangolo/fastapi/pull/3594) by [@alonme](https://github.com/alonme).
* ✏ 🌐 Fix typo in Portuguese translation for `docs/pt/docs/tutorial/path-params.md`. PR [#4722](https://github.com/tiangolo/fastapi/pull/4722) by [@CleoMenezesJr](https://github.com/CleoMenezesJr).
* 🌐 Fix live docs server for translations for some languages. PR [#4729](https://github.com/tiangolo/fastapi/pull/4729) by [@wakabame](https://github.com/wakabame).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/cookie-params.md`. PR [#4112](https://github.com/tiangolo/fastapi/pull/4112) by [@lbmendes](https://github.com/lbmendes).
* 🌐 Fix French translation for `docs/tutorial/body.md`. PR [#4332](https://github.com/tiangolo/fastapi/pull/4332) by [@Smlep](https://github.com/Smlep).
* 🌐 Add Japanese translation for `docs/ja/docs/advanced/conditional-openapi.md`. PR [#2631](https://github.com/tiangolo/fastapi/pull/2631) by [@sh0nk](https://github.com/sh0nk).
* 🌐 Fix Japanese translation of `docs/ja/docs/tutorial/body.md`. PR [#3062](https://github.com/tiangolo/fastapi/pull/3062) by [@a-takahashi223](https://github.com/a-takahashi223).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/background-tasks.md`. PR [#2170](https://github.com/tiangolo/fastapi/pull/2170) by [@izaguerreiro](https://github.com/izaguerreiro).
* 🌐 Add Portuguese translation for `docs/deployment/deta.md`. PR [#4442](https://github.com/tiangolo/fastapi/pull/4442) by [@lsglucas](https://github.com/lsglucas).
* 🌐 Add Russian translation for `docs/async.md`. PR [#4036](https://github.com/tiangolo/fastapi/pull/4036) by [@Winand](https://github.com/Winand).
* 🌐 Add Portuguese translation for `docs/tutorial/body.md`. PR [#3960](https://github.com/tiangolo/fastapi/pull/3960) by [@leandrodesouzadev](https://github.com/leandrodesouzadev).
* 🌐 Add Portuguese translation of `tutorial/extra-data-types.md`. PR [#4077](https://github.com/tiangolo/fastapi/pull/4077) by [@luccasmmg](https://github.com/luccasmmg).
* 🌐 Update German translation for `docs/features.md`. PR [#3905](https://github.com/tiangolo/fastapi/pull/3905) by [@jomue](https://github.com/jomue).

## 0.76.0

### Upgrades

* ⬆ Upgrade Starlette from 0.17.1 to 0.18.0. PR [#4483](https://github.com/tiangolo/fastapi/pull/4483) by [@Kludex](https://github.com/Kludex).

### Internal

* 👥 Update FastAPI People. PR [#4847](https://github.com/tiangolo/fastapi/pull/4847) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Add Budget Insight sponsor. PR [#4824](https://github.com/tiangolo/fastapi/pull/4824) by [@tiangolo](https://github.com/tiangolo).
* 🍱 Update sponsor, ExoFlare badge. PR [#4822](https://github.com/tiangolo/fastapi/pull/4822) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, enable Dropbase again, update TalkPython link. PR [#4821](https://github.com/tiangolo/fastapi/pull/4821) by [@tiangolo](https://github.com/tiangolo).

## 0.75.2

This release includes upgrades to third-party packages that handle security issues. Although there's a chance these issues don't affect you in particular, please upgrade as soon as possible.

### Fixes

* ✅ Fix new/recent tests with new fixed `ValidationError` JSON Schema. PR [#4806](https://github.com/tiangolo/fastapi/pull/4806) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix JSON Schema for `ValidationError` at field `loc`. PR [#3810](https://github.com/tiangolo/fastapi/pull/3810) by [@dconathan](https://github.com/dconathan).
* 🐛 Fix support for prefix on APIRouter WebSockets. PR [#2640](https://github.com/tiangolo/fastapi/pull/2640) by [@Kludex](https://github.com/Kludex).

### Upgrades

* ⬆️ Update ujson ranges for CVE-2021-45958. PR [#4804](https://github.com/tiangolo/fastapi/pull/4804) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade dependencies upper range for extras "all". PR [#4803](https://github.com/tiangolo/fastapi/pull/4803) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Upgrade Swagger UI - swagger-ui-dist@4. This handles a security issue in Swagger UI itself where it could be possible to inject HTML into Swagger UI. Please upgrade as soon as you can, in particular if you expose your Swagger UI (`/docs`) publicly to non-expert users. PR [#4347](https://github.com/tiangolo/fastapi/pull/4347) by [@RAlanWright](https://github.com/RAlanWright).

### Internal

* 🔧 Update sponsors, add: ExoFlare, Ines Course; remove: Dropbase, Vim.so, Calmcode; update: Striveworks, TalkPython and TestDriven.io. PR [#4805](https://github.com/tiangolo/fastapi/pull/4805) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade Codecov GitHub Action. PR [#4801](https://github.com/tiangolo/fastapi/pull/4801) by [@tiangolo](https://github.com/tiangolo).

## 0.75.1

### Translations

* 🌐 Start Dutch translations. PR [#4703](https://github.com/tiangolo/fastapi/pull/4703) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Start Persian/Farsi translations. PR [#4243](https://github.com/tiangolo/fastapi/pull/4243) by [@aminalaee](https://github.com/aminalaee).
* ✏ Reword sentence about handling errors. PR [#1993](https://github.com/tiangolo/fastapi/pull/1993) by [@khuhroproeza](https://github.com/khuhroproeza).

### Internal

* 👥 Update FastAPI People. PR [#4752](https://github.com/tiangolo/fastapi/pull/4752) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ➖ Temporarily remove typer-cli from dependencies and upgrade Black to unblock Pydantic CI. PR [#4754](https://github.com/tiangolo/fastapi/pull/4754) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add configuration to notify Dutch translations. PR [#4702](https://github.com/tiangolo/fastapi/pull/4702) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#4699](https://github.com/tiangolo/fastapi/pull/4699) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🐛 Fix FastAPI People generation to include missing file in commit. PR [#4695](https://github.com/tiangolo/fastapi/pull/4695) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Classiq sponsor links. PR [#4688](https://github.com/tiangolo/fastapi/pull/4688) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add Classiq sponsor. PR [#4671](https://github.com/tiangolo/fastapi/pull/4671) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add Jina's QA Bot to the docs to help people that want to ask quick questions. PR [#4655](https://github.com/tiangolo/fastapi/pull/4655) by [@tiangolo](https://github.com/tiangolo) based on original PR [#4626](https://github.com/tiangolo/fastapi/pull/4626) by [@hanxiao](https://github.com/hanxiao).

## 0.75.0

### Features

* ✨ Add support for custom `generate_unique_id_function` and docs for generating clients. New docs: [Advanced - Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/). PR [#4650](https://github.com/tiangolo/fastapi/pull/4650) by [@tiangolo](https://github.com/tiangolo).

## 0.74.1

### Features

* ✨ Include route in scope to allow middleware and other tools to extract its information. PR [#4603](https://github.com/tiangolo/fastapi/pull/4603) by [@tiangolo](https://github.com/tiangolo).

## 0.74.0

### Breaking Changes

* ✨ Update internal `AsyncExitStack` to fix context for dependencies with `yield`. PR [#4575](https://github.com/tiangolo/fastapi/pull/4575) by [@tiangolo](https://github.com/tiangolo).

Dependencies with `yield` can now catch `HTTPException` and custom exceptions. For example:

```Python
async def get_database():
    with Session() as session:
        try:
            yield session
        except HTTPException:
            session.rollback()
            raise
        finally:
            session.close()
```

After the dependency with `yield` handles the exception (or not) the exception is raised again. So that any exception handlers can catch it, or ultimately the default internal `ServerErrorMiddleware`.

If you depended on exceptions not being received by dependencies with `yield`, and receiving an exception breaks the code after `yield`, you can use a block with `try` and `finally`:

```Python
async def do_something():
    try:
        yield something
    finally:
        some_cleanup()
```

...that way the `finally` block is run regardless of any exception that might happen.

### Features

* The same PR [#4575](https://github.com/tiangolo/fastapi/pull/4575) from above also fixes the `contextvars` context for the code before and after `yield`. This was the main objective of that PR.

This means that now, if you set a value in a context variable before `yield`, the value would still be available after `yield` (as you would intuitively expect). And it also means that you can reset the context variable with a token afterwards.

For example, this works correctly now:

```Python
from contextvars import ContextVar
from typing import Any, Dict, Optional


legacy_request_state_context_var: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "legacy_request_state_context_var", default=None
)

async def set_up_request_state_dependency():
    request_state = {"user": "deadpond"}
    contextvar_token = legacy_request_state_context_var.set(request_state)
    yield request_state
    legacy_request_state_context_var.reset(contextvar_token)
```

...before this change it would raise an error when resetting the context variable, because the `contextvars` context was different, because of the way it was implemented.

**Note**: You probably don't need `contextvars`, and you should probably avoid using them. But they are powerful and useful in some advanced scenarios, for example, migrating from code that used Flask's `g` semi-global variable.

**Technical Details**: If you want to know more of the technical details you can check out the PR description [#4575](https://github.com/tiangolo/fastapi/pull/4575).

### Internal

* 🔧 Add Striveworks sponsor. PR [#4596](https://github.com/tiangolo/fastapi/pull/4596) by [@tiangolo](https://github.com/tiangolo).
* 💚 Only build docs on push when on master to avoid duplicate runs from PRs. PR [#4564](https://github.com/tiangolo/fastapi/pull/4564) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#4502](https://github.com/tiangolo/fastapi/pull/4502) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.73.0

### Features

* ✨ Add support for declaring `UploadFile` parameters without explicit `File()`. PR [#4469](https://github.com/tiangolo/fastapi/pull/4469) by [@tiangolo](https://github.com/tiangolo). New docs: [Request Files - File Parameters with UploadFile](https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile).
* ✨ Add support for tags with Enums. PR [#4468](https://github.com/tiangolo/fastapi/pull/4468) by [@tiangolo](https://github.com/tiangolo). New docs: [Path Operation Configuration - Tags with Enums](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags-with-enums).
* ✨ Allow hiding from OpenAPI (and Swagger UI) `Query`, `Cookie`, `Header`, and `Path` parameters. PR [#3144](https://github.com/tiangolo/fastapi/pull/3144) by [@astraldawn](https://github.com/astraldawn). New docs: [Query Parameters and String Validations - Exclude from OpenAPI](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).

### Docs

* 📝 Tweak and improve docs for Request Files. PR [#4470](https://github.com/tiangolo/fastapi/pull/4470) by [@tiangolo](https://github.com/tiangolo).

### Fixes

* 🐛 Fix bug preventing to use OpenAPI when using tuples. PR [#3874](https://github.com/tiangolo/fastapi/pull/3874) by [@victorbenichoux](https://github.com/victorbenichoux).
* 🐛 Prefer custom encoder over defaults if specified in `jsonable_encoder`. PR [#2061](https://github.com/tiangolo/fastapi/pull/2061) by [@viveksunder](https://github.com/viveksunder).
    * 💚 Duplicate PR to trigger CI. PR [#4467](https://github.com/tiangolo/fastapi/pull/4467) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🐛 Fix docs dependencies cache, to get the latest Material for MkDocs. PR [#4466](https://github.com/tiangolo/fastapi/pull/4466) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add sponsor Dropbase. PR [#4465](https://github.com/tiangolo/fastapi/pull/4465) by [@tiangolo](https://github.com/tiangolo).

## 0.72.0

### Features

* ✨ Enable configuring Swagger UI parameters. Original PR [#2568](https://github.com/tiangolo/fastapi/pull/2568) by [@jmriebold](https://github.com/jmriebold). Here are the new docs: [Configuring Swagger UI](https://fastapi.tiangolo.com/advanced/extending-openapi/#configuring-swagger-ui).

### Docs

* 📝 Update Python Types docs, add missing 3.6 / 3.9 example. PR [#4434](https://github.com/tiangolo/fastapi/pull/4434) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update Chinese translation for `docs/help-fastapi.md`. PR [#3847](https://github.com/tiangolo/fastapi/pull/3847) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Fix Korean translation for `docs/ko/docs/index.md`. PR [#4195](https://github.com/tiangolo/fastapi/pull/4195) by [@kty4119](https://github.com/kty4119).
* 🌐 Add Polish translation for `docs/pl/docs/index.md`. PR [#4245](https://github.com/tiangolo/fastapi/pull/4245) by [@MicroPanda123](https://github.com/MicroPanda123).
* 🌐 Add Chinese translation for `docs\tutorial\path-operation-configuration.md`. PR [#3312](https://github.com/tiangolo/fastapi/pull/3312) by [@jaystone776](https://github.com/jaystone776).

### Internal

* 🔧 Enable MkDocs Material Insiders' `content.tabs.link`. PR [#4399](https://github.com/tiangolo/fastapi/pull/4399) by [@tiangolo](https://github.com/tiangolo).

## 0.71.0

### Features

* ✨ Add docs and tests for Python 3.9 and Python 3.10. PR [#3712](https://github.com/tiangolo/fastapi/pull/3712) by [@tiangolo](https://github.com/tiangolo).
    * You can start with [Python Types Intro](https://fastapi.tiangolo.com/python-types/), it explains what changes between different Python versions, in Python 3.9 and in Python 3.10.
    * All the FastAPI docs are updated. Each code example in the docs that could use different syntax in Python 3.9 or Python 3.10 now has all the alternatives in tabs.
* ⬆️ Upgrade Starlette to 0.17.1. PR [#4145](https://github.com/tiangolo/fastapi/pull/4145) by [@simondale00](https://github.com/simondale00).

### Internal

* 👥 Update FastAPI People. PR [#4354](https://github.com/tiangolo/fastapi/pull/4354) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Add FastAPI Trove Classifier for PyPI as now there's one 🤷😁. PR [#4386](https://github.com/tiangolo/fastapi/pull/4386) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Upgrade MkDocs Material and configs. PR [#4385](https://github.com/tiangolo/fastapi/pull/4385) by [@tiangolo](https://github.com/tiangolo).

## 0.70.1

There's nothing interesting in this particular FastAPI release. It is mainly to enable/unblock the release of the next version of Pydantic that comes packed with features and improvements. 🤩

### Fixes

* 🐛 Fix JSON Schema for dataclasses, supporting the fixes in Pydantic 1.9. PR [#4272](https://github.com/tiangolo/fastapi/pull/4272) by [@PrettyWood](https://github.com/PrettyWood).

### Translations

* 🌐 Add Korean translation for `docs/tutorial/request-forms-and-files.md`. PR [#3744](https://github.com/tiangolo/fastapi/pull/3744) by [@NinaHwang](https://github.com/NinaHwang).
* 🌐 Add Korean translation for `docs/tutorial/request-files.md`. PR [#3743](https://github.com/tiangolo/fastapi/pull/3743) by [@NinaHwang](https://github.com/NinaHwang).
* 🌐 Add portuguese translation for `docs/tutorial/query-params-str-validations.md`. PR [#3965](https://github.com/tiangolo/fastapi/pull/3965) by [@leandrodesouzadev](https://github.com/leandrodesouzadev).
* 🌐 Add Korean translation for `docs/tutorial/response-status-code.md`. PR [#3742](https://github.com/tiangolo/fastapi/pull/3742) by [@NinaHwang](https://github.com/NinaHwang).
* 🌐 Add Korean translation for Tutorial - JSON Compatible Encoder. PR [#3152](https://github.com/tiangolo/fastapi/pull/3152) by [@NEONKID](https://github.com/NEONKID).
* 🌐 Add Korean translation for Tutorial - Path Parameters and Numeric Validations. PR [#2432](https://github.com/tiangolo/fastapi/pull/2432) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/deployment/versions.md`. PR [#4121](https://github.com/tiangolo/fastapi/pull/4121) by [@DevDae](https://github.com/DevDae).
* 🌐 Fix Korean translation for `docs/ko/docs/tutorial/index.md`. PR [#4193](https://github.com/tiangolo/fastapi/pull/4193) by [@kimjaeyoonn](https://github.com/kimjaeyoonn).
* 🔧 Add CryptAPI sponsor. PR [#4264](https://github.com/tiangolo/fastapi/pull/4264) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update `docs/tutorial/dependencies/classes-as-dependencies`: Add type of query parameters in a description of `Classes as dependencies`. PR [#4015](https://github.com/tiangolo/fastapi/pull/4015) by [@0417taehyun](https://github.com/0417taehyun).
* 🌐 Add French translation for Tutorial - First steps. PR [#3455](https://github.com/tiangolo/fastapi/pull/3455) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for `docs/tutorial/path-params.md`. PR [#3548](https://github.com/tiangolo/fastapi/pull/3548) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for `docs/tutorial/query-params.md`. PR [#3556](https://github.com/tiangolo/fastapi/pull/3556) by [@Smlep](https://github.com/Smlep).
* 🌐 Add Turkish translation for `docs/python-types.md`. PR [#3926](https://github.com/tiangolo/fastapi/pull/3926) by [@BilalAlpaslan](https://github.com/BilalAlpaslan).

### Internal

* 👥 Update FastAPI People. PR [#4274](https://github.com/tiangolo/fastapi/pull/4274) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.70.0

This release just upgrades Starlette to the latest version, `0.16.0`, which includes several bug fixes and some small breaking changes.

These last **three consecutive releases** are independent so that you can **migrate gradually**:

* First to FastAPI `0.68.2`, with no breaking changes, but upgrading all the sub-dependencies.
* Next to FastAPI `0.69.0`, which upgrades Starlette to `0.15.0`, with AnyIO support, and a higher chance of having breaking changes in your code.
* Finally to FastAPI `0.70.0`, just upgrading Starlette to the latest version `0.16.0` with additional bug fixes.

This way, in case there was a breaking change for your code in one of the releases, you can still benefit from the previous upgrades. ✨

### Breaking Changes - Upgrade

* ⬆️ Upgrade Starlette to 0.16.0. PR [#4016](https://github.com/tiangolo/fastapi/pull/4016) by [@tiangolo](https://github.com/tiangolo).

Also upgrades the ranges of optional dependencies:

* `"jinja2 >=2.11.2,<4.0.0"`
* `"itsdangerous >=1.1.0,<3.0.0"`

## 0.69.0

### Breaking Changes - Upgrade

This release adds support for [Trio](https://trio.readthedocs.io/en/stable/). ✨

It upgrades the version of Starlette to `0.15.0`, now based on [AnyIO](https://anyio.readthedocs.io/en/stable/), and the internal async components in **FastAPI** are now based on AnyIO as well, making it compatible with both **asyncio** and **Trio**.

You can read the docs about running [FastAPI with Trio using Hypercorn](https://fastapi.tiangolo.com/deployment/manually/#hypercorn-with-trio).

This release also removes `graphene` as an optional dependency for GraphQL. If you need to work with GraphQL, the recommended library now is [Strawberry](https://strawberry.rocks/). You can read the new [FastAPI with GraphQL docs](https://fastapi.tiangolo.com/advanced/graphql/).

### Features

* ✨ Add support for Trio via AnyIO, upgrading Starlette to `0.15.0`. PR [#3372](https://github.com/tiangolo/fastapi/pull/3372) by [@graingert](https://github.com/graingert).
* ➖ Remove `graphene` as an optional dependency. PR [#4007](https://github.com/tiangolo/fastapi/pull/4007) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Add docs for using Trio with Hypercorn. PR [#4014](https://github.com/tiangolo/fastapi/pull/4014) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typos in Deployment Guide. PR [#3975](https://github.com/tiangolo/fastapi/pull/3975) by [@ghandic](https://github.com/ghandic).
* 📝 Update docs with pip install calls when using extras with brackets, use quotes for compatibility with Zsh. PR [#3131](https://github.com/tiangolo/fastapi/pull/3131) by [@tomwei7](https://github.com/tomwei7).
* 📝 Add external link to article: Deploying ML Models as API Using FastAPI and Heroku. PR [#3904](https://github.com/tiangolo/fastapi/pull/3904) by [@kaustubhgupta](https://github.com/kaustubhgupta).
* ✏ Fix typo in file paths in `docs/en/docs/contributing.md`. PR [#3752](https://github.com/tiangolo/fastapi/pull/3752) by [@NinaHwang](https://github.com/NinaHwang).
* ✏ Fix a typo in `docs/en/docs/advanced/path-operation-advanced-configuration.md` and `docs/en/docs/release-notes.md`. PR [#3750](https://github.com/tiangolo/fastapi/pull/3750) by [@saintmalik](https://github.com/saintmalik).
* ✏️ Add a missing comma in the security tutorial. PR [#3564](https://github.com/tiangolo/fastapi/pull/3564) by [@jalvaradosegura](https://github.com/jalvaradosegura).
* ✏ Fix typo in `docs/en/docs/help-fastapi.md`. PR [#3760](https://github.com/tiangolo/fastapi/pull/3760) by [@jaystone776](https://github.com/jaystone776).
* ✏ Fix typo about file path in `docs/en/docs/tutorial/bigger-applications.md`. PR [#3285](https://github.com/tiangolo/fastapi/pull/3285) by [@HolyDorus](https://github.com/HolyDorus).
* ✏ Re-word to clarify test client in `docs/en/docs/tutorial/testing.md`. PR [#3382](https://github.com/tiangolo/fastapi/pull/3382) by [@Bharat123rox](https://github.com/Bharat123rox).
* 📝  Fix incorrect highlighted code. PR [#3325](https://github.com/tiangolo/fastapi/pull/3325) by [@paxcodes](https://github.com/paxcodes).
* 📝 Add external link to article: How-to deploy FastAPI app to Heroku. PR [#3241](https://github.com/tiangolo/fastapi/pull/3241) by [@Jarmos-san](https://github.com/Jarmos-san).
* ✏ Fix typo (mistranslation) in `docs/en/docs/advanced/templates.md`. PR [#3211](https://github.com/tiangolo/fastapi/pull/3211) by [@oerpli](https://github.com/oerpli).
* 📝 Remove note about (now supported) feature from Swagger UI in `docs/en/docs/tutorial/request-files.md`. PR [#2803](https://github.com/tiangolo/fastapi/pull/2803) by [@gsganden](https://github.com/gsganden).
* ✏ Fix typo re-word in `docs/tutorial/handling-errors.md`. PR [#2700](https://github.com/tiangolo/fastapi/pull/2700) by [@graue70](https://github.com/graue70).

### Translations

* 🌐 Initialize Azerbaijani translations. PR [#3941](https://github.com/tiangolo/fastapi/pull/3941) by [@madatbay](https://github.com/madatbay).
* 🌐 Add Turkish translation for `docs/fastapi-people.md`. PR [#3848](https://github.com/tiangolo/fastapi/pull/3848) by [@BilalAlpaslan](https://github.com/BilalAlpaslan).

### Internal

* 📝 Add supported Python versions badge. PR [#2794](https://github.com/tiangolo/fastapi/pull/2794) by [@hramezani](https://github.com/hramezani).
* ✏ Fix link in Japanese docs for `docs/ja/docs/deployment/docker.md`. PR [#3245](https://github.com/tiangolo/fastapi/pull/3245) by [@utamori](https://github.com/utamori).
* 🔧 Correct DeprecationWarning config and comment in pytest settings. PR [#4008](https://github.com/tiangolo/fastapi/pull/4008) by [@graingert](https://github.com/graingert).
* 🔧 Swap light/dark theme button icon. PR [#3246](https://github.com/tiangolo/fastapi/pull/3246) by [@eddsalkield](https://github.com/eddsalkield).
* 🔧 Lint only in Python 3.7 and above. PR [#4006](https://github.com/tiangolo/fastapi/pull/4006) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add GitHub Action notify-translations config for Azerbaijani. PR [#3995](https://github.com/tiangolo/fastapi/pull/3995) by [@tiangolo](https://github.com/tiangolo).

## 0.68.2

This release has **no breaking changes**. 🎉

It upgrades the version ranges of sub-dependencies to allow applications using FastAPI to easily upgrade them.

Soon there will be a new FastAPI release upgrading Starlette to take advantage of recent improvements, but as that has a higher chance of having breaking changes, it will be in a separate release.

### Features

* ⬆Increase supported version of aiofiles to suppress warnings. PR [#2899](https://github.com/tiangolo/fastapi/pull/2899) by [@SnkSynthesis](https://github.com/SnkSynthesis).
* ➖ Do not require backports in Python >= 3.7. PR [#1880](https://github.com/tiangolo/fastapi/pull/1880) by [@FFY00](https://github.com/FFY00).
* ⬆ Upgrade required Python version to >= 3.6.1, needed by typing.Deque, used by Pydantic. PR [#2733](https://github.com/tiangolo/fastapi/pull/2733) by [@hukkin](https://github.com/hukkin).
* ⬆️ Bump Uvicorn max range to 0.15.0. PR [#3345](https://github.com/tiangolo/fastapi/pull/3345) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Update GraphQL docs, recommend Strawberry. PR [#3981](https://github.com/tiangolo/fastapi/pull/3981) by [@tiangolo](https://github.com/tiangolo).
* 📝 Re-write and extend Deployment guide: Concepts, Uvicorn, Gunicorn, Docker, Containers, Kubernetes. PR [#3974](https://github.com/tiangolo/fastapi/pull/3974) by [@tiangolo](https://github.com/tiangolo).
* 📝 Upgrade HTTPS guide with more explanations and diagrams. PR [#3950](https://github.com/tiangolo/fastapi/pull/3950) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Turkish translation for `docs/features.md`. PR [#1950](https://github.com/tiangolo/fastapi/pull/1950) by [@ycd](https://github.com/ycd).
* 🌐 Add Turkish translation for `docs/benchmarks.md`. PR [#2729](https://github.com/tiangolo/fastapi/pull/2729) by [@Telomeraz](https://github.com/Telomeraz).
* 🌐 Add Turkish translation for `docs/index.md`. PR [#1908](https://github.com/tiangolo/fastapi/pull/1908) by [@ycd](https://github.com/ycd).
* 🌐 Add French translation for `docs/tutorial/body.md`. PR [#3671](https://github.com/tiangolo/fastapi/pull/3671) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for `deployment/docker.md`. PR [#3694](https://github.com/tiangolo/fastapi/pull/3694) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Add Portuguese translation for `docs/tutorial/path-params.md`. PR [#3664](https://github.com/tiangolo/fastapi/pull/3664) by [@FelipeSilva93](https://github.com/FelipeSilva93).
* 🌐 Add Portuguese translation for `docs/deployment/https.md`. PR [#3754](https://github.com/tiangolo/fastapi/pull/3754) by [@lsglucas](https://github.com/lsglucas).
* 🌐 Add German translation for `docs/features.md`. PR [#3699](https://github.com/tiangolo/fastapi/pull/3699) by [@mawassk](https://github.com/mawassk).

### Internal

* ✨ Update GitHub Action: notify-translations, to avoid a race conditions. PR [#3989](https://github.com/tiangolo/fastapi/pull/3989) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade development `autoflake`, supporting multi-line imports. PR [#3988](https://github.com/tiangolo/fastapi/pull/3988) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Increase dependency ranges for tests and docs: pytest-cov, pytest-asyncio, black, httpx, sqlalchemy, databases, mkdocs-markdownextradata-plugin. PR [#3987](https://github.com/tiangolo/fastapi/pull/3987) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#3986](https://github.com/tiangolo/fastapi/pull/3986) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 💚 Fix badges in README and main page. PR [#3979](https://github.com/tiangolo/fastapi/pull/3979) by [@ghandic](https://github.com/ghandic).
* ⬆ Upgrade internal testing dependencies: mypy to version 0.910, add newly needed type packages. PR [#3350](https://github.com/tiangolo/fastapi/pull/3350) by [@ArcLightSlavik](https://github.com/ArcLightSlavik).
* ✨ Add Deepset Sponsorship. PR [#3976](https://github.com/tiangolo/fastapi/pull/3976) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Tweak CSS styles for shell animations. PR [#3888](https://github.com/tiangolo/fastapi/pull/3888) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Sponsor Calmcode.io. PR [#3777](https://github.com/tiangolo/fastapi/pull/3777) by [@tiangolo](https://github.com/tiangolo).

## 0.68.1

* ✨ Add support for `read_with_orm_mode`, to support [SQLModel](https://sqlmodel.tiangolo.com/) relationship attributes. PR [#3757](https://github.com/tiangolo/fastapi/pull/3757) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Portuguese translation of `docs/fastapi-people.md`. PR [#3461](https://github.com/tiangolo/fastapi/pull/3461) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#3492](https://github.com/tiangolo/fastapi/pull/3492) by [@jaystone776](https://github.com/jaystone776).
* 🔧 Add new Translation tracking issues for German and Indonesian. PR [#3718](https://github.com/tiangolo/fastapi/pull/3718) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/sub-dependencies.md`. PR [#3491](https://github.com/tiangolo/fastapi/pull/3491) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Portuguese translation for `docs/advanced/index.md`. PR [#3460](https://github.com/tiangolo/fastapi/pull/3460) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🌐 Portuguese translation of `docs/async.md`. PR [#1330](https://github.com/tiangolo/fastapi/pull/1330) by [@Serrones](https://github.com/Serrones).
* 🌐 Add French translation for `docs/async.md`. PR [#3416](https://github.com/tiangolo/fastapi/pull/3416) by [@Smlep](https://github.com/Smlep).

### Internal

* ✨ Add GitHub Action: Notify Translations. PR [#3715](https://github.com/tiangolo/fastapi/pull/3715) by [@tiangolo](https://github.com/tiangolo).
* ✨ Update computation of FastAPI People and sponsors. PR [#3714](https://github.com/tiangolo/fastapi/pull/3714) by [@tiangolo](https://github.com/tiangolo).
* ✨ Enable recent Material for MkDocs Insiders features. PR [#3710](https://github.com/tiangolo/fastapi/pull/3710) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove/clean extra imports from examples in docs for features. PR [#3709](https://github.com/tiangolo/fastapi/pull/3709) by [@tiangolo](https://github.com/tiangolo).
* ➕ Update docs library to include sources in Markdown. PR [#3648](https://github.com/tiangolo/fastapi/pull/3648) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Enable tests for Python 3.9. PR [#2298](https://github.com/tiangolo/fastapi/pull/2298) by [@Kludex](https://github.com/Kludex).
* 👥 Update FastAPI People. PR [#3642](https://github.com/tiangolo/fastapi/pull/3642) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.68.0

### Features

* ✨ Add support for extensions and updates to the OpenAPI schema in each *path operation*. New docs: [FastAPI Path Operation Advanced Configuration - OpenAPI Extra](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#openapi-extra). Initial PR [#1922](https://github.com/tiangolo/fastapi/pull/1922) by [@edouardlp](https://github.com/edouardlp).
* ✨ Add additional OpenAPI metadata parameters to `FastAPI` class, shown on the automatic API docs UI. New docs: [Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/). Initial PR [#1812](https://github.com/tiangolo/fastapi/pull/1812) by [@dkreeft](https://github.com/dkreeft).
* ✨ Add `description` parameter to all the security scheme classes, e.g. `APIKeyQuery(name="key", description="A very cool API key")`. PR [#1757](https://github.com/tiangolo/fastapi/pull/1757) by [@hylkepostma](https://github.com/hylkepostma).
* ✨ Update OpenAPI models, supporting recursive models and extensions. PR [#3628](https://github.com/tiangolo/fastapi/pull/3628) by [@tiangolo](https://github.com/tiangolo).
* ✨ Import and re-export data structures from Starlette, used by Request properties, on `fastapi.datastructures`. Initial PR [#1872](https://github.com/tiangolo/fastapi/pull/1872) by [@jamescurtin](https://github.com/jamescurtin).

### Docs

* 📝 Update docs about async and response-model with more gender neutral language. PR [#1869](https://github.com/tiangolo/fastapi/pull/1869) by [@Edward-Knight](https://github.com/Edward-Knight).

### Translations

* 🌐 Add Russian translation for `docs/python-types.md`. PR [#3039](https://github.com/tiangolo/fastapi/pull/3039) by [@dukkee](https://github.com/dukkee).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/index.md`. PR [#3489](https://github.com/tiangolo/fastapi/pull/3489) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Russian translation for `docs/external-links.md`. PR [#3036](https://github.com/tiangolo/fastapi/pull/3036) by [@dukkee](https://github.com/dukkee).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/global-dependencies.md`. PR [#3493](https://github.com/tiangolo/fastapi/pull/3493) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Portuguese translation for `docs/deployment/versions.md`. PR [#3618](https://github.com/tiangolo/fastapi/pull/3618) by [@lsglucas](https://github.com/lsglucas).
* 🌐 Add Japanese translation for `docs/tutorial/security/oauth2-jwt.md`. PR [#3526](https://github.com/tiangolo/fastapi/pull/3526) by [@sattosan](https://github.com/sattosan).

### Internal

* ✅ Add  the `docs_src` directory to test coverage and update tests. Initial PR [#1904](https://github.com/tiangolo/fastapi/pull/1904) by [@Kludex](https://github.com/Kludex).
* 🔧 Add new GitHub templates with forms for new issues. PR [#3612](https://github.com/tiangolo/fastapi/pull/3612) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add official FastAPI Twitter to docs: [@fastapi](https://twitter.com/fastapi). PR [#3578](https://github.com/tiangolo/fastapi/pull/3578) by [@tiangolo](https://github.com/tiangolo).

## 0.67.0

### Features

* ✨ Add support for `dataclasses` in request bodies and `response_model`. New documentation: [Advanced User Guide - Using Dataclasses](https://fastapi.tiangolo.com/advanced/dataclasses/). PR [#3577](https://github.com/tiangolo/fastapi/pull/3577) by [@tiangolo](https://github.com/tiangolo).
* ✨ Support `dataclasses` in responses. PR [#3576](https://github.com/tiangolo/fastapi/pull/3576) by [@tiangolo](https://github.com/tiangolo), continuation from initial PR [#2722](https://github.com/tiangolo/fastapi/pull/2722) by [@amitlissack](https://github.com/amitlissack).

### Docs

* 📝 Add external link: How to Create A Fake Certificate Authority And Generate TLS Certs for FastAPI. PR [#2839](https://github.com/tiangolo/fastapi/pull/2839) by [@aitoehigie](https://github.com/aitoehigie).
* ✏ Fix code highlighted line in: `body-nested-models.md`. PR [#3463](https://github.com/tiangolo/fastapi/pull/3463) by [@jaystone776](https://github.com/jaystone776).
* ✏ Fix typo in `body-nested-models.md`. PR [#3462](https://github.com/tiangolo/fastapi/pull/3462) by [@jaystone776](https://github.com/jaystone776).
* ✏ Fix typo "might me" -> "might be" in `docs/en/docs/tutorial/schema-extra-example.md`. PR [#3362](https://github.com/tiangolo/fastapi/pull/3362) by [@dbrakman](https://github.com/dbrakman).
* 📝 Add external link: Building simple E-Commerce with NuxtJS and FastAPI. PR [#3271](https://github.com/tiangolo/fastapi/pull/3271) by [@ShahriyarR](https://github.com/ShahriyarR).
* 📝 Add external link: Serve a machine learning model using Sklearn, FastAPI and Docker. PR [#2974](https://github.com/tiangolo/fastapi/pull/2974) by [@rodrigo-arenas](https://github.com/rodrigo-arenas).
* ✏️ Fix typo on docstring in datastructures file. PR [#2887](https://github.com/tiangolo/fastapi/pull/2887) by [@Kludex](https://github.com/Kludex).
* 📝 Add External Link: Deploy FastAPI on Ubuntu and Serve using Caddy 2 Web Server. PR [#3572](https://github.com/tiangolo/fastapi/pull/3572) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add External Link, replaces #1898. PR [#3571](https://github.com/tiangolo/fastapi/pull/3571) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🎨 Improve style for sponsors, add radius border. PR [#2388](https://github.com/tiangolo/fastapi/pull/2388) by [@Kludex](https://github.com/Kludex).
* 👷 Update GitHub Action latest-changes. PR [#3574](https://github.com/tiangolo/fastapi/pull/3574) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action latest-changes. PR [#3573](https://github.com/tiangolo/fastapi/pull/3573) by [@tiangolo](https://github.com/tiangolo).
* 👷 Rename and clarify CI workflow job names. PR [#3570](https://github.com/tiangolo/fastapi/pull/3570) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action latest-changes, strike 2 ⚾. PR [#3575](https://github.com/tiangolo/fastapi/pull/3575) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Sort external links in docs to have the most recent at the top. PR [#3568](https://github.com/tiangolo/fastapi/pull/3568) by [@tiangolo](https://github.com/tiangolo).

## 0.66.1

### Translations

* 🌐 Add basic setup for German translations. PR [#3522](https://github.com/tiangolo/fastapi/pull/3522) by [@0x4Dark](https://github.com/0x4Dark).
* 🌐 Add Portuguese translation for `docs/tutorial/security/index.md`. PR [#3507](https://github.com/tiangolo/fastapi/pull/3507) by [@oandersonmagalhaes](https://github.com/oandersonmagalhaes).
* 🌐 Add Portuguese translation for `docs/deployment/index.md`. PR [#3337](https://github.com/tiangolo/fastapi/pull/3337) by [@lsglucas](https://github.com/lsglucas).

### Internal

* 🔧 Configure strict pytest options and update/refactor tests. Upgrade pytest to `>=6.2.4,<7.0.0` and pytest-cov to `>=2.12.0,<3.0.0`. Initial PR [#2790](https://github.com/tiangolo/fastapi/pull/2790) by [@graingert](https://github.com/graingert).
* ⬆️ Upgrade python-jose dependency to `>=3.3.0,<4.0.0` for tests. PR [#3468](https://github.com/tiangolo/fastapi/pull/3468) by [@tiangolo](https://github.com/tiangolo).

## 0.66.0

### Features

* ✨ Allow setting the `response_class` to `RedirectResponse` or `FileResponse` and returning the URL from the function. New and updated docs are in the tutorial section **Custom Response - HTML, Stream, File, others**, in [RedirectResponse](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse) and in [FileResponse](https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse). PR [#3457](https://github.com/tiangolo/fastapi/pull/3457) by [@tiangolo](https://github.com/tiangolo).

### Fixes

* 🐛 Fix include/exclude for dicts in `jsonable_encoder`. PR [#2016](https://github.com/tiangolo/fastapi/pull/2016) by [@Rubikoid](https://github.com/Rubikoid).
* 🐛 Support custom OpenAPI / JSON Schema fields in the generated output OpenAPI. PR [#1429](https://github.com/tiangolo/fastapi/pull/1429) by [@jmagnusson](https://github.com/jmagnusson).

### Translations

* 🌐 Add Spanish translation for `tutorial/query-params.md`. PR [#2243](https://github.com/tiangolo/fastapi/pull/2243) by [@mariacamilagl](https://github.com/mariacamilagl).
* 🌐 Add Spanish translation for `advanced/response-directly.md`. PR [#1253](https://github.com/tiangolo/fastapi/pull/1253) by [@jfunez](https://github.com/jfunez).
* 🌐 Add Spanish translation for `advanced/additional-status-codes.md`. PR [#1252](https://github.com/tiangolo/fastapi/pull/1252) by [@jfunez](https://github.com/jfunez).
* 🌐 Add Spanish translation for `advanced/path-operation-advanced-configuration.md`. PR [#1251](https://github.com/tiangolo/fastapi/pull/1251) by [@jfunez](https://github.com/jfunez).

## 0.65.3

### Fixes

* ♻ Assume request bodies contain JSON when no Content-Type header is provided. This fixes a breaking change introduced by [0.65.2 with PR #2118](https://github.com/tiangolo/fastapi/pull/2118). It should allow upgrading FastAPI applications with clients that send JSON data without a `Content-Type` header. And there's still protection against CSRFs. PR [#3456](https://github.com/tiangolo/fastapi/pull/3456) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Initialize Indonesian translations. PR [#3014](https://github.com/tiangolo/fastapi/pull/3014) by [@pace-noge](https://github.com/pace-noge).
* 🌐 Add Spanish translation of Tutorial - Path Parameters. PR [#2219](https://github.com/tiangolo/fastapi/pull/2219) by [@mariacamilagl](https://github.com/mariacamilagl).
* 🌐 Add Spanish translation of Tutorial - First Steps. PR [#2208](https://github.com/tiangolo/fastapi/pull/2208) by [@mariacamilagl](https://github.com/mariacamilagl).
* 🌐 Portuguese translation of Tutorial - Body - Fields. PR [#3420](https://github.com/tiangolo/fastapi/pull/3420) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🌐 Add Chinese translation for Tutorial - Request - Forms - and - Files. PR [#3249](https://github.com/tiangolo/fastapi/pull/3249) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for Tutorial - Handling - Errors. PR [#3299](https://github.com/tiangolo/fastapi/pull/3299) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for Tutorial - Form - Data. PR [#3248](https://github.com/tiangolo/fastapi/pull/3248) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for Tutorial - Body - Updates. PR [#3237](https://github.com/tiangolo/fastapi/pull/3237) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for FastAPI People. PR [#3112](https://github.com/tiangolo/fastapi/pull/3112) by [@hareru](https://github.com/hareru).
* 🌐 Add French translation for Project Generation. PR [#3197](https://github.com/tiangolo/fastapi/pull/3197) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for Python Types Intro. PR [#3185](https://github.com/tiangolo/fastapi/pull/3185) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for External Links. PR [#3103](https://github.com/tiangolo/fastapi/pull/3103) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for Alternatives, Inspiration and Comparisons. PR [#3020](https://github.com/tiangolo/fastapi/pull/3020) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Fix Chinese translation code snippet mismatch in Tutorial - Python Types Intro. PR [#2573](https://github.com/tiangolo/fastapi/pull/2573) by [@BoYanZh](https://github.com/BoYanZh).
* 🌐 Add Portuguese translation for Development Contributing. PR [#1364](https://github.com/tiangolo/fastapi/pull/1364) by [@Serrones](https://github.com/Serrones).
* 🌐 Add Chinese translation for Tutorial - Request - Files. PR [#3244](https://github.com/tiangolo/fastapi/pull/3244) by [@jaystone776](https://github.com/jaystone776).

### Internal

* 👥 Update FastAPI People. PR [#3450](https://github.com/tiangolo/fastapi/pull/3450) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 👥 Update FastAPI People. PR [#3319](https://github.com/tiangolo/fastapi/pull/3319) by [@github-actions[bot]](https://github.com/apps/github-actions).
* ⬆ Upgrade docs development dependency on `typer-cli` to >=0.0.12 to fix conflicts. PR [#3429](https://github.com/tiangolo/fastapi/pull/3429) by [@tiangolo](https://github.com/tiangolo).

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

* 📌 Upgrade pydantic pin, to handle security vulnerability [CVE-2021-29510](https://github.com/pydantic/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh). PR [#3213](https://github.com/tiangolo/fastapi/pull/3213) by [@tiangolo](https://github.com/tiangolo).

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

* Fix handling of enums with their own schema in path parameters. To support [pydantic/pydantic#1432](https://github.com/pydantic/pydantic/pull/1432) in FastAPI. PR [#1463](https://github.com/tiangolo/fastapi/pull/1463).

## 0.55.0

* Allow enums to allow them to have their own schemas in OpenAPI. To support [pydantic/pydantic#1432](https://github.com/pydantic/pydantic/pull/1432) in FastAPI. PR [#1461](https://github.com/tiangolo/fastapi/pull/1461).
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
