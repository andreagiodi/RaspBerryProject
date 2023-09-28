import cv2
import sys
import numpy
import os
import csv
import time

size = 4
haar_file = './models/haarcascade_frontalface_default.xml'
datasets = 'datasets'

def get_user_info(user_id):
    with open('users.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                name = row[3]
                surname = row[4]
                info = row[6] if len(row) > 6 else None
                return name, surname, info
    return None, None, None

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

# Inizializza le variabili per il controllo del tempo e dello stato del tornello.
utente_pagante_rilevato = False
tempo_iniziale = 0

while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Conta il numero di volti rilevati
    numero_di_volti_rilevati = len(faces)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1] < 100:
            user_id = names[prediction[0]]
            name, surname, info = get_user_info(user_id)
            if name and surname:
                if info:
                    if info == 'True':
                        info = 'PAGANTE'
                        color = (0, 255, 0)
                        
                        # Se l'utente pagante è stato rilevato per la prima volta, registra il tempo iniziale.
                        if not utente_pagante_rilevato:
                            utente_pagante_rilevato = True
                            tempo_iniziale = time.time()
                    else:
                        info = 'NON PAGANTE'
                        color = (255, 255, 0)
                        utente_pagante_rilevato = False
                        
                    
                    text = f'{name} {surname} - {info}'
                else:
                    text = f'{name} {surname}'
                    utente_pagante_rilevato = False
            else:
                text = 'Utente non riconosciuto'
                color = (255, 0, 0)
                utente_pagante_rilevato = False
        else:
            text = 'Non riconosciuto'
            color = (255, 0, 0)
            utente_pagante_rilevato = False
            
        cv2.putText(im, text, (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 2, color)
    
    # Aggiungi il numero di volti rilevati in tempo reale in alto a destra della schermata
    cv2.putText(im, f'Volti Rilevati: {numero_di_volti_rilevati}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('OpenCV', im)
    
    # Verifica se l'utente pagante è stato rilevato per più di 2 secondi e apri il tornello.
    if utente_pagante_rilevato and (time.time() - tempo_iniziale) >= 2:
        if utente_pagante_rilevato:
            print('Apertura Tornello...')
        else:
            print("Errore Riprovare")   
            
        utente_pagante_rilevato = False  # Resetta il flag
        
    key = cv2.waitKey(10)
    if key == 27:
        break

# Chiudi la finestra e rilascia la videocamera
webcam.release()
cv2.destroyAllWindows()
