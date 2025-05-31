from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), default='student') # e.g., student, instructor, admin
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships (examples, to be expanded)
    # courses_enrolled = db.relationship('Enrollment', backref='student', lazy=True)
    # courses_instructing = db.relationship('Course', backref='instructor', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Nullable if courses can be system-generated
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

    # Relationships
    # modules = db.relationship('Module', backref='course', lazy=True, cascade="all, delete-orphan")
    # enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.title}>'

# Add more models as needed: Module, Lesson, Enrollment, Quiz, Submission, etc.
# Example:
# class Module(db.Model):
#     __tablename__ = 'modules'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
#     order = db.Column(db.Integer, nullable=False) # To maintain order of modules in a course
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# class Enrollment(db.Model):
#     __tablename__ = 'enrollments'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
#     enrolled_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     progress = db.Column(db.Float, default=0.0) # e.g., 0.0 to 1.0 or percentage
#     completed_at = db.Column(db.DateTime, nullable=True)

#     __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='_user_course_uc'),)