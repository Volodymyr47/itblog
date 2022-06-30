from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text

from extention import Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    text = Column(Text, nullable=False)
    dlm = Column(DateTime, default=datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


# class User(UserMixin, app.Model):
#     id = app.Column(app.Integer, primary_key=True, autoincrement=True)
#     username = app.Column(app.String(100), nullable=False, unique=True)
#     passwd = app.Column(app.String(254), nullable=False)
#     email = app.Column(app.String(100), nullable=False, unique=True)
#     is_active = app.Column(app.Boolean, default=True)
#     register_date = app.Column(app.DateTime, default=datetime.utcnow)
#     dlm = app.Column(app.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<User %r>' % self.username

