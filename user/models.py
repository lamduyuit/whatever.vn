from mongoengine import signals
from flask import url_for
import os
from mongoengine import CASCADE

from application import db
from utilities.common import utc_now_ts as now
from flask_login import UserMixin
#from settings import STATIC_IMAGE_URL, AWS_BUCKET, AWS_CONTENT_URL


class User(db.Document, UserMixin):
    username = db.StringField(db_field="u", required=True, unique=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    first_name = db.StringField(db_field="fn", max_length=50)
    last_name = db.StringField(db_field="ln", max_length=50)
    created = db.IntField(db_field="c", default=now())
    bio = db.StringField(db_field="b", max_length=160)
    email_confirmed = db.BooleanField(db_field="ecf", default=False)
    change_configuration = db.DictField(db_field="cc")
    profile_image = db.StringField(db_field="i", default=None)
    
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.username = document.username.lower()
        document.email = document.email.lower()

    meta = {
        'indexes': ['username', 'email', '-created']
    }

signals.pre_save.connect(User.pre_save, sender=User)

class Save_valuation(db.Document):
    stock_id = db.StringField(max_length=10, required=True)
    form_data = db.DictField()
    from_user = db.ReferenceField(User, reverse_delete_rule=CASCADE)
    created = db.IntField(default=now())

    meta = {
        'indexes': ['stock_id', ('stock_id', 'from_user')]
    }