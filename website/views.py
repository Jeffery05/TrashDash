from flask import Blueprint, render_template

views = Blueprint("views", __name__)

#this one will run the home page for the website
@views.route("/")
def home():
    return render_template("index.html")

@views.route("/c")
def dashboard():
    return render_template("dashboard.html")

@views.route("/donate")
def donate():
    return render_template("donate.html")

@views.route("/resolve")
def resolve():
    return render_template("resolve.html")

@views.route("/report")
def report():
    return render_template("report.html")
