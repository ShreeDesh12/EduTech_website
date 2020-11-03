from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import User
from flask_login import current_user
from flaskapp import bcrypt
from datetime import date

#number = "+49 176 1234 5678"

class loginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Submit')

class registerForm(FlaskForm):
    firstname = StringField('First name', validators = [DataRequired(),Length(min=2,max=60)])
    lastname = StringField('Last name', validators = [DataRequired(),Length(min=2,max=60)])
    dob = DateField('DOB', validators = [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    Confirmpassword = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already present')

    def validate_dob(self, dob):
        d = date.today()
        dob = dob.data
        if (d.year-dob.year)<=17:
            print('Only 18+ allowed')
            raise ValidationError('Only 18+ allowed')
        elif d.year-dob.year==18:
            if d.month>=dob.month and d.day>=dob.day:
                pass
            else:
                raise ValidationError('Only 18+ allowed')
        else:
            pass

class loginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Submit')

class TelephoneForm(FlaskForm):
    number = IntegerField('Number',validators = [DataRequired()])
    submit = SubmitField('Generate OTP')
    def validate_number(self, number):
        user = User.query.filter_by(number=number.data).first()
        if user:
            raise ValidationError('Number already present')

class otpForm(FlaskForm):
    otp = IntegerField('Number',validators = [DataRequired()])
    submit = SubmitField('Submit OTP')

class questionForm(FlaskForm):
    question = StringField('Add new Question', validators = [DataRequired()])
    submit = SubmitField('Add question')

class ansForm(FlaskForm):
    answer = StringField('Your Answer', validators = [DataRequired(),Length(max = 500)])
    submit = SubmitField('Submit Solution')

class uploadCourse(FlaskForm):
    picture = FileField('Update profile picture', validators = [FileAllowed(['svg']), DataRequired()])
    name = StringField('Course name', validators = [DataRequired()])
    price = IntegerField('Price', validators = [DataRequired()])
    submit = SubmitField('Submit')

