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
    # if select != st.session_state.selected_page:
    #     st.session_state.selected_page = select
    return select


# if 'selected_page' not in st.session_state:
#     st.session_state.selected_page = None

# # Llama a la función menu y guarda la selección en el estado de la sesión
# selected_option = menu()
# if selected_option != st.session_state.selected_page:
#     st.session_state.selected_page = selected_option  # Actualiza el estado de la selección

# # Cambia de página según la opción seleccionada
# if st.session_state.selected_page == 'Home':
#     st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py')
# elif st.session_state.selected_page == "Model":
#     st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py')
# elif st.session_state.selected_page == "About Us":
#     st.switch_page('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_5_AboutUs.py')
    #     break
    # return page
    # st.page_link('main_page.py',label='Home')
    # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py',label='Model')
    # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_5_AboutUs.py',label='About Us')
    # orientation = "horizontal"

# def menu():

    # with st.sidebar:
    #     st.page_link('main_page.py',label='Home',icon="house-fill")
    #     st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py',label='Model',icon="cpu")
    #     st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py',label='Model',icon="cpu")

    # if select == 'Home':
    #     main_page.show()
    # elif select == "Model":
    #     pass
    #     # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_2_detection.py',label='Imagen',icon="🖼️")
    #     # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_3_video.py',label='Video',icon="📽️")
    #     # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_4_model.py',label='Modelo',icon="🧠")
        
    # elif select == "About Us":
    #     pass
    #     # st.page_link('/home/santenana/Proyectos/02_ObjectDetection/Front/pages/page_5_AboutUs.py',label='About Us',icon="🪪")
        


  
