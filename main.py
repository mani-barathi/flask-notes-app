from flask import Flask, render_template, request, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())


# ORM - Obejct relational Mapper
# Flask-SQLAlchemy
con = sqlite3.connect('database.db', check_same_thread=False)
cursor = con.cursor()


@app.route("/")
def home_page():
    # res = cursor.execute( 'select id, title  from notes order by updated_at desc')
    # notes = res.fetchall()
    notes = Note.query.all()
    # [Note(id=1,title='some', content='sadfsaf', created_at='22/6/12 15:45:56')]
    # print(notes)
    # print(notes[0].id, notes[0].title)
    # print(type(notes[0]))
    return render_template('home.html', notes=notes)


@app.route("/create", methods=['GET', 'POST'])
def create_note_page():
    if request.method == 'GET':
        return render_template('create.html')

    title = request.form.get('title')
    content = request.form.get('content')
    # cursor.execute( 'insert into notes(title, content) values(?,?)', (title,  content))
    # con.commit()

    new_note = Note(title=title,  content=content)
    db.session.add(new_note)   # runs insert query
    db.session.commit()
    return redirect('/')


@app.route('/notes/<note_id>')
def single_note_page(note_id):
    # res = cursor.execute('select * from notes where id=?', (note_id,))
    # note = res.fetchone()
    note = Note.query.get(note_id)
    print(note.id, note.title)
    return render_template('single_note.html', note=note)


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def edit_note_page(note_id):
    if request.method == 'GET':
        # res = cursor.execute('select * from notes where id=?', (note_id,))
        # note = res.fetchone()
        note = Note.query.get(note_id)
        print(note.id, note.title)
        return render_template('edit_note.html', note=note)

    title = request.form.get('title')
    content = request.form.get('content')
    # cursor.execute( 'update notes set title=?, content=? where id=?', (title,  content, note_id))
    # con.commit()
    note = Note.query.get(note_id)
    note.title = title
    note.content = content
    db.session.commit()
    return redirect(f'/notes/{note_id}')


@app.route('/notes/delete/<note_id>')
def delete_note_page(note_id):
    # cursor.execute('delete from notes where id=?', (note_id,))
    # con.commit()
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all(app=app)
    app.run(debug=True)
