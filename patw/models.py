from patw import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}' created on {self.date_created})"

# in User # data = db.relationship('something model', backref='author', lazy=True)
# in other # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
