from datetime import datetime
from models.models import db, Users, Treks, Staff, Booking
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt







app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config["SECRET_KEY"]='you-secret-key'
app.config["JWT_SECRET_KEY"]="your-jwt-key"

CORS(app)
JWTManager(app)
db.init_app(app)

app.app_context().push()
db.create_all()



# ── Data sapport ──────────────────────────────────────────────────────────


TREK_IMAGES = [
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80",
    "https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&q=80",
    "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=600&q=80",
    "https://images.unsplash.com/photo-1606768666853-403c90a981ad?w=600&q=80",
    "https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=600&q=80",
    "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=600&q=80",
    "https://images.unsplash.com/photo-1612892483236-52d32a0e0ac1?w=600&q=80",
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=600&q=80",
]


def make_token(user):
    role = (user.role or 'trekker').strip().lower()
    return create_access_token(
        identity=user.email_id,         
        additional_claims={"role": role}  
    )



def current_identity():
   email = get_jwt_identity()
   role = get_jwt().get("role", "trekker")
   return email, role


def trek_to_dict(t):
    staff_name = t.staff.staff_name if t.assigned_staff_id and t.staff else None
    return {
        "trek_id": t.trek_id, "trek_name": t.trek_name,
        "trek_Location": t.trek_Location, "trek_difficulty": t.trek_difficulty,
        "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
        "end_date":   t.end_date.strftime('%Y-%m-%d')   if t.end_date   else None,
        "duration": t.duration, "avilable_Slots": t.avilable_Slots,
        "total_slots": t.total_slots, "assigned_staff_id": t.assigned_staff_id,
        "assigned_staff_name": staff_name, "status": t.status,
        "image": t.image, "description": t.description,
        "price": t.price, "completed": t.completed,
    }

def booking_to_dict(b):
    return {
        "booking_id": b.booking_id,
        "user_id": b.user_id,
        "user_name": b.user.name if b.user else b.user_id,
        "trek_id": b.trek_id,
        "trek_name": b.trek.trek_name if b.trek else "",
        "trek_location": b.trek.trek_Location if b.trek else "",
        "trek_image": b.trek.image if b.trek else "",
        "start_date": b.trek.start_date.strftime('%d %b %Y') if b.trek and b.trek.start_date else "",
        "end_date":   b.trek.end_date.strftime('%d %b %Y')   if b.trek and b.trek.end_date   else "",
        "booking_date": b.booking_date.strftime('%d %b %Y') if b.booking_date else "",
        "status": b.status, "payment_status": b.payment_status,
        "completed": b.trek.completed if b.trek else False,
        "completed_on": b.completed_on.strftime('%d %b %Y') if b.completed_on else None,
    }


# ─── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    data     = request.get_json()

    email_id = data.get("email_id", "")
    password = data.get("password", "")

    if not email_id or not password:
        return jsonify({"message": "Email and password required"}), 400
    
    user = Users.query.filter_by(email_id=email_id).first()

    if not user or user.password != password:
        return jsonify({"message": "Invalid email or password"}), 401
    token = make_token(user)

    role  = (user.role).strip().lower()
    return jsonify({
        "message": f"{role.capitalize()} login successfully",
        "access_token": token, "role": role,
        "name": user.name, "email_id": user.email_id
    }), 200





# ─── registration ─────────────────────────────────────────────────────────────────────

@app.route('/register', methods=['POST'])
def Register():
    data = request.get_json()

    name= data.get("name")
    email_id= data.get("email_id")
    contact=data.get("contact")
    password=data.get("password")

    if not name or not email_id or not contact or not password:
        return jsonify({"message": "All fields are required"}), 400

    if Users.query.filter_by(email_id=email_id).first():
     return jsonify({"message": "User already exists"}), 400
     
    user= Users(name=name, email_id=email_id, contact=contact, password=password)

    db.session.add(user)

    db.session.commit()

    return jsonify({"message":"You are registered successfully"}), 201






# ───  Admin(USERS) ────────────────────────────────────────────────────────────

@app.route('/users', methods=["GET"])
@jwt_required()
def admin_dashboard():
   identity = get_jwt_identity()

   if identity.get("role") != "admin":
      return jsonify({"error": "Unauthorized access"}), 403

   users = Users.query.filter_by(role='trekker').all()

   result = []
   for user in users:
      result.append({
         "email_id": user.email_id,
         "name": user.name,
         "contact": user.contact,
         "is_active": user.is_active,
         "created_at": user.created_at.strftime('%Y-%m-%d') 
      })

   return jsonify(result), 200


@app.route('/users/<email_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_user(email_id):
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    user = Users.query.get(email_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = not user.is_active
    db.session.commit()

    status = "activated" if user.is_active else "blacklisted"
    return jsonify({
        "message":   f"User {status} successfully",
        "is_active": user.is_active
    }), 200


@app.route('/users/<email_id>', methods=['DELETE'])
@jwt_required()
def delete_user(email_id):
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    user = Users.query.get(email_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


# ─── STAFF ────────────────────────────────────────────────────────────────────
@app.route('/staff', methods=['GET'])
@jwt_required()
def get_staff():
    result = []
    for s in Staff.query.all():
        result.append({
            "staff_id":       s.staff_id,
            "email_id":       s.email_id,
            "staff_name":     s.staff_name,
            "contact":        s.contact,
            "specialization": s.specialization,
            "experience":     s.experience,
            "is_active":      s.is_active,
        })
    return jsonify(result), 200



@app.route('/staff', methods=['POST'])
@jwt_required()
def add_staff():
   
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data       = request.get_json()
    email_id   = data.get("email_id", "")
    staff_name = (data.get("staff_name") or data.get("name", "")).strip()
    contact    = str(data.get("contact", "")).strip()
    password   = data.get("password", "").strip()
    spec       = data.get("specialization", "")
    exp        = data.get("experience", "")

    if not all([email_id, staff_name, contact]):
        return jsonify({"message": "Name, email and contact are required"}), 400

    if Staff.query.filter_by(email_id=email_id).first():
        return jsonify({"message": "Staff already exists with this email"}), 400

    if not Users.query.get(email_id):
        user = Users(
            email_id=email_id, name=staff_name,
            contact=contact, password=password,
            role='staff', specialization=spec, experience=exp
        )
        db.session.add(user)
    else:
        Users.query.filter_by(email_id=email_id).update({"role": "staff"})

    s = Staff(
        email_id=email_id, staff_name=staff_name,
        contact=contact, specialization=spec, experience=exp
    )
    db.session.add(s)
    db.session.commit()


    return jsonify({
        "message":  f"Staff '{staff_name}' created. Login details sent to {email_id}",
        "staff_id": s.staff_id
    }), 201



@app.route('/staff/<int:staff_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_staff(staff_id):
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    s = Staff.query.get(staff_id)
    if not s:
        return jsonify({"message": "Staff not found"}), 404
    s.is_active = not s.is_active
    if s.user:
        s.user.is_active = s.is_active
    db.session.commit()
    return jsonify({"message": "Staff status updated", "is_active": s.is_active}), 200


@app.route('/staff/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def delete_staff(staff_id):
    email, role = current_identity()

    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    s = Staff.query.get(staff_id)
    if not s:
        return jsonify({"message": "Staff not found"}), 404
    
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Staff deleted"}), 200


# ─── TREKS ────────────────────────────────────────────────────────────────────

@app.route('/treks', methods=['GET'])
def get_trek():
   result = []
   for t in Treks.query.all():
      result.append(trek_to_dict(t))
   return jsonify(result), 200
   


@app.route('/treks', methods=["POST"])
@jwt_required()
def add_trek():

   email, role = current_identity()
   if role != "admin":
      return jsonify({"message": "Unauthorized"}), 403
   
   data  = request.get_json() or {}
   name = data.get("trek_name", "").strip()
   loc  = data.get("trek_Location", "").strip()
   sd   = data.get("start_date", "")
   ed   = data.get("end_date", "")

   if not all([name, loc, sd, ed]):
            return jsonify({"message": "Data are required"}), 400
   
   slots = int(data.get("avilable_Slots"))
   img   = data.get("image", "").strip()

   trek  = Treks(
            trek_name=name, trek_Location=loc,
            trek_difficulty=data.get("trek_difficulty", "Easy"),
            start_date=datetime.strptime(sd, '%Y-%m-%d'),
            end_date  =datetime.strptime(ed, '%Y-%m-%d'),
            duration=int(data.get("duration")),
            avilable_Slots=slots, total_slots=slots,
            assigned_staff_id=data.get("assigned_staff_id"),
            status=data.get("status", "Open"),
            image=img, description=data.get("description", ""),
            price=float(data.get("price", 0)),
         )
   db.session.add(trek)
   db.session.commit()

   return jsonify({"message": "trek created successfully", "trek_id": trek.id}), 201

@app.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    email, role = current_identity()
    if role not in ("admin", "staff"):
        return jsonify({"message": "Unauthorized"}), 403


    trek = Treks.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    data = request.get_json()

    for field in ("trek_name", "trek_Location", "trek_difficulty", "duration",
                  "avilable_Slots", "status", "image", "assigned_staff_id",
                  "description", "price", "completed", "total_slots"):
        if field in data:
            setattr(trek, field, data[field])

    if "start_date" in data and data["start_date"]:
        trek.start_date = datetime.strptime(data["start_date"], '%Y-%m-%d')

    if "end_date" in data and data["end_date"]:
        trek.end_date = datetime.strptime(data["end_date"], '%Y-%m-%d')

    db.session.commit()

    return jsonify({"message": "Trek updated successfully"}), 200



@app.route('/treks/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    trek = Treks.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted"}), 200


@app.route('/treks/<int:trek_id>/participants', methods=['GET'])
@jwt_required()
def get_trek_participants(trek_id):
    result = []
    for b in Booking.query.filter_by(trek_id=trek_id).all():
        result.append({
        "booking_id": b.booking_id,
        "user_name":  b.user.name    if b.user else b.user_id,
        "email_id":   b.user_id,
        "contact":    b.user.contact if b.user else "",
        "booking_date": b.booking_date.strftime('%d %b %Y') if b.booking_date else "",
        "status": b.status, "payment_status": b.payment_status,
        } )

    return jsonify(result), 200





# ─── BOOKINGS ─────────────────────────────────────────────────────────────────
@app.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    email, role = current_identity()
    if role == "trekker":
        bookings = Booking.query.filter_by(user_id=email).order_by(Booking.booking_date.desc()).all()
    else:
        bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return jsonify([booking_to_dict(b) for b in bookings]), 200



@app.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    email, role = current_identity()
    data    = request.get_json()
    trek_id = data.get("trek_id")

    if not trek_id:
            return jsonify({"message": "trek_id is required"}), 400
    
    trek = Treks.query.get(trek_id)
    if not trek:
      return jsonify({"message": "Trek not found"}), 404
    if trek.status != "Open":
      return jsonify({"message": f"Trek is currently {trek.status} and not accepting bookings"}), 400
    if trek.avilable_Slots <= 0:
      return jsonify({"message": "No slots available — this trek is full"}), 400
    if Booking.query.filter_by(user_id=email, trek_id=trek_id).first():
      return jsonify({"message": "You have already booked this trek"}), 400

    booking = Booking(user_id=email, trek_id=trek_id,
        status="Confirmed", payment_status="Pending")
    trek.avilable_Slots -= 1
    db.session.add(booking)
    db.session.commit()
    return jsonify({
            "message": "Trek booked successfully!",
            "booking_id": booking.booking_id,
            "trek_name": trek.trek_name
        }), 201



@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    email, role = current_identity()
    b = Booking.query.get(booking_id)
    if not b:
        return jsonify({"message": "Booking not found"}), 404
    if role == "trekker" and b.user_id != email:
        return jsonify({"message": "You can only cancel your own bookings"}), 403
    
    trek    = Treks.query.get(b.trek_id)

    

    if trek:
        trek.avilable_Slots += 1

    db.session.delete(b)
    db.session.commit()
    return jsonify({"message": "Booking cancelled successfully"}), 200

   
# ─── PROFILE ──────────────────────────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    email, role = current_identity()
    user = Users.query.get(email)
    if not user:
        return jsonify({"message": "Not found"}), 404
    
    if request.method == 'GET':
        return jsonify({
            "email_id": user.email_id, "name": user.name,
            "contact": user.contact, "role": user.role,
            "is_active": user.is_active
        }), 200
    data = request.get_json()
    if data.get("name"):     user.name     = data["name"].strip()
    if data.get("contact"):  user.contact  = data["contact"].strip()
    if data.get("password"): user.password = data["password"]
    db.session.commit()
    return jsonify({"message": "Profile updated"}), 200

         
# ─── STATS ────────────────────────────────────────────────────────────────────
@app.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    email, role = current_identity()

    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403


    recent = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()

    result = {
        "total_treks":    Treks.query.count(),
        "total_staff":    Staff.query.count(),
        "total_users":    Users.query.filter_by(role='trekker').count(),
        "total_bookings": Booking.query.count(),
        "recent_bookings": [{
            "booking_id": b.booking_id,
            "user_name":  b.user.name if b.user else b.user_id,
            "trek_name":  b.trek.trek_name if b.trek else "",
            "booking_date": b.booking_date.strftime('%d %b %Y') if b.booking_date else "",
            "status": b.status
        } for b in recent]
    }
    return jsonify(result), 200



# ─── REPORTS ──────────────────────────────────────────────────────────────────
@app.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = []
    for t in Treks.query.all():
        slots_filled = max(0, (t.total_slots or 0) - t.avilable_Slots)
        data.append({
            "trek_name":       t.trek_name,
            "trek_location":   t.trek_Location,
            "trek_difficulty": t.trek_difficulty,
            "status":          t.status,
            "total_slots":     t.total_slots,
            "available_slots": t.avilable_Slots,
            "slots_filled":    slots_filled,
            "bookings_count":  Booking.query.filter_by(trek_id=t.trek_id).count(),
            "fill_rate":       round((slots_filled / t.total_slots * 100) if t.total_slots else 0, 1)
        })
    return jsonify(data), 200


# ─── CHART DATA (for vue-chartjs) ─────────────────────────────────────────────
@app.route('/charts/bookings-per-trek', methods=['GET'])
@jwt_required()
def chart_bookings_per_trek():
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    labels = []
    values = []
    for t in Treks.query.all():
        labels.append(t.trek_name)
        values.append(Booking.query.filter_by(trek_id=t.trek_id).count())

    return jsonify({"labels": labels, "values": values}), 200


@app.route('/charts/difficulty-split', methods=['GET'])
@jwt_required()
def chart_difficulty_split():

    _, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    difficulty_map = {}
    for t in Treks.query.all():
        d = t.trek_difficulty
        difficulty_map[d] = difficulty_map.get(d, 0) + 1

    return jsonify({
        "labels": list(difficulty_map.keys()),
        "values": list(difficulty_map.values())
    }), 200


def chart_slots_status():
    email, role = current_identity()
    if role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    labels    = []
    available = []
    filled    = []
    for t in Treks.query.all():
        labels.append(t.trek_name)
        available.append(t.avilable_Slots)
        filled.append(max(0, (t.total_slots or 0) - t.avilable_Slots))

    return jsonify({
        "labels":    labels,
        "available": available,
        "filled":    filled
    }), 200









if __name__ == '__main__':
    if not Users.query.filter_by(email_id='admin123@gmail.com').first():
        admin  = Users(email_id='admin123@gmail.com', name='Rohan Sharma',  role='admin',   password='Admin123',  contact='8178757590')
        staff1 = Users(email_id='rohit123@gmail.com', name='Rohit Singh',   role='staff',   password='staff123',  contact='8178666666')
        staff2 = Users(email_id='priya123@gmail.com', name='Priya Mehra',   role='staff',   password='staff123',  contact='9911223344')
        trek1  = Users(email_id='mohit123@gmail.com', name='Mohit Kumar',   role='trekker', password='mohit123',  contact='9989877868')
        trek2  = Users(email_id='amit123@gmail.com',  name='Amit Sharma',   role='trekker', password='amit123',   contact='9876543210')
        trek3  = Users(email_id='neha123@gmail.com',  name='Neha Gupta',    role='trekker', password='neha123',   contact='9811223344')
        db.session.add_all([admin, staff1, staff2, trek1, trek2, trek3])
        db.session.commit()

        s1 = Staff(email_id='rohit123@gmail.com', staff_name='Rohit Singh', contact='8178666666', specialization='High Altitude, First Aid', experience='5 years')
        s2 = Staff(email_id='priya123@gmail.com', staff_name='Priya Mehra', contact='9911223344', specialization='Mountain Rescue, Navigation', experience='3 years')
        db.session.add_all([s1, s2])
        db.session.commit()

        sample = [
                        {"name":"Everest Base Camp", "loc":"Nepal",            "diff":"Hard",     "dur":14, "slots":12, "img":TREK_IMAGES[0], "desc":"One of the world's most iconic treks through the Khumbu Valley.", "price":45000, "staff":s1.staff_id},
                        {"name":"Roopkund Trek",     "loc":"Uttarakhand",      "diff":"Moderate", "dur":7,  "slots":15, "img":TREK_IMAGES[1], "desc":"Famous for the mysterious skeleton lake at 5029m altitude.",      "price":12000, "staff":s1.staff_id},
                        {"name":"Hampta Pass",       "loc":"Himachal Pradesh", "diff":"Moderate", "dur":5,  "slots":20, "img":TREK_IMAGES[2], "desc":"A dramatic crossover trek from Kullu to Lahaul valley.",          "price":8500,  "staff":s2.staff_id},
                        {"name":"Valley of Flowers", "loc":"Uttarakhand",      "diff":"Easy",     "dur":6,  "slots":25, "img":TREK_IMAGES[3], "desc":"UNESCO World Heritage site with stunning alpine wildflowers.",     "price":9000,  "staff":s2.staff_id},
                        {"name":"Kedarkantha Trek",  "loc":"Uttarakhand",      "diff":"Easy",     "dur":5,  "slots":18, "img":TREK_IMAGES[4], "desc":"A perfect winter trek with 360° summit panoramas.",               "price":7500,  "staff":None},
                        {"name":"Chadar Trek",       "loc":"Ladakh",           "diff":"Expert",   "dur":9,  "slots":10, "img":TREK_IMAGES[5], "desc":"Walk on the frozen Zanskar river — nature's ultimate adventure.", "price":22000, "staff":None},
                    ]
        treks_list = []
        for i, t in enumerate(sample):
            obj = Treks(
                trek_name=t["name"], trek_Location=t["loc"], trek_difficulty=t["diff"],
                start_date=datetime(2026, 9+(i//2), 10),
                end_date  =datetime(2026, 9+(i//2), 10+t["dur"]),
                duration=t["dur"], avilable_Slots=t["slots"], total_slots=t["slots"],
                assigned_staff_id=t["staff"], status="Open",
                image=t["img"], description=t["desc"], price=t["price"]
            )
            db.session.add(obj)
            treks_list.append(obj)
            db.session.commit()
            
                    # Seed sample bookings
        for uid, tr, d, st, pay in [
            (trek1.email_id, treks_list[0], '2026-05-12', 'Confirmed', 'Paid'),
            (trek2.email_id, treks_list[1], '2026-05-15', 'Confirmed', 'Paid'),
            (trek3.email_id, treks_list[0], '2026-05-18', 'Confirmed', 'Paid'),
            (trek2.email_id, treks_list[3], '2026-05-20', 'Confirmed', 'Paid'),
        ]:
            b = Booking(user_id=uid, trek_id=tr.trek_id, status=st,
                        payment_status=pay, booking_date=datetime.strptime(d, '%Y-%m-%d'))
            tr.avilable_Slots = max(0, tr.avilable_Slots - 1)
            db.session.add(b)
            db.session.commit()
            
    app.run(debug=True)