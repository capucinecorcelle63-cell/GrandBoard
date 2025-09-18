from flask_wtf import FlaskForm

class DeleteForm(FlaskForm):
    pass
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

class EntryForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=120)])
    category = SelectField("Category", coerce=int, validators=[DataRequired()])
    theme_principal = SelectField("Thème 1", coerce=int, validators=[Optional()])
    theme_associe = SelectField("Thème 2", coerce=int, validators=[Optional()])
    description = TextAreaField("Description", validators=[Length(max=200)])
    image_upload = FileField(
        "Image (upload)",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Accepted formats: jpg, png, gif, webp")],
    )
    image_url = StringField("Image (URL)", validators=[Optional(), URL(message="Invalid URL")])
    link = StringField("Link", validators=[Optional(), URL(message="Invalid URL")])
    submit = SubmitField("Add Entry")

    # Only require image for new entries, not for edit
    def __init__(self, *args, require_image=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.require_image = require_image

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        if self.require_image:
            upload = self.image_upload.data
            has_upload = bool(upload and getattr(upload, "filename", ""))
            has_url = bool(self.image_url.data)
            if not has_upload and not has_url:
                message = "Please provide an image (upload or URL)."
                self.image_upload.errors.append(message)
                self.image_url.errors.append(message)
                return False
        return True


# Form to add a new category
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField("Nom de la catégorie", validators=[DataRequired(), Length(max=80)])
    color = StringField("Couleur (hex)", validators=[DataRequired(), Length(max=20)])
    complementary_color = StringField("Couleur complémentaire (hex)", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Ajouter la catégorie")
