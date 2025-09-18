from . import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False, default="#cccccc")
    complementary_color = db.Column(db.String(20), nullable=False, default="#222222")
    entries = db.relationship("Entry", back_populates="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name!r}>"

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.Integer, nullable=False)  # 1 for Thème 1, 2 for Thème 2

    def __repr__(self):
        return f"<Theme {self.name!r} (type {self.type})>"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(512))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    theme_principal = db.Column(db.String(120), nullable=False)
    theme_associe = db.Column(db.String(120))
    description = db.Column(db.String(200))
    link = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.relationship("Category", back_populates="entries")

    def __repr__(self):
        return f"<Entry {self.title!r}>"
