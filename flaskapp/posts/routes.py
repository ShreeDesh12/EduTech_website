from flask import Blueprint, render_template, redirect, flash, url_for, abort
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import User, Course, Ans, Post
from flaskapp.posts.forms import loginForm, ansForm, uploadCourse, questionForm, 

posts = Blueprint('posts', __name__)


@posts.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and (bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                try: 
                    load = redirect(next_page, user_id = user.id)
                except:
                    load = redirect(next_page)
                return load
            return redirect(url_for('account', user_id = user.id))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@posts.route('/add-course/<course_id>')
@login_required
def add_course(course_id):
    if current_user.admin == False:
        c = Course.query.get(course_id)
        current_user.courses.append(c)
        db.session.commit()
        return redirect(url_for('account',user_id = current_user.id))
    else:
        abort()


@posts.route('/post/<int:post_id>', methods = ['GET','POST'])
@login_required
def enter_ans(post_id):
    accform = ansForm()
    if accform.validate_on_submit():
        ans = Ans()
        ans.sol = accform.answer.data
        ans.user_id = current_user.id
        ans.post_id = post_id
        db.session.add(ans)
        db.session.commit()
        return redirect(url_for('askQues'))
    return render_template('answer.html', accform = accform, heading = 'Question', post = Post.query.get(post_id))




@posts.route('/upload-courses', methods=['GET', 'POST'])
@login_required
def upload_course():
    if current_user.admin == False:
        abort(403)
    accform = uploadCourse()
    if accform.validate_on_submit():
        c1 = Course(name = accform.name.data, price = accform.price.data)
        db.session.add(c1)
        db.session.commit()
        savepicture(accform.picture.data,file_name=c1.id,  folder='courses')
        return  redirect(url_for('allcourses'))
    return render_template('uploadCourse.html', title='Upload Course', accform = accform)


@posts.route('/account/ask-ques', methods = ['GET', 'POST'])
@login_required
def askQues():
    accform = questionForm()
    if accform.validate_on_submit():
        p = Post()
        p.ques = accform.question.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('askQues'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5)
    return render_template('account_forms.html', accform = accform, posts = posts, heading='Ask Questions')
