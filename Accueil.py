import streamlit as st
from PIL import Image
from style.css import hide_menu_style, hide_sidebar_style
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import urllib.request
from io import BytesIO

archives_name = ["The Chev Party - volume 1"]
archives_time = ["Juin 2023"]

def _login():
    if "try_login" not in st.session_state:
            st.session_state["try_login"] = 1
    else :
        st.session_state["try_login"] += 1
    if st.session_state["try_login"] == 5:
        st.error('TEST : user=chevleboss, password=chev')

def spawn_login():
    e1, c = st.columns([5,1])
    with c :
        login = st.button('Connexion', on_click = _login, disabled = ("try_login" in st.session_state and st.session_state["try_login"] > 4))

def _invit():
    st.session_state["invit"] = True

def spawn_invit():
    c1, e1, c2, e2, c3 = st.columns([3,1,6,1,3])
    with c1:
        response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo2.png')
        image = Image.open(BytesIO(response.content))
        st.image(image)
    with c2 :
        st.write(" ")
        st.metric(label="Le weekend du", value="31 mai - 2 juin")
    with c3:
        st.write(" ")
        st.button(':ringed_planet: Particper', on_click = _invit)

def _send_mail(email):
    subject = "Nouvelle demande"
    body = email
    sender_email = "jules.chevenet.pro@gmail.com"
    receiver_email = "jules.chevenet.pro@gmail.com"
    password = st.secrets["gmail_password"]
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    context = ssl.create_default_context()
    if len(email)>0:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            st.balloons()
            st.session_state["mail"] = True

def spawn_event():
    c1, e1, c2, e2, c3 = st.columns([3,1,6,1,3])
    with c1:
        response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo2.png')
        image = Image.open(BytesIO(response.content))
    with c2 :
        st.write(" ")
        st.metric(label="Le weekend du", value="31 mai - 2 juin")

    st.divider()
    st.info("Ceci est une invitation pour ***The chev Party - volume 2*** pour célébrer le temps d'un week-end l'anniv du vraiment formidable *Jules Chevenet*")
    email = st.text_input("le mailos stp", label_visibility = "hidden", placeholder = "Lache ton mail pour t'inscrire")
    with c3:
        st.write(" ")
        st.write(" ")
        mail = st.button(':cake: Particper', args = email, disabled = "email" in st.session_state)
        if mail :
            _send_mail(email)
    spawn_archive()

def spawn_board(elem = None):
    c, e = st.columns([5,1])
    with c :
        event = st.container(border = True)
        with event:
            if elem == "invit":
                spawn_invit()
            if elem == 'event':
                spawn_event()

def spawn_archive():
    select_archive_menu = st.expander('Voir les archives')
    with select_archive_menu :
        e1, c1, e2, c2, e3, c3, e4 = st.columns([1,3,1,3,1,3,1])
        with c1 :
            response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo.png')
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=archives_time[0])
            st.link_button('Accéder', 'https://projet-chev.streamlit.app/TCP1', use_container_width=True)
            
def calc_event():
    if "invit" not in st.session_state:
        return "invit"
    else:
        return "event"

def spawn_foot():
    e1, c, e2 = st.columns([1,6,1])
    with c :
        spawn_archive()

st.set_page_config(page_title="Projet Chev", initial_sidebar_state="collapsed") #configue page (Nome et nav menu fermé)
st.markdown(hide_menu_style, unsafe_allow_html=True) #applique hide_menu_style
st.markdown(hide_sidebar_style,unsafe_allow_html=True)

spawn_login()
st.write(" ")
st.write(" ")
event = calc_event()
print(event)
spawn_board(event)            
