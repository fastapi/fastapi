import abc
from typing import List

from pydantic import BaseModel


class OpenAPIPlugin(BaseModel, abc.ABC):
    js_urls: List[str] = []
    css_urls: List[str] = []

    @abc.abstractmethod
    def config(self) -> str:
        """Creates and returns a JS object that will be unpacked and appended to the configuration options in SwaggerUIBundle"""

    @abc.abstractmethod
    def use(self) -> str:
        """Adds the plugin that was defined by the get() method to the SwaggerUIBundle plugins parameter"""

    @abc.abstractmethod
    def get(self) -> str:
        """Returns the JS code that creates the JS Plugin object"""
