from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class BackgroundForm(FlaskForm):
    background = SelectField("Fond", choices=[('light', 'Blanc'), ('dark', 'Noir')], validators=[DataRequired()])
    submit = SubmitField("Changer le fond")
