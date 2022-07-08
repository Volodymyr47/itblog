from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()
