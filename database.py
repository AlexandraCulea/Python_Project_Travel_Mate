from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
# db.create_all()
# exit()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    nr_days = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    holiday_type = db.Column(db.String(50), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    documents = db.Column(db.String(50), nullable=False)
    clothes = db.Column(db.String(50), nullable=False)
    care = db.Column(db.String(50), nullable=False)
    electronics = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False, default='../static/Plaja.jpg')

def delete_trip_by_id(trip_id):
    trip = Trip.query.get(trip_id)
    if trip:
        db.session.delete(trip)
        db.session.commit()