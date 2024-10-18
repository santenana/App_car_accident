import streamlit as st
import numpy as np
import os
from PIL import Image
from ultralytics import YOLO
import matplotlib.pyplot as plt

model_path = './best.pt'

st.markdown("# Detection Image")

try:
    model = YOLO(model_path)
    st.success("Model Loaded")
except Exception as e:
    st.error(f"Error in Model Load: {e}")

def read_image_file(path):
    img = Image.open(path)
    img = img.convert('RGB')
    img_array = np.array(img)
    return img_array

def imagen_detect(path):
    image_array = read_image_file(path)
    res = model.predict(image_array,imgsz=640)
    imagen = res[0].plot()
    labels = res[0].names
    predicted_labels = []
    for result in res:
        for pred in result.boxes:
            label_index = int(pred.cls)
            label = labels[label_index]
            predicted_labels.append(label)
    return (imagen,predicted_labels)

def main():
    if 'image_array' not in st.session_state:
        st.session_state.image_array = None
        st.session_state.label = None
        st.session_state.proba = None
        st.session_state.pdf_buffer = None  
        st.session_state.file_extension = None
        st.session_state.imagen = None
        st.session_state.predicted_labels = None
        st.session_state.show_initial_image = True
        st.session_state.path_img = None
    st.session_state.path_img = st.file_uploader("📁 Load Image", type=["dcm", "jpg", "jpeg", "png"])
    
    if st.session_state.path_img is not None and st.session_state.show_initial_image:
        file_extension = os.path.splitext(st.session_state.path_img.name)[1].lower()
        st.session_state.image_array = read_image_file(st.session_state.path_img)
        # st.image(st.session_state.image_array, caption="Image Loaded", use_column_width=True)
        # st.session_state.image_array = None

    if st.button("Detect Accident Severity"):
        st.session_state.imagen, st.session_state.predicted_labels  = imagen_detect(st.session_state.path_img)
        st.image(st.session_state.imagen, caption="Crash Detection", use_column_width=True)
        valor_predicho = st.session_state.predicted_labels[0]
        st.text_input("Prediction", value=valor_predicho, disabled=True)
        
        if st.button("Load Info ☁️"):
            st.write('Info Loaded')
            
    if st.button("🔄 Reiniciar Aplicación"):
        st.rerun()
    
    if st.button("🔙"):
        st.switch_page('./caraccident_app.py')
    



if __name__ == "__main__":
    main()