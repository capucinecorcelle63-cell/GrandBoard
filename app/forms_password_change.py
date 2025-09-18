from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Mot de passe actuel", validators=[DataRequired()])
    new_password = PasswordField(
        "Nouveau mot de passe",
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\d]).+$", message="Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.")
        ]
    )
    confirm_password = PasswordField("Confirmer le nouveau mot de passe", validators=[DataRequired(), EqualTo('new_password', message="Les mots de passe ne correspondent pas.")])
    submit = SubmitField("Changer le mot de passe")
