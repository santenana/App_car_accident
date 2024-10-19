import streamlit as st
import numpy as np
import os
from PIL import Image
from ultralytics import YOLO
from fpdf import FPDF
from caraccident_app import placa_id 

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

def generate_pdf(placa, label,imagen_det):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte diagnóstico de lesiones óseas", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID del paciente: {placa}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Zona afectada: {label}", ln=True)
    pdf.ln(10)
    try:
        pdf.image(imagen_det, x=10, y=50, w=100) 
    except RuntimeError:
        print("Error al cargar la imagen")
    pdf_output = f"reporte_{placa}.pdf"
    pdf.output(pdf_output)
    print(f"PDF generado con éxito: {pdf_output}")



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

    if st.button("Generate Report 📑"):
        placa = placa_id
        label = st.session_state.predicted_labels[0]
        imagen_det = st.session_state.imagen
        generate_pdf(placa, label,imagen_det)
        
            
    if st.button("🔄 Reiniciar Aplicación"):
        st.rerun()
        
    if st.button("🔙"):
        st.switch_page('./caraccident_app.py')
    
    
        



if __name__ == "__main__":
    main()