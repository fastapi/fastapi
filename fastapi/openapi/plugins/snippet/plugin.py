from typing import Dict, List

from fastapi.openapi.plugins.base import OpenAPIPlugin
from fastapi.openapi.plugins.snippet.auto import PremadeSnippets
from fastapi.openapi.plugins.snippet.models import (
    Snippet,
    default_openapi_snippets,
    supported_snippet_languages,
)


class SnippetPlugin(OpenAPIPlugin):
    """[summary]

    Kudos for the JS library and suggestions goes to:
    - https://github.com/ErikWittern/openapi-snippet
    - https://github.com/swagger-api/swagger-ui/pull/7181

    Examples:
        app = FastAPI(openapi_plugins=[SnippetPlugin(snippets={"curl": {"curl_bash": Snippet(title="cURL", syntax="bash")}})])
        app = FastAPI(openapi_plugins=[SnippetPlugin(snippets={**PremadeSnippets.get_all()})])

    """

    snippets: Dict[str, Snippet] = PremadeSnippets.get(["curl", "python"])
    js_urls: List = [
        "/public/openapisnippet.min.js"
    ]  # TODO: Waiting for this to be added to CDN

    def __init__(self, **kwargs):
        if "snippets" in kwargs:
            # assert supported_snippet_languages.union(default_openapi_snippets).issuperset(set(kwargs["snippets"].keys()))
            kwargs["snippets"]
        super().__init__(**kwargs)

    def config(self) -> str:
        generators = self.dict()["snippets"]
        return f"""{{
            requestSnippetsEnabled: true,
            requestSnippets: {{
                generators: {generators},
                languages: {list(self.snippets.keys())}
            }}
        }}
        """

    def use(self) -> str:
        return self.__class__.__name__

    def get(self) -> str:
        return f"""

            function targetMatches(arr, language, title) {{
                return arr.find(function(el) {{
                    return el.lang === language && el.label === title;
                }}); 
            }}

            let supported = {list(supported_snippet_languages)}


            function fn_generator(target, title) {{
                    return (req) => {{
                        const {{ spec, oasPathMethod }} = req.toJS();
                        const {{ path, method }} = oasPathMethod;

                        if (spec.paths[path][method]["x-codeSamples"]) {{
                            console.log(spec.paths[path][method]["x-codeSamples"])
                            let match = targetMatches(spec.paths[path][method]["x-codeSamples"], target, title)
                            if (typeof match !== "undefined" && match.source) {{
                                console.log(match)
                                return match.source
                            }}
                        }}

                        if (!supported.includes(target)) {{
                            return "No code sample found"

                        }}

                        if (typeof spec.servers == "undefined") {{
                            spec.servers = [{{url: window.location.origin}}]
                        }}

                        let snippet;
                        try {{
                            snippet = OpenAPISnippets.getEndpointSnippets(spec, path, method, [target]).snippets[0]
                                .content;
                        }} catch (err) {{
                            console.log(err);
                            snippet = "Unable to convert, try copying the cURL command into https://curl.trillworks.com and selecting your desired language"
                        }}
                        return snippet;
                    }};
                }}

            const {self.__class__.__name__} = {{
                statePlugins: {{
                    spec: {{
                        wrapSelectors: {{
                            requestFor: (ori, system) => (state, path, method) => {{
                                return ori(path, method)
                                    ?.set("spec", state.get("json", {{}}))
                                    ?.setIn(["oasPathMethod", "path"], path)
                                    ?.setIn(["oasPathMethod", "method"], method);
                            }},
                            mutatedRequestFor: (ori) => (state, path, method) => {{
                                return ori(path, method)
                                    ?.set("spec", state.get("json", {{}}))
                                    ?.setIn(["oasPathMethod", "path"], path)
                                    ?.setIn(["oasPathMethod", "method"], method);
                            }},
                        }},
                    }},
                }},
                fn: Object.fromEntries({[{"name":k,"title":v.title} for k, v in self.snippets.items() if k not in default_openapi_snippets]}.map((target) => [`requestSnippetGenerator_${{target.name}}`, fn_generator(target.name, target.title)])),

            }};
        """
