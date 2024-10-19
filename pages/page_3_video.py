import streamlit as st
import cv2
import numpy as np
from PIL import Image
from collections import Counter
from time import sleep
from ultralytics import YOLO
from tempfile import NamedTemporaryFile
from fpdf import FPDF

model_path = './best.pt'

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
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = st.progress(0)
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
        progress = (video.get(cv2.CAP_PROP_POS_FRAMES) / total_frames)
        progress_bar.progress(progress)
        sleep(1/30)  
    video.release()  
    cv2.destroyAllWindows()  
    f_label = [item for sublist in all_predicted_labels for item in sublist]
    label_counts = Counter(f_label)
    return label_counts

def generate_pdf(placa, L_label):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Report Car Accident", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"License Plate ID: {placa}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Detection Probabilities:", ln=True)
    pdf.ln(5)
    for label, probability in L_label.items():
        pdf.cell(200, 10, txt=f"{label}: {probability:.0%} probability", ln=True)

    # Generar el archivo PDF
    pdf_output = f"reporte_{placa}.pdf"
    pdf_output_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_output_bytes

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
            with st.spinner("Processing video..."):
                label_counts = Video(video_path, model)
                st.session_state.label_counts = label_counts
                st.session_state.video_processed = True     
    if st.session_state.video_processed:
        if st.button("Load Info ☁️"):
            # st.write("### Predicciones en el video:")
            placa = st.session_state.get('placa_id', None)
            len_lables = len(st.session_state.label_counts)
            L_label = {}
            total_detections = sum(st.session_state.label_counts.values())
            for label, count in st.session_state.label_counts.items():
                probability = count / total_detections
                # st.write(f"{label}: {probability:.0%} probability")
                L_label[label] = probability
            st.write('Info Loaded')
            
            PDF = generate_pdf(placa, L_label)
            if PDF:
                st.success("¡Reporte generado con éxito!")
                st.download_button(
                        label="Descargar Reporte",
                        data=PDF,
                        file_name=f"reporte_{placa}.pdf",
                        mime='application/pdf'
                    )
            else:
                st.warning("No se pudo generar el reporte. Verifica los datos.")

        else:
                    st.warning("No labels detected yet. Please run the detection first.")


    # if st.button("🔄 Reiniciar Aplicación"):
    #     st.session_state.video_processed = False
    #     st.session_state.label_counts = None
    #     st.rerun()
        
    if st.button("🔙"):
        st.switch_page('./caraccident_app.py')
    
if __name__ == "__main__":
    main()
