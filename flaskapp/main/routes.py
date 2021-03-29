from flask import Blueprint, render_template, request
from flaskapp.users.utils import refresh_count

from flaskapp.models import User, Course, subs
from flaskapp import db

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
def home():
    total_users = User.query.paginate().total
    total_courses = Course.query.paginate().total
    total_books = 0
    total_courses_bought = db.session.query(subs).count()
    refresh_count()
    return render_template('index.html', total_courses = total_courses, total_users=total_users,total_books=total_books, total_courses_bought=total_courses_bought)


