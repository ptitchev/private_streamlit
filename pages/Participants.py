import numpy as np
import pandas as pd
import streamlit as st
from github import Github

#1 : Data
df_shown = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/ds.csv')

df_rep = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/dr.csv')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """ #permet de cacher le burger menu

hide_sidebar_style =  """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """

st.set_page_config(page_title="Projet Chev", initial_sidebar_state="collapsed") #configue page (Nome et nav menu fermé)
st.markdown(hide_menu_style, unsafe_allow_html=True) #applique hide_menu_style

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"] or st.session_state["password"] == st.secrets["passworda"]:
            st.session_state["password_correct"] = True
            if st.session_state["password"] == st.secrets["passworda"]:
                st.session_state["a"] = 1
            del st.session_state["password"]
            
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown(hide_sidebar_style,unsafe_allow_html=True)
        st.text_input(
            "Mot de passe", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Mauvais mot de passe BG")
        return False
    else:
        return True
    
if check_password():

    with st.expander("Participants"):
        st.dataframe(df_shown, use_container_width= True)