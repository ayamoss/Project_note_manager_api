from app import db
from datetime import datetime, timezone


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    notes = db.relationship('Note', backref='category', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "category": self.category.name if self.category else None
        }