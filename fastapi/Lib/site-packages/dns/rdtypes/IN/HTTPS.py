# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license

import dns.immutable
import dns.rdtypes.svcbbase


@dns.immutable.immutable
class HTTPS(dns.rdtypes.svcbbase.SVCBBase):
    """HTTPS record"""
