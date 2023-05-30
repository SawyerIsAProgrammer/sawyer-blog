from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_gravatar import Gravatar

ckeditor = CKEditor()
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
gravatar = Gravatar()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    gravatar.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # so the part below should go after the blueprint part above
    with app.app_context():
        db.create_all()

    return app  

