# defusedxml
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See https://www.python.org/psf/license for licensing details.
"""Defuse XML bomb denial of service vulnerabilities
"""
from __future__ import absolute_import, print_function

import warnings

from .common import (
    DefusedXmlException,
    DTDForbidden,
    EntitiesForbidden,
    ExternalReferenceForbidden,
    NotSupportedError,
    _apply_defusing,
)


def defuse_stdlib():
    """Monkey patch and defuse all stdlib packages

    :warning: The monkey patch is an EXPERIMETNAL feature.
    """
    defused = {}

    with warnings.catch_warnings():
        from . import cElementTree
    from . import ElementTree, expatbuilder, expatreader, minidom, pulldom, sax, xmlrpc

    xmlrpc.monkey_patch()
    defused[xmlrpc] = None

    defused_mods = [
        cElementTree,
        ElementTree,
        minidom,
        pulldom,
        sax,
        expatbuilder,
        expatreader,
    ]

    for defused_mod in defused_mods:
        stdlib_mod = _apply_defusing(defused_mod)
        defused[defused_mod] = stdlib_mod

    return defused


__version__ = "0.7.1"

__all__ = [
    "DefusedXmlException",
    "DTDForbidden",
    "EntitiesForbidden",
    "ExternalReferenceForbidden",
    "NotSupportedError",
]
