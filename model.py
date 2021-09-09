from peewee import PrimaryKeyField, SqliteDatabase, AutoField, CharField, DateField, ForeignKeyField, Model

db = SqliteDatabase('notes.db')

class Users(Model):
   user_id = PrimaryKeyField(AutoField)
   email = CharField(unique=True)
   password = CharField()
   token = CharField()

   class Meta:
       database = db

class Notes(Model):
   notes_id = PrimaryKeyField(AutoField)
   content = CharField()
   user_fk = ForeignKeyField(Users)

   class Meta:
       database = db


def init():
    db.connect()
    db.create_tables([Users, Notes])


# chamo = Profesores( nombre='Chamo',
#                    apellido='Linares',
#                    telefono='640568923',
#                    email='alinares@paradigmadigital.com')
# chamo.save()

