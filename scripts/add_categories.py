from app import create_app
from app.models import db, Category


palette = [
    "#E3EA3A",
    "#D452B8",
    "#2DC66B",
    "#98C7F3",
    "#F393C1",
    "#1268EF",
    "#EF8040",
    "#7284F0",
]

category_names = [
    "Podcast", "Documentaire", "Film", "Vidéo", "Exposition", "Livre", "Article", "Interview",
    "Musique", "Image", "Marque", "Personnalité", "Adresse", "Site/Appli", "Tutoriel", "Conférence", "Forum"
]

# Assign colors, avoiding adjacent duplicates
categories = []
for i, name in enumerate(category_names):
    color = palette[i % len(palette)]
    # Avoid adjacent duplicate colors
    if i > 0 and color == categories[-1][1]:
        color = palette[(i+1) % len(palette)]
    categories.append((name, color))

app = create_app()
with app.app_context():
    for name, color in categories:
        cat = Category.query.filter_by(name=name).first()
        if cat:
            cat.color = color
        else:
            db.session.add(Category(name=name, color=color))
    db.session.commit()
    print("Catégories ajoutées et mises à jour !")