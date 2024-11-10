from typing import List, Optional, Tuple
import re

FILES_TO_EDIT = [
    "./docs/fa/docs/tutorial/middleware.md",
    "./docs/fa/docs/advanced/sub-applications.md",
    "./docs/tr/docs/tutorial/request-forms.md",
    "./docs/tr/docs/tutorial/path-params.md",
    "./docs/tr/docs/tutorial/static-files.md",
    "./docs/tr/docs/tutorial/first-steps.md",
    "./docs/tr/docs/tutorial/query-params.md",
    "./docs/pt/docs/tutorial/body.md",
    "./docs/tr/docs/tutorial/cookie-params.md",
    "./docs/pt/docs/tutorial/encoder.md",
    "./docs/pt/docs/tutorial/request-forms.md",
    "./docs/pt/docs/tutorial/metadata.md",
    "./docs/pt/docs/tutorial/path-params.md",
    "./docs/pt/docs/tutorial/body-updates.md",
    "./docs/pt/docs/tutorial/query-param-models.md",
    "./docs/tr/docs/advanced/testing-websockets.md",
    "./docs/tr/docs/advanced/wsgi.md",
    "./docs/pt/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/pt/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/pt/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/de/docs/tutorial/body.md",
    "./docs/de/docs/tutorial/extra-data-types.md",
    "./docs/pt/docs/tutorial/dependencies/index.md",
    "./docs/de/docs/tutorial/encoder.md",
    "./docs/vi/docs/tutorial/first-steps.md",
    "./docs/de/docs/tutorial/header-params.md",
    "./docs/de/docs/tutorial/request-forms.md",
    "./docs/pt/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/de/docs/tutorial/testing.md",
    "./docs/de/docs/tutorial/metadata.md",
    "./docs/tr/docs/python-types.md",
    "./docs/pt/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/de/docs/tutorial/path-params-numeric-validations.md",
    "./docs/vi/docs/python-types.md",
    "./docs/de/docs/tutorial/path-params.md",
    "./docs/pt/docs/tutorial/path-operation-configuration.md",
    "./docs/de/docs/tutorial/body-updates.md",
    "./docs/de/docs/tutorial/response-model.md",
    "./docs/pt/docs/tutorial/query-params-str-validations.md",
    "./docs/de/docs/tutorial/request-files.md",
    "./docs/pt/docs/tutorial/handling-errors.md",
    "./docs/pt/docs/tutorial/response-status-code.md",
    "./docs/pt/docs/tutorial/middleware.md",
    "./docs/de/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/pt/docs/tutorial/schema-extra-example.md",
    "./docs/em/docs/tutorial/body.md",
    "./docs/pt/docs/tutorial/static-files.md",
    "./docs/de/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/de/docs/tutorial/security/get-current-user.md",
    "./docs/em/docs/tutorial/encoder.md",
    "./docs/pt/docs/tutorial/header-param-models.md",
    "./docs/de/docs/tutorial/security/oauth2-jwt.md",
    "./docs/de/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/em/docs/tutorial/request-forms.md",
    "./docs/uk/docs/tutorial/body.md",
    "./docs/pt/docs/tutorial/first-steps.md",
    "./docs/de/docs/tutorial/security/first-steps.md",
    "./docs/de/docs/tutorial/dependencies/index.md",
    "./docs/em/docs/tutorial/metadata.md",
    "./docs/uk/docs/tutorial/encoder.md",
    "./docs/pt/docs/tutorial/path-params-numeric-validations.md",
    "./docs/ko/docs/tutorial/body.md",
    "./docs/de/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/em/docs/tutorial/path-params.md",
    "./docs/uk/docs/tutorial/first-steps.md",
    "./docs/de/docs/tutorial/security/simple-oauth2.md",
    "./docs/pt/docs/tutorial/debugging.md",
    "./docs/ko/docs/tutorial/encoder.md",
    "./docs/de/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/de/docs/tutorial/background-tasks.md",
    "./docs/ko/docs/tutorial/metadata.md",
    "./docs/em/docs/tutorial/request-files.md",
    "./docs/de/docs/tutorial/path-operation-configuration.md",
    "./docs/de/docs/tutorial/static-files.md",
    "./docs/de/docs/tutorial/extra-models.md",
    "./docs/pt/docs/tutorial/security/first-steps.md",
    "./docs/ko/docs/tutorial/path-params.md",
    "./docs/de/docs/advanced/async-tests.md",
    "./docs/de/docs/tutorial/query-params-str-validations.md",
    "./docs/de/docs/tutorial/first-steps.md",
    "./docs/ko/docs/tutorial/request-files.md",
    "./docs/de/docs/tutorial/query-params.md",
    "./docs/de/docs/advanced/testing-events.md",
    "./docs/pt/docs/tutorial/security/simple-oauth2.md",
    "./docs/de/docs/tutorial/handling-errors.md",
    "./docs/de/docs/tutorial/bigger-applications.md",
    "./docs/de/docs/advanced/openapi-callbacks.md",
    "./docs/pt/docs/tutorial/body-fields.md",
    "./docs/em/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/pt/docs/tutorial/extra-models.md",
    "./docs/de/docs/tutorial/body-nested-models.md",
    "./docs/pt/docs/tutorial/body-multiple-params.md",
    "./docs/ko/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/de/docs/advanced/additional-status-codes.md",
    "./docs/em/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/de/docs/tutorial/request-forms-and-files.md",
    "./docs/pt/docs/tutorial/request-form-models.md",
    "./docs/pt/docs/tutorial/extra-data-types.md",
    "./docs/ko/docs/tutorial/dependencies/index.md",
    "./docs/de/docs/advanced/testing-websockets.md",
    "./docs/em/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/de/docs/tutorial/cookie-params.md",
    "./docs/pt/docs/tutorial/header-params.md",
    "./docs/pt/docs/tutorial/query-params.md",
    "./docs/de/docs/advanced/middleware.md",
    "./docs/ko/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/de/docs/tutorial/body-fields.md",
    "./docs/em/docs/tutorial/dependencies/index.md",
    "./docs/pt/docs/tutorial/request_files.md",
    "./docs/pt/docs/tutorial/bigger-applications.md",
    "./docs/de/docs/advanced/using-request-directly.md",
    "./docs/ko/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/pt/docs/tutorial/testing.md",
    "./docs/em/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/pt/docs/tutorial/cookie-param-models.md",
    "./docs/de/docs/advanced/behind-a-proxy.md",
    "./docs/ko/docs/tutorial/path-operation-configuration.md",
    "./docs/pt/docs/tutorial/body-nested-models.md",
    "./docs/em/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/ko/docs/tutorial/query-params-str-validations.md",
    "./docs/de/docs/advanced/response-headers.md",
    "./docs/pt/docs/advanced/dataclasses.md",
    "./docs/pt/docs/tutorial/request-forms-and-files.md",
    "./docs/em/docs/tutorial/path-operation-configuration.md",
    "./docs/ko/docs/tutorial/response-status-code.md",
    "./docs/de/docs/advanced/response-change-status-code.md",
    "./docs/pt/docs/advanced/async-tests.md",
    "./docs/pt/docs/how-to/extending-openapi.md",
    "./docs/pt/docs/tutorial/cookie-params.md",
    "./docs/em/docs/tutorial/query-params-str-validations.md",
    "./docs/ko/docs/tutorial/middleware.md",
    "./docs/de/docs/advanced/advanced-dependencies.md",
    "./docs/pt/docs/advanced/testing-events.md",
    "./docs/pt/docs/tutorial/cors.md",
    "./docs/pt/docs/how-to/custom-request-and-route.md",
    "./docs/em/docs/tutorial/handling-errors.md",
    "./docs/de/docs/advanced/wsgi.md",
    "./docs/pt/docs/advanced/openapi-callbacks.md",
    "./docs/ko/docs/tutorial/static-files.md",
    "./docs/uk/docs/python-types.md",
    "./docs/em/docs/tutorial/response-status-code.md",
    "./docs/pt/docs/how-to/configure-swagger-ui.md",
    "./docs/ko/docs/tutorial/first-steps.md",
    "./docs/pt/docs/advanced/additional-responses.md",
    "./docs/de/docs/advanced/sub-applications.md",
    "./docs/em/docs/tutorial/middleware.md",
    "./docs/ko/docs/tutorial/path-params-numeric-validations.md",
    "./docs/pt/docs/advanced/additional-status-codes.md",
    "./docs/pt/docs/how-to/conditional-openapi.md",
    "./docs/em/docs/tutorial/schema-extra-example.md",
    "./docs/pt/docs/advanced/testing-websockets.md",
    "./docs/pt/docs/how-to/custom-docs-ui-assets.md",
    "./docs/ko/docs/tutorial/debugging.md",
    "./docs/em/docs/tutorial/static-files.md",
    "./docs/ko/docs/tutorial/response-model.md",
    "./docs/pt/docs/advanced/using-request-directly.md",
    "./docs/pt/docs/how-to/separate-openapi-schemas.md",
    "./docs/em/docs/tutorial/first-steps.md",
    "./docs/de/docs/advanced/security/oauth2-scopes.md",
    "./docs/pt/docs/how-to/graphql.md",
    "./docs/em/docs/tutorial/path-params-numeric-validations.md",
    "./docs/pt/docs/advanced/response-headers.md",
    "./docs/de/docs/advanced/settings.md",
    "./docs/ko/docs/tutorial/security/get-current-user.md",
    "./docs/em/docs/tutorial/debugging.md",
    "./docs/pt/docs/advanced/response-change-status-code.md",
    "./docs/de/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/ko/docs/tutorial/security/simple-oauth2.md",
    "./docs/bn/docs/python-types.md",
    "./docs/pt/docs/advanced/advanced-dependencies.md",
    "./docs/em/docs/tutorial/sql-databases.md",
    "./docs/ko/docs/tutorial/background-tasks.md",
    "./docs/de/docs/advanced/openapi-webhooks.md",
    "./docs/ko/docs/tutorial/query-params.md",
    "./docs/pt/docs/advanced/wsgi.md",
    "./docs/em/docs/tutorial/response-model.md",
    "./docs/de/docs/advanced/events.md",
    "./docs/ko/docs/tutorial/body-nested-models.md",
    "./docs/pt/docs/python-types.md",
    "./docs/de/docs/advanced/response-cookies.md",
    "./docs/pt/docs/advanced/sub-applications.md",
    "./docs/ko/docs/tutorial/request-forms-and-files.md",
    "./docs/de/docs/advanced/generate-clients.md",
    "./docs/ko/docs/tutorial/cookie-params.md",
    "./docs/de/docs/advanced/websockets.md",
    "./docs/em/docs/tutorial/security/get-current-user.md",
    "./docs/ko/docs/tutorial/cors.md",
    "./docs/ko/docs/tutorial/body-fields.md",
    "./docs/de/docs/advanced/testing-dependencies.md",
    "./docs/em/docs/tutorial/security/oauth2-jwt.md",
    "./docs/pt/docs/advanced/security/http-basic-auth.md",
    "./docs/ko/docs/tutorial/body-multiple-params.md",
    "./docs/de/docs/advanced/templates.md",
    "./docs/em/docs/tutorial/security/first-steps.md",
    "./docs/uk/docs/tutorial/extra-data-types.md",
    "./docs/ko/docs/tutorial/extra-data-types.md",
    "./docs/pt/docs/advanced/security/oauth2-scopes.md",
    "./docs/de/docs/advanced/response-directly.md",
    "./docs/uk/docs/tutorial/body-fields.md",
    "./docs/ko/docs/tutorial/header-params.md",
    "./docs/em/docs/tutorial/security/simple-oauth2.md",
    "./docs/pt/docs/advanced/settings.md",
    "./docs/de/docs/advanced/custom-response.md",
    "./docs/em/docs/tutorial/background-tasks.md",
    "./docs/pt/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/em/docs/tutorial/extra-models.md",
    "./docs/pt/docs/advanced/openapi-webhooks.md",
    "./docs/ko/docs/python-types.md",
    "./docs/em/docs/tutorial/query-params.md",
    "./docs/pt/docs/advanced/events.md",
    "./docs/nl/docs/python-types.md",
    "./docs/em/docs/tutorial/bigger-applications.md",
    "./docs/pt/docs/advanced/response-cookies.md",
    "./docs/de/docs/how-to/extending-openapi.md",
    "./docs/em/docs/tutorial/body-nested-models.md",
    "./docs/pt/docs/advanced/websockets.md",
    "./docs/de/docs/how-to/custom-request-and-route.md",
    "./docs/em/docs/tutorial/request-forms-and-files.md",
    "./docs/pt/docs/advanced/testing-dependencies.md",
    "./docs/pt/docs/advanced/templates.md",
    "./docs/em/docs/tutorial/cookie-params.md",
    "./docs/ko/docs/advanced/testing-events.md",
    "./docs/de/docs/how-to/conditional-openapi.md",
    "./docs/pt/docs/advanced/response-directly.md",
    "./docs/em/docs/tutorial/cors.md",
    "./docs/ko/docs/advanced/testing-websockets.md",
    "./docs/de/docs/how-to/custom-docs-ui-assets.md",
    "./docs/ko/docs/advanced/events.md",
    "./docs/pt/docs/advanced/custom-response.md",
    "./docs/ko/docs/advanced/using-request-directly.md",
    "./docs/em/docs/tutorial/body-fields.md",
    "./docs/de/docs/how-to/separate-openapi-schemas.md",
    "./docs/ko/docs/advanced/response-cookies.md",
    "./docs/ko/docs/advanced/response-headers.md",
    "./docs/es/docs/tutorial/path-params.md",
    "./docs/em/docs/tutorial/body-multiple-params.md",
    "./docs/de/docs/how-to/graphql.md",
    "./docs/ko/docs/advanced/response-directly.md",
    "./docs/ko/docs/advanced/response-change-status-code.md",
    "./docs/es/docs/tutorial/first-steps.md",
    "./docs/em/docs/tutorial/extra-data-types.md",
    "./docs/ko/docs/advanced/advanced-dependencies.md",
    "./docs/em/docs/tutorial/header-params.md",
    "./docs/ko/docs/advanced/wsgi.md",
    "./docs/es/docs/tutorial/query-params.md",
    "./docs/es/docs/how-to/graphql.md",
    "./docs/em/docs/tutorial/testing.md",
    "./docs/em/docs/python-types.md",
    "./docs/de/docs/python-types.md",
    "./docs/es/docs/python-types.md",
    "./docs/em/docs/how-to/extending-openapi.md",
    "./docs/em/docs/how-to/custom-request-and-route.md",
    "./docs/es/docs/advanced/additional-status-codes.md",
    "./docs/em/docs/how-to/conditional-openapi.md",
    "./docs/en/docs/tutorial/body.md",
    "./docs/es/docs/advanced/response-headers.md",
    "./docs/em/docs/how-to/graphql.md",
    "./docs/en/docs/tutorial/request-forms.md",
    "./docs/es/docs/advanced/response-change-status-code.md",
    "./docs/em/docs/advanced/settings.md",
    "./docs/en/docs/tutorial/metadata.md",
    "./docs/ru/docs/tutorial/body.md",
    "./docs/em/docs/advanced/dataclasses.md",
    "./docs/em/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/ru/docs/tutorial/encoder.md",
    "./docs/em/docs/advanced/async-tests.md",
    "./docs/en/docs/tutorial/body-updates.md",
    "./docs/em/docs/advanced/events.md",
    "./docs/es/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/ru/docs/tutorial/request-forms.md",
    "./docs/em/docs/advanced/testing-events.md",
    "./docs/em/docs/advanced/response-cookies.md",
    "./docs/es/docs/advanced/response-directly.md",
    "./docs/ru/docs/tutorial/metadata.md",
    "./docs/em/docs/advanced/openapi-callbacks.md",
    "./docs/em/docs/advanced/generate-clients.md",
    "./docs/ru/docs/tutorial/cookie-params.md",
    "./docs/ru/docs/tutorial/path-params.md",
    "./docs/em/docs/advanced/websockets.md",
    "./docs/em/docs/advanced/additional-responses.md",
    "./docs/ru/docs/tutorial/cors.md",
    "./docs/em/docs/advanced/testing-dependencies.md",
    "./docs/ru/docs/tutorial/body-updates.md",
    "./docs/em/docs/advanced/additional-status-codes.md",
    "./docs/ja/docs/tutorial/body.md",
    "./docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/em/docs/advanced/templates.md",
    "./docs/ru/docs/tutorial/body-fields.md",
    "./docs/ru/docs/tutorial/request-files.md",
    "./docs/em/docs/advanced/testing-websockets.md",
    "./docs/ja/docs/tutorial/encoder.md",
    "./docs/em/docs/advanced/response-directly.md",
    "./docs/en/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/ru/docs/tutorial/body-multiple-params.md",
    "./docs/em/docs/advanced/middleware.md",
    "./docs/ja/docs/tutorial/request-forms.md",
    "./docs/em/docs/advanced/custom-response.md",
    "./docs/ru/docs/tutorial/extra-data-types.md",
    "./docs/em/docs/advanced/using-request-directly.md",
    "./docs/em/docs/advanced/wsgi.md",
    "./docs/ja/docs/tutorial/metadata.md",
    "./docs/en/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/ru/docs/tutorial/header-params.md",
    "./docs/em/docs/advanced/behind-a-proxy.md",
    "./docs/ru/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/ja/docs/tutorial/path-params.md",
    "./docs/em/docs/advanced/sub-applications.md",
    "./docs/em/docs/advanced/response-headers.md",
    "./docs/ru/docs/tutorial/testing.md",
    "./docs/ru/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/en/docs/tutorial/query-params-str-validations.md",
    "./docs/ja/docs/tutorial/body-updates.md",
    "./docs/em/docs/advanced/response-change-status-code.md",
    "./docs/en/docs/tutorial/handling-errors.md",
    "./docs/ru/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/em/docs/advanced/advanced-dependencies.md",
    "./docs/em/docs/advanced/security/http-basic-auth.md",
    "./docs/ru/docs/tutorial/dependencies/index.md",
    "./docs/fr/docs/advanced/additional-status-codes.md",
    "./docs/ja/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/em/docs/advanced/security/oauth2-scopes.md",
    "./docs/ru/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/en/docs/tutorial/header-param-models.md",
    "./docs/ja/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/ru/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/ja/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/en/docs/tutorial/debugging.md",
    "./docs/ja/docs/tutorial/dependencies/index.md",
    "./docs/ru/docs/tutorial/path-operation-configuration.md",
    "./docs/ja/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/en/docs/tutorial/extra-data-types.md",
    "./docs/ru/docs/tutorial/query-params-str-validations.md",
    "./docs/ja/docs/tutorial/path-operation-configuration.md",
    "./docs/ru/docs/tutorial/handling-errors.md",
    "./docs/en/docs/tutorial/testing.md",
    "./docs/ja/docs/tutorial/query-params-str-validations.md",
    "./docs/ru/docs/tutorial/response-status-code.md",
    "./docs/en/docs/python-types.md",
    "./docs/en/docs/tutorial/security/oauth2-jwt.md",
    "./docs/ja/docs/tutorial/handling-errors.md",
    "./docs/ru/docs/tutorial/schema-extra-example.md",
    "./docs/ja/docs/tutorial/response-status-code.md",
    "./docs/ru/docs/tutorial/static-files.md",
    "./docs/ru/docs/python-types.md",
    "./docs/ja/docs/tutorial/middleware.md",
    "./docs/en/docs/tutorial/security/simple-oauth2.md",
    "./docs/ru/docs/tutorial/first-steps.md",
    "./docs/ja/docs/tutorial/schema-extra-example.md",
    "./docs/ru/docs/tutorial/path-params-numeric-validations.md",
    "./docs/ja/docs/tutorial/static-files.md",
    "./docs/en/docs/tutorial/request-form-models.md",
    "./docs/en/docs/advanced/testing-events.md",
    "./docs/ja/docs/tutorial/first-steps.md",
    "./docs/ru/docs/tutorial/extra-models.md",
    "./docs/uk/docs/tutorial/cookie-params.md",
    "./docs/en/docs/tutorial/query-params.md",
    "./docs/ja/docs/tutorial/path-params-numeric-validations.md",
    "./docs/ru/docs/tutorial/query-params.md",
    "./docs/en/docs/tutorial/bigger-applications.md",
    "./docs/ja/docs/tutorial/debugging.md",
    "./docs/ru/docs/tutorial/body-nested-models.md",
    "./docs/ja/docs/tutorial/response-model.md",
    "./docs/ru/docs/tutorial/request-forms-and-files.md",
    "./docs/en/docs/tutorial/request-forms-and-files.md",
    "./docs/ru/docs/tutorial/security/first-steps.md",
    "./docs/ja/docs/tutorial/security/get-current-user.md",
    "./docs/ja/docs/tutorial/security/oauth2-jwt.md",
    "./docs/ru/docs/tutorial/background-tasks.md",
    "./docs/ja/docs/advanced/additional-status-codes.md",
    "./docs/en/docs/advanced/settings.md",
    "./docs/ja/docs/tutorial/security/first-steps.md",
    "./docs/ru/docs/tutorial/response-model.md",
    "./docs/ja/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/ja/docs/tutorial/background-tasks.md",
    "./docs/ja/docs/advanced/websockets.md",
    "./docs/en/docs/advanced/generate-clients.md",
    "./docs/ja/docs/tutorial/extra-models.md",
    "./docs/ja/docs/advanced/response-directly.md",
    "./docs/ja/docs/tutorial/query-params.md",
    "./docs/en/docs/advanced/testing-dependencies.md",
    "./docs/ja/docs/advanced/custom-response.md",
    "./docs/ja/docs/tutorial/body-nested-models.md",
    "./docs/en/docs/advanced/templates.md",
    "./docs/ja/docs/tutorial/request-forms-and-files.md",
    "./docs/ja/docs/tutorial/cookie-params.md",
    "./docs/ja/docs/tutorial/cors.md",
    "./docs/ja/docs/how-to/conditional-openapi.md",
    "./docs/ja/docs/tutorial/body-fields.md",
    "./docs/ja/docs/tutorial/body-multiple-params.md",
    "./docs/ja/docs/tutorial/extra-data-types.md",
    "./docs/ja/docs/tutorial/header-params.md",
    "./docs/ja/docs/python-types.md",
    "./docs/zh/docs/tutorial/body.md",
    "./docs/ja/docs/tutorial/testing.md",
    "./docs/zh/docs/tutorial/encoder.md",
    "./docs/zh/docs/tutorial/request-forms.md",
    "./docs/zh/docs/tutorial/request-forms-and-files.md",
    "./docs/zh/docs/tutorial/metadata.md",
    "./docs/zh/docs/tutorial/cookie-params.md",
    "./docs/zh/docs/tutorial/path-params.md",
    "./docs/zh/docs/tutorial/cors.md",
    "./docs/zh/docs/tutorial/body-updates.md",
    "./docs/zh/docs/tutorial/body-fields.md",
    "./docs/zh/docs/tutorial/request-files.md",
    "./docs/zh/docs/tutorial/body-multiple-params.md",
    "./docs/zh/docs/tutorial/extra-data-types.md",
    "./docs/zh/docs/tutorial/debugging.md",
    "./docs/zh/docs/tutorial/header-params.md",
    "./docs/zh/docs/tutorial/sql-databases.md",
    "./docs/zh/docs/tutorial/testing.md",
    "./docs/zh/docs/tutorial/dependencies/sub-dependencies.md",
    "./docs/zh/docs/tutorial/response-model.md",
    "./docs/zh/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md",
    "./docs/zh/docs/tutorial/dependencies/dependencies-with-yield.md",
    "./docs/zh/docs/tutorial/dependencies/index.md",
    "./docs/zh/docs/tutorial/security/get-current-user.md",
    "./docs/zh/docs/tutorial/dependencies/classes-as-dependencies.md",
    "./docs/zh/docs/tutorial/security/oauth2-jwt.md",
    "./docs/zh/docs/tutorial/dependencies/global-dependencies.md",
    "./docs/zh/docs/tutorial/security/first-steps.md",
    "./docs/zh/docs/tutorial/path-operation-configuration.md",
    "./docs/zh/docs/tutorial/security/simple-oauth2.md",
    "./docs/zh/docs/tutorial/query-params-str-validations.md",
    "./docs/zh/docs/tutorial/handling-errors.md",
    "./docs/zh/docs/tutorial/extra-models.md",
    "./docs/zh/docs/tutorial/response-status-code.md",
    "./docs/zh/docs/tutorial/query-params.md",
    "./docs/zh/docs/advanced/dataclasses.md",
    "./docs/zh/docs/tutorial/middleware.md",
    "./docs/zh/docs/advanced/testing-events.md",
    "./docs/zh/docs/tutorial/bigger-applications.md",
    "./docs/zh/docs/tutorial/schema-extra-example.md",
    "./docs/zh/docs/advanced/openapi-callbacks.md",
    "./docs/zh/docs/tutorial/body-nested-models.md",
    "./docs/zh/docs/tutorial/static-files.md",
    "./docs/zh/docs/tutorial/path-params-numeric-validations.md",
    "./docs/zh/docs/advanced/additional-status-codes.md",
    "./docs/zh/docs/tutorial/first-steps.md",
    "./docs/zh/docs/advanced/testing-websockets.md",
    "./docs/zh/docs/advanced/middleware.md",
    "./docs/zh/docs/advanced/templates.md",
    "./docs/zh/docs/advanced/using-request-directly.md",
    "./docs/zh/docs/advanced/response-directly.md",
    "./docs/zh/docs/advanced/behind-a-proxy.md",
    "./docs/zh/docs/advanced/custom-response.md",
    "./docs/zh/docs/advanced/response-headers.md",
    "./docs/zh/docs/advanced/response-change-status-code.md",
    "./docs/zh/docs/advanced/advanced-dependencies.md",
    "./docs/zh/docs/advanced/wsgi.md",
    "./docs/zh/docs/how-to/configure-swagger-ui.md",
    "./docs/zh/docs/advanced/sub-applications.md",
    "./docs/zh/docs/advanced/security/http-basic-auth.md",
    "./docs/zh/docs/python-types.md",
    "./docs/zh/docs/advanced/response-cookies.md",
    "./docs/zh/docs/advanced/path-operation-advanced-configuration.md",
    "./docs/zh/docs/advanced/security/oauth2-scopes.md",
    "./docs/zh/docs/advanced/websockets.md",
    "./docs/zh/docs/advanced/events.md",
    "./docs/zh/docs/advanced/generate-clients.md",
    "./docs/zh/docs/advanced/testing-dependencies.md",
    "./docs/zh/docs/advanced/settings.md",
    "./docs/ru/docs/tutorial/debugging.md",
]


class InvalidFromatError(Exception):
    """
    Signifies some incorrect format.
    """


def convert_python_block(old_format: List[str]) -> str:
    if len(old_format) < 2:
        raise InvalidFromatError("Invalid format.")
    first_line = old_format[0]
    if not first_line.startswith("```Python"):
        raise InvalidFromatError("Invalid starting format.")
    hlines = get_hlines(first_line)
    file_ref, line_ref = convert_file_reference(old_format[1])
    return (
        "{* "
        + f"{file_ref} {f'ln[{line_ref}] ' if line_ref else ''}{f'hl[{hlines}] ' if hlines else ''}"
        + "*}\n"
    )


def get_hlines(old_first_line: str) -> Optional[str]:
    """
    Takes lines such as:
    ```Python hl_lines="3"
    and extracts the hl_ines part and returns the new hlines string "3" in this example.
    For groups of likes such as
    ```Python hl_lines="5-10"
    it needs to convert the - to a : so in this example it would be "5:10".
    For multiple lines it needs to seperate them by comma, such as:
    ```Python hl_lines="3   5-10   12"
    would be "3,5:10,12".
    For examples with no hlighted lines such as
    ```Python
    it should return None.
    """
    old_hl = re.search(r"hl_lines=\"(.*)\"", old_first_line)
    if old_hl is None:
        return None
    old_hl = old_hl.group(1)
    hl_lines = []
    for line in old_hl.split():
        if "-" in line:
            hl_lines.append(replace_hypen_with_colon(line))
        else:
            hl_lines.append(line)
    return ",".join(hl_lines)


def replace_hypen_with_colon(line: str) -> str:
    start, end = line.split("-")
    return f"{start}:{end}"


def convert_file_reference(reference_line: str) -> Tuple[str, Optional[str]]:
    """
    This takes a line such as:
        {!> ../../docs_src/security/tutorial006_an_py39.py!}
    and extracts the file reference such as ../../docs_src/security/tutorial006_an_py39.py.
    This can also accept file references with a line reference such as
    {!> ../../docs_src/separate_openapi_schemas/tutorial001_py310.py[ln:1-7]!}
    in this case it will return the file reference ../../docs_src/separate_openapi_schemas/tutorial001_py310.py and the line reference 1:7 (where we have replaced - with a :).
    """
    file_ref = re.search(r"../(.*).py", reference_line)
    if file_ref is None:
        raise InvalidFromatError("Invalid file reference.")
    file_ref = file_ref.group(0)
    line_ref = re.search(r"\[ln:(.*)\]", reference_line)
    if line_ref is None:
        return file_ref, None
    line_ref = line_ref.group(1)
    if "-" not in line_ref:
        return file_ref, line_ref
    return file_ref, replace_hypen_with_colon(line_ref)


FORWARDSLASH = "////"
TAB = "//// tab"


class Status:
    def __init__(self):
        print("init")
        self.tab_depth = 0
        self.included_tab_block = False
        self.previous_tab_block = False
        self.python_block = []

    def increase_tab_depth(self):
        print("increase")
        self.previous_tab_block = True
        self.tab_depth += 1

    def end_slash_block(self):
        print("decrease")
        self.tab_depth -= 1

    def end_previous_tab_block(self):
        print("reset")
        self.tab_depth = 0
        self.previous_tab_block = False
        self.included_tab_block = False

    @property
    def in_tab_block(self):
        return self.tab_depth > 0

    def __str__(self):
        return f"Tab Depth: {self.tab_depth}, In Tab Block: {self.in_tab_block}, Previous Tab Block: {self.previous_tab_block}, Python Block: {self.python_block}, Included tab block {self.included_tab_block}"


def get_line_to_write(line: str, status: Status) -> List[str]:
    python_line = line.startswith("```Python")
    forwardslash_line = line.startswith(FORWARDSLASH)
    if not (
        python_line
        or forwardslash_line
        or status.previous_tab_block
        or status.python_block
    ):
        return [line]
    if status.python_block:
        if line.startswith("{!"):
            status.python_block.append(line)
            return []
        if line.startswith("```"):
            converted_line = convert_python_block(status.python_block)
            status.python_block = []
            status.included_tab_block = status.in_tab_block
            return [converted_line]
        raise InvalidFromatError("Invalid format.")
    if python_line:
        if not status.included_tab_block:
            status.python_block.append(line)
        return []
    if forwardslash_line:
        if status.tab_depth > 0:
            if line.strip() == FORWARDSLASH:
                status.end_slash_block()
                return []
            status.increase_tab_depth()
            return []
        if status.tab_depth < 0:
            raise InvalidFromatError("Invalid format too many ends.")
        if line.startswith(TAB):
            status.increase_tab_depth()
            return []
    # At this point we only have previous tab block being true.
    # If the line is empty add it to the lines to print otherwise end the previous block.
    if status.in_tab_block:
        return []

    if len(line.strip()) == 0:
        return []
    status.end_previous_tab_block()
    return ["\n", line]


def edit_file(file_name: str):
    status = Status()
    output_lines = []
    with open(file_name, "r") as file_to_edit:
        for line in file_to_edit:
            new_line = get_line_to_write(line, status)
            if new_line != [line]:
                print(f"Line: {line}")
                print(f"Status: {status}")
                print(f"New lines: {new_line}")
            output_lines.extend(new_line)
    with open(file_name, "w") as file_to_edit:
        file_to_edit.writelines(output_lines)


import subprocess


def make_change_for_file(file_name: str) -> bool:
    branch_name = f"docs-update{file_name.replace('.', '_')}"
    commit_message = f"📝 Update includes in `{file_name}`"
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        edit_file(file_name)
        subprocess.run(["git", "add", file_name], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(
            ["git", "push", "--force", "-u", "origin", branch_name], check=True
        )
        subprocess.run(["git", "checkout", "master"], check=True)

    except (subprocess.CalledProcessError, InvalidFromatError) as e:
        print(f"An error occurred in file {file_name}: {e}")
        return False
    return True


if __name__ == "__main__":
    missing_files = []
    for file_name in FILES_TO_EDIT:
        if not make_change_for_file(file_name):
            missing_files.append(file_name)
    print(missing_files)
