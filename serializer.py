from model import Notes
from marshmallow import Schema, fields, post_load

class User:
    def __init__(self, email, password):        
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '__all__'

class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class Note:
    def __init__(self, content, user_fk):        
        self.content = content
        self.user_fk = user_fk
    
    def __repr__(self):
        return '__all__'

class NotesSchema(Schema):
    content = fields.Str()
    user_fk = fields.Nested(UserSchema)

    @post_load
    def make_note(self, data, **kwargs):
        return Note(**data)
