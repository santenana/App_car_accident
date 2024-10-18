import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from collections import Counter
from time import sleep
from ultralytics import YOLO
from tempfile import NamedTemporaryFile
from io import BytesIO

model_path = '/home/santenana/Proyectos/02_ObjectDetection/Front/best.pt'

st.markdown("# Detection Video")

try:
    model = YOLO(model_path)
    st.success("Model Loaded")
except Exception as e:
    st.error(f"Error in Model Load: {e}")

def Video(video_path, best_model):
    video = cv2.VideoCapture(video_path)
    labels = best_model.model.names
    all_predicted_labels = []
    frame_placeholder = st.empty()
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        res = best_model.predict(frame, imgsz=640)
        predicted_labels = []
        for result in res:
            for pred in result.boxes:
                label_index = int(pred.cls)
                label = labels[label_index]
                predicted_labels.append(label)
        all_predicted_labels.append(predicted_labels)
        annotated_frame = res[0].plot()
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(annotated_frame_rgb, channels="RGB")
        sleep(1/30)  
    video.release()  
    cv2.destroyAllWindows()  
    f_label = [item for sublist in all_predicted_labels for item in sublist]
    label_counts = Counter(f_label)
    return label_counts

def main():
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
        st.session_state.predicted_labels = None
        st.session_state.label_counts = None
        st.session_state.video_processed = False  
    uploaded_file = st.file_uploader("📁 Load Video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        tfile = NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        if st.button("Detect Accident Severity in Video"):
            label_counts = Video(video_path, model)
            st.session_state.label_counts = label_counts
            st.session_state.video_processed = True     
    if st.session_state.video_processed:
        if st.button("Load Info ☁️"):
            st.write("### Predicciones en el video:")
            len_lables = len(st.session_state.label_counts)
            total_detections = sum(st.session_state.label_counts.values())
            for label, count in st.session_state.label_counts.items():
                probability = count / total_detections
                st.write(f"{label}: {probability:.0%} probability")
            st.write('Info Loaded')
    
    if st.button("🔄 Reiniciar Aplicación"):
        st.session_state.video_processed = False
        st.session_state.label_counts = None
        st.rerun()
        
    if st.button("🔙"):
        st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/front.py')
    
if __name__ == "__main__":
    main()
