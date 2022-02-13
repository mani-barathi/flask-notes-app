from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask_notes'
    app.config['SECRET_KEY'] = 'omawosfd23nkjasndfwasdf'

    from .models import Note, User

    db.init_app(app)
    db.create_all(app=app)

    from .routes import notes
    from .auth_routes import auth
    app.register_blueprint(notes)
    app.register_blueprint(auth)

    return app

# app.run(debug=True)
