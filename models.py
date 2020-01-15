import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    messages = db.relationship("Message", backref="channel", lazy=True)
    
    
    def add_channel(self):
        db.session.add(self)
        db.session.commit()
        return self

    def add_message(self, message, user_id):
        m = Message(message=message, channel_id=self.id, user_id=user_id)
        db.session.add(m)
        db.session.commit()
    

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def add_user(self):
        db.session.add(self)
        db.session.commit()

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    message = db.Column(db.String, nullable=False)

