from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql import func
import json
import time
import traceback
import json
# get this object
from flask import Response


views = Blueprint("views", __name__)

#this one will run the home page for the website
@views.route("/")
def home():
    return render_template("index.html", user=current_user)

@views.route("/dashboard")
#@login_required
def dashboard():
    #current_user = User.query.all()
    return render_template("dashboard.html", user=current_user)

@views.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    if request.method == "POST":
        donationAMT = request.form.get("Quantity")
        #console.log(donationAMT)
        user = User.query.filter_by(username=current_user.username).first()

        try:
            if (user.points < float(donationAMT)):
                flash("You do not have sufficent funds to complete this transaction.", category="error")
            else:
                user.points = user.points - float(donationAMT)
                if not user.donationValue:
                    user.donationValue = float(donationAMT) / 100.0
                else:
                    user.donationValue = user.donationValue + (float(donationAMT) / 100.0)
                print("Donated")
                print(user.donationValue)
                db.session.commit()
        except:
            flash("Please make sure you have sufficient funds.", category="error")
    time.sleep(0.1)
    return render_template("donate.html", user=current_user)

@views.route("/resolve", methods=["GET", "POST"])
@login_required
def resolve():
    if request.method == "POST":
        #title = request.form.get("title-text")
        #msg = request.form.get("message")
        long = request.form.get("longitude")
        lat = request.form.get("latitude")

        try:
            temp_num = float(long)
            long = round(temp_num * 100000)/100000.0
            temp_num = float(lat)
            lat = round(temp_num * 100000)/100000.0
            user = User.query.filter_by(username=current_user.username).first()

            if not user.litters_cleaned:
                user.litters_cleaned = 1
            else:
                user.litters_cleaned = user.litters_cleaned + 1

            if not user.points:
                user.points = 100
            else:
                user.points = user.points + 100

            report_to_be_removed = db.session.query(Report).filter_by(longitude=long, latitude=lat).first()
            #print("We have reached this point successfully")
            print(report_to_be_removed)
            #report_to_be_removed = Report.query.filter_by(long=long).filter_by(lat=lat).first()
            db.session.delete(report_to_be_removed)
            db.session.commit() #updates the database
            flash("Thank you for cleaning up the trash!", category="success")
        except:
            flash("Please make sure that the inputted values for the latitude and/or longitude are valid decimals.", category="error")

    time.sleep(0.1)

    reports = Report.query.all()
    return render_template("resolve.html", user=current_user, reports2=reports)

@views.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        title = request.form.get("title-text")
        msg = request.form.get("message")
        long = request.form.get("longitude")
        lat = request.form.get("latitude")

        try:
            temp_num = float(long)
            long = round(temp_num * 100000)/100000.0
            temp_num = float(lat)
            lat = round(temp_num * 100000)/100000.0
            if len(title) > 100:
                flash("Title must be less than 101 characters.", category="error")
            elif len(msg) > 250:
                flash("Description must be less than 251 characters.", category="error")
            else:
                user = User.query.filter_by(username=current_user.username).first()
                
                if not user.litters_found:
                    user.litters_found = 1

                else:
                    user.litters_found = user.litters_found + 1

                if not user.points:
                    user.points = 100
                else:
                    user.points = user.points + 100

                new_report = Report(title=title, description=msg, longitude=long, latitude=lat, user_id=user.id, date=func.now())
                db.session.add(new_report)
                db.session.commit() #updates the database
                
                flash("Thank you for the reporting trash!", category="success")
        except:
            print(traceback.format_exc())
            flash("Please make sure that the inputted values for the latitude and/or longitude are valid decimals.", category="error")

    time.sleep(0.1)

    reports = Report.query.all()
    return render_template("report.html", user=current_user, reports=reports)

@views.route("/fetchLocations", methods=["GET", "POST"])
def fetchLocations():
    reports = Report.query.all()
    resp = "|".join([report.__repr__() for report in reports])
    return Response(resp)

from . import db
from .models import User, Report