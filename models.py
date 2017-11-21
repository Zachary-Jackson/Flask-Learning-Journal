import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    """This is the model for a user."""
    email = CharField(unique=True)
    password = CharField(max_length=35)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('joined_at',)

    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    """This is the model for an entry."""
    user = ForeignKeyField(
        rel_model=User,
        related_name='user'
    )
    title = CharField()
    entry_date = CharField()
    submit_date = DateTimeField(default=datetime.datetime.now)
    time_spent = CharField()
    learned = CharField()
    resources = CharField()

    class Meta:
        databse = DATABASE
        order_by = ('-submit_date',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
