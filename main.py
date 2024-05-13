from flask import Flask, render_template

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

if __name__ == '__main__':
   app.run(debug=True)