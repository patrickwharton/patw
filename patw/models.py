from datetime import datetime
from flask_login import UserMixin
from patw import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    map_data = db.relationship("Polar", backref="user", lazy=True)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}' created on {self.date_created})"

class Polar(db.Model):
    __tablename__ = "polar"

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), nullable=False)
    time_spent = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    __table_args__ = (db.UniqueConstraint('country_code', 'user_id', name="_multiple_countries_uc"),)

    def __repr__(self):
        return f"User #{user_id} spent {time_spent} seconds in {country_code}"
# in User # data = db.relationship('something model', backref='author', lazy=True)
# in other # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
