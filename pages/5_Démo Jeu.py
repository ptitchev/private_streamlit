import streamlit as st
import numpy as np
import pandas as pd
from game_tools.game_engine import *
import json
from PIL import Image
from io import BytesIO
import requests

#CSS
st.markdown(
    """ 
    <style>
        .stProgress > div > div > div > div {
            background-color: c319b8;
        }
    </style>""",
    unsafe_allow_html=True,
)

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
st.markdown(hide_menu_style, unsafe_allow_html=True) #applique hide_menu_style
st.markdown(hide_sidebar_style,unsafe_allow_html=True)


def start_G():
    st.session_state["is_playing"] = True
    st.session_state["game"], st.session_state["trois_choix"] = start_game()
    
def play_G0():
    st.session_state["game"], st.session_state["trois_choix"] = player_play(st.session_state["game"], st.session_state["trois_choix"][0])

def play_G1():
    st.session_state["game"], st.session_state["trois_choix"] = player_play(st.session_state["game"], st.session_state["trois_choix"][1])

def play_G2():
    st.session_state["game"], st.session_state["trois_choix"] = player_play(st.session_state["game"], st.session_state["trois_choix"][2])
    
url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/image 1024/'

st.info('Sur téléphone, il est conseillé de passer en mode paysage')
st.subheader("Jouer à : Démo jeu Chev")

if "is_playing" not in st.session_state:
    blank1 = st.write("")
    blank2 = st.write("")
    e1, c1, e2 = st.columns([5, 3, 5])
    with c1 :
        st.button('Jouer', on_click=start_G)
    blank1 = st.write("")
    blank2 = st.write("")

if "is_playing" in st.session_state :

    if len(st.session_state["trois_choix"]) > 2 :

        c1, c2, c3, c4 = st.columns([2,2,3,1])
        with c1 :
            Time = st.metric("Heure", conv_time(st.session_state["game"][1]))
        with c3:
            Musique = st.selectbox('Musique', ('Aucune','Rap','Rock','Techno','Commercial', 'House'), index = 0)
        with c4 :
            Bpm = st.metric("BPM", str(int(st.session_state["game"][2])))
        blank1 = st.write("")
        blank2 = st.write("")

        e1, c1, e2, c2, e3, c3, e4 = st.columns([1,3,1,3,1,3,1])
        with c1 :
            response = requests.get(url + str(st.session_state["trois_choix"][0]) + '.png')
            image0 = Image.open(BytesIO(response.content))            
            i0 = st.image(image0)
            b0 = st.button(L_nom[st.session_state["trois_choix"][0]], on_click=play_G0)
        with c2 :
            response = requests.get(url + str(st.session_state["trois_choix"][1]) + '.png')
            image1 = Image.open(BytesIO(response.content))            
            i1 = st.image(image1)
            b1 = st.button(L_nom[st.session_state["trois_choix"][1]], on_click=play_G1)
        with c3 :
            response = requests.get(url + str(st.session_state["trois_choix"][2]) + '.png')
            image2 = Image.open(BytesIO(response.content))            
            i2 = st.image(image2)
            b2 = st.button(L_nom[st.session_state["trois_choix"][2]], on_click=play_G2)
        blank1 = st.write("")
        blank2 = st.write("")

        c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
        with c1 :
            Energie = st.progress(bar_val(st.session_state["game"],3), text="Energie")
        with c2 :
            Soif = st.progress(bar_val(st.session_state["game"],4), text="Alcool")
        with c3 :
            Drogue = st.progress(bar_val(st.session_state["game"],5), text="Drogue")
        with c4 :
            Faim = st.progress(bar_val(st.session_state["game"],6), text="Faim")
        with c5 :
            Fun = st.progress(bar_val(st.session_state["game"],7), text="Fun")

    else :

        st.write(show_death(st.session_state["game"], st.session_state["trois_choix"]))
        restart = st.button('Restart', on_click=start_G)

with st.expander("Règles"):
        st.write("Comprend tout seul frerot c'est que la démo")
