from flask import Blueprint, request, jsonify
from .models import User, Course, db # Assuming Course might be used soon
from . import db as main_db # Alias to avoid conflict if 'db' is used as a variable
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Using 'main_bp' as a common convention for a main blueprint.
# You can create more blueprints for different parts of the application,
# e.g., auth_bp, course_bp, user_bp.
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Welcome to the LMS API!"

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing username, email, or password'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        role=data.get('role', 'student') # Default role
    )
    try:
        main_db.session.add(new_user)
        main_db.session.commit()
        return jsonify({'message': 'User registered successfully!', 'user_id': new_user.id}), 201
    except Exception as e:
        main_db.session.rollback()
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500


@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not (data.get('username') or data.get('email')) or not data.get('password'):
        return jsonify({'message': 'Missing username/email or password'}), 400

    user = None
    if data.get('username'):
        user = User.query.filter_by(username=data['username']).first()
    elif data.get('email'): # Allow login with email
        user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Here you would typically generate a token (e.g., JWT)
    # For simplicity, we'll just return a success message.
    # token = generate_jwt_token(user.id) # Placeholder for token generation
    return jsonify({
        'message': 'Login successful!',
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
        # 'token': token # Include token in response
    }), 200

# Placeholder for other routes (courses, user profile, etc.)
@main_bp.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = Course.query.all()
        courses_data = []
        for course in courses:
            courses_data.append({
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'instructor_id': course.instructor_id,
                'created_at': course.created_at.isoformat() if course.created_at else None,
                'is_published': course.is_published
            })
        return jsonify(courses_data), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve courses', 'error': str(e)}), 500

# @main_bp.route('/courses/<int:course_id>', methods=['GET'])
# def get_course(course_id):
#     # ...
#     pass

# Remember to register this blueprint in app/__init__.py
# from .routes import main_bp
# app.register_blueprint(main_bp, url_prefix='/api') # Example with /api prefix