from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .models import User, Report
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
    user = db.session.query(User).filter_by(username=current_user.username).first()
    print(user.donationValue)
    #current_user = User.query.all()
    return render_template("dashboard.html", user=current_user)

@views.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    if request.method == "POST":
        donationAMT = int(request.form.get("Quantity"))
        charity = request.form.get("Charity")
        #console.log(donationAMT)
        user = db.session.query(User).filter_by(username=current_user.username).first()

        if (charity == "null"):
            flash("Please enter a valid charity!", category="error")
        elif (donationAMT <= 0):
            flash("Please enter a positive integer for the amount of money you want to donate.", category="error")
        elif (user.points < donationAMT):
            flash("You do not have sufficent funds to complete this transaction.", category="error")
        else:
            user.points -= donationAMT
            user.donationValue += (float(donationAMT) / 100.0)

            """
            if not user.donationValue:
                user.donationValue = float(donationAMT) / 100.0
            else:
                user.donationValue = user.donationValue + (float(donationAMT) / 100.0)
            """

            print("Donated")
            print(user.donationValue)
            flash("Thank you for donating $" + str((float(donationAMT) / 100.0)) + "!", category="success")
            db.session.commit()
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
        except:
            print(traceback.format_exc())
            flash("Please make sure that the inputted values for the latitude and/or longitude are valid decimals.", category="error")
        user = db.session.query(User).filter_by(username=current_user.username).first()
        
        user.litters_cleaned += 1
        user.points += 100

        """
        if not user.litters_cleaned:
            user.litters_cleaned = 1
        else:
            user.litters_cleaned = user.litters_cleaned + 1

        if not user.points:
            user.points = 100
        else:
            user.points = user.points + 100
        """

        report_to_be_removed = db.session.query(Report).filter_by(longitude=long, latitude=lat).first()
        #print("We have reached this point successfully")
        print(report_to_be_removed)
        #report_to_be_removed = Report.query.filter_by(long=long).filter_by(lat=lat).first()
        if (report_to_be_removed is not None):
            db.session.delete(report_to_be_removed)
            db.session.commit() #updates the database
            flash("Thank you for cleaning up the trash!", category="success")
        else:
            flash("Please click on an actual trash site.", category="error")

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
        except:
            print(traceback.format_exc())
            flash("Please make sure that the inputted values for the latitude and/or longitude are valid decimals.", category="error")

        if len(title) > 100:
            flash("Title must be less than 101 characters.", category="error")
        elif len(msg) > 250:
            flash("Description must be less than 251 characters.", category="error")
        else:
            user = db.session.query(User).filter_by(username=current_user.username).first()
            
            user.litters_found += 1
            user.points += 100

            """
            if not user.litters_found:
                user.litters_found = 1
            else:
                user.litters_found = user.litters_found + 1

            if not user.points:
                user.points = 100
            else:
                user.points = user.points + 100
            """

            new_report = Report(title=title, description=msg, longitude=long, latitude=lat, user_id=user.id, date=func.now())
            db.session.add(new_report)
            db.session.commit() #updates the database
            
            flash("Thank you for the reporting trash!", category="success")

    time.sleep(0.1)

    reports = Report.query.all()
    return render_template("report.html", user=current_user, reports=reports)

@views.route("/fetchLocations", methods=["GET", "POST"])
def fetchLocations():
    reports = Report.query.all()
    resp = "|".join([report.__repr__() for report in reports])
    return Response(resp)

from . import db