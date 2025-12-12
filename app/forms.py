from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class AdminLoginForm(FlaskForm):
    username = StringField('Admin Username', validators=[DataRequired()])
    password = PasswordField('Admin Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReservationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    seatRow = IntegerField('Seat Row (1-12)', validators=[DataRequired(), NumberRange(min=1, max=12)])
    seatColumn = IntegerField('Seat Column (1-4)', validators=[DataRequired(), NumberRange(min=1, max=4)])
    submit = SubmitField('Submit Reservation')