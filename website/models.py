from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(250))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #picture_name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __repr__(self):
        return f"{self.title}|{self.description}|{self.longitude}|{self.latitude}|{self.date}|"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    litters_found = db.Column(db.Integer)
    litters_cleaned = db.Column(db.Integer)
    points = db.Column(db.Integer)
    donationValue = db.Column(db.Integer)
    reports = db.relationship('Report', backref="user")
