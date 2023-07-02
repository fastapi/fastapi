python-webencodings
===================

This is a Python implementation of the `WHATWG Encoding standard
<http://encoding.spec.whatwg.org/>`_.

* Latest documentation: http://packages.python.org/webencodings/
* Source code and issue tracker:
  https://github.com/gsnedders/python-webencodings
* PyPI releases: http://pypi.python.org/pypi/webencodings
* License: BSD
* Python 2.6+ and 3.3+

In order to be compatible with legacy web content
when interpreting something like ``Content-Type: text/html; charset=latin1``,
tools need to use a particular set of aliases for encoding labels
as well as some overriding rules.
For example, ``US-ASCII`` and ``iso-8859-1`` on the web are actually
aliases for ``windows-1252``, and an UTF-8 or UTF-16 BOM takes precedence
over any other encoding declaration.
The Encoding standard defines all such details so that implementations do
not have to reverse-engineer each other.

This module has encoding labels and BOM detection,
but the actual implementation for encoders and decoders is Python’s.


