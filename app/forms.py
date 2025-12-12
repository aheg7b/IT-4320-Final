from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ReservationForm(FlaskForm):
    name = StringField('Passenger Name', validators=[DataRequired()])
    seat_row = IntegerField('Seat Row', validators=[DataRequired(), NumberRange(min=1)])
    seat_column = IntegerField('Seat Column', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Reserve Seat')