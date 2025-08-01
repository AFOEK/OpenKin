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
