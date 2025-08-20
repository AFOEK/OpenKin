from flask import Blueprint, request, jsonify
from app.models import db, Users
from datetime import datetime
from app.utils.auth import hash_password, check_password
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/register', methods=['POST'])
def register() -> tuple[dict, int]:
    """
    Register handler. This endpoint accepts email, username, password, and country.

    Request JSON:
        - Email (str)
        - Username (str)
        - Password (str)
        - Country (str)

    Returns:
        tuple[dict, int]: JSON-compatible dict with message and a HTTP response code
    """
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
def login() -> tuple[dict, int]:
    """
    User login handler. This endpoint accepts either email or username along with password,
    verifies the credentials, and returns JWT token if successful

    Request JSON:
        - Email (str, optional)
        - Username (str, optional)
        - Password (str)

    Return:
        tuple[dict, int]: JSON-compatible dict with JWT tokens or error message,
        and an HTTP status code
    """
    data = request.get_json(force=True)
    login_field = data.get('email') or data.get('username')
    password = data.get('password')
    
    if not login_field or not password:
        return({'message':'Invalid login'}), 400
    
    user = Users.query.filter(
        (Users.email == login_field) | (Users.username == login_field)
    ).first()

    if user and check_password(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': str(user.id)
        }), 200
    else:
        return jsonify({"message":'Invalid credential'}), 401

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def me() -> tuple[dict, int]:
    """
    Return current authenticated user's profile.

    Auth:
        Required a valid JWT access token (Authorization: Bearer <access_token>).

    Returns:
        tuple[dict, int]: JSON-compatible with user profile and HTTP status
    """
    current_user_id = get_jwt_identity()
    user = Users.query.get_or_404(current_user_id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'country': user.country,
        'role': user.role,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'updated_at': user.updated_at.isoformat() if user.updated_at else None
    }), 200

@users_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh() -> tuple[dict, int]:
    """
    Issue new access token using valid refresh token.

    Auth:
        Requires a valid refresh token (Authorization: Bearer <refresh_token>)

    Returns:
        tuple[dict, int]: JSON-compatible with a new access token and HTTP status   
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200