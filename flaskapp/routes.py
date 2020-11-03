from flask import render_template, url_for,flash,redirect , request, session, abort
from flaskapp.form import loginForm, registerForm, TelephoneForm, otpForm, loginForm,questionForm, ansForm, uploadCourse
from flaskapp.models import User, Course, Post, Ans, subs
from flaskapp.token import generate_confirmation_token, confirm_token, send_email, generateOTP
from flaskapp import app, db, login_manager, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from PIL  import Image
from datetime import date
import os

def refresh_count():
    total_users = User.query.paginate().total
    total_courses = Course.query.paginate().total
    total_books = 0
    total_courses_bought = db.session.query(subs).count()

@app.route('/', methods = ['GET', 'POST'])
def home():
    refresh_count()
    return render_template('index.html', total_courses = total_courses, total_users=total_users,total_books=total_books, total_courses_bought=total_courses_bought)


user = User()

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        hashedpwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.email=form.email.data
        user.password=hashedpwd
        dob = str(form.dob.data)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        user.dob = dob
        if(user.email == User.query.filter_by(email = user.email).first()):
            flash('Email already exist', 'danger')
            return redirect(url_for('register'))
        flash('Form submitted successfully', 'success')
        #print('session opt - ', session['otp'])
        print('Form submitted')
        return redirect(url_for('mobileform'))
    return render_template('register.html', title = 'user-form', form = form)
    

@app.route('/generate-otp/', methods = ['GET', 'POST'])
def mobileform():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = TelephoneForm()
    if form.validate_on_submit():
        number = form.number.data
        print('Number submitted')
        session['otp'] = generateOTP(str(number))
        if session['otp']:
            user.number = number
            flash("OTP Generated", 'info')
            return redirect(url_for('mobileConfirmation'))
        else:
            flash('Enter valid mobile number')
            return redirect(url_for('mobileform'))
    return render_template('mobileForm.html', title = "Generate OTP", form = form)
    
@app.route('/check-otp', methods=['GET', 'POST'])
def mobileConfirmation():
    if current_user.is_authenticated:
        return redirect(url_for('account', user_id = current_user.id))
    form = otpForm()
    if form.validate_on_submit():
        otp = form.otp.data
        if otp == session['otp']:
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            mail_content = 'Please confirm your email by clicking on ' + confirm_url
            subject = "Please confirm your email"
            send_email(user.email, subject, mail_content)
            login_user(user)
            flash('Successfully Registered', 'success')
            return redirect(url_for('account', user_id = user.id))
        else:
            flash('OTP not matched', 'danger')
    return render_template('checkOTP.html', form = form, title = 'Check OTP')


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if current_user.is_authenticated:
        flash('Email is already confirmed')
        return redirect(url_for('account'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
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
                return redirect(next_page, user_id = user.id)
            return redirect(url_for('account', user_id = user.id))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/account/<user_id>')
@login_required
def account(user_id):
    if current_user.admin:
        return redirect(url_for('allcourses'))
    return render_template('account.html', title = 'Account', heading = 'My courses')

@app.route('/deleteCourse/<course_id>')
@login_required
def delete_course(course_id):
    if current_user.admin:
        c = Course.query.get(course_id)
        db.session.delete(c)
        db.session.commit()
        picPath = os.path.join(app.root_path , 'static/courses' , str(course_id) + '.svg')
        if os.path.exists(picPath):
          os.remove(picPath)
        return redirect(url_for('allcourses'))
    else:
        abort()


@app.route('/add-course/<course_id>')
@login_required
def add_course(course_id):
    if current_user.admin == False:
        c = Course.query.get(course_id)
        current_user.courses.append(c)
        db.session.commit()
        return redirect(url_for('account',user_id = current_user.id))
    else:
        abort()


@app.route('/account/ask-ques', methods = ['GET', 'POST'])
@login_required
def askQues():
    accform = questionForm()
    if accform.validate_on_submit():
        p = Post()
        p.ques = accform.question.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('askQues'))
    posts = Post.query.all()
    return render_template('account_forms.html', accform = accform, posts = posts, heading='Ask Questions')

@app.route('/post/<int:post_id>', methods = ['GET','POST'])
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


@app.route('/account/courses', methods = ['GET', 'POST'])
@login_required
def allcourses():
    courses = Course.query.all()
    return render_template('courses.html', courses = courses, heading='All courses')



def savepicture(form_pic,file_name, folder='courses'):
    picPath = os.path.join(app.root_path , 'static/'+folder , str(file_name) + '.svg')
    form_pic.save(picPath)

@app.route('/upload-courses', methods=['GET', 'POST'])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
