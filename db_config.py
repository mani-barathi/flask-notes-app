import sqlite3

con = sqlite3.connect('database.db')
cursor = con.cursor()

cursor.execute('''
    create table if not exists notes(
        id integer primary key autoincrement,
        title varchar2(250), 
        content text,
        created_at timestamp default current_timestamp,
        updated_at timestamp default current_timestamp
    )
''')
con.commit()

# '2022-01-9 23:45:45'
