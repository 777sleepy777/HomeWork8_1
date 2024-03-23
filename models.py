from datetime import datetime

from mongoengine import EmbeddedDocument, Document, CASCADE
from mongoengine.fields import ReferenceField, BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField

class Author(Document): #)(EmbeddedDocument):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField(max_length=50)
    description = StringField()
    meta = {"collection": "authors"}

class Quotes(Document):
    tags = ListField(StringField(max_length=15))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}


class Tag(EmbeddedDocument):
    name = StringField()


class Record(EmbeddedDocument):
    description = StringField()
    done = BooleanField(default=False)


class Notes(Document):
    name = StringField()
    created = DateTimeField(default=datetime.now())
    records = ListField(EmbeddedDocumentField(Record))
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {'allow_inheritance': True}