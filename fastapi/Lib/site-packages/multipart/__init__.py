# This is the canonical package information.
__author__ = "Andrew Dunham"
__license__ = "Apache"
__copyright__ = "Copyright (c) 2012-2013, Andrew Dunham"
__version__ = "0.0.6"


from .multipart import (
    FormParser,
    MultipartParser,
    OctetStreamParser,
    QuerystringParser,
    create_form_parser,
    parse_form,
)
