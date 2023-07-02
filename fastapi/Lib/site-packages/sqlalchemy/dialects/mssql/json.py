from ... import types as sqltypes

# technically, all the dialect-specific datatypes that don't have any special
# behaviors would be private with names like _MSJson. However, we haven't been
# doing this for mysql.JSON or sqlite.JSON which both have JSON / JSONIndexType
# / JSONPathType in their json.py files, so keep consistent with that
# sub-convention for now.  A future change can update them all to be
# package-private at once.


class JSON(sqltypes.JSON):
    """MSSQL JSON type.

    MSSQL supports JSON-formatted data as of SQL Server 2016.

    The :class:`_mssql.JSON` datatype at the DDL level will represent the
    datatype as ``NVARCHAR(max)``, but provides for JSON-level comparison
    functions as well as Python coercion behavior.

    :class:`_mssql.JSON` is used automatically whenever the base
    :class:`_types.JSON` datatype is used against a SQL Server backend.

    .. seealso::

        :class:`_types.JSON` - main documentation for the generic
        cross-platform JSON datatype.

    The :class:`_mssql.JSON` type supports persistence of JSON values
    as well as the core index operations provided by :class:`_types.JSON`
    datatype, by adapting the operations to render the ``JSON_VALUE``
    or ``JSON_QUERY`` functions at the database level.

    The SQL Server :class:`_mssql.JSON` type necessarily makes use of the
    ``JSON_QUERY`` and ``JSON_VALUE`` functions when querying for elements
    of a JSON object.   These two functions have a major restriction in that
    they are **mutually exclusive** based on the type of object to be returned.
    The ``JSON_QUERY`` function **only** returns a JSON dictionary or list,
    but not an individual string, numeric, or boolean element; the
    ``JSON_VALUE`` function **only** returns an individual string, numeric,
    or boolean element.   **both functions either return NULL or raise
    an error if they are not used against the correct expected value**.

    To handle this awkward requirement, indexed access rules are as follows:

    1. When extracting a sub element from a JSON that is itself a JSON
       dictionary or list, the :meth:`_types.JSON.Comparator.as_json` accessor
       should be used::

            stmt = select(
                data_table.c.data["some key"].as_json()
            ).where(
                data_table.c.data["some key"].as_json() == {"sub": "structure"}
            )

    2. When extracting a sub element from a JSON that is a plain boolean,
       string, integer, or float, use the appropriate method among
       :meth:`_types.JSON.Comparator.as_boolean`,
       :meth:`_types.JSON.Comparator.as_string`,
       :meth:`_types.JSON.Comparator.as_integer`,
       :meth:`_types.JSON.Comparator.as_float`::

            stmt = select(
                data_table.c.data["some key"].as_string()
            ).where(
                data_table.c.data["some key"].as_string() == "some string"
            )

    .. versionadded:: 1.4


    """

    # note there was a result processor here that was looking for "number",
    # but none of the tests seem to exercise it.


# Note: these objects currently match exactly those of MySQL, however since
# these are not generalizable to all JSON implementations, remain separately
# implemented for each dialect.
class _FormatTypeMixin(object):
    def _format_value(self, value):
        raise NotImplementedError()

    def bind_processor(self, dialect):
        super_proc = self.string_bind_processor(dialect)

        def process(value):
            value = self._format_value(value)
            if super_proc:
                value = super_proc(value)
            return value

        return process

    def literal_processor(self, dialect):
        super_proc = self.string_literal_processor(dialect)

        def process(value):
            value = self._format_value(value)
            if super_proc:
                value = super_proc(value)
            return value

        return process


class JSONIndexType(_FormatTypeMixin, sqltypes.JSON.JSONIndexType):
    def _format_value(self, value):
        if isinstance(value, int):
            value = "$[%s]" % value
        else:
            value = '$."%s"' % value
        return value


class JSONPathType(_FormatTypeMixin, sqltypes.JSON.JSONPathType):
    def _format_value(self, value):
        return "$%s" % (
            "".join(
                [
                    "[%s]" % elem if isinstance(elem, int) else '."%s"' % elem
                    for elem in value
                ]
            )
        )
