from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = SelectField('Rating (/5)', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    description = StringField('Text', widget=TextArea())
    photo = FileField('Photo')
    submit = SubmitField('Submit')