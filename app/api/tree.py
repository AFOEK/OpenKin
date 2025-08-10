from flask import Blueprint, jsonify
from app.models import db, Persons, Relationship
from sqlalchemy import text
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime
from app.utils.clan import same_clan
from uuid import UUID

tree_bp = Blueprint('tree_bp', __name__)

def is_minor(person):
    if not person.dob or person.is_live:
        return False
    
    today = date.today()
    age = today.year - person.dob.year - ((today.month, today.day) < (person.dob.month, person.dob.day))
    return age < 18

def is_direct_family(user_id, person_id):
    direct_types = {'parent', 'spouse', 'child'}
    direct = Relationship.query.filter(
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
    
    if visibility == "clan":
        user_row = {
            'id': user_id,
            'chinese_name': getattr(current_user, 'chinese_name', None) or current_user.get('chinese_name')
        }
        return same_clan(db, user_row, person)
    
    return False

def serialize_person(data):
    out = {}
    for k, v in data.items():
        if isinstance(v, UUID):
            out[k] = str(v)
        elif isinstance(v, (date, datetime)):
            out[k] = v.isoformat()
        elif k == 'path' and isinstance(v, list):
            out[k] = [str(x) if isinstance(x, UUID) else x for x in v]
        else:
            out[k] = v
    return out

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
    WITH RECURSIVE OutgoingTree AS (
    SELECT
        p.*,
        0 AS gen,
        ARRAY[p.id] AS path,
        NULL::uuid AS prev_id,
        NULL::varchar AS rel_type
    FROM "CoreDB".persons p
    WHERE p.id = :person_id

    UNION ALL

    SELECT
        p2.*,
        ot.gen + 1 AS gen,
        ot.path || p2.id AS path,
        ot.id AS prev_id,
        r.relationship_type AS rel_type
    FROM OutgoingTree ot
    JOIN "CoreDB".relationships r ON r.from_person_id = ot.id
    JOIN "CoreDB".persons p2 ON p2.id = r.to_person_id
    WHERE NOT p2.id = ANY(ot.path)
        AND r.visibility IN ('public','family','private','clan')
    ),

    IncomingTree AS (
    SELECT
        p.*,
        0 AS gen,
        ARRAY[p.id] AS path,
        NULL::uuid AS prev_id,
        NULL::varchar AS rel_type
    FROM "CoreDB".persons p
    WHERE p.id = :person_id

    UNION ALL

    SELECT
        p1.*,
        it.gen + 1 AS gen,
        it.path || p1.id AS path,
        it.id AS prev_id,
        r.relationship_type AS rel_type
    FROM IncomingTree it
    JOIN "CoreDB".relationships r ON r.to_person_id = it.id
    JOIN "CoreDB".persons p1 ON p1.id = r.from_person_id
    WHERE NOT p1.id = ANY(it.path)
        AND r.visibility IN ('public','family','private','clan')
    )

    SELECT DISTINCT ON (id) *
    FROM (
    SELECT * FROM OutgoingTree
    UNION ALL
    SELECT * FROM IncomingTree
    ) t
    ORDER BY id, gen;
    """)

    tree_people = db.session.execute(sql, {'person_id':person_id})
    tree_people = tree_people.mappings().all()
    
    response = []

    for row in tree_people:
        person = serialize_person(dict(row))

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
            for field in ['latin_name', 'chinese_name', 'note', 'dob', 'dod', 'pob', 'pod']:
                person[field] = "" if field not in ('latin_name', 'chinese_name') else "Protected Minor" if field == 'latin_name' else "受保护的未成年人"
        elif protected:
            for field in ['latin_name', 'chinese_name', 'note', 'dob', 'dod', 'pob', 'pod']:
                person[field] = "" if field not in ('latin_name', 'chinese_name') else "Protected Person" if field == 'latin_name' else "受保护人"
        elif refugee:
            for field in ['latin_name', 'chinese_name', 'note', 'dob', 'dod', 'pob', 'pod']:
                person[field] = "" if field not in ('latin_name', 'chinese_name') else "Protected Refugee" if field == 'latin_name' else "受保护难民"

        response.append(person)
    return jsonify(response)