from flask import Blueprint, jsonify
from app.models import db, Persons, Relationship, Users
from sqlalchemy import text
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

tree_bp = Blueprint('tree_bp', __name__)

def is_minor(person):
    if not person.dob or person.is_live:
        return False
    
    today = date.today()
    age = today.year - person.dob.year - ((today.month, today.day) < (person.dob.month, person.dob.day))
    return age < 18

def is_direct_family(user_id, person_id):
    direct_types = {'parent', 'spouse', 'child'}
    direct = Relationship.qurey.filter(
        (Relationship.from_person_id == user_id) & (Relationship.to_person_id == person_id) |
        (Relationship.from_person_id == user_id) & (Relationship.to_person_id == user_id)
    ).filter(Relationship.relationship_type.in_(direct_types)).first
    return direct is not None

def get_surname(person):
    for field in ['latin_name', 'chinese_name']:
        name = person.get(field)
        if name:
            return name.split()[0] if ' ' in name else name[0]
        
    return None

def is_direct_family(user_id, person_id):
    direct_type = ['parent', 'child', 'spouse', 'sibling']

    rel = Relationship.query.filter(
        (
            (Relationship.from_person_id == user_id) & (Relationship.to_person_id == person_id)
        ) | (
            (Relationship.from_person_id == person_id) & (Relationship.to_person_id == user_id)
        )
    ).filter(Relationship.relationship_type.in_(direct_type)).first
    return rel is not None

def can_view_person(current_user, person):
    visibility = person.get('visibility', 'public')
    owner_id = str(person.get('create_by_user_id'))
    user_id = str(current_user.id)

    if visibility == 'public':
        return True
    
    if visibility == 'private':
        return user_id == owner_id
    
    if visibility == 'family':
        return is_direct_family(user_id, person['id'])
    
    person_surname = get_surname(person)
    user_surname  = get_surname({'latin_name': current_user.latin_name, 'chinese_name': current_user.chinese_name})
    return person_surname and user_surname and person_surname == user_surname

@tree_bp.route('/<person_id>', methods=['GET'])
@jwt_required()
def get_family_tree(person_id):
    current_user_id = get_jwt_identity()

    root_person = Persons.query.get(person_id)
    if not root_person:
        return jsonify({
            'message':'Root person not found'
        }), 404
    
    sql = text("""
    WITH RECURSIVE family_tree AS(
    SELECT p.*, 0 AS generation
    FROM persons p
    WHERE p.id = :person_id
    UNION ALL
    SELECT p2.*, ft.generation + 1
    FROM family_tree ft
    JOIN relationships r ON r.from_person_id = ft.id
    JOIN persons p2 ON p2.id = r.to_person_id
    WHERE r.visibility IN ('public', 'family', 'private', 'clan')
    UNION ALL
    SELECT p1.*, ft.generation + 1
    FROM family_tree ft
    JOIN relationships r ON r.to_person_id = ft.id
    JOIN persons p1 ON p1.id = r.from_person_id
    WHERE r.visibility IN ('public', 'family', 'private', 'clan')
    )
    SELECT * FROM family_tree;
    """)

    tree_people = db.session.execute(sql, {'person_id':person_id}).fetchall()

    response = []

    for row in tree_people:
        person = dict(row)

        person['id'] = str(person['id'])
        person['dob'] = person['dob'].isoformat() if person['dob'] else None
        person['dod'] = person['dod'].isoformat() if person['dod'] else None

        if not can_view_person(current_user_id, person):
            response.append({'id':person['id'], 'redacted': True})
            continue

        tags = person.get('sensitifity_tags', []) or []

        if isinstance(tags, str):
            tags = [t.strip().strip('"') for t in tags.strip('{}').split(',') if t.strip()]

        minor = 'minor' in tags or is_minor(person)
        protected = 'protected' in tags
        refugee = 'refugee' in tags

        if minor and not is_direct_family(current_user_id, person['id']):
            person['latin_name'] = "Protected Minor"
            person['chinese_name'] = "受保护的未成年人"
            person['note'] = ""
            person['dob'] = ""
            person['dod'] = ""
            person['pob'] = ""
            person['pod'] = ""

        if protected:
            person['latin_name'] = "Protected Person"
            person['chinese_name'] = "受保护人"
            person['note'] = ""
            person['dob'] = ""
            person['dod'] = ""
            person['pob'] = ""
            person['pod'] = ""
        if refugee:
            person['latin_name'] = "Protected Refugee"
            person['chinese_name'] = "受保护难民"
            person['note'] = ""
            person['dob'] = ""
            person['dod'] = ""
            person['pob'] = ""
            person['pod'] = ""

        response.append(person)
    return jsonify(response)