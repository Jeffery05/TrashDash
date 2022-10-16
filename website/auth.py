#from distutils.command import check
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).one()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.dashboard"))
                else:
                    flash("Incorrect password, try again.", category="error")
        except:
            flash("Username does not exist.", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email is taken.", category="error")
            elif len(email) < 4:
                flash("Email must be greater than 3 characters.", category="error")
            elif len(username) < 2:
                flash("Username must be greater than 1 character.", category="error")
            elif password1 != password2:
                flash("Passwords don't match.", category="error")
            elif len(password1) < 7:
                flash("Password must be at least 7 characters.", category="error")
            else:
                #add user to the database
                new_user = User(email=email, password=generate_password_hash(password1, method="sha256"), username=username)
                db.session.add(new_user)
                db.session.commit() #updates the database
                flash("Account created!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.dashboard")) #this doesn't redirect to a URL, it just redirects to the HTML file that should be rendered next.
        except:
            pass

    return render_template("signup.html", user=current_user)