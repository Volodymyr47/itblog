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
    # status = Column(Integer, ForeignKey('status.code'), nullable=False)
    dlm = Column(DateTime, default=datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer)
    name = Column(String(30),nullable=False)
    dlm = Column(DateTime, default=datetime.utcnow())
    ulm = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.name