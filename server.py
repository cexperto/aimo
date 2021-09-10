from model import Users, init, Notes
from serializer import UserSchema, User, NotesSchema
from bottle import debug, run, get, post, request, delete,route
from marshmallow import ValidationError, exceptions
import json, jwt, typing
from werkzeug.security import generate_password_hash, check_password_hash

init()
secret ='secret_aimo'
    
def encode_token(payload: dict):
    token_bytes = jwt.encode(payload, secret, algorithm='HS256')
    return token_bytes


def decode_token(encoded_token):
    try:
        response = jwt.decode(encoded_token, secret, algorithms=['HS256'])
        return response
    except jwt.exceptions.DecodeError:
        return "Token no valido"



def insert_user(user_email, user_password):
    my_dict = {
        "email": user_email
    }
    try:
        key = generate_password_hash(user_password, 'sha256')
        print(f'key : {str(key)}')
        my_token= encode_token(my_dict)
        new_user = Users.insert(email=user_email,password=key,token=my_token).execute()
        print(f'new notes {new_user}')
        return {"message":"ok", "id": new_user, "email": user_email}
    except:
        return{"message": "user already exist"}


def insert_note(content_note,user_fk_note):
    try:        
        new_note = Notes.insert(content=content_note,user_fk=user_fk_note).execute()
        print(new_note)
        return{"message":"note added"}
    except:
        return{"message":"error"}


@post('/addUser')
def add_user():
    try:
        new_data = {'email' : request.json.get('email'), 'password' : request.json.get('password')}
        result = UserSchema().load(new_data)
        my_email = request.json.get('email')
        my_password = request.json.get('password')
        if result:  
            insert = insert_user(my_email,my_password)
            return insert

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
                user_exist['user_id']= user.user_id
                user_exist['email']= user.email
                user_exist['password']= user.password
                user_exist['token']= user.token
            
            if len(user_exist)>0 and check_password_hash(user_exist['password'],my_pass):
                return{
                    "user_id": user_exist['user_id'],
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
            "err": "something happend, check the data",
        }


@post('/addNotes')
def addNote():
    email = request.json.get('email')
    content = request.json.get('content')
    token = request.json.get('token')
    user_fk =request.json.get('user_fk')
    
    de_token = decode_token(token)
    json_user = {
        "email" : email
    }
    if json_user['email'] == de_token['email']:
        new_note = {'content' : content, 'user_fk' : user_fk}
        
        if new_note:
            insert = insert_note(content, user_fk)
            if insert['message']== 'error':
                return insert
            else:
                return {"message":"ok"}
        else:
            return{"message":"error"}
    

@post('/myNotes')
def query_users():
    email = request.json.get('email')
    token = request.json.get('token')
    user_id =request.json.get('user_fk')
    
    de_token = decode_token(token)
    json_user = {
        "email" : email
    }
    if json_user['email'] == de_token['email']:        
        query = Notes.select(Notes.content, Notes.user_fk).where(Notes.user_fk == user_id)
        my_ls = []
        for v in query:
            my_ls.append(dict(content=v.content))
        
        print(my_ls)
        notesDict = json.dumps(my_ls)
        return notesDict



run(host='localhost', port=8000, reloader=True)