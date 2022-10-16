from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Report
from sqlalchemy.sql import func
import json

views = Blueprint("views", __name__)

#this one will run the home page for the website
@views.route("/")
def home():
    return render_template("index.html", user=current_user)

@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@views.route("/donate")
def donate():
    return render_template("donate.html", user=current_user)

@views.route("/resolve")
def resolve():
    return render_template("resolve.html", user=current_user)

@views.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        title = request.form.get("title-text")
        msg = request.form.get("message")
        long = request.form.get("longitude")
        lat = request.form.get("latitude")

        try:
            float(long)
            float(lat)
            if len(title) > 100:
                flash("Title must be less than 101 characters.", category="error")
            elif len(msg) > 251:
                flash("Title must be less than 101 characters.", category="error")
            else:
                new_report = Report(title=title, description=msg, longitude=long, latitude=lat, date=func.now())
                db.session.add(new_report)
                db.session.commit() #updates the database
                flash("Thank you for reporting trash!", category="success")
        except:
            flash("Please make sure that the inputted values for the latitude and/or longitude are numbers.", category="error")

    return render_template("report.html", user=current_user)
