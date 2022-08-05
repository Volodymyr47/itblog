from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()

# Mail
mail = Mail()

# Time
OUR_TIME = datetime.now(timezone('Europe/Kiev'))
