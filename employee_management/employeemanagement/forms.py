from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     IntegerField, DateField, TextAreaField)
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange
from wtforms.fields.html5 import EmailField
from wtforms.widgets.html5 import SearchInput
from employeemanagement.models import Employee
from datetime import date, datetime


class RegistrationForm(FlaskForm):
    FirstName = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    LastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999, message="Please enter a 10 digit no ")])
    dob = DateField('Date', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Username is taken please choose a different one')

    def validate_dob(self, dob):
        delta = (date.today() - dob.data).days/365
        print(delta)
        if delta<=18:
            raise ValidationError("Age of Employee must be greater than 18 years")



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    FirstName = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    LastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    dob = DateField('Date of birth', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')


class SearchForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-sm btn-block'})

class ChangePassword(FlaskForm):
    OldPassword = PasswordField('Old Password', validators=[DataRequired()])
    NewPassword = PasswordField('New Password', validators=[DataRequired()])
    ConfirmNewPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('NewPassword')])
    submit = SubmitField('Update', render_kw={'class': 'btn btn-success btn-sm btn-block'})


class NewAnnouncement(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date_posted = DateField('Date', validators=[DataRequired()], default=datetime.utcnow)
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Update', render_kw={'class': 'btn btn-success btn-sm btn-block'})

class UpdateAnnouncement(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Update', render_kw={'class': 'btn btn-success btn-sm btn-block'})


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')