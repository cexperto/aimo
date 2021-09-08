from model import Users, init
from hashlib import sha1
from serializer import UserSchema, User
from bottle import debug, run, get, post, request, delete
from marshmallow import ValidationError
import json, jwt
from werkzeug.security import generate_password_hash, check_password_hash

init()

    
def encript(word):
    encoded = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")


@post('/addUser')
def add_user():
    try:
        new_data = {'email' : request.json.get('email'), 'password' : request.json.get('password')}
        result = UserSchema().load(new_data)
        if result:
            def validate_user():
                try:
                    my_email = request.json.get('email')
                    my_password = request.json.get('password')                    
                    key = generate_password_hash(my_password, 'sha256')
                    print(f'key : {str(key)}')
                    new_user = Users.insert(email=my_email,password=key).execute()
                    print(new_user)
                    return {"id": new_user, "email": my_email}
                except:
                    return{"message": "user already exist"}

            validate_user()

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return{
            "err": err.messages,            
        }
    
@get('/users')
def query_users():
    query = Users.select(Users.email, Users.password)
    my_ls = []
    for v in query:
        my_ls.append(dict(email=v.email,password=v.password))

    userDict = json.dumps(my_ls)
    
    return userDict
    

@post('/notes')
def addNote():
    new_note = {'name' : request.json.get('name'), 'password' : request.json.get('password')}
    return {'ok': new_note}
    

def login(email, password):
    try:
        return (User
                .select()
                .where(
                    (Users.email == email) &
                    (Users.password == password) == True)).get()
    except User.DoesNotExist:
        # Incorrect username and/or password.
        return False


@post('/login') 
def do_login():
    try:
        new_login = {'email' : request.json.get('email'), 'password' : request.json.get('password')}
        result = UserSchema().load(new_login)
        if result:
            login(request.json.get('email'),request.json.get('password'))
        

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return{
            "err": "something happend, check the data"
        }

    
run(host='localhost', port=8000, reloader=True)