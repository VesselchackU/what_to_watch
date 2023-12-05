from opinions_app import db, app
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import Opinion
from opinions_app.validators import validate_opinion_text_unique
from flask import jsonify, request



@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    opinion = Opinion.get_opinion_for_api(id)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    opinion = Opinion.get_opinion_for_api(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = Opinion.get_opinion_for_api(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    res = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': res}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    opinion = Opinion(data)
    if 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля.')
    if not validate_opinion_text_unique(opinion.text):
        raise InvalidAPIUsage('Такое мнение уже есть')
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    opinion = Opinion.random_opinion()
    if not opinion:
        raise InvalidAPIUsage('В базе данных нет мнений', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200
