from datetime import datetime

from flask import flash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from extention import Base, db
from flask_login import UserMixin


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    passwd = Column(String(254), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    register_date = Column(DateTime, default=datetime.utcnow)
    dlm = Column(DateTime, default=datetime.utcnow)
    ulm = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('userrole.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class UserRole(Base):
    __tablename__ = 'userrole'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(String(100), nullable=False, unique=True)
    ulm = Column(Integer, ForeignKey('user.id'))
    dlm = Column(DateTime, default=datetime.utcnow())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return self.rolename

    def __str__(self):
        return self.rolename

    def add_new_role(self, rolename, curr_user):
        new_role = db.session.query(UserRole).filter_by(id=id, rolename=rolename).first()
        if new_role:
            return flash(f'User role {new_role} already exist in database', 'warning')
        else:
            new_role = UserRole(rolename=rolename, ulm=curr_user)
            return new_role

    def deactive_role(self, rolename, is_active):
        active = db.session.query(UserRole).filter_by(rolename=rolename, is_active = True)
        if active:
            is_active = False
            return is_active

    def active_role(self, rolename, is_active):
        active = db.session.query(UserRole).filter_by(rolename=rolename, is_active=False)
        if active:
            is_active = True
            return is_active