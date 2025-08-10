from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Relationship, Persons
from sqlalchemy.exc import IntegrityError

relations_bp = Blueprint('relations_bp', __name__)

@relations_bp.route('/', methods=['POST'])
@jwt_required()
def create_relationship() -> tuple[dict, int]:
    """
    Relationship creation handler. This endpoint accepts either 2 person_name or person_data,
    where it will be checked if the person already have existing connection. Before adding the
    create relationship data, the user must have valid JWT access token and returns successfull
    message if not or conflict it will returns error message and HTTP.

    Request JSON:
        - is_adopted (bool)
        - relationship_type (str)
        - visibility (str)
        - start_date (datetime, optional)
        - end_date (datetime, optional)
        - verified (str, optional)
        - notes (str, optional)

    Returns:
        tuple[dict, int]: JSON-compatible dict with message and a HTTP response
    """
    current_user_id = get_jwt_identity()
    data = request.json

    from_id = data.get('from_person_id')
    pA = None
    existing_rel = None
    if not from_id and data.get('from_person_name'):
        pA = Persons.query.filter(
            (Persons.latin_name == data['from_person_name']) |
            (Persons.chinese_name == data['from_person_name'])
        ).first()
        if not pA:
            return jsonify({'message': f"Person not found: {data['from_person_name']}"}), 404
        from_id = pA.id
    elif from_id:
        pA = Persons.query.get(from_id)
    else:
        return jsonify({
            'message':'from_person_id or to_person_id required'
        }), 400

    to_id = data.get('to_person_id')
    if not to_id and data.get('to_person_name'):
        pB = Persons.query.filter(
            (Persons.latin_name == data['to_person_name']) |
            (Persons.chinese_name == data['to_person_name'])
        ).first()
        if not pB:
            return jsonify({'message': f"Person not found: {data['to_person_name']}"}), 404
        to_id = pB.id
    elif to_id:
        pB = Persons.query.get(to_id)
    else:
        return jsonify({
            'message':'from_person_id or to_person_id required'
        }), 400
    
    if not pA or not pB:
        return jsonify({
            'message':'One or both persons not found'
        }), 404

    rel_type = data.get('relationship_type')
    if rel_type in ("parent","child"):
        if rel_type == "parent":
            existing_rel = Relationship.query.filter_by(
                from_person_id=from_id,
                to_person_id=to_id,
                relationship_type="parent"
            ).first() or Relationship.query.filter_by(
                from_person_id=to_id,
                to_person_id=from_id,
                relationship_type="child"
            ).first()
        elif rel_type == "child":
            existing_rel = Relationship.query.filter_by(
                from_person_id=from_id,
                to_person_id=to_id,
                relationship_type="child"
            ).first() or Relationship.query.filter_by(
                from_person_id=to_id,
                to_person_id=from_id,
                relationship_type="parent"
            ).first()
    else:
        existing_rel = Relationship.query.filter(
        (
            ((Relationship.from_person_id == from_id) & (Relationship.to_person_id == to_id)) |
            ((Relationship.from_person_id == to_id) & (Relationship.to_person_id == from_id))
        ),
        Relationship.relationship_type == rel_type).first()
        
    if existing_rel:
        return jsonify({
            'message':'Relationship already exists',
            'id':existing_rel.id
    }), 409

    relationship = Relationship(
        from_person_id = from_id,
        to_person_id = to_id,
        relationship_type = rel_type,
        is_adopted = data.get('is_adopted'),
        start_date = data.get('start_date'),
        end_date = data.get('end_date'),
        visibility = data.get('visibility'),
        verified = data.get('verified'),
        notes = data.get('notes'),
        created_by_user_id = current_user_id
    )

    try:
        db.session.add(relationship)
        db.session.commit()
        return jsonify({
            'message':'Relationship created successfully',
            'id':relationship.id
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Relationship already exists (by constraint)'}), 409

@relations_bp.route('/<rel_id>', methods=['GET'])
@jwt_required()
def get_relationship(rel_id):
    current_user_id = get_jwt_identity()
    rel = Relationship.query.get_or_404(rel_id)

    if current_user_id != rel['created_by_user_id']:
        return jsonify({
            'message':'Invalid user'
    }), 403
    else:
        return jsonify({
            'id': rel.id,
            'from_person_id': rel.from_person_id,
            'to_person_id': rel.to_person_id,
            'relationship_type': rel.relationship_type,
            'is_adopted': rel.is_adopted,
            'start_date': rel.start_date,
            'end_date': rel.end_date,
            'verified': rel.verified,
            'confidence': rel.confidence,
            'visibility': rel.visibility,
            'notes': rel.notes,
            'created_by_user_id': rel.created_by_user_id,
            'created_at': rel.created_at,
            'updated_by_user_id': rel.updated_by_user_id,
            'updated_at': rel.updated_at,
        }), 200
    

@relations_bp.route('/<rel_id>', methods=['DELETE'])
@jwt_required()
def delete_relationship(rel_id):
    current_user_id = get_jwt_identity()
    relationship = Relationship.query.get(rel_id)
    if not relationship:
        return jsonify({
            'message':'Relationship not found'
        }), 404
    
    if relationship.created_by_user_id != current_user_id:
        return jsonify({
            'message':'Forbidden'
        }), 403
    
    db.session.delete(relationship)
    db.session.commit()
    return jsonify({
        'message':'Relationship deleted'
    }), 200

@relations_bp.route('/<rel_id>', methods=['PATCH'])
@jwt_required()
def update_relationship(rel_id):
    current_user_id = get_jwt_identity()
    relationship = Relationship.query.get(rel_id)
    if not relationship:
        return jsonify({
            'message':'Relationship not found'
        }), 404
    
    if relationship.created_by_user_id != current_user_id:
        return jsonify({
            'message':'Forbidden'
        }), 403
    
    data = request.json
    if 'relationship_type' in data:
        relationship.relatioship_type = data['relationship_type']

    if 'notes' in data:
        relationship.notes = data['notes']

    if 'confidence' in data:
        relationship.confidence = data['confidence']

    if 'visibility' in data:
        relationship.visibility = data['visibility']

    db.session.commit()
    return jsonify({
        'message':'Relationship updated'
    }), 200