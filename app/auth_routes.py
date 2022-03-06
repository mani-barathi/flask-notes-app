from flask import render_template, redirect, request, Blueprint
from .models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html', message="")

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')


    # password validation can be done here

    # select * from users where email = email
    # [ user1 ]
    user = User.query.filter_by(email=email).first()
    if user:
        # user already exists with the same email
        return render_template('signup.html',message="User Already Exists with that email")
    else:
        hashed_password = generate_password_hash(password, "sha256")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


    return redirect('/login')


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    # validation
    user = User.query.filter_by(email=email).first()
    if user:
        # print(user.email, user.username)
        if check_password_hash(user.password, password):
            pass 
        else:
            return render_template('login.html',message="Invalid Credentials!")
    else:
        return render_template('login.html',message="No user Exists!")
    return render_template('login.html')
