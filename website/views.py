from flask import Blueprint, render_template

views = Blueprint("views", __name__)

#this will run the home page for the website
@views.route("/")
def home():
    return render_template("index.html")
