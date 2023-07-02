# ext/serializer.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Serializer/Deserializer objects for usage with SQLAlchemy query structures,
allowing "contextual" deserialization.

Any SQLAlchemy query structure, either based on sqlalchemy.sql.*
or sqlalchemy.orm.* can be used.  The mappers, Tables, Columns, Session
etc. which are referenced by the structure are not persisted in serialized
form, but are instead re-associated with the query structure
when it is deserialized.

Usage is nearly the same as that of the standard Python pickle module::

    from sqlalchemy.ext.serializer import loads, dumps
    metadata = MetaData(bind=some_engine)
    Session = scoped_session(sessionmaker())

    # ... define mappers

    query = Session.query(MyClass).
        filter(MyClass.somedata=='foo').order_by(MyClass.sortkey)

    # pickle the query
    serialized = dumps(query)

    # unpickle.  Pass in metadata + scoped_session
    query2 = loads(serialized, metadata, Session)

    print query2.all()

Similar restrictions as when using raw pickle apply; mapped classes must be
themselves be pickleable, meaning they are importable from a module-level
namespace.

The serializer module is only appropriate for query structures.  It is not
needed for:

* instances of user-defined classes.   These contain no references to engines,
  sessions or expression constructs in the typical case and can be serialized
  directly.

* Table metadata that is to be loaded entirely from the serialized structure
  (i.e. is not already declared in the application).   Regular
  pickle.loads()/dumps() can be used to fully dump any ``MetaData`` object,
  typically one which was reflected from an existing database at some previous
  point in time.  The serializer module is specifically for the opposite case,
  where the Table metadata is already present in memory.

"""

import re

from .. import Column, Table
from ..engine import Engine
from ..orm import class_mapper
from ..orm.interfaces import MapperProperty
from ..orm.mapper import Mapper
from ..orm.session import Session
from ..util import b64decode, b64encode, byte_buffer, pickle, text_type

__all__ = ["Serializer", "Deserializer", "dumps", "loads"]


def Serializer(*args, **kw):
    pickler = pickle.Pickler(*args, **kw)

    def persistent_id(obj):
        # print "serializing:", repr(obj)
        if isinstance(obj, Mapper) and not obj.non_primary:
            id_ = "mapper:" + b64encode(pickle.dumps(obj.class_))
        elif isinstance(obj, MapperProperty) and not obj.parent.non_primary:
            id_ = (
                "mapperprop:"
                + b64encode(pickle.dumps(obj.parent.class_))
                + ":"
                + obj.key
            )
        elif isinstance(obj, Table):
            if "parententity" in obj._annotations:
                id_ = "mapper_selectable:" + b64encode(
                    pickle.dumps(obj._annotations["parententity"].class_)
                )
            else:
                id_ = "table:" + text_type(obj.key)
        elif isinstance(obj, Column) and isinstance(obj.table, Table):
            id_ = "column:" + text_type(obj.table.key) + ":" + text_type(obj.key)
        elif isinstance(obj, Session):
            id_ = "session:"
        elif isinstance(obj, Engine):
            id_ = "engine:"
        else:
            return None
        return id_

    pickler.persistent_id = persistent_id
    return pickler


our_ids = re.compile(
    r"(mapperprop|mapper|mapper_selectable|table|column|"
    r"session|attribute|engine):(.*)"
)


def Deserializer(file, metadata=None, scoped_session=None, engine=None):
    unpickler = pickle.Unpickler(file)

    def get_engine():
        if engine:
            return engine
        elif scoped_session and scoped_session().bind:
            return scoped_session().bind
        elif metadata and metadata.bind:
            return metadata.bind
        else:
            return None

    def persistent_load(id_):
        m = our_ids.match(text_type(id_))
        if not m:
            return None
        else:
            type_, args = m.group(1, 2)
            if type_ == "attribute":
                key, clsarg = args.split(":")
                cls = pickle.loads(b64decode(clsarg))
                return getattr(cls, key)
            elif type_ == "mapper":
                cls = pickle.loads(b64decode(args))
                return class_mapper(cls)
            elif type_ == "mapper_selectable":
                cls = pickle.loads(b64decode(args))
                return class_mapper(cls).__clause_element__()
            elif type_ == "mapperprop":
                mapper, keyname = args.split(":")
                cls = pickle.loads(b64decode(mapper))
                return class_mapper(cls).attrs[keyname]
            elif type_ == "table":
                return metadata.tables[args]
            elif type_ == "column":
                table, colname = args.split(":")
                return metadata.tables[table].c[colname]
            elif type_ == "session":
                return scoped_session()
            elif type_ == "engine":
                return get_engine()
            else:
                raise Exception("Unknown token: %s" % type_)

    unpickler.persistent_load = persistent_load
    return unpickler


def dumps(obj, protocol=pickle.HIGHEST_PROTOCOL):
    buf = byte_buffer()
    pickler = Serializer(buf, protocol)
    pickler.dump(obj)
    return buf.getvalue()


def loads(data, metadata=None, scoped_session=None, engine=None):
    buf = byte_buffer(data)
    unpickler = Deserializer(buf, metadata, scoped_session, engine)
    return unpickler.load()
