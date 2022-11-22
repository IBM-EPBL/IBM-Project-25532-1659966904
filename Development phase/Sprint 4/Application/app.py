#import numpy as np
#import pickle
#import sklearn
#from flask import Flask, request, render_template
#model = pickle.load(open('models.pkl', 'rb')) 

#app = Flask(__name__)
#@app.route('/')
#def home():
 #return render_template('home.html')
#@app.route('/signin')
#def signin():
   #return render_template('signin.html')

#@app.route('/signup')
#def signup():
   #return render_template('signup.html')


#@app.route('/predict', methods =['POST'])
#def predict():
  
  #features = [float(i) for i in request.form.values()]
  #Convert features to array
  #array_features = [np.array(features)]
  #Predict features
  #prediction = model.predict(array_features)
  #output = prediction
  #if output == 1:
    #return render_template('Heart_Disease_Classifier.html', result = 'The patient is not likely to have heart disease!')
  #else:
    #return render_template('Heart_Disease_Classifier.html', result = 'The patient is likely to have heart disease!')

#if __name__ == '__main__':
   #debug(True)
import numpy as np
import pickle
import sklearn
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
model = pickle.load(open('models.pkl', 'rb')) 
app = Flask(__name__)
app.secret_key = "7847541"

def get_db():
    conn = sqlite3.connect('user_details.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signin', methods=('GET', 'POST'))
def signin():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT name FROM user_details WHERE password = ?', (password, )
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
  

        if error is None:
            return render_template('index.html', title="Home", succ="login successfull!")
        flash(error)
        db.close()

    return render_template('signin.html', title='Sign In', error=error)


@app.route('/signup', methods=('POST', 'GET'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        curr = db.cursor()
        curr.execute(
            'INSERT INTO user_details (name, email, password) VALUES (?, ?, ? );', (name, email, password )
        )
        db.commit()
        curr.close()
        db.close()
        return render_template('index.html', title="Home", succ="Registration Successfull!")
    return render_template('signup.html', title='Sign Up')


@app.route('/Heart_Disease_Classifier')
def Heart_Disease_Classifier():
       return render_template('Heart_Disease_Classifier.html')   

@app.route('/predict', methods =['POST'])
def predict():
  
  features = [float(i) for i in request.form.values()]
  #Convert features to array
  array_features = [np.array(features)]
  #Predict features
  prediction = model.predict(array_features)
  output = prediction
  if output == 1:
    return render_template('Heart_Disease_Classifier.html', result = 'The patient is not likely to have heart disease!')
  else:
    return render_template('Heart_Disease_Classifier.html', result = 'The patient is likely to have heart disease!')

if __name__ == '__main__':
   debug(True)
