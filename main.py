from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('database.db', check_same_thread=False)
cursor = con.cursor()


@app.route("/")
def home_page():
    res = cursor.execute(
        'select id, title  from notes order by updated_at desc')
    notes = res.fetchall()
    print(notes)
    return render_template('home.html', notes=notes)

# '/edit/23'
# '/delete/23'


@app.route("/create", methods=['GET', 'POST'])
def create_note_page():
    if request.method == 'GET':
        return render_template('create.html')

    title = request.form.get('title')
    content = request.form.get('content')
    cursor.execute(
        'insert into notes(title, content) values(?,?)', (title,  content))
    con.commit()
    return redirect('/')


# CRUD
# create
# read
# update
# delete
if __name__ == '__main__':
    app.run(debug=True)
