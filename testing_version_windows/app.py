from flask import Flask, render_template, request, url_for, redirect, session
import cv2
import numpy as np
import os
import base64
from PIL import Image
from io import BytesIO
import csv
import uuid
import pandas as pd

app = Flask(__name__)
app.secret_key = '5F8AD21EC73BF96204A5E8739F10B628'

@app.route('/')
def index():
    username = session.get('saved_username')
    password = session.get('saved_password')
    logged = False 
    usernamerow = ''
    paying = False

    if username and password:
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if username.strip().lower() == row[1].strip().lower() and password == row[2]:
                    logged = True
                    usernamerow = row[3]
                    if row[6] == 'True':
                        paying = True
                    else:
                        paying = False
                    break 
    
    return render_template('index.html', logged=logged, usernamerow=usernamerow, paying=paying)

@app.route('/admin')
def admin():
    username = session.get('saved_username')
    password = session.get('saved_password')
    logged = False 
    usernamerow = ''
    paying = False
    admin = False

    if username and password:
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if username.strip().lower() == row[1].strip().lower() and password == row[2]:
                    logged = True
                    if row[5] == 'True':


                        admin = True
                        csv_file = "users.csv"  
                        user_data = pd.read_csv(csv_file, header=None)

                        user_data.columns = ["id", "username", "password", "name", "surname", "admin", "status"]

                        user_data = user_data.to_dict(orient='records')

                        print(user_data)
                    else:
                        return redirect('/')
                    
                    break
                
    else:
        return redirect('/')
    
    return render_template('admin-panel.html', logged=logged, usernamerow=usernamerow, paying=paying, isadmin=admin, user_data=user_data)



@app.route('/home')
def redirecthome():
    return redirect('/')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/new-account')
def newaccount():
    return render_template('new-account.html')

def generate_unique_id():
    return str(uuid.uuid4())

@app.route('/confirm-login', methods=['POST'])
def confirmlogin():
    username = request.form['username']
    password = request.form['password']

    with open('users.csv', mode='r', newline='') as file:
        reader = csv.reader(file) 
        for row in reader:
            
            if row[1] == username and row[2] == password:
                print(row[0])
                session['saved_user_id'] = row[0]
                session['saved_username'] = row[1]
                session['saved_password'] = row[2]
                
                return redirect('/')

    return 'Credenziali errate. Riprova.'
    

@app.route('/confirm-account-registration', methods=['POST'])
def confirmaccount():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    surname = request.form['surname']
    
    user_id = generate_unique_id()
    
    admin = False
    paying = False

    new_user = [user_id, username, password, name, surname, admin, paying]

    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_user)
    
    session['saved_user_id'] = user_id
    session['saved_username'] = username
    session['saved_password'] = password

    return redirect('/')

@app.route('/confirm-registration', methods=['POST'] )
def confirmreg():
    #username = request.form['username']
    user_id = session.get('saved_user_id')
    if not user_id:
        return redirect('/login')
    base64image = request.form['userimg']

    haar_file = './models/haarcascade_frontalface_default.xml'
    datasets = 'datasets'
    sub_data = user_id

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)

    (width, height) = (130, 100)

    face_cascade = cv2.CascadeClassifier(haar_file)


    #image_path = 'dwane.jpg'
    #image = cv2.imread(image_path)
    base64_data = base64image.split(',')[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    image_path = "./temp/temp_image.jpg"
    image.save(image_path)

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

    count = 1 
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        cv2.imwrite(os.path.join(path, f'{count}.png'), face_resize)
        

    #cv2.imshow('OpenCV', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return render_template('confirm-registration.html')


if __name__ == '__main__':
    app.run(debug=True)
