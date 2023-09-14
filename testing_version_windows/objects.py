import cv2
import numpy as np

# Carica il modello YOLO preaddestrato
net = cv2.dnn.readNet('./models/yolov3.weights', './models/yolov3.cfg')

# Carica il file delle etichette dei classi
with open('./models/coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

# Leggi l'immagine locale
image_path = 'dwane1.jpg' 
image = cv2.imread(image_path)

# Definisci il colore e il font per il testo di output
color = (0, 255, 0)  # Colore del rettangolo
font = cv2.FONT_HERSHEY_SIMPLEX  # Tipo di font per il testo

# Esegui la rilevazione degli oggetti nell'immagine
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
outs = net.forward(net.getUnconnectedOutLayersNames())

class_ids = []
confidences = []
boxes = []

# Analizza le detection
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:
            # Coordinate del box
            center_x = int(detection[0] * image.shape[1])
            center_y = int(detection[1] * image.shape[0])
            width = int(detection[2] * image.shape[1])
            height = int(detection[3] * image.shape[0])

            # Calcola le coordinate del rettangolo
            x = int(center_x - width / 2)
            y = int(center_y - height / 2)

            boxes.append([x, y, width, height])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Applica la non-maximum suppression per rimuovere le sovrapposizioni
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Disegna i box e i nomi degli oggetti
for i in range(len(boxes)):
    if i in indices:
        box = boxes[i]
        x, y, width, height = box
        class_id = class_ids[i]
        label = str(classes[class_id])
        confidence = confidences[i]

        cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)
        cv2.putText(image, f'{label} {confidence:.2f}', (x, y - 10), font, 0.5, color, 2)

# Mostra l'immagine con i box e i nomi degli oggetti
cv2.imshow('Object Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
