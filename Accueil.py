import numpy as np
import pandas as pd
import streamlit as st
from github import Github

#0 : Data
df_shown = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/ds.csv')

df_rep = pd.read_csv('https://raw.githubusercontent.com/ptitchev/private_streamlit/main/data/dr.csv')


#1 : BackEnd + password

def add_data_rep():
    rep = st.session_state['rep']
    g = Github(st.secrets["github_token"])
    repo = g.get_user().get_repo("private_streamlit")
    file = repo.get_contents("/data/dr.csv")
    content = file.decoded_content.decode('utf-8')
    df_row = pd.DataFrame([rep], columns = df_rep.columns)
    df = pd.concat((df_rep, df_row))
    updated_content = df.to_csv(index=False)
    repo.update_file("data/dr.csv", 'Updated', updated_content, file.sha)
    

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
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

#2 : FrontEnd

st.set_page_config(page_title="Projet Chev")

if check_password():

    st.subheader("Bien joué mon reuf : tu es invité(e) à l'anniv de Chev")

    with st.expander("Informations"):
        st.write("Comme chaque années depuis 2015, pour célébrer mon anniversaire, j'organise un grand weekend festif. Au programme, BBQ, piscine, basket, pétanque et autres activités, mais surtout beaucoup d'alcool (même si c'est pas cool) et de rires.")
        st.write("J'avoue ça a l'air barbant comme ça, mais pour voir encore plus grand, je m'organise en avance pour nous permettre de mieux festoyer. Si t'es chaud, on se retrouve en région maconnaise pour fêter ça.")
        st.write("Le site va pas mal évoluer jusqu'à la date de la soirée donc hésite pas à revenir jetter un coup d'oeil.")
        st.write("Pour info, mon anniv c'est le 2 juin.")
        st.write("Chev")

    with st.expander("Participants"):
        st.dataframe(df_shown, use_container_width= True)

    with st.form("Inscription", clear_on_submit = True):
        st.write('Remplis-moi ça :')
        idp = st.text_input("Nom, Prénom, Surnom ou N° de sécu :")
        st.caption("Disponibilité :")
        col1, col2 =st.columns(2)
        with col1 :
            we1 = st.checkbox('Weekend 2-4 juin')
            st.write(" ")
            contact = st.multiselect(
            'Moyen de contact privilégié',
            ["Insta", "Messenger", "WhatsApp", "SMS", "Snap", "Mail", "LinkedIn", "Tinder", "Pigeon voyageur"]
        )
        with col2 :
            we2 = st.checkbox('Weekend 9-11 juin')
            st.write(" ")
            info_contact = st.text_input("Infos de contact supplémentaires :", ' ')
        st.write(" ")
        st.write(" ")
        hype = st.select_slider("Echelle de la hype pour l'évènement :", ["claqué au sol", "rien de ouf", "dinguerie", "pétage de crâne en prévision"])
        st.write(" ")
        st.write(" ")
        ptheme = st.text_input("Proposition de thème :", ' ')
        st.write(" ")
        st.write(" ")
        blank1, mid, blank2 = st.columns(3)
        with mid :
            submitted = st.form_submit_button("Valider", use_container_width  = True, on_click = add_data_rep)

        st.session_state['rep'] = (idp, we1, we2, contact, info_contact, hype, ptheme)

    if submitted :
        st.success("Let's go ! Je te tiens au courant pour la suite")
        st.balloons()
