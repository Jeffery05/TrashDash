from flask import Blueprint

views = Blueprint("views", __name__)

#this will run the home page for the website
@views.route("/")
def home():
    return "<h1>Test</h1>"