
from fpdf import FPDF
from caraccident_app import placa_id 

placa = placa_id

def generate_pdf(placa, label, proba, original_image, heatmap_image):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte diagnóstico de lesiones óseas", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID del paciente: {placa}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Zona afectada: {label}", ln=True)
    pdf.cell(200, 10, txt=f"Probabilidad de lesión crítica: {proba:.2f}%", ln=True)

    pdf.ln(10)

    # Convertir imágenes a PIL para agregar al PDF
    original_image_pil = Image.fromarray(original_image)
    heatmap_image_pil = Image.fromarray(heatmap_image)

    # Guardar imágenes en buffers de memoria
    original_image_buffer = BytesIO()
    heatmap_image_buffer = BytesIO()

    original_image_pil.save(original_image_buffer, format="PNG")
    heatmap_image_pil.save(heatmap_image_buffer, format="PNG")

    # Volver a la posición inicial del buffer
    original_image_buffer.seek(0)
    heatmap_image_buffer.seek(0)

    # Convertir los buffers de imágenes a archivos temporales
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as original_temp_file:
        original_temp_file.write(original_image_buffer.getvalue())
        original_temp_file_path = original_temp_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as heatmap_temp_file:
        heatmap_temp_file.write(heatmap_image_buffer.getvalue())
        heatmap_temp_file_path = heatmap_temp_file.name

    # Agregar las imágenes desde archivos temporales
    pdf.image(original_temp_file_path, x=10, y=80, w=90)
    pdf.image(heatmap_temp_file_path, x=110, y=80, w=90)

    pdf.ln(85)
    pdf.cell(200, 10, txt="Imagen Original", ln=False, align="C")
    pdf.cell(200, 10, txt="Heatmap de Imagen", ln=False, align="C")

    # Guardar el PDF en un buffer de memoria y devolverlo
    pdf_buffer = BytesIO()
    pdf_buffer.write(pdf.output(dest='S').encode("latin1"))

    # Regresar los bytes del PDF para descargar
    pdf_buffer.seek(0)
    
    # Eliminar archivos temporales
    os.remove(original_temp_file_path)
    os.remove(heatmap_temp_file_path)
    
    return pdf_buffer