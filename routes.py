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
        except Exception as e:
            return f'An error occurred while adding an article: {str(e)}'
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




# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = register_form()
#     if form.validate_on_submit():
#         try:
#             email = form.email.data
#             passwd = form.passwd.data
#             username = form.username.data
#
#             new_user = User(username=username, email=email, passwd=generate_password_hash(passwd))
#
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account successfully created', 'success')
#             return redirect(url_for('login'))
#
#         except InvalidRequestError:
#             db.session.rollback()
#             flash('Something is wrong!', 'danger')
#         except IntegrityError:
#             db.session.rollback()
#             flash('User already exists!.', 'warning')
#         except DataError:
#             db.session.rollback()
#             flash('Invalid Entry', 'warning')
#         except InterfaceError:
#             db.session.rollback()
#             flash('Error connecting to the database', 'danger')
#         except DatabaseError:
#             db.session.rollback()
#             flash('Error connecting to the database', 'danger')
#         except BuildError:
#             db.session.rollback()
#             flash('An error occured !', 'danger')
#     return render_template('register.html',form=form,text='Create account',title='Register',btn_action='Register account')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = login_form()
#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(email=form.email.data).first()
#             if user is None:
#                 flash('User is None', 'danger')
#             else:
#                 if check_password_hash(user.passwd, form.passwd.data):
#                     login_user(user)
#                     return redirect(url_for('index'))
#                 else:
#                     flash('Invalid username or password!', 'danger')
#         except Exception as e:
#             flash(e, 'danger')
#     return render_template('login.html', form=form, text='Login', title='Login', btn_action='Login')
#
#
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))