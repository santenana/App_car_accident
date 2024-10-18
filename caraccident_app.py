import streamlit as st
from streamlit_option_menu import option_menu
import utilidades as util
import re

a = util.menu()
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
        st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_2_detection.py')
    if video_but:
        st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_3_video.py')
    
    
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
