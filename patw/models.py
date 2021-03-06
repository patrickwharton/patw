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

    def get_username(self):
        return str(self.username)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}' created on {self.date_created})"

class Polar(db.Model):
    __tablename__ = "polar"

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.BigInteger, nullable=False)
    end_time = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    map_name = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    __table_args__ = (db.UniqueConstraint('country_code', 'start_time', 'end_time', 'user_id', 'map_name', name="_multiple_countries_uc"),)

    def __repr__(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        # return f"{user.username} spent from {self.start_time} to {self.end_time} for a total of
        #             {self.end_time - self.start_time} in {self.country_code} [{self.map_name}]"
        return f"{user.username} was in {self.country_code} from {datetime.utcfromtimestamp(self.start_time)} \
                    until {datetime.utcfromtimestamp(self.start_time)} for a total of \
                    {((self.end_time - self.start_time) / 86400):.2f} days. [{self.map_name}]"
