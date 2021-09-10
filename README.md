
# Callengue aimo

Rest API for save notes from users, for aimo challengue




## Authors

- [@cexperto](https://github.com/cexperto)

  
## Deployment

To deploy this project:

clone this repo

```bash
  py -m venv venv
  pip install -r requiremnets.txt
  py server.py
```

  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Tech Stack

**Client:** Html, JavaScript

**Server:** python, bottle, peewee, marshmallow, pyjwt

  
## API Reference

#### Get all notes

```http
Post /myNotes
```
body:

json{
    "email": "email@mail.com",
    "token" "lknlnjlojnoijoij",
    "user_fk": 1
}

#### add notes
Post /addNotes
body
json{
    "email": "email@mail.com",
    "content": "one note",
    "token" "lknlnjlojnoijoij",
    "user_fk": 1
}
#### add user
body
Post /addNotes

json{
    "email": "email@mail.com",
    "password": "somepassword",   
}

#### login
body
Post /login

json{
    "email": "email@mail.com",
    "password": "somepassword",   
}

  