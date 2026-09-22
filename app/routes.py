from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app import db
from app.models import Note, Category

bp = Blueprint('routes', __name__)


# ---------- CATEGORY ----------

@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json(silent=True)
    if not data or 'name' not in data:
        return jsonify({"error": "Поле 'name' обязательно"}), 400

    if Category.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Категория с таким именем уже существует"}), 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


# ---------- NOTES ----------

@bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json(silent=True)

    if not data or 'title' not in data:
        return jsonify({"error": "Поле 'title' обязательно"}), 400

    category_id = data.get('category_id')
    if category_id is not None and not db.session.get(Category, category_id):
        return jsonify({"error": "Категория не найдена"}), 400
    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        category_id=category_id
    )
    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@bp.route('/notes', methods=['GET'])
def get_notes():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    category_name = request.args.get('category')

    # joinedload убирает N+1 при обращении к note.category
    query = Note.query.options(joinedload(Note.category))

    if category_name:
        query = query.join(Category).filter(Category.name == category_name)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    notes = pagination.items

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "notes": [note.to_dict() for note in notes]
    }), 200


@bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404
    return jsonify(note.to_dict()), 200


@bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Тело запроса должно быть JSON"}), 400

    if 'category_id' in data and data['category_id'] is not None:
        if not db.session.get(Category, data['category_id']):
            return jsonify({"error": "Категория не найдена"}), 400

    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    if 'category_id' in data:
        note.category_id = data['category_id']

    db.session.commit()
    return jsonify(note.to_dict()), 200


@bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Заметка удалена"}), 204