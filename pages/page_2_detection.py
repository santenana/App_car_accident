import streamlit as st
import numpy as np
import sys
import os
from PIL import Image
from ultralytics import YOLO
from fpdf import FPDF

from io import BytesIO
import tempfile

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './caraccident_app.py')))

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


def generate_pdf(placa, label, imagen_det):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Report Car Accident", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"License Plate ID: {placa}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    original_image_pil = Image.fromarray(imagen_det)
    original_image_buffer = BytesIO()
    original_image_pil.save(original_image_buffer, format="PNG")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as original_temp_file:
        original_temp_file.write(original_image_buffer.getvalue())
        original_temp_file_path = original_temp_file.name
    try:
        pdf.image(original_temp_file_path, x=10, y=50, w=100)  
    except RuntimeError:
        st.error("Error al cargar la imagen")
        return None 
    pdf_output = f"reporte_{placa}.pdf"
    pdf_output_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_output_bytes

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
        st.session_state.imagen_processed = False 
        st.session_state.image_loaded = False
    st.session_state.path_img = st.file_uploader("📁 Load Image", type=["dcm", "jpg", "jpeg", "png"])
    
    if st.session_state.path_img is not None and st.session_state.show_initial_image:
        file_extension = os.path.splitext(st.session_state.path_img.name)[1].lower()
        st.session_state.image_array = read_image_file(st.session_state.path_img)
        # st.image(st.session_state.image_array, caption="Image Loaded", use_column_width=True)
        # st.session_state.image_array = None
        st.session_state.image_loaded = True

    if st.session_state.image_loaded:
        if st.button("Detect Accident Severity"):
            st.session_state.imagen, st.session_state.predicted_labels  = imagen_detect(st.session_state.path_img)
            st.image(st.session_state.imagen, caption="Crash Detection", use_column_width=True)
            valor_predicho = st.session_state.predicted_labels[0]
            st.text_input("Prediction", value=valor_predicho, disabled=True)
            st.session_state.imagen_processed = True 
        
    if st.session_state.imagen_processed:      
        if st.button("Load Info ☁️"):
            placa = st.session_state.get('placa_id', None)
            label = st.session_state.predicted_labels
            imagen_det = st.session_state.imagen
            PDF = generate_pdf(placa, label,imagen_det)
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
    #     st.rerun()
        
    if st.button("🔙"):
        st.switch_page('./caraccident_app.py')
    
    
        



if __name__ == "__main__":
    main()