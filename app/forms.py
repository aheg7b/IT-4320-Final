from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ReservationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    seat_number = StringField('Seat Number', validators=[DataRequired()])
    submit = SubmitField('Reserve Seat')