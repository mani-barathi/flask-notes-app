from flask import render_template, redirect, request, Blueprint, abort, make_response
from .models import Note
from . import db
from flask_login import current_user, login_required
# from app.models import Note
# from app import db

notes = Blueprint('notes', __name__)


@notes.route("/")
@login_required
def home_page():
    print(request.cookies.get('name'))
    # res = cursor.execute( 'select id, title  from notes order by updated_at desc')
    # notes = res.fetchall()
    notes = Note.query.filter_by(user_id = current_user.id).all()
    # [Note(id=1,title='some', content='sadfsaf', created_at='22/6/12 15:45:56')]
    # print(notes)
    # print(notes[0].id, notes[0].title)
    # print(type(notes[0]))
    res = make_response(render_template('home.html', notes=notes))
    res.set_cookie('name',current_user.username, httponly=True)
    return res


@notes.route("/create", methods=['GET', 'POST'])
@login_required
def create_note_page():
    if request.method == 'GET':
        return render_template('create.html')

    title = request.form.get('title')
    content = request.form.get('content')
    # cursor.execute( 'insert into notes(title, content) values(?,?)', (title,  content))
    # con.commit()

    new_note = Note(title=title,  content=content, user_id = current_user.id)
    db.session.add(new_note)   # runs insert query
    db.session.commit()
    return redirect('/')


@notes.route('/notes/<note_id>')
@login_required
def single_note_page(note_id):
    # res = cursor.execute('select * from notes where id=?', (note_id,))
    # note = res.fetchone()
    note = Note.query.get(note_id)
    print(note.id, note.title)
    return render_template('single_note.html', note=note)


@notes.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
@login_required
def edit_note_page(note_id):
    if request.method == 'GET':
        # res = cursor.execute('select * from notes where id=?', (note_id,))
        # note = res.fetchone()
        note = Note.query.get(note_id)
        if note.user_id == current_user.id:
            print(note.id, note.title)
            return render_template('edit_note.html', note=note)
        else:
            return abort(403)

    title = request.form.get('title')
    content = request.form.get('content')
    # cursor.execute( 'update notes set title=?, content=? where id=?', (title,  content, note_id))
    # con.commit()
    note = Note.query.get(note_id)
    note.title = title
    note.content = content
    db.session.commit()
    return redirect(f'/notes/{note_id}')


@notes.route('/notes/delete/<note_id>')
@login_required
def delete_note_page(note_id):
    note = Note.query.get(note_id)
    if note.user_id == current_user.id:
        print(note.id, note.title)
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    else:
        return abort(403)
