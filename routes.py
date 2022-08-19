from datetime import datetime
from flask import render_template, request, redirect, flash, url_for, make_response
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from app import app
from extention import db, OUR_TIME
from models import Article, Comment, ArticleRating
from forms import NewComment, Rating


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add-article', methods=['POST', 'GET'])
@login_required
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text, user_id=current_user.id)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except Exception as err:
            return f'An error occurred while adding an article: {str(err)}'
    else:
        return render_template('add-article.html')


@app.route('/posts')
def posts():
    articles = db.session.query(Article).order_by(Article.dlm.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def article_detail(id, current_user_rating=''):
    '''
    Show article detail:
    '''
    comment_form = NewComment()
    rating_form = Rating()
    current_comments_count = db.session.query(Comment).filter_by(article_id=id).count()
    comments = db.session.query(Comment).filter_by(article_id=id).order_by(Comment.id)
    # current_user_rating = db.session.query(ArticleRating.rating).filter_by(user_id=current_user.id, article_id=id)
    if id:
        article = db.session.query(Article).get(id)
        return render_template('article_detail.html', article=article, comment_form=comment_form,
                               current_comments_count=current_comments_count, comments=comments,
                               current_user_rating=current_user_rating, rating_form=rating_form)
    else:
        return f'Post {id} does not exist'


@app.route('/posts/<int:id>/delete')
@login_required
def article_delete(id):
    '''
    Delete current article
    '''
    article = db.session.get(Article, id)
    if article.id:
        if article is None:
            abort(404)
        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error was found on delete article"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def article_update(id):
    '''
    Update current article
    '''
    article = db.session.query(Article).get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        article.dlm = datetime.utcnow()
        article = Article(title=article.title, intro=article.intro, text=article.text, dlm=article.dlm)

        try:
            db.session.commit()
            return redirect('/posts')
        except Exception as e:
            return f'An error occurred while updating the article: {str(e)}'
    else:
        return render_template('article_update.html', article=article)


@app.route('/posts/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    '''
    Add new comment
    '''
    article = db.session.get(Article, id)
    comment_form = NewComment()
    comment = Comment()
    parent = 0
    level = -1
    comments = db.session.query(Comment).filter_by(article_id=id).order_by(Comment.dlm.desc())
    if comment_form.validate_on_submit():
        if comment_form.id.data is not None:
            parent = comment_form.id.data
        new_level = db.session.query(Comment.level).filter_by(article_id=id, id=parent).first()
        if new_level is None:
            new_level = level
        else:
            new_level = new_level[0]
        comment.add_comment(text=comment_form.comment_text.data, article_id=id, parent=parent,
                                  level=new_level+1, ulm=current_user.id), 'success'
        flash('Your comment has been added', 'success')
        return redirect(url_for('article_detail',id=id))
    else:
        flash(comment_form.errors, 'danger')
    current_comments_count = db.session.query(Comment).filter_by(article_id=id).count()
    return redirect(url_for('article_detail', id=id))


@app.route('/posts/<int:id>', methods=['POST'])
@login_required
def article_rating(id):
    ar = ArticleRating()
    print(ar.get_avg_rating(art_id=id))
    try:
        rating_result = ArticleRating(rating=request.form['rating'],
                                      avg_rating=ar.get_avg_rating(art_id=id),
                                      article_id=id,
                                      user_id=current_user.id,
                                      dlm=OUR_TIME)
        db.session.add(rating_result)
        db.session.commit()
        flash('Your rating has been added', 'success')
    except BaseException as err:
        db.session.rollback()
        flash(f'RatingError: {err}')
    return redirect(url_for('article_detail', id=id, current_user_rating=request.form['rating']))

