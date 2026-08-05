from models.models import db, Users, Treks, Admin, Staff, Booking
import os
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'


if __name__ == '__main__':
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    
    app.run()