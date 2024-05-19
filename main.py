# from flask import Flask, request, render_template, redirect, url_for
import requests
import json
from datetime import datetime
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename




from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from database import Trip, db



from database import delete_trip_by_id


global_age=""
global_sex=""
global_dest=""
global_startDate=""
global_nrDays=""
global_type=""
global_activities=""

app = Flask(__name__, static_folder='static')






app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# migrate.init_app(app, db)

with app.app_context():
      #   from . import models, routes
        db.create_all()






@app.route('/')
def index():
   return render_template('index.html')

@app.route('/trips')
def trips():
   trips = Trip.query.order_by(Trip.id.desc()).all()
   return render_template('trips.html', trips = trips)





@app.route('/delete_trip', methods=['POST'])
def delete_trip():
    trip_id = request.form['trip_id']
    delete_trip_by_id(trip_id)  # Implement this function to delete the trip from your database
    return redirect(url_for('trips')) 










@app.route('/elements', methods=['POST', 'GET'])
def elements():
   trip = Trip.query.filter_by(id=int(request.form["trip_id"])).first()
   files = os.listdir(app.config['UPLOAD_PATH'])
   return render_template('elements.html', trip=trip, files=files)

@app.route('/new_trip')
def new_trip():
   return render_template('new_trip.html')

@app.route('/generate_trip', methods=['POST', 'GET'])
def generate_trip():
   #pt generare
   headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDkzNWY4MzgtMjQ2Ny00ODQ3LTg1NGEtYTQ0ZGFlZDQ2ZThjIiwidHlwZSI6ImFwaV90b2tlbiJ9.TCml4_L1JZiQPA7A54449jU0s49Ty1gjIuRJoR_PVLc",
              "Content-Type": "application/json"}
   url = "https://api.edenai.run/v2/text/generation"
    
   global global_age
   global global_sex
   global global_dest
   global global_startDate
   global global_nrDays
   global global_type
   global global_activities
   generated_documents="Please refresh"
   generated_clothing="Please refresh"
   generated_care="Please refresh"
   generated_electronics="Please refresh"
   generated_activity="Please refresh"


   global_dest = request.form['destination']
   global_startDate = request.form['start_date']
   global_nrDays = request.form['nr_days']
   global_type = request.form.getlist('holiday_type')
   global_activities = request.form['activities']
   #formatare text
   holiday_type_str = ', '.join(global_type)

   #luna vacantei
   date = datetime.strptime(global_startDate, '%Y-%m-%d')
   month = date.month

   # Documents and Money
   payload = {
      "providers": "cohere", #,cohere","openai"
      "text": f"only a list with Documents and Money that i have to pack if i am a {global_age} {global_sex} i go to {global_dest} in month {month} and i want to {global_activities}. i stay for {global_nrDays} days",
      # "response_format": { "type": "json_object" },
      "temperature" : 0.2,
      "max_tokens":2500
   }
   response_documents = requests.post(url, json=payload, headers=headers)
   if response_documents.status_code == 200:
      # Parse the response
      result_documents = response_documents.json()
      generated_documents = result_documents.get('cohere', {}).get('generated_text', '')

    # Clothing and Accessories
   payload = {
      "providers": "cohere", #,cohere","openai"
      "text": f"only a list with Clothing (from underware to shoes) that i have to pack if i am a {global_age} {global_sex} i go to {global_dest} in month {month} and i want to {global_activities}. i want to know how many items i need from each if i stay for {global_nrDays} days depending on the weather for the next {global_nrDays} in {global_dest} starting with {global_startDate}",
      "temperature" : 0.2,
      "max_tokens":2500
   }
   response_clothing = requests.post(url, json=payload, headers=headers)
   if response_clothing.status_code == 200:
      result_clothing = response_clothing.json()
      generated_clothing = result_clothing.get('cohere', {}).get('generated_text', '')

   # Personal Care and Health Products
   payload = {
      "providers": "cohere", #,cohere","openai"
      "text": f"only a list with Hygiene Products that i have to pack if i am a {global_sex} and i go to {global_dest} in month {month} and i want to {global_activities}. i stay for {global_nrDays} days",
      "temperature" : 0.2,
      "max_tokens":2500
   }
   response_care = requests.post(url, json=payload, headers=headers)
   if response_care.status_code == 200:
      # Parse the response
      result_care = response_care.json()
      generated_care = result_care.get('cohere', {}).get('generated_text', '')

   # Electronics and Accessories
   payload = {
      "providers": "cohere", #,cohere","openai"
      "text": f"only a list with Electronics and Accessories that i have to pack if i am a {global_age} {global_sex} and i go to {global_dest} in month {month} and i want to {global_activities}. i stay for {global_nrDays} days",
      "temperature" : 0.2,
      "max_tokens":2500
   }
   response_electronics = requests.post(url, json=payload, headers=headers)
   if response_electronics.status_code == 200:
      # Parse the response
      result_electronics = response_electronics.json()
      generated_electronics = result_electronics.get('cohere', {}).get('generated_text', '')

   # Other
   payload = {
      "providers": "cohere", #,cohere","openai"
      "text": f"only a list of things that i need if i want to {global_activities} and i go for the {global_type}",
      "temperature" : 0.2,
      "max_tokens":2500
   }
   response_activity = requests.post(url, json=payload, headers=headers)
   if response_activity.status_code == 200:
      # Parse the response
      result_activity = response_activity.json()
      generated_activity = result_activity.get('cohere', {}).get('generated_text', '')

   # # Weather
   # payload = {
   #    "providers": "cohere", #,cohere","openai"
   #    "text": f" the temperature and the overrall weather for the next {global_nrDays} in {global_dest} starting with {global_startDate} in Celsius",
   #    "temperature" : 0.2,
   #    "max_tokens":250
   # }
   # response_weather = requests.post(url, json=payload, headers=headers)
   # result_weather = json.loads(response_weather.text)


   new_trip=Trip(destination=global_dest,
                  nr_days=global_nrDays,
                  start_date=global_startDate,
                  holiday_type=''.join(global_activities),
                  activity_type=global_activities,
                  documents=generated_documents,
                  clothes=generated_clothing,
                  care=generated_care,
                  electronics=generated_electronics,
                  activity=generated_activity)
   db.session.add(new_trip)
   db.session.commit()
   last_trip = Trip.query.order_by(Trip.id.desc()).first()

   return render_template('generate_trip.html', 
                           trip=last_trip
                           #top
                           #  destination=global_dest,
                           #  start_date=global_startDate,
                           #  nr_days=global_nrDays,
                           #  holiday_type=holiday_type_str,
                           #  activities=global_activities,
                           # # generate 
                           # #  result_weather=result_weather,
                           #  result_clothing=generated_clothing,
                           #  result_activity=generated_activity,
                           #  result_documents=generated_documents,
                           #  result_care=generated_care,
                           #  result_electronics=generated_electronics
                            )

# upload image for trip
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/create_trip', methods=['POST','GET'])
def image():
   trip_id=request.form['trip_id']
   trip=Trip.query.filter_by(id = int(trip_id)).first()
   uploaded_file = request.files['file']
   filename = secure_filename(uploaded_file.filename)
   if filename == '':
      return redirect(url_for('trips'))
   
   file_ext = os.path.splitext(filename)[1]
   if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
      abort(400)

   uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
   files = os.listdir(app.config['UPLOAD_PATH'])

   trip.image = filename
   # db.session.merge(trip)
   db.session.commit()


   result_documents = request.form['result_documents']
   # return render_template('create_trip.html', files=files, result_documents=result_documents,fileName = filename, trip=trip)
   return redirect(url_for('trips'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)











if __name__ == '__main__':
   app.run(debug=True)