from typing import Dict

from fastapi.openapi.plugins.snippet.models import Snippet


class CodeSampleFactory(Snippet):
    language: str

    def snippet(self) -> Dict[str, Snippet]:
        return {self.language: Snippet(title=self.title, syntax=self.syntax)}

    def sample(self, source: str) -> Dict[str, str]:
        return {"lang": self.language, "source": source, "label": self.title}
