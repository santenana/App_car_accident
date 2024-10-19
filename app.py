import streamlit as st
from streamlit_option_menu import option_menu
import utilidades as util
import re
from PIL import Image
from ultralytics import YOLO
import os
import numpy as np
import cv2
import numpy as np
from collections import Counter
from time import sleep
from tempfile import NamedTemporaryFile

a = util.menu()
model_path = './best.pt'
if a == 'Home':
    st.markdown("# Welcome")
    st.markdown(
            """
            <style>
            .custom-text {
                font-size: 20px;
                font-family: 'Rockwell', Rockwell;
                color: #002f6c;
                text-align: justify;
            }
            </style>
            <p class="custom-text">
            Welcome to the Automatic Vehicle Accident Detection app.
            If you have suffered a crash or witnessed a car accident, please write the vehicle's 
            license plate and select the options for Image or Video to analyze the severity of 
            the incident and provide you with the steps to follow to claim your insurance or the 
            affected party's insurance.
            </p>
            """,
            unsafe_allow_html=True)

    placa_id = st.text_input("Write license plate:", "", key="texto", help="Linces Plate in capital letters and no Sapces")

    def validar_texto(texto):
        patron = r'^[A-Z]{3}[0-9][0-9][0-9]'
        return re.match(patron, texto) is not None

    if st.button("Enviar"):
        if validar_texto(placa_id):
            st.success("Your Linces Plate is: " + placa_id)
        else:
            st.error("Invalid Format. Make sure the linces plate contains all 3 letters in capital and 3 numbers")

    st.markdown("---")
    image_but = st.button('Imagen')
    video_but = st.button('Video')
    
    if image_but:
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
                if st.session_state.predicted_labels:
                    st.write(f"Predicted Labels: {', '.join(st.session_state.predicted_labels)}")
                else:
                    st.warning("No labels detected yet. Please run the detection first.")
                    
            if st.button("🔄 Reiniciar Aplicación"):
                st.rerun()
                
            if st.button("🔙"):
                st.switch_page('./caraccident_app.py')
        if __name__ == "__main__":
            main()
                
    if video_but:
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
                sleep(1/60)  
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
                st.switch_page('./caraccident_app.py')
            
        if __name__ == "__main__":
            main()
    
    
if a == 'Model':
    st.markdown("# Model")
    
    
    
if a == 'About Us':
    st.markdown("# About SGS Insurance")

    st.markdown(
        """
        <style>
        .custom-text {
            font-size: 20px;
            font-family: 'Rockwell', Rockwell;
            color: #002f6c;
            text-align: justify;
        }
        </style>
        <p class="custom-text">
        At SGS Insurance, we love serving our clients by helping them with whatever
        they need, always working for their well-being and peace of mind.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .custom-text {
            font-size: 20px;
            font-family: 'Rockwell', Rockwell;
            color: #002f6c;
            text-align: justify;
        }
        </style>
        <p class="custom-text">
        At Founded in 1997, this insurance company has been helping people around the 
        world, taking care of them during the toughest moments of their lives. 
        SGS Insurance assists its clients in overcoming the challenges they face.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .custom-text {
            font-size: 20px;
            font-family: 'Rockwell', Rockwell;
            color: #002f6c;
            text-align: justify;
        }
        </style>
        <p class="custom-text">
        Throughout our history, we have evolved to meet the demands of a modern 
        world, adapting to the needs of our clients. For this reason, with the 
        rise of AI, we have developed our own AI to help our clients make informed 
        decisions and provide peace of mind. That's why we are launching SGS-View, 
        our new AI that can quickly assess the severity of an accident and notify 
        you of the steps you need to take for your safety and peace of mind.
        </p>
        """,
        unsafe_allow_html=True
    )
