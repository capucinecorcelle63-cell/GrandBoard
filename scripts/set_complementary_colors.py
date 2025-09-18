from app import create_app
from app.models import db, Category

# Map pastel background colors to complementary text colors
complementary_map = {
    "#AEE9F9": "#1A237E",      # Podcast (light blue) -> dark blue
    "#FFF9C4": "#283593",     # Documentaire (light yellow) -> dark blue
    "#FFD8B2": "#6D4C41",     # Film (peach) -> brown
    "#FFB3C6": "#4A148C",     # Vidéo (pink) -> purple
    "#D4FFB2": "#388E3C",     # Exposition (light green) -> dark green
    "#E1B2FF": "#4A148C",     # Livre (lavender) -> purple
    "#B2F2E1": "#00695C",     # Article (aqua) -> teal
    "#FFD6E0": "#C51162",     # Interview (rose) -> magenta
    "#B2D7FF": "#0D47A1",     # Musique (light blue) -> blue
    "#B2FFD8": "#004D40",     # Image (mint) -> dark teal
    "#E6E6FF": "#1A237E",     # Marque (very light blue) -> dark blue
    "#FFE5B2": "#6D4C41",     # Personnalité (beige) -> brown
    "#D6FFE0": "#388E3C",     # Adresse (light green) -> dark green
    "#FFE0F7": "#4A148C",     # Site/Appli (light pink) -> purple
    "#FFF2B2": "#283593",     # Tutoriel (light yellow) -> dark blue
    "#FFCCE5": "#C51162",     # Conférence (light magenta) -> magenta
    "#E0FFD6": "#388E3C",     # Forum (light green) -> dark green
}

app = create_app()
with app.app_context():
    for category in Category.query.all():
        comp = complementary_map.get(category.color, "#222222")
        category.complementary_color = comp
    db.session.commit()
    print("Couleurs complémentaires mises à jour !")