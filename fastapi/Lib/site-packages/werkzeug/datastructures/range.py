from __future__ import annotations


class IfRange:
    """Very simple object that represents the `If-Range` header in parsed
    form.  It will either have neither a etag or date or one of either but
    never both.

    .. versionadded:: 0.7
    """

    def __init__(self, etag=None, date=None):
        #: The etag parsed and unquoted.  Ranges always operate on strong
        #: etags so the weakness information is not necessary.
        self.etag = etag
        #: The date in parsed format or `None`.
        self.date = date

    def to_header(self):
        """Converts the object back into an HTTP header."""
        if self.date is not None:
            return http.http_date(self.date)
        if self.etag is not None:
            return http.quote_etag(self.etag)
        return ""

    def __str__(self):
        return self.to_header()

    def __repr__(self):
        return f"<{type(self).__name__} {str(self)!r}>"


class Range:
    """Represents a ``Range`` header. All methods only support only
    bytes as the unit. Stores a list of ranges if given, but the methods
    only work if only one range is provided.

    :raise ValueError: If the ranges provided are invalid.

    .. versionchanged:: 0.15
        The ranges passed in are validated.

    .. versionadded:: 0.7
    """

    def __init__(self, units, ranges):
        #: The units of this range.  Usually "bytes".
        self.units = units
        #: A list of ``(begin, end)`` tuples for the range header provided.
        #: The ranges are non-inclusive.
        self.ranges = ranges

        for start, end in ranges:
            if start is None or (end is not None and (start < 0 or start >= end)):
                raise ValueError(f"{(start, end)} is not a valid range.")

    def range_for_length(self, length):
        """If the range is for bytes, the length is not None and there is
        exactly one range and it is satisfiable it returns a ``(start, stop)``
        tuple, otherwise `None`.
        """
        if self.units != "bytes" or length is None or len(self.ranges) != 1:
            return None
        start, end = self.ranges[0]
        if end is None:
            end = length
            if start < 0:
                start += length
        if http.is_byte_range_valid(start, end, length):
            return start, min(end, length)
        return None

    def make_content_range(self, length):
        """Creates a :class:`~werkzeug.datastructures.ContentRange` object
        from the current range and given content length.
        """
        rng = self.range_for_length(length)
        if rng is not None:
            return ContentRange(self.units, rng[0], rng[1], length)
        return None

    def to_header(self):
        """Converts the object back into an HTTP header."""
        ranges = []
        for begin, end in self.ranges:
            if end is None:
                ranges.append(f"{begin}-" if begin >= 0 else str(begin))
            else:
                ranges.append(f"{begin}-{end - 1}")
        return f"{self.units}={','.join(ranges)}"

    def to_content_range_header(self, length):
        """Converts the object into `Content-Range` HTTP header,
        based on given length
        """
        range = self.range_for_length(length)
        if range is not None:
            return f"{self.units} {range[0]}-{range[1] - 1}/{length}"
        return None

    def __str__(self):
        return self.to_header()

    def __repr__(self):
        return f"<{type(self).__name__} {str(self)!r}>"


def _callback_property(name):
    def fget(self):
        return getattr(self, name)

    def fset(self, value):
        setattr(self, name, value)
        if self.on_update is not None:
            self.on_update(self)

    return property(fget, fset)


class ContentRange:
    """Represents the content range header.

    .. versionadded:: 0.7
    """

    def __init__(self, units, start, stop, length=None, on_update=None):
        assert http.is_byte_range_valid(start, stop, length), "Bad range provided"
        self.on_update = on_update
        self.set(start, stop, length, units)

    #: The units to use, usually "bytes"
    units = _callback_property("_units")
    #: The start point of the range or `None`.
    start = _callback_property("_start")
    #: The stop point of the range (non-inclusive) or `None`.  Can only be
    #: `None` if also start is `None`.
    stop = _callback_property("_stop")
    #: The length of the range or `None`.
    length = _callback_property("_length")

    def set(self, start, stop, length=None, units="bytes"):
        """Simple method to update the ranges."""
        assert http.is_byte_range_valid(start, stop, length), "Bad range provided"
        self._units = units
        self._start = start
        self._stop = stop
        self._length = length
        if self.on_update is not None:
            self.on_update(self)

    def unset(self):
        """Sets the units to `None` which indicates that the header should
        no longer be used.
        """
        self.set(None, None, units=None)

    def to_header(self):
        if self.units is None:
            return ""
        if self.length is None:
            length = "*"
        else:
            length = self.length
        if self.start is None:
            return f"{self.units} */{length}"
        return f"{self.units} {self.start}-{self.stop - 1}/{length}"

    def __bool__(self):
        return self.units is not None

    def __str__(self):
        return self.to_header()

    def __repr__(self):
        return f"<{type(self).__name__} {str(self)!r}>"


# circular dependencies
from .. import http
