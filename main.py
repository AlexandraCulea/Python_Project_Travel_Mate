# from flask import Flask, render_template
from flask import Flask, request, render_template, redirect, url_for






import requests
import json







app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/trips')
def trips():
   return render_template('trips.html')

@app.route('/elements')
def elements():
   return render_template('elements.html')

@app.route('/new_trip')
def new_trip():
   return render_template('new_trip.html')

@app.route('/generate_trip', methods=['POST', 'GET'])
def generate_trip():
    destination = request.form['destination']
    # destination ="loca"
    return render_template('generate_trip.html', destination=destination)







@app.route('/generate_text', methods=['POST','GET'])
def generate_text():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDkzNWY4MzgtMjQ2Ny00ODQ3LTg1NGEtYTQ0ZGFlZDQ2ZThjIiwidHlwZSI6ImFwaV90b2tlbiJ9.TCml4_L1JZiQPA7A54449jU0s49Ty1gjIuRJoR_PVLc"}
    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": "lista cu ce trebuie sa imi iau in bagaj daca merg la mare in Italia",
        "temperature" : 0.2,
        "max_tokens":250
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    print(result)
    return result








if __name__ == '__main__':
   app.run(debug=True)