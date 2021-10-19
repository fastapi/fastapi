from pydantic import BaseModel

supported_snippet_languages = {
    "c_libcurl",
    "csharp_restsharp",
    "go_native",
    "java_okhttp",
    "java_unires",
    "javascript_jquery",
    "javascript_xhr",
    "node_native",
    "node_request",
    "node_unirest",
    "objc_nsurlsession",
    "ocaml_cohttp",
    "php_curl",
    "php_http1",
    "php_http2",
    "python_python3",
    "python_requests",
    "ruby_native",
    "shell_curl",
    "shell_httpie",
    "shell_wget",
    "swift_nsurlsession",
}

default_openapi_snippets = {"curl_bash", "curl_powershell", "curl_cmd"}


class Snippet(BaseModel):
    title: str
    syntax: str
