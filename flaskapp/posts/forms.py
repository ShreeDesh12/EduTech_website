from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError

#number = "+49 176 1234 5678"

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

