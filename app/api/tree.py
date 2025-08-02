from flask import Blueprint, jsonify
from app.models import db, Persons, Relationship, Users
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

@tree_bp.route('/tree/<person_id>', methods=['GET'])
@jwt_required
def get_family_tree(person_id):
    current_user_id = get_jwt_identity()

    root_person = Persons.query.get(person_id)
    if not root_person:
        return jsonify({
            'message':'Root person not found'
        }), 404
    
    sql = """
    WITH RECURSIVE family_tree AS(
    SELECT p.*, 0 AS generation
    FROM persons p
    WHERE p.id = :person_id
    UNION
    SELECT p2.*, ft.generation + 1
    FROM family_tree ft
    JOIN relationships r ON r.from_person_id = ft.id
    JOIN persons p2 ON p2.id = r.to_person_id
    WHERE r.visibility IN ('public', 'family', 'private')
    UNION
    SELECT p1.*, ft.generation + 1
    FROM family_tree ft
    JOIN relationships r ON r.to_person_id = ft.id
    JOIN persons p1 ON p1.id = r.from_person_id
    WHERE r.visibility IN ('public', 'family', 'private')
    )
    SELECT * FROM family_tree;
    """

    tree_people = db.session.execute(sql, {'person_id':person_id}).fetchall()

    response = []

    for row in tree_people:
        person = dict(row)

        person['id'] = str(person[id])
        person['dob'] = person['dob'].isoformat() if person['dob'] else None
        person['dod'] = person['dod'].isoformat() if person['dod'] else None

        visibility = person.get('visibility', 'public')
        allowed = False

        is_owner = (current_user_id == str(person.get(current_user_id)))
        if visibility == 'public':
            allowed = True
        elif visibility == 'family':
            allowed = is_owner
        elif visibility == 'private':
            allowed = is_owner or is_direct_family(current_user_id, person['id'])

        tags = person.get('sensitifity_tags', []) or []

        if isinstance(tags, str):
            tags = [t.strip() for t in tags.strip('{}').split(',') if t.strip()]

        minor = 'minor' in tags or is_minor(row)
        protected = 'protected' in tags
        refugee = 'refugee' in tags

        if not allowed:
            response.append({'id':person['id'], 'redacted': True})
            continue

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