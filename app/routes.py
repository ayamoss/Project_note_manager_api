from flask import Blueprint, request, jsonify
from app import db
from app.models import Note

bp = Blueprint('routes', __name__)


# CREATE — создать заметку
@bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "Поле 'title' обязательно"}), 400

    note = Note(title=data['title'], content=data.get('content', ''))
    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


# READ — получить все заметки
@bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes]), 200


# READ — получить одну заметку по id
@bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404
    return jsonify(note.to_dict()), 200


# UPDATE — обновить заметку
@bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404

    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)

    db.session.commit()
    return jsonify(note.to_dict()), 200


# DELETE — удалить заметку
@bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Заметка не найдена"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Заметка удалена"}), 200