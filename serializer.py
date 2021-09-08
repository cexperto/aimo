from marshmallow import Schema, fields, post_load

class User:
    def __init__(self, email, password):        
        self.email = email
        self.password = password
    
    def __repr__(self):
        return self.email


class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

        

class NotesSchema(Schema):
    title = fields.Str()    
    artist = fields.Nested(UserSchema())
