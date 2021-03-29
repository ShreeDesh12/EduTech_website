from flask import Blueprint, render_template, request
from flaskapp.users.utils import refresh_count

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
def home():
    refresh_count()
    return render_template('index.html', total_courses = total_courses, total_users=total_users,total_books=total_books, total_courses_bought=total_courses_bought)


