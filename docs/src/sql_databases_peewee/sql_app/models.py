import peewee

from .database import db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db


class Item(peewee.Model):
    title = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="items")

    class Meta:
        database = db
