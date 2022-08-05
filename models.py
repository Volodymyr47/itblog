from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, desc
from extention import Base, db, OUR_TIME


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(Integer, ForeignKey('status.code'), nullable=False, default=1)
    dlm = Column(DateTime, default=OUR_TIME)
    creation_date = Column(DateTime, default=OUR_TIME)

    def __repr__(self):
        return '<Article %r>' % self.id


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer)
    name = Column(String(30),nullable=False)
    dlm = Column(DateTime, default=OUR_TIME)
    ulm = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'{self.code} - {self.name}'

    def get_name(self, id):
        if id:
            name = db.session.query(Status).filter_by(code=id).first()
            return name.name
        print('get_name(): ID is null')

    def get_code(self, id):
        if id:
            data = db.session.query(Status).filter_by(id=id).first()
            return data.code
        else:
            print('get_code(): ID is null')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('comment.id'), nullable=True, default=-1)
    level = Column(Integer, nullable=False, default=1)
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(Integer, ForeignKey('status.code'), nullable=False, default=1)
    ulm = Column(Integer, ForeignKey('user.id'), nullable=False)
    dlm = Column(DateTime, default=OUR_TIME)

    def __str__(self):
        return self.text

    def add_comment(self, text, article_id, parent, level, ulm):
        try:
            comment = Comment(parent_id=parent, level=level, article_id=article_id, text=text, ulm=ulm)
            db.session.add(comment)
            db.session.commit()
            message = 'The comment has been added successful'
        except BaseException as err:
            db.session.rollback()
            message = f'Comment adding error: {err} '
        return message


class ArticleRating(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    rating = Column(Integer, nullable=False, default=0)
    avg_rating = Column(Integer, nullable=False, default=0)
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    dlm = Column(DateTime, nullable=False, default=OUR_TIME)

    def __str__(self):
        return str(self.rating)

    def get_avg_rating(self):
        count = db.session.query(ArticleRating).filter_by(self.rating > 0).count()
        summ = db.session.query(ArticleRating.rating).filter_by(self.rating > 0).sum()
        return round(summ/count, 0)


