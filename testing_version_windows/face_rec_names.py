import cv2, sys, numpy, os, csv
size = 4
haar_file = './models/haarcascade_frontalface_default.xml'
datasets = 'datasets'



def get_user_name_and_surname(user_id):
    with open('users.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                return row[3], row[4]  # Restituisci il nome e il cognome
    return None, None  # Restituisci None se l'utente non è stato trovato


print('Recognizing Face Please Be in sufficient Lights...')


(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)


(images, labels) = [numpy.array(lis) for lis in [images, labels]]


model = cv2.face.LBPHFaceRecognizer.create()
model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1] < 100:
            user_id = names[prediction[0]]
            name, surname = get_user_name_and_surname(user_id)
            if name and surname:
                text = f'{name} {surname}'
            else:
                text = 'Utente non riconosciuto'
        else:
            text = 'Non riconosciuto'
            
        cv2.putText(im, text, (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    cv2.imshow('OpenCV', im)
    
    key = cv2.waitKey(10)
    if key == 27:
        break

