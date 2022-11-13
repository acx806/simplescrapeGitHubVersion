from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    # first_name = db.Column(db.String(150))
    # last_name = db.Column(db.String(150))
    account_creation_date = db.Column(db.DateTime(timezone=True), default=func.now())

    website = db.relationship("Website", backref="user", lazy=True)

    def get_id(self):
        return (self.user_id)


class Website(db.Model):
    website_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    url = db.Column(db.String(1000))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    regex = db.Column(db.String(500))
    search_string = db.Column(db.String(500))

    def get_id(self):
        return (self.website_id)


class Data(db.Model):
    data_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website_id = db.Column(db.Integer, db.ForeignKey("website.website_id"), nullable=False)

    content = db.Column(db.String(2000))
    content_date = db.Column(db.DateTime(timezone=True), default=func.now())

    def get_id(self):
        return (self.data_id)
