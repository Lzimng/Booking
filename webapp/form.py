from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField
from wtforms.fields.core import DateField, Label
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from webapp.models import User
from datetime import date

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class BookingForm(FlaskForm):
    
    def validate_start(self, start_to_check):
        today = date.today()
        if start_to_check.data < today:
            raise ValidationError('Start date is earlier than today!')

    def validate_end(form, field):
        today = date.today()
        if field.data < today:
            raise ValidationError('End date is earlier than today!')
        if field.data < form.start.data:
            raise ValidationError("End date must not be earlier than start date.")

    ins_name = StringField()
    user_id = IntegerField()

    username = StringField(label='User Name:')
    start = DateField(label='Start Date:', validators=[DataRequired()])
    end = DateField(label='End Date:', validators=[DataRequired()])
    submit = SubmitField(label='Confirm')

class RemoveRecordForm(FlaskForm):
    record_id = IntegerField()
    submit = SubmitField(label='Remove')