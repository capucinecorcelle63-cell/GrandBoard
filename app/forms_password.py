from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

class PasswordForm(FlaskForm):
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Entrer")
