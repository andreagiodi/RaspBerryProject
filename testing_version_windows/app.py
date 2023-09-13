from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    name = "Ciao"
    return render_template('index.html',name=name)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/confirm-registration', methods=['POST'] )
def confirmreg():
    username = request.form['username']

    import cv2
    import numpy as np
    import os

    haar_file = './models/haarcascade_frontalface_default.xml'
    datasets = 'datasets'
    sub_data = username

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)

    (width, height) = (130, 100)

    face_cascade = cv2.CascadeClassifier(haar_file)

# Carica un'immagine locale per la registrazione del volto
    image_path = 'dwane.jpg'
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

    count = 1
    while count <= 30:  
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite(os.path.join(path, f'{count}.png'), face_resize)
            count += 1

    #cv2.imshow('OpenCV', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return render_template('confirm-registration.html',username=username)


if __name__ == '__main__':
    app.run(debug=True)