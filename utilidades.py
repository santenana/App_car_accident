import streamlit as st
from streamlit_option_menu import option_menu

def menu():
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = None
    select = option_menu(
        menu_title = None,
        options = ["Home","Model","About Us"],
        icons = ["house-fill","cpu","question"],
        orientation = "horizontal")
    return select