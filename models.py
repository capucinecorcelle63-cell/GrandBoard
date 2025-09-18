from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False)  # couleur hex ou nom css

    def __repr__(self):
        return f"<Category {self.name}>"

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image_filename = db.Column(db.String(200))   # si upload
    image_url = db.Column(db.String(500))        # si URL fournie
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    theme = db.Column(db.String(120))
    related_theme = db.Column(db.String(120))
    description = db.Column(db.String(200))      # limité à 200 char
    link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship("Category", backref="entries")

    def image_src(self):
        # retourne la source à utiliser dans <img src="...">
        if self.image_filename:
            return "/static/uploads/" + self.image_filename
        return self.image_url or "/static/placeholder.png"
