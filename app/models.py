from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'CoreDB'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(124))
    password_hash = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(90))
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Persons(db.Model):
    __tablename__ = 'persons'
    __table_args__ = (
        db.UniqueConstraint('latin_name','chinese_name', 'pob', "dialect", name='unique_person'),
        {'schema': 'CoreDB'}
        )
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    chinese_name = db.Column(db.String(64))
    latin_name = db.Column(db.String(128))
    gender = db.Column(db.Integer)
    dob = db.Column(db.Date)
    dod = db.Column(db.Date)
    is_live = db.Column(db.Boolean, default=True)
    pob = db.Column(db.String(128))
    pod = db.Column(db.String(128))
    dialect = db.Column(db.String(64), default='mandarin')
    is_adopted = db.Column(db.Boolean, default=False)
    sensitivity_tags = db.Column(db.ARRAY(db.String))
    profile_photo_url = db.Column(db.Text)
    note = db.Column(db.Text)
    visibility = db.Column(db.String(20), default='family')
    create_by_user_id = db.Column(db.String(36), db.ForeignKey('CoreDB.users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Relationship(db.Model):
    __tablename__ = 'relationships'
    __table_args__ = (
        db.UniqueConstraint('from_person_id', 'to_person_id', name='unique_relationships'),
        {'schema': 'CoreDB'}
        )
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    from_person_id = db.Column(db.String(36), db.ForeignKey('CoreDB.persons.id'), nullable=False)
    to_person_id = db.Column(db.String(36), db.ForeignKey('CoreDB.persons.id'), nullable=False)
    relationship_type = db.Column(db.String(64), nullable=False)
    is_adopted = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    verified = db.Column(db.Boolean, default=False)
    confidence = db.Column(db.Integer, default=100)
    visibility = db.Column(db.String(20), default='family')
    notes = db.Column(db.Text)
    created_by_user_id = db.Column(db.String(36), db.ForeignKey('CoreDB.users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by_user_id = db.Column(db.String(36), db.ForeignKey('CoreDB.users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
