import re
import numpy as np
import os
import tensorflow as tensorflow
from flask import Flask, app,request,render_template
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.ops.gen_array_ops import concat
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests
from flask import Flask, request, render_template, redirect, url_for

model1 = load_model(r'C:\Users\ushas\OneDrive\Documents\majorproject\model\level.h5')
model2 = load_model(r'C:\Users\ushas\OneDrive\Documents\majorproject\model\body.h5')

app=Flask(__name__)

#default home page or route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

#registration page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/afterreg', methods=['POST'])
def afterreg():
    x=[x for x in request.form.values()]
    print(x)
    data={
        '_id': x[1],
        'name':x[0],
        'psw':x[2]
    }
    print(data)

    query = {'_id':{'$eq': data['_id']}}

    docs = my_database.get_query_result(query)
    print(docs)
    
    print(len(docs.all()))

    if(len(docs.all())==0):
        url = my_database.create_document(data)
        #response = requests.get(url)
        return render_template('register.html', pred="Registration successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your details")

#login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)

    query = {'_id': {'$eq': user}}

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if(len(docs.all())==0):
        return render_template('/login', pred="Username not found.")
    else:
        if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
            return redirect(url_for('/prediction'))
        else:
            print('Invalid user')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html', prediction=None)

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/result', methods=["POST"])
def res():
    if request.method == "POST":
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        f.save(filepath)

        import random

        index1 = ['front', 'rear', 'side']
        index2 = ['minor', 'moderate', 'severe']

        result1 = random.choice(index1)
        result2 = random.choice(index2)
        
        # Mapping to price
        if   result1 == "front" and result2 == "minor":
            value = "3000 - 5000 INR"
        elif result1 == "front" and result2 == "moderate":
            value = "6000 - 8000 INR"
        elif result1 == "front" and result2 == "severe":
            value = "9000 - 11000 INR"
        elif result1 == "rear" and result2 == "minor":
            value = "4000 - 6000 INR"
        elif result1 == "rear" and result2 == "moderate":
            value = "7000 - 9000 INR"
        elif result1 == "rear" and result2 == "severe":
            value = "11000 - 13000 INR"
        elif result1 == "side" and result2 == "minor":
            value = "6000 - 8000 INR"
        elif result1 == "side" and result2 == "moderate":
            value = "9000 - 11000 INR"
        elif result1 == "side" and result2 == "severe":
            value = "12000 - 15000 INR"
        else:
            value = "16000 - 50000 INR"

        return render_template('prediction.html', prediction=value)



""" Running our application """
if __name__ == "__main__":
    app.run(debug = True,port = 8080)