from datetime import datetime
from pytz import timezone

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError, InterfaceError, DatabaseError
from werkzeug.routing import BuildError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message

from .models import User, UserRole
from .forms import LoginForm, RegisterForm, PasswdForgotForm, PasswdRecover
from extention import db, mail


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

        except InvalidRequestError as ire:
            db.session.rollback()
            flash(f'Something is wrong! {ire}', 'danger')
        except IntegrityError as ige:
            db.session.rollback()
            flash(f'User already exists!. {ige}', 'warning')
        except DataError as de:
            db.session.rollback()
            flash(f'Invalid Entry. {de}', 'warning')
        except InterfaceError as ife:
            db.session.rollback()
            flash(f'Error connecting to the database. {ife}', 'danger')
        except DatabaseError as dbe:
            db.session.rollback()
            flash(f'Error connecting to the database. {dbe}', 'danger')
        except BuildError as be:
            db.session.rollback()
            flash(f'An error occurred! {be}', 'danger')
    return render_template('register.html',form=form,text='Create account',
                           title='Register',btn_action='Register account')


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


@users.route('/password_forgot', methods=['POST', 'GET'])
def passwd_forgot():
    passfg_form = PasswdForgotForm()
    if request.method == 'POST':
        if passfg_form.validate_on_submit():
            user = db.session.query(User).filter_by(email=passfg_form.email.data).first()
            if user:
                try:
                    msg = Message(subject='Password forgotten', sender='mysimpleblog.notifier@gmail.com',
                                  recipients=[str(passfg_form.email.data),],
                                  html= f'Please open the link to change your password '
                                        f'http://127.0.0.1:5000/users/password_recover/{user.id}')
                    mail.send(msg)
                    flash(f'Email sent to {passfg_form.email.data} successful', 'success')
                    return render_template('password_forgot.html', passfg_form=passfg_form, success='success')
                except Exception as err:
                    flash(f'Mail sending error was found: {err}')
            else:
                flash(f'Email {passfg_form.email.data} not found', 'danger')
            return render_template('password_forgot.html', passfg_form=passfg_form)
    else:
        return render_template('password_forgot.html', passfg_form=passfg_form)


@users.route('/password_recover/<int:id>', methods=['POST', 'GET'])
def passwd_recover(id):
    passrec_form = PasswdRecover()
    if passrec_form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(id=id).first()
            user.passwd = generate_password_hash(passrec_form.passwd.data)
            user.dlm = datetime.now(timezone('Europe/Kiev'))
            user.ulm = id
            db.session.commit()
            flash('Password changed successful', 'success')
        except BaseException as err:
            db.session.rollback()
            flash(f'Password changing error found. {err}')
    return render_template('password_recover.html', passrec_form=passrec_form)