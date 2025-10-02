from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
bp = Blueprint("main", __name__)

@bp.route("/tutoriel")
def tutoriel():
    return render_template("tutoriel.html")
from .translations import t
@bp.app_context_processor
def inject_translations():
    def t_fr(key):
        from .translations import translations
        return translations['fr'].get(key, key)
    return dict(t=t_fr)
from .forms_password import PasswordForm
from .forms_password_change import ChangePasswordForm
from .forms_background import BackgroundForm
from .forms_language import LanguageForm

@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()
    error = None
    success = None
    # Store password in session for demo (should be in DB for real app)
    current_pw = session.get("site_password", "ThalesDesignBoard25!")
    if form.validate_on_submit():
        if form.current_password.data != current_pw:
            error = "Mot de passe actuel incorrect."
        else:
            session["site_password"] = form.new_password.data
            success = "Mot de passe changé avec succès !"
    return render_template("change_password.html", form=form, error=error, success=success)

@bp.route("/background", methods=["GET", "POST"])
def set_background():
    form = BackgroundForm()
    if form.validate_on_submit():
        session["background"] = form.background.data
        flash("Fond changé !", "success")
        return redirect(url_for("main.index"))
    return render_template("background.html", form=form)

@bp.route("/language", methods=["GET", "POST"])
def set_language():
    form = LanguageForm()
    if form.validate_on_submit():
        session["language"] = form.language.data
        flash("Langue changée !", "success")
        return redirect(url_for("main.index"))
    return render_template("language.html", form=form)

# Password protection
PASSWORD = "ThalesDesignBoard25!"

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = PasswordForm()
    error = None
    if form.validate_on_submit():
        if form.password.data == PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("main.index"))
        else:
            error = "Mot de passe incorrect."
    return render_template("login.html", form=form, error=error)

@bp.before_app_request
def require_password():
    allowed_routes = ["main.login", "static"]
    if not session.get("authenticated") and request.endpoint not in allowed_routes:
        return redirect(url_for("main.login"))

from .forms import CategoryForm
import random

# Pastel color palette (example)
PASTEL_COLORS = [
    "#FFD1DC", "#B5EAD7", "#C7CEEA", "#FFDAC1", "#E2F0CB", "#B5EAD7", "#FFB7B2", "#FF9AA2", "#E2F0CB", "#C7CEEA", "#B5EAD7", "#FFDAC1", "#FFB7B2", "#FFD1DC", "#FF9AA2", "#C7CEEA", "#E2F0CB"
]

@bp.route("/add_category", methods=["GET", "POST"])
def manage_categories():
    categories = Category.query.order_by(Category.name).all()
    form = CategoryForm()
    selected_id = request.args.get("id", type=int)
    selected_cat = Category.query.get(selected_id) if selected_id else None

    # Handle edit/delete
    if request.method == "POST":
        action = request.form.get("action")
        if action == "edit" and selected_cat:
            new_name = request.form.get("name", "").strip()
            if new_name and new_name != selected_cat.name:
                if Category.query.filter_by(name=new_name).first():
                    flash("Ce nom existe déjà.", "warning")
                else:
                    selected_cat.name = new_name
                    db.session.commit()
                    flash("Catégorie modifiée !", "success")
            return redirect(url_for("main.manage_categories", id=selected_cat.id))
        elif action == "delete" and selected_cat:
            db.session.delete(selected_cat)
            db.session.commit()
            flash("Catégorie supprimée !", "success")
            return redirect(url_for("main.manage_categories"))
        elif action == "add":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Nom requis.", "warning")
            elif Category.query.filter_by(name=name).first():
                flash("Cette catégorie existe déjà.", "warning")
            else:
                # Assign a random pastel color
                color = random.choice(PASTEL_COLORS)
                complementary_color = "#222222"
                new_cat = Category(name=name, color=color, complementary_color=complementary_color)
                db.session.add(new_cat)
                db.session.commit()
                flash("Catégorie ajoutée !", "success")
            return redirect(url_for("main.manage_categories"))

    return render_template("manage_categories.html", categories=categories, selected_cat=selected_cat)
from .models import Category, Entry, Theme
from .forms import EntryForm, DeleteForm
from . import db
from datetime import date, datetime
from werkzeug.utils import secure_filename
from pathlib import Path



# ...existing code...

@bp.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    form = DeleteForm()
    if form.validate_on_submit():
        entry = Entry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        flash("Entrée supprimée avec succès !", "success")
    else:
        flash("Erreur CSRF ou formulaire.", "danger")
    return redirect(url_for("main.index"))

@bp.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    categories = Category.query.order_by(Category.name).all()
    category_choices = [(c.id, c.name) for c in categories]
    themes_1 = Theme.query.filter_by(type=1).order_by(Theme.name).all()
    themes_2 = Theme.query.filter_by(type=2).order_by(Theme.name).all()
    theme_principal_choices = [(t.id, t.name) for t in themes_1]
    theme_associe_choices = [(t.id, t.name) for t in themes_2]
    form = EntryForm(obj=entry, require_image=False)
    form.category.choices = category_choices
    form.theme_principal.choices = theme_principal_choices
    form.theme_associe.choices = theme_associe_choices
    # Ensure category field defaults to entry's current category on GET
    if request.method == "GET":
        form.category.data = entry.category_id
    if form.validate_on_submit():
        entry.title = form.title.data
        # Only update category if the user actually changed it
        if form.category.data != entry.category_id:
            entry.category_id = form.category.data
        entry.theme_principal = dict(form.theme_principal.choices).get(form.theme_principal.data, "")
        entry.theme_associe = dict(form.theme_associe.choices).get(form.theme_associe.data, "")
        entry.description = form.description.data
        if form.image_upload.data and getattr(form.image_upload.data, "filename", ""):
            filename = secure_filename(form.image_upload.data.filename)
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            filename = f"{timestamp}_{filename}"
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            Path(upload_folder).mkdir(parents=True, exist_ok=True)
            form.image_upload.data.save(str(Path(upload_folder) / filename))
            entry.image_filename = f"uploads/{filename}"
        if form.image_url.data:
            entry.image_url = form.image_url.data
        db.session.commit()
        flash("Entrée modifiée avec succès !", "success")
        return redirect(url_for("main.index"))
    else:
        delete_form = DeleteForm()
    return render_template("edit_entry.html", form=form, delete_form=delete_form, categories=categories, entry=entry, themes_1=themes_1, themes_2=themes_2)


def _month_bounds(year, month):
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return start, end

@bp.route("/")
def index():
    categories = Category.query.order_by(Category.name).all()
    entries_dates = db.session.query(Entry.created_at).order_by(Entry.created_at.desc()).all()
    years = sorted({dt.year for (dt,) in entries_dates}, reverse=True)
    from .translations import translations
    month_names = translations['fr']['months']
    months = [(str(i).zfill(2), month_names[i-1]) for i in range(1, 13)]
    # Get selected filters
    selected_month = request.args.get("month")
    selected_year = request.args.get("year")
    cat_id = request.args.get("category", type=int)
    type_filter = request.args.get("type", default=None)
    theme_filter = request.args.get("theme", default=None)
    query = Entry.query
    # Filter by year and month if selected
    if selected_year and selected_year != "all":
        query = query.filter(db.extract('year', Entry.created_at) == int(selected_year))
    if selected_month and selected_month != "all":
        query = query.filter(db.extract('month', Entry.created_at) == int(selected_month))
    if cat_id:
        query = query.filter_by(category_id=cat_id)
    if type_filter:
        query = query.filter(Entry.theme_principal == type_filter)
    if theme_filter:
        query = query.filter(Entry.theme_associe == theme_filter)
    entries = query.order_by(Entry.created_at.desc()).all()
    # Get all unique types and themes for dropdowns
    all_types = [t[0] for t in db.session.query(Entry.theme_principal).distinct().order_by(Entry.theme_principal).all() if t[0]]
    all_themes = [t[0] for t in db.session.query(Entry.theme_associe).distinct().order_by(Entry.theme_associe).all() if t[0]]
    # Assign complementary colors to each category
    complementary_palette = [
        "#FF6F61", # Red
        "#6B5B95", # Purple
        "#88B04B", # Green
        "#F7CAC9", # Pink
        "#92A8D1", # Blue
        "#955251", # Brown
        "#B565A7", # Violet
        "#009B77", # Teal
        "#DD4124", # Orange
        "#45B8AC", # Aqua
        "#EFC050", # Yellow
        "#5F4B8B", # Indigo
        "#D65076", # Magenta
        "#9B2335", # Burgundy
        "#DFCFBE", # Beige
        "#55B4B0", # Turquoise
    ]
    category_colors = {}
    for i, cat in enumerate(categories):
        category_colors[cat.id] = complementary_palette[i % len(complementary_palette)]
    colored_entries = []
    for entry in entries:
        color = category_colors.get(entry.category_id, "#fff")
        colored_entries.append((entry, color))
    return render_template("index.html", entries=colored_entries, categories=categories, selected_category=cat_id, all_types=all_types, all_themes=all_themes, selected_type=type_filter, selected_theme=theme_filter, months=months, years=years, category_colors=category_colors)

@bp.route("/add", methods=["GET", "POST"])
def add_entry():
    # Restore form data from session if available
    form_data = session.pop('add_entry_form_data', None)
    form = EntryForm(data=form_data) if form_data else EntryForm()
    categories = Category.query.order_by(Category.name).all()
    form.category.choices = [(c.id, c.name) for c in categories]
    themes_1 = Theme.query.filter_by(type=1).order_by(Theme.name).all()
    themes_2 = Theme.query.filter_by(type=2).order_by(Theme.name).all()
    form.theme_principal.choices = [(t.id, t.name) for t in themes_1]
    form.theme_associe.choices = [(t.id, t.name) for t in themes_2]
    if request.method == "POST" and request.form.get("goto_manage_themes"):
        # Save current form data to session and redirect
        session['add_entry_form_data'] = request.form.to_dict()
        return redirect(url_for("main.manage_themes"))
    if form.validate_on_submit():
        image_filename = None
        if form.image_upload.data:
            filename = secure_filename(form.image_upload.data.filename)
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            filename = f"{timestamp}_{filename}"
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            Path(upload_folder).mkdir(parents=True, exist_ok=True)
            form.image_upload.data.save(str(Path(upload_folder) / filename))
            image_filename = f"uploads/{filename}"
        entry = Entry(
            title=form.title.data,
            category_id=form.category.data,
            theme_principal=dict(form.theme_principal.choices).get(form.theme_principal.data, ""),
            theme_associe=dict(form.theme_associe.choices).get(form.theme_associe.data, ""),
            description=form.description.data,
            image_filename=image_filename,
            image_url=form.image_url.data,
            link=form.link.data,
        )
        db.session.add(entry)
        db.session.commit()
        flash("Entrée ajoutée avec succès !", "success")
        return redirect(url_for("main.index"))
    return render_template("add_entry.html", form=form, categories=categories, themes_1=themes_1, themes_2=themes_2)
# Theme management route
@bp.route("/manage_themes", methods=["GET", "POST"])
def manage_themes():
    themes_1 = Theme.query.filter_by(type=1).order_by(Theme.name).all()
    themes_2 = Theme.query.filter_by(type=2).order_by(Theme.name).all()
    if request.method == "POST":
        action = request.form.get("action")
        theme_id = request.form.get("theme_id", type=int)
        name = request.form.get("name", "").strip()
        theme_type = request.form.get("type", type=int)
        if action == "add":
            if not name or theme_type not in [1, 2]:
                flash("Nom et type requis.", "warning")
            elif Theme.query.filter_by(name=name, type=theme_type).first():
                flash("Ce thème existe déjà.", "warning")
            else:
                new_theme = Theme(name=name, type=theme_type)
                db.session.add(new_theme)
                db.session.commit()
                flash("Thème ajouté !", "success")
        elif action == "edit" and theme_id:
            theme = Theme.query.get(theme_id)
            if theme and name:
                theme.name = name
                db.session.commit()
                flash("Thème modifié !", "success")
        elif action == "delete" and theme_id:
            theme = Theme.query.get(theme_id)
            if theme:
                db.session.delete(theme)
                db.session.commit()
                flash("Thème supprimé !", "success")
        return redirect(url_for("main.manage_themes"))
    return render_template("manage_themes.html", themes_1=themes_1, themes_2=themes_2)



