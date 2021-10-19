from typing import Dict, List

from fastapi.openapi.plugins.snippet.models import Snippet, default_openapi_snippets


class PremadeSnippets:

    _templates = {
        "curl": {"curl_bash": Snippet(title="cURL", syntax="bash")},
        "python": {"python_requests": Snippet(title="* Python - requests", syntax="python")},
        "csharp": {"csharp_restsharp": Snippet(title="* C# - restsharp", syntax="csharp")},
        "go": {"go_native": Snippet(title="* Go", syntax="go")},
        "java": {"java_okhttp": Snippet(title="* Java - okhttp", syntax="java")},
        "jquery": {"javascript_jquery": Snippet(title="* JQuery", syntax="javascript")},
        "node": {"node_native": Snippet(title="* Node - native", syntax="javascript")},
        "objectivec": {"objc_nsurlsession": Snippet(title="* Objective C - NSURLSession", syntax="objectivec")},
        "ocaml": {"ocaml_cohttp": Snippet(title="* OCaml - cohttp", syntax="ocaml")},
        "php": {"php_curl": Snippet(title="* PHP - curl", syntax="php")},
        "ruby": {"ruby_native": Snippet(title="* Ruby - native", syntax="ruby")},
        "swift": {"swift_nsurlsession": Snippet(title="* Swift - NSURLSession", syntax="swift")},
    }

    @staticmethod
    def get(programs: List[str]) -> Dict[str, Snippet]:
        template = {}
        for p in sorted(programs, key=lambda s: s in default_openapi_snippets):
            template = {**template, **PremadeSnippets._templates.get(p)}
        return template

    @staticmethod
    def get_all() -> Dict[str, Snippet]:
        template = {}
        for p in sorted(PremadeSnippets._templates.keys(), key=lambda s: s in default_openapi_snippets):
            template = {**template, **PremadeSnippets._templates.get(p)}
        return template
