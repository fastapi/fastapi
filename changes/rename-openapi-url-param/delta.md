Change: rename-openapi-url-param

Preserved behaviour (one sentence)

After this change, existing callers passing openapi\_url=... to FastAPI(...) must still get OpenAPI served at the same effective path and with the same enable/disable semantics as before.





ADDED

New public constructor parameter openapi\_path as the preferred name for configuring where the OpenAPI schema is served.



Alias mapping so internal behaviour continues to be driven by self.openapi\_url while allowing callers to migrate to openapi\_path.



MODIFIED

FastAPI.\_\_init\_\_ argument handling now performs alias resolution between openapi\_path and legacy openapi\_url.



Documentation surface (constructor signature / help text) changes: users will now see an additional parameter in the API surface area, changing how IDEs and signature inspection present configuration.



REMOVED

(Spent most time here; caller-visible behaviour loss/tightening.)





The ability to provide both openapi\_url and openapi\_path with conflicting values and still “get some outcome”. After this change, conflicting dual configuration is rejected (fail-fast) rather than being implicitly resolved.



The implicit guarantee that “any call that previously succeeded with openapi\_url will still succeed without new validation branches” — alias logic introduces a new error path when both parameters are set.



REMOVED audit

Touched file: fastapi/applications.py





Generator missed: the new alias resolution can cause a new startup-time exception path: providing both openapi\_path and openapi\_url (different) now raises ValueError. Previously, there was no equivalent “both-set conflict” failure mode because only one parameter existed.



Generator missed: a subtle but important behavioural contract to re-verify: openapi\_url=None previously disabled OpenAPI and therefore also disabled /docs and /redoc (as documented in the docstring). With aliasing, we must ensure that setting openapi\_path=None and/or openapi\_url=None preserves the disablement behaviour exactly (including docs/redoc disable).



Genuine “complete” (for this diff): aside from the above conflict/disable semantics and signature surface change, the remainder of runtime routing continues to use self.openapi\_url and should behave equivalently for single-parameter callers.



Risk note

Highest-risk preserved behaviour: openapi\_url=None still disables OpenAPI and automatically disables /docs and /redoc (no accidental exposure of docs endpoints).



Why at risk: the alias mapping introduces a new primary input (openapi\_path) and a new decision point; a small mistake could leave self.openapi\_url truthy or mis-set, re-enabling docs unexpectedly.



One test/check that proves it survives: add a test that constructs FastAPI(openapi\_url=None) and asserts:



GET /openapi.json is 404



GET /docs is 404



GET /redoc is 404

And add the same test for FastAPI(openapi\_path=None) to prove the new preferred parameter matches legacy behaviour.

