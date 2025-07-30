from flask import Blueprint, request, jsonify
from app.models import db, Persons

persons_bp = Blueprint('persons_bp', __name__)

@persons_bp.route('/', method=['POST'])
def create_person():
    data = request.json
    person = Persons(
        chinese_name = data.get('chinese_name'),
        latin_name = data.get('latin_name'),
        gender = data.get('gender'),
        dob = data.get('dob'),
        dod = data.get('dod'),
        dialect = data.get('dialect'),
        is_adopted = data.get('is_adopted'),
        sensitivity_tags = data.get('sensitivity_tags'),
        profile_photo_url = data.get('profile_photo_url'),
        note = data.get('note'),
        visibility = data.get('visibility').
        create_by_user_id = data.get('create_by_user_id')                          
    )