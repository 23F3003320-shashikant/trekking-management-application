from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, DateTime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True)
    name = Column(String(300), nullable=False)
    role = Column(String(100), nullable=False, default='user') #(Admin, Trek Staff, and Users (Trekkers))
    password = Column(String(100), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    Admin_id = Column(Integer, primary_key= True)
    Admin_name = Column(String(300), nullable=False)
    Admin_password = Column(String(100), nullable=False)

class Staff(db.Model):
    __tablename__ = 'staff'
    Staff_id = Column(Integer, primary_key= True)
    Staff_name = Column(String(300), nullable=False)
    Staff_password = Column(String(100), nullable=False)

class Treks(db.Model):
    __tablename__ = 'treks'
    Trek_id = Column(Integer, primary_key=True)
    Trek_name = Column(String(300), nullable=False)
    Trek_Location = Column(String(300), nullable=False)
    Trek_difficulty = Column(String(100), nullable=False)
    Start_date = Column(DateTime, nullable=False)
    End_date = Column(DateTime, nullable=False)
    Duration = Column(Integer, nullable=False)
    Avilable_Slots= Column(Integer, nullable=False, default='--')
    Assigned_Staff_id=Column(Text, nullable=False, default= 'Wait to assigned')
    Status = Column(Text, nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'

    Booking_id = Column(Integer, primary_key=True ,nullable=False)
    User_id = Column(Integer, nullable=False)
    Trek_id= Column(Integer, nullable=False)
    Booking_date= Column(DateTime, default=DateTime)
    Status = Column(String(200), nullable=False)
    Payment_status= Column(String(200), nullable=False)


