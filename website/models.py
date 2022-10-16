from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
#from sqlalchemy import Column, ForeignKey, Integer, Unicode
#from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_imageattach.entity import Image, image_attachment

#Base = declarative_base()

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(250))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #picture = image_attachment('UserPicture')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(20), nullable=False)
    #last_name = db.Column(db.String(20), nullable=False)
    #reports = db.relationship('Report')

"""
class ReportPicture(Base, Image, db.Model):
    report_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    report = db.relationship('User')
    __tablename__ = 'report_picture'
"""