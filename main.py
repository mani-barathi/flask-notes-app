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

# '/notes/edit/23'
# '/notes/delete/23'


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


@app.route('/notes/<note_id>')
def single_note_page(note_id):
    res = cursor.execute('select * from notes where id=?', (note_id,))
    note = res.fetchone()
    print(note)
    return render_template('single_note.html', note=note)


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def edit_note_page(note_id):
    if request.method == 'GET':
        res = cursor.execute('select * from notes where id=?', (note_id,))
        note = res.fetchone()
        return render_template('edit_note.html', note=note)

    title = request.form.get('title')
    content = request.form.get('content')
    print('update values', title, content)
    cursor.execute(
        'update notes set title=?, content=? where id=?', (title,  content, note_id))
    con.commit()
    return redirect(f'/notes/{note_id}')


@app.route('/notes/delete/<note_id>')
def delete_note_page(note_id):
    cursor.execute('delete from notes where id=?', (note_id,))
    con.commit()
    return redirect('/')


# CRUD
# create
# read
# update
# delete
if __name__ == '__main__':
    app.run(debug=True)
