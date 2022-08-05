from flask import Flask
from flask_login import LoginManager

from users.users import users
from admin.admin import admin
from extention import db, migrate, mail


app = Flask(__name__)


# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['EXPLAIN_TEMPLATE_LOADING'] = True


# Blueprint
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(admin, url_prefix='/admin')


app.secret_key = 'bdadc3c3cf4166a1c1c5a1b4a6b18a36012b4f5c3cb7bd04f76f91ebd8d6a1b2'

db.init_app(app)
migrate.init_app(app, db)


#Mail 25
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '8e8920087f0796'
app.config['MAIL_PASSWORD'] = '1ce666fca25012'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail.init_app(app)


#Login
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    from users.models import User
    return db.session.query(User).get(int(user_id))


from routes import *

if __name__ == '__main__':
    app.run(debug=True)



