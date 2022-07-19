from wtforms.fields.core import SelectField
from wtforms.fields.simple import PasswordField
from url_shortener_app.models import Creator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length, ValidationError, data_required

class CreateShortUrlForm(FlaskForm):
    url_name = StringField(label="URL Name", validators=[DataRequired()])
    original_url = StringField(label="Original URL", validators=[URL(), DataRequired()])
    submit_btn = SubmitField(label="Get Short URL")


class RegistrationForm(FlaskForm):
    # Should name the method validate_{field_name}

    def validate_username(self, username_to_check):
        user = Creator.query.filter_by(username=username_to_check.data).first()
        if(user):
            raise ValidationError('Username already exists! Please try a different name')

    def validate_email(self, email_to_check):
        email = Creator.query.filter_by(email= email_to_check.data).first()
        if(email):
            raise ValidationError('Email address already exists!')

    username = StringField(label="Username", validators=[Length(min=5, max=30), DataRequired()])
    email = StringField(label="Email", validators=[Email(), data_required()])
    password1 = PasswordField(label="Password", validators=[Length(min=6)])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo('password1')])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")