from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class LanguageForm(FlaskForm):
    language = SelectField("Langue", choices=[('fr', 'Français'), ('de', 'Deutsch'), ('en', 'English'), ('es', 'Español')], validators=[DataRequired()])
    submit = SubmitField("Changer la langue")
