from flask import flash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from extention import Base, db, OUR_TIME
from flask_login import UserMixin
from uuid import uuid4


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    passwd = Column(String(254), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    status = Column(Integer, ForeignKey('status.code'), default=1)
    register_date = Column(DateTime, default=OUR_TIME)
    dlm = Column(DateTime, default=OUR_TIME)
    ulm = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('userrole.id'))
    user_hash = Column(String(254), nullable=True, default='')

    def __repr__(self):
        return '<User %r>' % self.username

    def get_user_hash(self, uid):
        return str(uuid4())+str(uid)+str(uuid4())


class UserRole(Base):
    __tablename__ = 'userrole'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(String(100), nullable=False, unique=True)
    ulm = Column(Integer, ForeignKey('user.id'))
    dlm = Column(DateTime, default=OUR_TIME)
    status = Column(Integer, ForeignKey('status.code'))

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

    def change_roles_status(self, rolename, status):
        roles = db.session.query(UserRole).filter_by(rolename=rolename, status=2)
        if roles:
            roles.status = status
            try:
                db.session.commit()
            except Exception as err:
                raise f'Error changing roles status occurred: {err}'

