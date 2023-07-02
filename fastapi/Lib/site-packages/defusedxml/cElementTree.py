# defusedxml
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See https://www.python.org/psf/license for licensing details.
"""Defused xml.etree.cElementTree
"""
from __future__ import absolute_import

import warnings
from xml.etree.cElementTree import TreeBuilder as _TreeBuilder
from xml.etree.cElementTree import parse as _parse
from xml.etree.cElementTree import tostring

# iterparse from ElementTree!
from xml.etree.ElementTree import iterparse as _iterparse

from .common import _generate_etree_functions

# This module is an alias for ElementTree just like xml.etree.cElementTree
from .ElementTree import (
    XML,
    DefusedXMLParser,
    ParseError,
    XMLParse,
    XMLParser,
    XMLTreeBuilder,
    fromstring,
    iterparse,
    parse,
    tostring,
)

__origin__ = "xml.etree.cElementTree"


warnings.warn(
    "defusedxml.cElementTree is deprecated, import from defusedxml.ElementTree instead.",
    category=DeprecationWarning,
    stacklevel=2,
)

# XMLParse is a typo, keep it for backwards compatibility
XMLTreeBuilder = XMLParse = XMLParser = DefusedXMLParser

parse, iterparse, fromstring = _generate_etree_functions(
    DefusedXMLParser, _TreeBuilder, _parse, _iterparse
)
XML = fromstring

__all__ = [
    "ParseError",
    "XML",
    "XMLParse",
    "XMLParser",
    "XMLTreeBuilder",
    "fromstring",
    "iterparse",
    "parse",
    "tostring",
]
