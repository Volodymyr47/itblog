from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from extention import Base
from flask_login import UserMixin
# from extention import db


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    passwd = Column(String(254), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    register_date = Column(DateTime, default=datetime.utcnow)
    dlm = Column(DateTime, default=datetime.utcnow)
    ulm = Column(Integer, ForeignKey('self.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('userrole.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# class UserRole(Base):
#     __tablename__ = 'userrole'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     rolename = Column(String(100), nullable=False, unique=True)
#     ulm = Column(Integer, ForeignKey('user.id'), nullable=False)
#     dlm = Column(DateTime, default=datetime.utcnow())
#     is_active = Column(Boolean, default=True)
#
#     def __repr__(self):
#         return '<UserRole %r>' % self.rolename