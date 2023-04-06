import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from github import Github
from PIL import Image
import json
from style.css import hide_menu_style, hide_sidebar_style
from game_tools.game_engine import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Projet Chev", initial_sidebar_state="collapsed") #configue page (Nome et nav menu fermé)
st.markdown(hide_menu_style, unsafe_allow_html=True) #applique hide_menu_style

df_shown = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/ds.csv')
df_rep = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/dr.csv')

client_id=st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

@st.cache(allow_output_mutation=True)
def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        username = 'ptitchev',
        redirect_uri='https://projet-chev.streamlit.app/callback',
        scope= ['playlist-modify-public',"user-library-read"],
        open_browser=False    
    )
  
sp_oauth = get_spotify_oauth()  # récupère l'objet SpotifyOAuth

if sp_oauth._is_token_expired(sp_oauth.get_cached_token()):  # vérifie si le jeton est expiré
    token_info = sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])  # rafraîchit le jeton
    access_token = token_info['access_token']  # récupère le nouveau jeton d'accès
else:
    access_token = sp_oauth.get_cached_token()['access_token']

@st.cache(allow_output_mutation=True)
def get_spotify_client():
    return spotipy.Spotify(auth_manager=sp_oauth)

@st.cache(allow_output_mutation=True)
def handle_spotify_callback():
    uri = st.experimental_get_query_params()["code"][0]
    token_info = sp_oauth.get_access_token(uri)
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return sp

def commit(df, name):
    updated_content = df.to_csv(index=False)
    g = Github(st.secrets["github_token"])
    repo = g.get_user().get_repo("private_streamlit")
    file = repo.get_contents("/data/" + name + ".csv")
    #content = file.decoded_content.decode('utf-8')
    repo.update_file("data/" + name + ".csv", 'Updated', updated_content, file.sha)

def add_data_rep(idp, we1, contact, info_contact, hype, ptheme): #envoi les data sur github
    rep = (idp, we1, contact, info_contact, hype, ptheme)
    df_row = pd.DataFrame([rep], columns = df_rep.columns)
    df = pd.concat((df_rep, df_row))
    commit(df, "dr")

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
        st.text_input("Mot de passe", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Mot de passe", type="password", on_change=password_entered, key="password")
        st.error("Mauvais mot de passe BG, regarde ma bio insta")
        return False
    else:
        return True
    
def start_G():
    st.session_state["is_playing"] = True
    st.session_state["game"], st.session_state["t_der"], st.session_state["trois_choix"], st.session_state["limits"] = start_game()
    st.session_state["musique"] = 0
    if 'RS' in st.session_state :
        del st.session_state["RS"]

def check_track_in_playlist(track_id):
    tracks = sp.playlist_tracks(playlist_id=st.secrets["playlist_id"], fields="items.track.id,total")
    for item in tracks['items']:
        if item['track'] and item['track']['id'] == track_id:
            return True
    return False

def add_s(track_id):
    sp.playlist_add_items(st.secrets["playlist_id"], [track_id])

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

    
if check_password():

    if "a" not in st.session_state:
        st.subheader("Bien joué mon reuf : tu es invité(e) à l'anniv de Chev")
        tab1, tab2, tab3, tab4, tab5, tab6  = st.tabs(["Présentation", "Participants", "Jeux", "Thème", "Musique", "Infos supplémentaires"])

        with tab1 :
            st.markdown("### Informations")
            st.markdown("Comme chaque années depuis 2015, pour célébrer mon anniversaire, j'organise un **grand** **weekend** **festif**. Au programme, BBQ, piscine, basket, pétanque et autres activités, mais surtout beaucoup d'**alcool** (même si c'est pas cool) et de rires.")
            st.markdown("J'avoue ça a l'air barbant comme ça, mais pour voir encore plus grand, je m'organise en avance pour nous permettre de mieux festoyer. Si t'es chaud, on se retrouve en **région** **maconnaise** pour fêter ça.")
            st.markdown("Le site va pas mal évoluer jusqu'à la date de la soirée donc hésite pas à revenir jetter un coup d'oeil.")
            st.markdown("Pour info, mon anniv c'est le **2** **juin**.")
            st.markdown("**Chev**")


        with tab2:
            st.dataframe(df_shown, use_container_width= True)
            st.warning("Remplis l'inscription si ton nom n'apparait pas", icon="⚠️")
            with st.expander("Inscription"):
                with st.form("Inscription", clear_on_submit = True):
                    st.write('Remplis-moi ça :')
                    st.write(" ")
                    idp = st.text_input("Nom, Prénom, Surnom ou N° de sécu :")
                    st.write(" ")
                    we1 = st.checkbox('Disponible le Weekend du 2-4 juin')
                    col1, col2 =st.columns(2)
                    with col1 :
                        st.write(" ")
                        contact = st.multiselect(
                            'Moyen de contact privilégié',
                            ["Insta", "Messenger", "WhatsApp", "SMS", "Snap", "Mail", "LinkedIn", "Tinder", "Pigeon voyageur"]
                        )
                    with col2 :
                        st.write(" ")
                        info_contact = st.text_input("Infos de contact supplémentaires :", ' ')
                    st.write(" ")
                    hype = st.select_slider("Echelle de la hype pour l'évènement :", ["claqué au sol", "rien de ouf", "dinguerie", "pétage de crâne en prévision"])
                    st.write(" ")
                    ptheme = st.text_input("Proposition de thème :", ' ')
                    st.write(" ")
                    blank1, mid, blank2 = st.columns(3)
                    with mid :
                        submitted = st.form_submit_button("Valider", use_container_width  = True)
        if submitted :
            add_data_rep(idp, we1, contact, info_contact, hype, ptheme)
            st.success("Let's go ! Je te tiens au courant pour la suite")
            st.balloons()


        #Theme

        with tab4:
            col1, col2, col3 = st.columns(3)
            st.info("Reviens le 02/05 pour découvrir le thème")
            with col2:
                response = requests.get(url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/source/logo.png')
                image = Image.open(BytesIO(response.content))
                st.image(image, caption='Logo de la 1ere Chev Party')


        #Info sup

        with tab6 :
            with st.expander("Localisation"):
                st.write("2406 route de la Grisière, 71870, HURIGNY")
                st.write("Gares les plus proches : Mâcon Loché TGV ou Mâcon Ville")
                st.write("Afin de limiter l'impact environnemental de l'évènement, vous pouvez également faire du covoiturage avec les autres participants.")
            with st.expander("Principe du Weekend"):
                st.write("Durant l'ensemble du Weekend, il y aura différents évènements en équipe ou en solo, avec des goodies à la clé, c'est pour ça qu'il y a un logo.")
                st.write("Merci à toi de lire ces lignes, la curiosité et la réactivité vis à vis de ce site peuvent être utile pour prendre une longueur d'avance sur les autres. Joue-la comme Hercule Poirot.")

        with tab5 :
            
            components.html("""<iframe 
                                style="border-radius:12px" 
                                src="https://open.spotify.com/embed/playlist/0n3S3n3mroDR8ffyW9CTEJ?utm_source=generator&theme=0" 
                                width="100%" 
                                height="152" 
                                frameBorder="0" 
                                allowfullscreen="" 
                                allow="autoplay; 
                                clipboard-write; 
                                encrypted-media; 
                                fullscreen; 
                                picture-in-picture" 
                                loading="lazy">
                                </iframe>""", height=164)
            with st.expander('Ajouter des musiques'):
                sp = handle_spotify_callback()
                search_query = st.text_input('Rechercher une musique sur Spotify')
                if search_query:
                    results = sp.search(q=search_query, type='track', limit=10)
                    tracks = results["tracks"]["items"]
                    for track in tracks:
                        col1, col2 = st.columns([4,1])
                        with col1:
                            comp_musique(track["id"])
                        with col2:
                            st.write('')
                            st.write('')
                            st.button('Ajouter', key = track["id"], on_click=lambda track_id=track["id"]: add_s(track_id), disabled=check_track_in_playlist(track["id"]), use_container_width=True)
        #Jeu

        with tab3 :
            if "is_playing" not in st.session_state:
                st.info('Sur téléphone, il est conseillé de passer en mode paysage sans les images.')
            c1, e1, c2 = st.columns([4,2,2])
            with c1:
                st.markdown("### Jouer à : :violet[Party's Survivor]")#st.subheader("Jouer à : :violet[Party's Survivor]")
            with c2 :
                blank1 = st.write("")
                im = st.checkbox('Afficher image', value = False)
            if "is_playing" not in st.session_state:
                blank1 = st.write("")
                blank2 = st.write("")
                blank3 = st.write("")
                e1, c1, e2 = st.columns([5, 3, 5])
                with c1 :
                    st.button('Jouer', on_click=start_G, use_container_width=True)
                blank1 = st.write("")
                blank2 = st.write("")
                blank3 = st.write("")
            if "is_playing" in st.session_state :
                if len(st.session_state["trois_choix"]) > 2 :
                    c1, c2, c3, c4 = st.columns([2,2,3,1])
                    with c1 :
                        Time = st.metric("Heure", conv_time(st.session_state["game"][1]))
                    with c3:
                        Musique = st.selectbox('Musique', list(L_musique), index = 0)
                    with c4 :
                        Bpm = st.metric("BPM", str(int(st.session_state["game"][2])))
                    blank1 = st.write("")
                    blank2 = st.write("")

                    def play_G0(Musique = Musique):
                        st.session_state["musique"] = list(L_musique).index(Musique)
                        st.session_state["game"], st.session_state["t_der"], st.session_state["trois_choix"], st.session_state["limits"] = player_play(st.session_state["game"], st.session_state["t_der"], st.session_state["limits"], st.session_state["trois_choix"][0], st.session_state["musique"])
                    def play_G1(Musique = Musique):
                        st.session_state["musique"] = list(L_musique).index(Musique)
                        st.session_state["game"], st.session_state["t_der"], st.session_state["trois_choix"], st.session_state["limits"] = player_play(st.session_state["game"], st.session_state["t_der"], st.session_state["limits"], st.session_state["trois_choix"][1], st.session_state["musique"])
                    def play_G2(Musique = Musique):
                        st.session_state["musique"] = list(L_musique).index(Musique)
                        st.session_state["game"], st.session_state["t_der"], st.session_state["trois_choix"], st.session_state["limits"] = player_play(st.session_state["game"], st.session_state["t_der"], st.session_state["limits"], st.session_state["trois_choix"][2], st.session_state["musique"])

                    e1, c1, e2, c2, e3, c3, e4 = st.columns([1,3,1,3,1,3,1])
                    with c1 :
                        if im :
                            i0 = st.image(L_image[st.session_state["trois_choix"][0]])
                        b0 = st.button(L_nom[st.session_state["trois_choix"][0]], key = 'B0',on_click=play_G0, use_container_width=True)
                    with c2 :
                        if im :
                            i1 = st.image(L_image[st.session_state["trois_choix"][1]])
                        b1 = st.button(L_nom[st.session_state["trois_choix"][1]], key = 'B1',on_click=play_G1, use_container_width=True)
                    with c3 :
                        if im :
                            i2 = st.image(L_image[st.session_state["trois_choix"][2]])
                        b2 = st.button(L_nom[st.session_state["trois_choix"][2]], key = 'B2', on_click=play_G2, use_container_width=True)
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
                    ddd = show_death(st.session_state["game"], st.session_state["trois_choix"])
                    col1,e1,col2,col3 = st.columns([6,2,2,2])
                    with col1:
                        if ddd[0] == 0 :
                            st.markdown("### :red[Dommage !]")
                        if ddd[0] == 1 :
                            st.markdown("### :green[Bien joué !]")
                        st.markdown(ddd[1])
                    with col2:
                        st.metric('Score', int(st.session_state["game"][-1]))
                    with col3:
                        st.metric("Heure", conv_time(st.session_state["game"][1]))

                    m_score = dscore['data']
                    m_champ = dscore['index']
                    def is_champ(score, m_score = m_score):
                        if score > m_score[-1][0]:
                            return True
                        return False
                    def send_champ(champ, score, m_champ = m_champ, m_score = m_score):
                        m_score[-1][0] = score
                        m_champ[-1] = champ
                        ddd = pd.DataFrame(m_score, columns = dscore['columns'], index = m_champ)
                        ddd.sort_values(by=["Score"], ascending=False, inplace = True)
                        content = ddd.to_json(orient="split")
                        g = Github(st.secrets["github_token"])
                        repo = g.get_user().get_repo("private_streamlit")
                        file = repo.get_contents("/score.json")
                        repo.update_file("score.json", 'Updated', content, file.sha)

                    if 'RS' not in st.session_state:
                        st.session_state['RS'] = not is_champ(st.session_state["game"][-1])
                    st.session_state['champ'] = is_champ(st.session_state["game"][-1])
                    col1,e1, col2 = st.columns([6, 1, 5])
                    with col1:
                        st.write('')
                        st.write('')
                        if st.session_state['champ']:
                            st.success("Tu es un champion, rejoint la Légende !", icon="👑")
                        else :
                            st.error("Ton score mérite d'être oublié ...", icon="🍻")
                        c1,c2 = st.columns(2)
                        with c1 :
                            champion = st.text_input('Grave ton nom Champion : ', '', disabled = st.session_state['RS'])
                        with c2 :
                            st.write('')
                            st.write('')
                            restart = st.button('Rejouer', on_click=start_G, use_container_width=True, disabled = not st.session_state['RS'])
                        
                        st.session_state['RS'] = True
                        if champion : 
                            send_champ(champion, st.session_state["game"][-1])
                            

                    with col2:
                        st.write('')
                        st.write('')
                        df = pd.DataFrame(m_score, columns = dscore['columns'], index = m_champ)
                        st.dataframe(df, use_container_width = True)
                        st.write("")
                        st.write("")
                        

            with st.expander("Règles"):
                st.markdown("### Principe :")
                st.markdown("Tu arrives à une soirée remplis d'énergie et le ventre à moitié plein.")
                st.markdown("A chaque fois 3 choix sont proposés, il faut selectionner l'action souhaitée.")
                st.markdown("En fonction de ton choix, l'heure, ton BPM, ton Energie, ta Soif, ta Défonce et le Fun de la soirée évolue.")
                st.markdown("### Musique :")
                st.markdown("A tout moment tu peux changer la musique, ce qui influencera également ton état.")
                st.markdown("Chaque musique a ses avantages et ses inconvénients, choisi bien en fonction de ton état.")
                st.markdown("### Objectif :")
                st.markdown("Premièrement, il faut essayer de survivre à la soirée. Plus la soirée est cool, plus tu marques de point")
                st.markdown("A la fin de la partie, un score est attribué.")
                st.markdown("Que le meilleur gagne.")



    #Admin
    elif st.session_state["a"]==1:
        edited_ds = st.experimental_data_editor(df_shown, num_rows="dynamic")
        def modif_a1(df = edited_ds):
            commit(df, "ds")
        st.button("Valider 1", on_click = modif_a1)                                    
        edited_dr = st.experimental_data_editor(df_rep, num_rows="dynamic")
        def modif_a2(df = edited_dr):
            commit(df, "dr")
        st.button("Valider 2", on_click = modif_a2)
