from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))


subs = db.Table('subs',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable = False)
    dob= db.Column(db.Date, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    number = db.Column(db.String(13), nullable=False)
    confirmed = db.Column(db.Boolean, default = False, nullable = False)
    admin = db.Column(db.Boolean, default = False, nullable = False)
    courses = db.relationship('Course', secondary=subs, lazy='dynamic',
        backref=db.backref('subscribers', lazy=True))
    answer = db.relationship('Ans', backref = db.backref('author'), lazy = True)
    def __repr__(self):
        return f"User('{self.email}','{self.firstname}','{self.lastname}','{self.dob}','{self.number}','{self.confirmed}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"course( '{self.name}', '{self.price}' )"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    ques = db.Column(db.String(150), nullable = False)
    answers = db.relationship('Ans', backref = db.backref('question'), lazy = True)
    def __repr__(self):
        return f"post('{self.ques}')"

class Ans(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sol = db.Column(db.String(500), nullable =False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f"'{self.post_id}','{self.sol}'"
