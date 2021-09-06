from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_login import current_user
from project.models import mongo

class LoginForm(FlaskForm):

    email=StringField('Email ',validators=[DataRequired(),Email(message="Not a valid Email Format.")])
    password=PasswordField('Password ',validators=[DataRequired()])
    submit=SubmitField('Log In!')

class RegistrationForm(FlaskForm):

    f_name=StringField('Full Name ',validators=[DataRequired()])
    email=StringField('Email ',validators=[DataRequired(),Email(message="Not a valid Email Format.")])
    username=StringField('Username ',validators=[DataRequired()])
    password=PasswordField('Password ',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm=PasswordField('Confirm Password ',validators=[DataRequired()])
    submit=SubmitField('Register Me!')

    def validate_email(self,email):
        if mongo.db.users.find_one({'Email':self.email.data}):
            raise ValidationError('Your Email has already been registered!')

    def validate_username(self,username):
        if mongo.db.users.find_one({'username':self.username.data}):
            raise ValidationError('Your username has already been registered!')
        

class BookTicketForm(FlaskForm):

    name=StringField('Name ', validators=[DataRequired()])
    ticket_count=IntegerField('No of Ticket ',validators=[DataRequired()])
    book_ticket=SubmitField('Book Ticket')