from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if any field is empty
        if not email or not username or not password1 or not password2:
            flash('Please fill in all the fields.', category='danger')
            return render_template("signup.html", user=current_user)

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='danger')
        elif username_exists:
            flash('Username is already in use.', category='danger')
        elif password1 != password2:
            flash('Password don\'t match!', category='danger')
        elif len(username) < 2:
            flash('Username is too short.', category='danger')
        elif len(password1) < 6:
            flash('Password is too short.', category='danger')
        elif len(email) < 4:
            flash('Email is invalid.', category='danger')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("signup.html", user=current_user)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash('Please fill in all the fields.', category='danger')
            return render_template("login.html", user=current_user)

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='danger')
        else:
            flash('User does not exist. Please sign up.', category='danger')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.out"))