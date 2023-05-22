from mongoengine import *


class Users(Document):
    fullname = StringField()
    email = StringField()
    status = BooleanField()

