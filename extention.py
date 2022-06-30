from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
# from flask_migrate import Migrate
# import app

db = SQLAlchemy()
# migrate = Migrate(app, db)
Base = declarative_base()

