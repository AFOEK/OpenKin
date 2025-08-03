from flask import Blueprint, request, jsonify
from app.models import db, Persons
from flask_jwt_extended import jwt_required, get_jwt_identity

persons_bp = Blueprint('persons_bp', __name__)

@persons_bp.route('/', methods=['POST'])
@jwt_required()
def create_person():
    data = request.json
    current_user_id = get_jwt_identity()

    print(f"Checking for duplicate with values: {data.get('chinese_name')}, {data.get('latin_name')}, {data.get('dob')}, {data.get('pob')}, {data.get('dialect')}")

    duplicate = Persons.query.filter_by(
        chinese_name = data.get('chinese_name'),
        latin_name = data.get('latin_name'),
        pob = data.get('pob'),
        dialect = data.get('dialect')
    ).first()

    print(duplicate)

    if duplicate:
        return jsonify({
            'message':'Person already exists',
            'id': str(duplicate.id)
        }), 409

    person = Persons(
        chinese_name = data.get('chinese_name'),
        latin_name = data.get('latin_name'),
        gender = data.get('gender'),
        dob = data.get('dob'),
        dod = data.get('dod'),
        pob = data.get('pob'),
        pod = data.get('pod'),
        dialect = data.get('dialect'),
        is_adopted = data.get('is_adopted'),
        sensitivity_tags = data.get('sensitivity_tags'),
        profile_photo_url = data.get('profile_photo_url'),
        note = data.get('note'),
        visibility = data.get('visibility'),
        create_by_user_id = current_user_id                        
    )
    db.session.add(person)
    db.session.commit()
    return jsonify({
        'message':'Person created successfully',
        'id': person.id
    }), 201

@persons_bp.route('/<person_id>', methods=['GET'])
@jwt_required()
def get_person(person_id):
    person = Persons.query.get_or_404(person_id)
    return jsonify({
        'id': person.id,
        'chinese_name': person.chinese_name,
        'latin_name': person.latin_name,
        'gender': person.gender,
        'dob': person.dob,
        'dod': person.dod,
        'is_live': person.is_live,
        'pob': person.pob,
        'pod': person.pod,
        'dialect': person.dialect,
        'is_adopted': person.is_adopted,
        'sensitivity_tags': person.sensitivity_tags,
        'profile_photo_url': person.profile_photo_url,
        'note': person.note,
        'visibility': person.visibility,
        'create_by_user_id': person.create_by_user_id,
        'created_at': person.created_at,
        'updated_at': person.updated_at,
    }), 200

@persons_bp.route('/', methods=['GET'])
@jwt_required()
def list_persons():
    persons = Persons.query.all()
    return jsonify([{
        'id': p.id,
        'chinese_name': p.chinese_name,
        'latin_name': p.latin_name,
        'gender': p.gender,
        'dob': p.dob,
        'dod': p.dod,
        'is_live': p.is_live,
        'pob': p.pob,
        'pod': p.pod,
        'dialect': p.dialect,
        'is_adopted': p.is_adopted,
        'visibility': p.visibility,
        'create_by_user_id': p.create_by_user_id,
        'created_at': p.created_at,
        'updated_at': p.updated_at
    } for p in persons
    ]), 200