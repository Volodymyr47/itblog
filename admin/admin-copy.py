from datetime import datetime

from flask import Blueprint, flash, redirect, url_for
from flask_login import login_user, logout_user, LoginManager, login_required, login_fresh, current_user
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError, InterfaceError, DatabaseError
from werkzeug.exceptions import abort
from werkzeug.routing import BuildError
from flask import render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import AdminLoginForm, AdminRegisterForm
from extention import db
from users.models import User, UserRole
from models import Article


admin = Blueprint('admin', __name__, template_folder='templates/admin', static_folder='static')
login_manager = LoginManager(admin)
login_manager.session_protection = 'strong'


@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        try:
            adm_user = db.session.query(User).filter_by(
                username=form.username.data,role_id=1).first()
            if adm_user is None:
                flash('No admin-user found.', 'danger')
            else:
                if check_password_hash(adm_user.passwd, form.passwd.data):
                    login_user(adm_user)
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Invalid name or password!', 'danger')
        except Exception as err:
            flash(err, 'danger')
    return render_template('admin_login.html', form=form, title='Administrative authentification', btn_action='Login')


@admin.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route('/user_register', methods=['POST', 'GET'])
@login_required
def user_register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            rolename = form.rolename.data
            passwd = form.passwd.data
            username = form.username.data
            role_id = db.session.query(UserRole.id).filter_by(rolename=str(rolename)) if True else None

            new_user = User(username=username, email=email, passwd=generate_password_hash(passwd),
                            role_id=role_id, ulm=current_user.id)

            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created', 'success')
            return redirect(url_for('.dashboard'))

        except InvalidRequestError as ire:
            db.session.rollback()
            flash(f'Something is wrong! {ire}', 'danger')
        except IntegrityError as ige:
            db.session.rollback()
            flash(f'User already exists! {ige}', 'warning')
        except DataError as de:
            db.session.rollback()
            flash(f'Invalid Entry. {de} ', 'warning')
        except InterfaceError as ife:
            db.session.rollback()
            flash(f'Error connecting to the database. {ife}', 'danger')
        except DatabaseError as dbe:
            db.session.rollback()
            flash(f'Error connecting to the database. {dbe}', 'danger')
        except BuildError as be:
            db.session.rollback()
            flash(f'An error occurred ! {be}', 'danger')
    return render_template('dashboard.html', form=form, errors=form.errors)


@admin.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    form = AdminRegisterForm()
    users = db.session.query(User).order_by(User.username.asc()).all()
    roles = db.session.query(UserRole).order_by(UserRole.rolename.asc()).all()
    articles = db.session.query(Article).order_by(Article.dlm.desc()).all()

    return render_template('dashboard.html', form=form, users=users, roles=roles, articles=articles)


@admin.route('/dashboard/article/<int:id>', methods=['POST','GET'])
@login_required
def article(id):
    if id:
        art = db.session.query(Article).get(id)
        return render_template('article.html', article=art, id=id)
    else:
        return f'Post {id} does not exist'


@admin.route('/dashboard/article/<int:id>/update', methods=['POST', 'GET'])
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
            return redirect('/admin/dashboard')
        except Exception as e:
            return f'An error occurred while updating the article: {str(e)}'
    else:
        return render_template('art_update.html', article=article)


@admin.route('/dashboard/article/<int:id>/delete')
@login_required
def article_delete(id):
    article = db.session.get(Article, id)
    if article is None:
        abort(404)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/admin/dashboard')
    except Exception as err:
        return f'Error was found on delete apticle: {err}'