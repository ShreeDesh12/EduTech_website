from flask import Blueprint, redirect, render_template, url_for, request, flash, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User, Post, Ans, subs, Course
from flaskapp.users.forms import registerForm, TelephoneForm, otpForm, loginForm
from flaskapp.users.utils import savepicture, refresh_count
import os

users = Blueprint('users', __name__)


@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
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
            return redirect(url_for('users.account', user_id = user.id))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title = 'Login', form = form)



@users.route('/register', methods = ['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        hashedpwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        session['firstname']=form.firstname.data
        session['lastname']=form.lastname.data
        session['email']=form.email.data
        session['password']=hashedpwd
        dob = str(form.dob.data)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        session['dob'] = dob
        if(user.email == User.query.filter_by(email = user.email).first()):
            flash('Email already exist', 'danger')
            return redirect(url_for('users.register'))
        flash('Form submitted successfully', 'success')
        #print('session opt - ', session['otp'])
        print('Form submitted')
        return redirect(url_for('users.mobileform'))
    return render_template('register.html', title = 'user-form', form = form)
    



@users.route('/generate-otp/', methods = ['GET', 'POST'])
def mobileform():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = TelephoneForm()
    if form.validate_on_submit():
        number = form.number.data
        print('Number submitted')
        session['otp'] = generateOTP(str(number))
        if session['otp']:
            session['number'] = number
            flash("OTP Generated", 'info')
            return redirect(url_for('mobileConfirmation'))
        else:
            flash('Enter valid mobile number')
            return redirect(url_for('users.mobileform'))
    return render_template('mobileForm.html', title = "Generate OTP", form = form)

        
@users.route('/check-otp', methods=['GET', 'POST'])
def mobileConfirmation():
    if current_user.is_authenticated:
        return redirect(url_for('users.account', user_id = current_user.id))
    form = otpForm()
    if form.validate_on_submit():
        otp = form.otp.data
        if otp == session['otp']:
            u = user(
                firstname=session['firstname'], lastname = session['lastname'], 
                email = session['email'], password = session['password'],
                dob = session['dob'], number = session['number']
            )
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            mail_content = 'Please confirm your email by clicking on ' + confirm_url
            subject = "Please confirm your email"
            send_email(user.email, subject, mail_content)
            login_user(user)
            flash('Successfully Registered', 'success')
            return redirect(url_for('users.account', user_id = user.id))
        else:
            flash('OTP not matched', 'danger')
    return render_template('checkOTP.html', form = form, title = 'Check OTP')


@users.route('/account/<user_id>')
@login_required
def account(user_id):
    if current_user.admin:
        return redirect(url_for('users.allcourses'))
    return render_template('account.html', title = 'Account', heading = 'My courses')


@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if current_user.is_authenticated:
        flash('Email is already confirmed')
        return redirect(url_for('users.account'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))



@users.route('/account/courses', methods = ['GET', 'POST'])
@login_required
def allcourses():
    courses = Course.query.all()
    return render_template('courses.html', courses = courses, heading='All courses')


@users.route('/deleteCourse/<course_id>')
@login_required
def delete_course(course_id):
    if current_user.admin:
        c = Course.query.get(course_id)
        db.session.delete(c)
        db.session.commit()
        picPath = os.path.join(current_app.root_path , 'static/courses' , str(course_id) + '.svg')
        if os.path.exists(picPath):
          os.remove(picPath)
        return redirect(url_for('users.allcourses'))
    else:
        abort()



@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
