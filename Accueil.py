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
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#----------------------------------------------------------------------------------------

archives_name = ["The Chev Party - volume 1"]
archives_time = ["Juin 2023"]

client_id=st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


#------------------------------------------------------------------------------------------------------------------------
#def _login():
#    if "try_login" not in st.session_state:
#            st.session_state["try_login"] = 1
#    else :
#        st.session_state["try_login"] += 1
#    if st.session_state["try_login"] == 5:
#        st.error('TEST : user=chevleboss, password=chev')

def spawn_login():
    e1, c = st.columns([5,1])
    with c :
        login = st.button('Connexion', on_click = _login, disabled = ("try_login" in st.session_state and st.session_state["try_login"] > 4))

def _invit():
    st.session_state["invit"] = True



def _try_log(user, psw):
    user = user.split(' ')[0]
    psw = psw.split(' ')[0]
    if len(user) + len(psw) > 0 :
        sql_test_log = f"""
        SELECT id, mail, surnom FROM conn
        WHERE (
        mail = $${user}$$ OR surnom = $${user}$$
        )
        AND mdp = $${psw}$$
        """
        df = conn.query(sql_test_log)
        if df.shape[0] == 1:
            st.session_state["connect"] = True
            st.session_state["u_mail"] = df.mail[0]
            st.session_state["u_surnom"] = df.surnom[0]

    else :
        if "try_login" not in st.session_state:
            st.session_state["try_login"] = 1
        else :
            st.session_state["try_login"] += 1
        if st.session_state["try_login"] == 5:
            st.error('TEST : user=chevleboss, password=chev')

        

def _login():
    st.session_state["login"] = True

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

def spawn_invit2():
    response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo2.png')
    image = Image.open(BytesIO(response.content))
    st.image(image, use_column_width =True)
    c1, c2 = st.columns(2)
    with c1 :
        st.button(':ringed_planet: Particper', on_click = _invit, use_container_width = True)
    with c2 :
        st.button(':rocket: Connexion', on_click = _login, use_container_width = True, disabled = ("try_login" in st.session_state and st.session_state["try_login"] > 4))

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

def spawn_event2():
    st.metric(label="Le weekend du", value="31 mai - 2 juin")
    st.divider()
    st.info("Ceci est une invitation pour ***The chev Party - volume 2*** pour célébrer le temps d'un week-end l'anniv du vraiment formidable *Jules Chevenet*")
    email = st.text_input("le mailos stp", label_visibility = "hidden", placeholder = "Lache ton mail pour t'inscrire")
    st.write(" ")
    e1, c, e2 = st.columns(3)
    with c :
        mail = st.button(':cake: Particper', args = email, disabled = "mail" in st.session_state, use_container_width = True)
        retour = st.button("Retour", use_container_width = True)
        if retour :
            del st.session_state["invit"]
            st.rerun()
    if (mail or email) and "mail" not in st.session_state:
        _send_mail(email)
        
    st.write(" ")
    spawn_archive2()

    
def spawn_login2():
    st.metric(label="Le weekend du", value="31 mai - 2 juin")
    st.divider()
    st.info("Ceci est une invitation pour ***The chev Party - volume 2*** pour célébrer le temps d'un week-end l'anniv du vraiment formidable *Jules Chevenet*")
    user = st.text_input("mail / nom d'utilisateur", placeholder = "Jean")
    password = st.text_input("mot de passe", placeholder = "Kultonpair", type = "password")
    st.write(" ")
    e1, c, e2 = st.columns(3)
    with c :
        log = st.button(':cake: Feu', use_container_width = True, disabled = ("try_login" in st.session_state and st.session_state["try_login"] > 4))
        if (log or password) and "connect" not in st.session_state:
            _try_log(user, password)   
            st.rerun()
        retour = st.button("Retour", use_container_width = True)
        st.write("")
        if retour :
            del st.session_state["login"]
            st.rerun()
    spawn_archive2()

def spawn_infos():
    st.info("Les prochaines infos arriveront + tard")
    response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/TCP_2_Poster.png')
    image = Image.open(BytesIO(response.content))
    st.image(image, use_column_width =True)
    
def comp_musique(id):
    return components.html("""<iframe 
                    style="border-radius:12px" 
                    src="https://open.spotify.com/embed/track/"""+ id + """?utm_source=generator&theme=0" 
                    width="100%" height="80" frameBorder="0" allowfullscreen="" 
                    allow="autoplay; 
                    clipboard-write; 
                    encrypted-media; 
                    fullscreen; 
                    picture-in-picture" 
                    loading="lazy">
                    </iframe>""", height=92)

def _send_track(track_id, track):
    subject = "Nouvelle musique"
    body = track_id + '\n' + '\n' + str(track)
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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def spawn_playlist():
    components.html("""<iframe style="border-radius:12px" 
                    src="https://open.spotify.com/embed/playlist/313eWtMAEHe7qf5wEFDToF?utm_source=generator" 
                    width="100%" height="152" 
                    frameBorder="0" 
                    allowfullscreen="" 
                    allow="autoplay; 
                    clipboard-write; 
                    encrypted-media; 
                    fullscreen; 
                    picture-in-picture" 
                    loading="lazy">
                    </iframe>""", 
                    height=164)
    with st.expander('Ajoute tes pépites'):
        search_query = st.text_input('Rechercher une musique sur Spotify')
        if search_query:
            results = sp.search(q=search_query, type='track', limit=6)
            tracks = results["tracks"]["items"]
            for track in tracks:
                comp_musique(track["id"])
                st.button('Ajouter', key = track["id"], on_click = lambda track_id=track["id"]: _send_track(track_id, track), use_container_width=True)
                st.divider()

def _send_surnom(mail, n_surnom):
    if type(mail) is str: 
        subject = "Nouvelle musique"
        body = mail + '\n' + '\n' + n_surnom
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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

def spawn_info_profil(mail, surnom, value = 0):
    if surnom :
        st.write(f"Hello **{value}**, j'espère que tu passe une bonne journée")
    else :
        st.write("Hello l'ami(e), ajoute ton surnom stp")
    n_surnom = st.text_input("le mailos stp", label_visibility = "hidden", placeholder = "Lache ton meilleur surnom")
    e1, c, e2 = st.columns(3)
    with c :
        change = st.button(':cake: Changer', args = n_surnom, use_container_width = True)
    if change:
        if len(n_surnom) > 0:
            _send_surnom(mail, n_surnom)
            st.session_state["u_surnom"] = n_surnom
            st.rerun()


def spawn_get_profil():
    surnom = "u_surnom" in st.session_state
    if surnom :
        spawn_info_profil(st.session_state["u_mail"], surnom, st.session_state["u_surnom"])
    else :
        spawn_info_profil(st.session_state["u_mail"], surnom)



def spawn_profil():
    st.metric(label="Le weekend du", value="31 mai - 2 juin")
    st.divider()
    tab1, tab2, tab3 = st.tabs(["Infos", "Playlist", "Profil"])
    with tab1 :
        spawn_infos()
    with tab2 :
        spawn_playlist()
    with tab3 :
        spawn_get_profil()
    spawn_archive2()
    



#-------------------------------------------------------------------
def spawn_board(elem = None):
    c, e = st.columns([5,1])
    with c :
        event = st.container(border = True)
        with event:
            if elem == "invit":
                spawn_invit()
            if elem == 'event':
                spawn_event()

def spawn_board2(elem = None):
    E, c, e = st.columns([1,2,1])
    with c :
        event = st.container(border = True)
        with event:
            if elem == "invit":
                spawn_invit2()
            if elem == 'event':
                spawn_event2()
            if elem == 'login':
                spawn_login2()
            if elem == 'connect':
                spawn_profil()

def spawn_archive():
    select_archive_menu = st.expander('Voir les archives')
    with select_archive_menu :
        e1, c1, e2, c2, e3, c3, e4 = st.columns([1,3,1,3,1,3,1])
        with c1 :
            response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo.png')
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=archives_time[0])
            st.link_button('Accéder', 'http://172.20.10.2:8501/TCP1', use_container_width=True)

def spawn_archive2():
    select_archive_menu = st.expander('Voir les archives')
    with select_archive_menu :
        c1, c2 = st.columns(2)
        with c1 :
            response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo.png')
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=archives_time[0])
            st.link_button('Accéder', 'https://projet-chev.streamlit.app/TCP1', use_container_width=True)
            
def calc_event():
    if "connect" in st.session_state:
        return "connect"
    if "login" in st.session_state:
        return "login"
    if "invit" not in st.session_state:
        return "invit"
    else:
        return "event"

def spawn_foot():
    e1, c, e2 = st.columns([1,6,1])
    with c :
        spawn_archive()







# ------------------------------------------------------------------------------------------------------------------------------------




st.set_page_config(page_title="Projet Chev", initial_sidebar_state="collapsed") #configue page (Nome et nav menu fermé)
st.markdown(hide_menu_style, unsafe_allow_html=True) #applique hide_menu_style
st.markdown(hide_sidebar_style,unsafe_allow_html=True)

#spawn_login()
#st.write(" ")
#st.write(" ")
conn = st.connection("gsheets", type=GSheetsConnection)
event = calc_event()
spawn_board2(event)            
