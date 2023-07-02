# coding: utf-8
"""verrrrry basic unicode column name testing"""

from sqlalchemy import ForeignKey, Integer, MetaData, desc, testing, util
from sqlalchemy.testing import eq_, fixtures
from sqlalchemy.testing.schema import Column, Table
from sqlalchemy.util import u, ue


class UnicodeSchemaTest(fixtures.TablesTest):
    __requires__ = ("unicode_ddl",)
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        global t1, t2, t3

        t1 = Table(
            u("unitable1"),
            metadata,
            Column(u("méil"), Integer, primary_key=True),
            Column(ue("\u6e2c\u8a66"), Integer),
            test_needs_fk=True,
        )
        t2 = Table(
            u("Unitéble2"),
            metadata,
            Column(u("méil"), Integer, primary_key=True, key="a"),
            Column(
                ue("\u6e2c\u8a66"),
                Integer,
                ForeignKey(u("unitable1.méil")),
                key="b",
            ),
            test_needs_fk=True,
        )

        # Few DBs support Unicode foreign keys
        if testing.against("sqlite"):
            t3 = Table(
                ue("\u6e2c\u8a66"),
                metadata,
                Column(
                    ue("\u6e2c\u8a66_id"),
                    Integer,
                    primary_key=True,
                    autoincrement=False,
                ),
                Column(
                    ue("unitable1_\u6e2c\u8a66"),
                    Integer,
                    ForeignKey(ue("unitable1.\u6e2c\u8a66")),
                ),
                Column(u("Unitéble2_b"), Integer, ForeignKey(u("Unitéble2.b"))),
                Column(
                    ue("\u6e2c\u8a66_self"),
                    Integer,
                    ForeignKey(ue("\u6e2c\u8a66.\u6e2c\u8a66_id")),
                ),
                test_needs_fk=True,
            )
        else:
            t3 = Table(
                ue("\u6e2c\u8a66"),
                metadata,
                Column(
                    ue("\u6e2c\u8a66_id"),
                    Integer,
                    primary_key=True,
                    autoincrement=False,
                ),
                Column(ue("unitable1_\u6e2c\u8a66"), Integer),
                Column(u("Unitéble2_b"), Integer),
                Column(ue("\u6e2c\u8a66_self"), Integer),
                test_needs_fk=True,
            )

    def test_insert(self, connection):
        connection.execute(t1.insert(), {u("méil"): 1, ue("\u6e2c\u8a66"): 5})
        connection.execute(t2.insert(), {u("a"): 1, u("b"): 1})
        connection.execute(
            t3.insert(),
            {
                ue("\u6e2c\u8a66_id"): 1,
                ue("unitable1_\u6e2c\u8a66"): 5,
                u("Unitéble2_b"): 1,
                ue("\u6e2c\u8a66_self"): 1,
            },
        )

        eq_(connection.execute(t1.select()).fetchall(), [(1, 5)])
        eq_(connection.execute(t2.select()).fetchall(), [(1, 1)])
        eq_(connection.execute(t3.select()).fetchall(), [(1, 5, 1, 1)])

    def test_col_targeting(self, connection):
        connection.execute(t1.insert(), {u("méil"): 1, ue("\u6e2c\u8a66"): 5})
        connection.execute(t2.insert(), {u("a"): 1, u("b"): 1})
        connection.execute(
            t3.insert(),
            {
                ue("\u6e2c\u8a66_id"): 1,
                ue("unitable1_\u6e2c\u8a66"): 5,
                u("Unitéble2_b"): 1,
                ue("\u6e2c\u8a66_self"): 1,
            },
        )

        row = connection.execute(t1.select()).first()
        eq_(row._mapping[t1.c[u("méil")]], 1)
        eq_(row._mapping[t1.c[ue("\u6e2c\u8a66")]], 5)

        row = connection.execute(t2.select()).first()
        eq_(row._mapping[t2.c[u("a")]], 1)
        eq_(row._mapping[t2.c[u("b")]], 1)

        row = connection.execute(t3.select()).first()
        eq_(row._mapping[t3.c[ue("\u6e2c\u8a66_id")]], 1)
        eq_(row._mapping[t3.c[ue("unitable1_\u6e2c\u8a66")]], 5)
        eq_(row._mapping[t3.c[u("Unitéble2_b")]], 1)
        eq_(row._mapping[t3.c[ue("\u6e2c\u8a66_self")]], 1)

    def test_reflect(self, connection):
        connection.execute(t1.insert(), {u("méil"): 2, ue("\u6e2c\u8a66"): 7})
        connection.execute(t2.insert(), {u("a"): 2, u("b"): 2})
        connection.execute(
            t3.insert(),
            {
                ue("\u6e2c\u8a66_id"): 2,
                ue("unitable1_\u6e2c\u8a66"): 7,
                u("Unitéble2_b"): 2,
                ue("\u6e2c\u8a66_self"): 2,
            },
        )

        meta = MetaData()
        tt1 = Table(t1.name, meta, autoload_with=connection)
        tt2 = Table(t2.name, meta, autoload_with=connection)
        tt3 = Table(t3.name, meta, autoload_with=connection)

        connection.execute(tt1.insert(), {u("méil"): 1, ue("\u6e2c\u8a66"): 5})
        connection.execute(tt2.insert(), {u("méil"): 1, ue("\u6e2c\u8a66"): 1})
        connection.execute(
            tt3.insert(),
            {
                ue("\u6e2c\u8a66_id"): 1,
                ue("unitable1_\u6e2c\u8a66"): 5,
                u("Unitéble2_b"): 1,
                ue("\u6e2c\u8a66_self"): 1,
            },
        )

        eq_(
            connection.execute(tt1.select().order_by(desc(u("méil")))).fetchall(),
            [(2, 7), (1, 5)],
        )
        eq_(
            connection.execute(tt2.select().order_by(desc(u("méil")))).fetchall(),
            [(2, 2), (1, 1)],
        )
        eq_(
            connection.execute(
                tt3.select().order_by(desc(ue("\u6e2c\u8a66_id")))
            ).fetchall(),
            [(2, 7, 2, 2), (1, 5, 1, 1)],
        )

    def test_repr(self):
        meta = MetaData()
        t = Table(ue("\u6e2c\u8a66"), meta, Column(ue("\u6e2c\u8a66_id"), Integer))

        if util.py2k:
            eq_(
                repr(t),
                (
                    "Table('\\u6e2c\\u8a66', MetaData(), "
                    "Column('\\u6e2c\\u8a66_id', Integer(), "
                    "table=<\u6e2c\u8a66>), "
                    "schema=None)"
                ),
            )
        else:
            eq_(
                repr(t),
                (
                    "Table('測試', MetaData(), "
                    "Column('測試_id', Integer(), "
                    "table=<測試>), "
                    "schema=None)"
                ),
            )
