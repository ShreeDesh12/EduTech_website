from flaskapp.models import User, Course, subs
import os
from PIL import Image
from flask import url_for
from flaskapp import db, app

def savepicture(form_pic,file_name, folder='courses'):
    picPath = os.path.join(app.root_path , 'static/'+folder , str(file_name) + '.svg')
    form_pic.save(picPath)

def refresh_count():
    total_users = User.query.paginate().total
    total_courses = Course.query.paginate().total
    total_books = 0
    total_courses_bought = db.session.query(subs).count()
