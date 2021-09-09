from model import Users, init
from hashlib import sha1
from serializer import UserSchema, User, NotesSchema
from bottle import debug, run, get, post, request, delete
from marshmallow import ValidationError
import json, jwt, typing
from werkzeug.security import generate_password_hash, check_password_hash

init()

    
def encript(payload: dict):
    encoded = jwt.encode(payload, "secret_aimo", algorithm="HS256")
    return encoded


def insert_user(user_email, user_password):
    try:
        key = generate_password_hash(user_password, 'sha256')
        print(f'key : {str(key)}')
        new_user = Users.insert(email=user_email,password=key,token=str(encript({"email":user_email}))).execute()
        print(new_user)
        return {"id": new_user, "email": user_email}
    except:
        return{"message": "user already exist"}



@post('/addUser')
def add_user():
    try:
        new_data = {'email' : request.json.get('email'), 'password' : request.json.get('password')}
        result = UserSchema().load(new_data)
        my_email = request.json.get('email')
        my_password = request.json.get('password')
        if result:  
            insert_user(my_email,my_password)

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return{
            "err": err.messages,
        }

    
@get('/users')
def query_users():
    query = Users.select(Users.email, Users.password, Users.token)
    my_ls = []
    for v in query:
        my_ls.append(dict(email=v.email,password=v.password,token=v.token))

    userDict = json.dumps(my_ls)
    print(userDict)
    return userDict


@post('/login') 
def do_login():
    try:
        new_login = {'email' : request.json.get('email'), 'password' : request.json.get('password')}
        result = UserSchema().load(new_login)
        if result:
            my_email=request.json.get('email')
            my_pass=request.json.get('password')            

            query = Users.select(Users.user_id,Users.email,Users.password,Users.token).where(Users.email==my_email)
            user_exist ={}
            for user in query:                
                user_exist['email']= user.email
                user_exist['password']= user.password
                user_exist['token']= user.token
            
            if len(user_exist)>0 and check_password_hash(user_exist['password'],my_pass):
                return{
                    "email": my_email,
                    "token": user_exist['token']
                }
                
            else:
                return{
                     "error": "something happend"
                }


    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return{
            "err": "something happend, check the data"
        }


@post('/notes')
def addNote():
    new_note = {'name' : request.json.get('name'), 'password' : request.json.get('password')}
    return {'ok': new_note}


run(host='localhost', port=8000, reloader=True)