from __future__ import annotations

from click import ClickException, echo


class MkDocsException(ClickException):
    """The base class which all MkDocs exceptions inherit from. This should
    not be raised directly. One of the subclasses should be raised instead."""


class Abort(MkDocsException):
    """Abort the build"""

    def show(self, *args, **kwargs) -> None:
        echo(self.format_message())


class ConfigurationError(MkDocsException):
    """This error is raised by configuration validation when a validation error
    is encountered. This error should be raised by any configuration options
    defined in a plugin's [config_scheme][]."""


class BuildError(MkDocsException):
    """This error may be raised by MkDocs during the build process. Plugins should
    not raise this error."""


class PluginError(BuildError):
    """A subclass of [`mkdocs.exceptions.BuildError`][] which can be raised by plugin
    events."""
