from flask import Blueprint, request, jsonify
from app.models import db, Users
from app.utils.auth import hash_password, check_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if Users.query.filter_by(email=data['email']).first():
        return jsonify(
            {'message':'Email already registered'}
        ), 409
    else:
        user = Users(
            email = data.get('email'),
            username = data.get('username'),
            password_hash = hash_password(data.get('password')),
            country = data.get('country'),
            verified = False,
            role = 1
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message':'User created successfully',
            'id':'user.id'
        }), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    login_field = data.get('email') or data.get('username')
    password = data.get('password')
    
    if not login_field or not password:
        return({'message':'Invalid login'}), 400
    
    user = Users.query.filter(
        (Users.email == login_field) | (Users.username == login_field)
    ).first()

    if user and check_password(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': str(user.id)
        }), 200
    else:
        return jsonify({"message":'Invalid credential'}), 401

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = Users.query.get_or_404(current_user_id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'country': user.country,
        'role': user.role,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
    }), 200

@users_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200