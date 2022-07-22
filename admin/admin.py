from datetime import datetime
from flask import Blueprint, flash, redirect, url_for, g
from flask_login import login_user, logout_user, LoginManager, login_required, login_fresh, current_user
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError, InterfaceError, DatabaseError
from werkzeug.exceptions import abort
from werkzeug.routing import BuildError
from flask import render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import AdminLoginForm, AdminRegisterForm, AddNewRole, ArticleStatusUpdate
from extention import db
from users.models import User, UserRole
from models import Article, Status


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


####################################################

@admin.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    reg_form = AdminRegisterForm()
    role_form = AddNewRole()
    users = db.session.query(User).order_by(User.id.asc()).all()
    roles = db.session.query(UserRole).order_by(UserRole.id.asc()).all()
    articles = db.session.query(Article).order_by(Article.dlm.desc()).all()

    # print(col1)
    return render_template('dashboard.html', reg_form=reg_form, role_form=role_form,
                           users=users, roles=roles, articles=articles)


####################################################

# Users

@admin.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route('/user_register', methods=['POST', 'GET'])
@login_required
def user_register():
    reg_form = AdminRegisterForm()
    if reg_form.validate_on_submit():
        try:
            email = reg_form.email.data
            rolename = reg_form.rolename.data
            passwd = reg_form.passwd.data
            username = reg_form.username.data
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
    return render_template('dashboard.html', reg_form=reg_form, errors=reg_form.errors)


# Articles

@admin.route('/dashboard/article/<int:id>', methods=['POST','GET'])
@login_required
def article(id):
    if id:
        _status = Status()
        specific_article = db.session.query(Article).get(id)
        status_code_name = str(specific_article.status) + ' - ' + _status.get_name(id=specific_article.status)
        return render_template('article.html', specific_article=specific_article,
                               status_code_name=status_code_name, id=id)
    else:
        return f'Post {id} does not exist'


@admin.route('/dashboard/article/<int:id>/update', methods=['POST', 'GET'])
@login_required
def article_update(id):
    article = db.session.query(Article).get(id)
    status_form = ArticleStatusUpdate()
    _status = Status()
    status_code_name = str(article.status) + ' - ' + _status.get_name(id=article.status)

    status_form.status.blank_text = status_code_name

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        if request.form['status'] != '__None':
            print(request.form['status'])
            article.status = _status.get_code(id=request.form['status'])
        print(request.form['status'])
        article.dlm = datetime.utcnow()

        article = Article(title=article.title, intro=article.intro, text=article.text,
                          status=article.status, dlm=article.dlm)

        try:
            db.session.commit()
            return redirect('/admin/dashboard')
        except Exception as e:
            return flash(f'An error has occurred while updating the article: {str(e)}', 'danger')
    else:
        return render_template('art_update.html', article=article, status_form=status_form)


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
        return flash(f'Error was found on delete apticle: {err}', 'danger')


# Roles
@admin.route('/add_role', methods=['POST', 'GET'])
@login_required
def add_role():
    role_form = AddNewRole()
    reg_form = AdminRegisterForm()
    if role_form.validate_on_submit():
        rolename = role_form.rolename.data
        status = role_form.status.data
        ulm = current_user.id

        newrole = UserRole(rolename=rolename, ulm=ulm, status=status.code)
        try:
            db.session.add(newrole)
            db.session.commit()
            return redirect(url_for('.dashboard'))
        except BaseException as err:
            db.session.rollback()
            flash (f'Error with adding new role occurred. {err}', 'danger')
    return render_template('dashboard.html', role_form=role_form, reg_form=reg_form, errors=role_form.errors)