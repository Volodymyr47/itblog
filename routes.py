from datetime import datetime
from flask import render_template, request, redirect
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from app import app
from extention import db
from models import Article


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
def article_detail(id):
    if id:
        article = db.session.query(Article).get(id)
        return render_template('article_detail.html', article=article)
    else:
        return f'Post {id} does not exist'


@app.route('/posts/<int:id>/delete')
@login_required
def article_delete(id):
    article = db.session.get(Article, id) #query(Article).get(id) # Article().query.get_or_404(id)
    if article is None:
        abort(404)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error was found on delete apticle"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def article_update(id):
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


@app.route('/password_forgot')
def password_forgot():
    return render_template('password_forgot.html')