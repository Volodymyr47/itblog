from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError, InterfaceError, DatabaseError
from werkzeug.routing import BuildError
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, UserRole
from .forms import LoginForm, RegisterForm
from extention import db


users = Blueprint('users', __name__, template_folder='templates/users', static_folder='/static')
login_manager = LoginManager(users)
login_manager.session_protection = 'strong'


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            passwd = form.passwd.data
            username = form.username.data
            role_id = db.session.query(UserRole.id).filter_by(rolename='Guest') if True else None
            new_user = User(username=username, email=email, passwd=generate_password_hash(passwd), role_id=role_id)

            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created', 'success')
            return redirect(url_for('.login'))

        except InvalidRequestError:
            db.session.rollback()
            flash('Something is wrong!', 'danger')
        except IntegrityError:
            db.session.rollback()
            flash('User already exists!.', 'warning')
        except DataError:
            db.session.rollback()
            flash('Invalid Entry', 'warning')
        except InterfaceError:
            db.session.rollback()
            flash('Error connecting to the database', 'danger')
        except DatabaseError:
            db.session.rollback()
            flash('Error connecting to the database', 'danger')
        except BuildError:
            db.session.rollback()
            flash('An error occurred !', 'danger')
    return render_template('register.html',form=form,text='Create account',title='Register',btn_action='Register account')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(email=form.email.data).first()
            if user is None:
                flash('No user found.', 'danger')
            else:
                if check_password_hash(user.passwd, form.passwd.data):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('Invalid email or password!', 'danger')
        except Exception as err:
            flash(err, 'danger')
    return render_template('login.html', form=form, text='Login', title='Login', btn_action='Login')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@users.route('/password_forgot')
def passwd_forgot():
    pass