from models.models import db, Users, Treks, Staff, Booking
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'

app.config["SECRET_KEY"]='you-secret-key'

app.config["JWT_SECRET_KEY"]="your-jwt-key"

CORS(app)

JWTManager(app)

db.init_app(app)
app.app_context().push()
# remove existing sqlite DB files in development to avoid schema/datatype mismatches
# if not os.environ.get('WERKZEUG_RUN_MAIN'):
#    for _p in ('db.sqlite3', os.path.join('instance', 'db.sqlite3')):
#       p = os.path.join(os.path.dirname(__file__), _p)
#       if os.path.exists(p):
#          try:
#             os.remove(p)
#          except PermissionError:
#             pass

db.create_all()

@app.route('/', methods=["GET", "POST"])
@jwt_required()
def home():
   print(get_jwt_identity())
   data = {"numbers" : [1, 2, 3, 4, 5], 
            "message" : "Hello, World!"}
   return jsonify(data, 200) 

@app.route('/register', methods=['GET', 'POST'])
def Register():
    data = request.get_json()
    if not data:
      return jsonify({"message":"Invalid data"}), 400
    
    if data:
       return jsonify({"message":"User already exists"}), 400
    
    if request.method == 'POST':
      name= data.get("name")
      email_id= data.get("email_id")
      contact=data.get("contact")
      password=data.get("password")

      user= Users(name=name, email_id=email_id, contact=contact, password=password)
      db.session.add(user)
      db.session.commit()
    return jsonify({"message":"You are registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():       
      data = request.get_json()

      if not data:
         return jsonify({"message":"Invalid data"}), 400

      
      email_id=data.get("email_id")
      password=data.get("password")

      if not email_id or not password:
         return jsonify({"message":"Email and password are required"}), 400

      user= Users.query.filter_by(email_id=email_id).first()

      if not user or user.password != password:
         return jsonify({"message":"Invalid email or password"}), 401
      
     

      user_role = (user.role or "").strip().lower()
      access_token = create_access_token(identity={"email_id": user.email_id, "role": user.role})

                  
                 

      if user_role == "admin":
         return jsonify({"message": "Admin login successfully", "access_token": access_token, "role":user_role}), 200

      elif user_role == "staff":
         return jsonify({"message": "Staff login successfully", "access_token": access_token, "role":user_role}), 200

      else:
         return jsonify({"message": "Trekker login successfully", "access_token": access_token, "role":user_role}), 200
         









if __name__ == '__main__':
     if not Users.query.filter_by(email_id='admin123@gmail.com').first():
        ad = Users( email_id='admin123@gmail.com', name="rohan", role='admin', password='Admin123', contact=8178757590 )
        stf = Users( email_id='rohit123@gmail.com', name="rohit", role='staff', password='satff123', contact=8178666666 )
        trk= Users( email_id="mohit123@gmail.com", name="mohit", role="trekker", password="mohit123", contact=9989877868 )
        db.session.add(ad)
        db.session.add(stf)
        db.session.add(trk)
        db.session.commit()          
     app.run(debug=True)