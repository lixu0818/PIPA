# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        try:
            email_exists = User.query.filter_by(email=field.data).first()
        except:
            email_exists = User.query.filter_by(email=field.data).first()
        if email_exists:
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        try:
            username_exists = User.query.filter_by(username=field.data).first()
        except:
            username_exists = User.query.filter_by(username=field.data).first()
        if username_exists:
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')