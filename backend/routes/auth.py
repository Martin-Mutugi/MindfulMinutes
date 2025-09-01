from flask import Blueprint, render_template, redirect, url_for, flash, request
from backend.forms import LoginForm, RegistrationForm
from backend.extensions import db
from backend.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask_login import login_user, logout_user, current_user


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print("User found:", user)
        if user and check_password_hash(user.password_hash, form.password.data):
            print("Password match:", True)
            login_user(user)
            print("Logged in:", current_user.is_authenticated)
            return redirect(url_for('dashboard.index'))
        else:
            print("Login failed")
            flash('Invalid credentials', 'danger')
    return render_template('auth/login.html', form=form)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot_password.html')
