from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

import forms

app = Flask(__name__)

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Login
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'

# Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mysimpleblog.notifier@gmail.com'
app.config['MAIL_PASSWORD'] = 'Myblogpassword1!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)



