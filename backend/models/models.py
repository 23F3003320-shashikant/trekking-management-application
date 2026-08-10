from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    email_id   = db.Column(db.String(320), primary_key=True)
    name       = db.Column(db.String(300), nullable=False)
    role       = db.Column(db.String(100), nullable=False, default='trekker')
    password   = db.Column(db.String(100), nullable=False)
    contact    = db.Column(db.String(20),  nullable=False)
    is_active   = db.Column(db.Boolean, default=True)
    specialization = db.Column(db.String(300))
    experience = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    staff   = db.relationship('Staff',   back_populates='user', uselist=False)
    booking = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')


class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id   = db.Column(db.String(320), db.ForeignKey('users.email_id'), nullable=False, unique=True)
    staff_name = db.Column(db.String(300), nullable=False)
    contact    = db.Column(db.String(20),  nullable=False)
    specialization = db.Column(db.String(300))
    experience = db.Column(db.String(100))
    is_active  = db.Column(db.Boolean, default=True)

    user = db.relationship('Users', back_populates='staff')
    trek = db.relationship('Treks', back_populates='staff')


class Treks(db.Model):
    __tablename__ = 'treks'
    
    trek_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trek_name       = db.Column(db.String(300), nullable=False)
    trek_Location   = db.Column(db.String(300), nullable=False)
    trek_difficulty = db.Column(db.String(100), nullable=False)
    start_date      = db.Column(db.DateTime,    nullable=False)
    end_date        = db.Column(db.DateTime,    nullable=False)
    duration        = db.Column(db.Integer,     nullable=False)
    avilable_Slots  = db.Column(db.Integer,     nullable=False, default=0)
    total_slots     = db.Column(db.Integer,     nullable=False, default=0)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    status          = db.Column(db.String(20),  default='Open', nullable=False)
    image           = db.Column(db.Text)
    description     = db.Column(db.Text)
    price           = db.Column(db.Float, default=0.0)
    completed       = db.Column(db.Boolean, default=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    staff   = db.relationship('Staff',   back_populates='trek')
    booking = db.relationship('Booking', back_populates='trek', cascade='all, delete-orphan')


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id        = db.Column(db.String(320), db.ForeignKey('users.email_id'), nullable=False)
    trek_id        = db.Column(db.Integer,     db.ForeignKey('treks.trek_id'),  nullable=False)
    booking_date   = db.Column(db.DateTime, default=datetime.utcnow)
    status         = db.Column(db.String(200), nullable=False, default='Confirmed')
    payment_status = db.Column(db.String(200), nullable=False, default='Pending')
    completed_on   = db.Column(db.DateTime)

    user = db.relationship('Users', back_populates='booking')
    trek = db.relationship('Treks', back_populates='booking')
