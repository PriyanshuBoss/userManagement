from mongoengine import Document, StringField, DateField, EmailField

class User(Document):
    firstname = StringField(max_length=100, required=True)
    lastname = StringField(max_length=100, required=True)
    dob = DateField()
    address = StringField(max_length=255)
    gender = StringField(choices=['male', 'female', 'other'])
    email = EmailField(unique=True)
    phone_number = StringField(max_length=15)

    meta = {
        'collection': 'users'  # MongoDB collection name
    }
