from datetime import datetime

def get_email():
    if auth.user:
        return auth.user.email
    else:
        return 'None'

db.define_table('entries',
    # There is also a column called 'id'. 
    # Field('author', default = get_email()), # 512 chars at most
    Field('author', default = get_email()),
    Field('creation_date', 'datetime', default=datetime.utcnow()),
    Field('data1','integer'),
    Field('data2', 'integer'),
    Field('data3', 'integer'),
    Field('results', 'text'),          
    )

db.entries.author.writable = False
db.entries.id.readable = False
db.entries.data1.writable = True
db.entries.data2.writable = True
db.entries.data3.writable = True
db.entries.creation_date.writable = False

db.entries.data1.label = 'Variable: X'
db.entries.data2.label = 'Variable: Y'
db.entries.data3.label = 'Variable: Z'