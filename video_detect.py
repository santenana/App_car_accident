from time import  sleep
import cv2 as cv2
from collections import Counter
from ultralytics import YOLO 

best_model = YOLO("/home/santenana/Proyectos/02_ObjectDetection/best.pt")

def Video(path_video,best_model):
    video = cv2.VideoCapture(path_video)  
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter('deteccion.avi',fourcc,30,(w,h))  
    labels = best_model.model.names 
    all_predicted_labels = []
    while video.isOpened():  
        ret,frame = video.read()
        if ret == False:
            break
        cv2.imshow("", frame)
        res = best_model.predict(frame,imgsz=640) 
        predicted_labels = []
        for result in res:
            for pred in result.boxes:
                label_index = int(pred.cls) 
                label = labels[label_index]
                predicted_labels.append(label)
        all_predicted_labels.append(predicted_labels)
        anote = res[0].plot()
        out.write(anote)
        cv2.imshow("", anote)         
        if cv2.waitKey(1) == 27: 
            break
        sleep(1/60)
    video.release()
    label = all_predicted_labels
    f_label = [item for sublist in label for item in sublist]
    label_counts = Counter(f_label)
    total_count = sum(label_counts.values())
    label_probabilities = {key: value / total_count for key, value in label_counts.items()}
    for label, prob in label_probabilities.items():
        label = label
        prob = prob
        # print(f"Clase: {label}, Probabilidad: {prob:.4f}")
    
    cv2.destroyAllWindows()
    return label,prob