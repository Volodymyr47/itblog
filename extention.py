from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()

# Mail
mail = Mail()

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# mail.config['MAIL_PORT'] = 465
# mail.config['MAIL_USERNAME'] = 'mysimpleblog.notifier@gmail.com'
# mail.config['MAIL_PASSWORD'] = 'Myblogpassword1!'
# mail.config['MAIL_USE_TLS'] = False
# mail.config['MAIL_USE_SSL'] = True
