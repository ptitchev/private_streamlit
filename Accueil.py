
import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

#1 : BackEnd + password

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1686ALWAOK-hf-PffltoH3axFiUUREZUdF4lI7sCXmqQ"
POST_NAME = "Reponse"
GET_NAME = "Montrer"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

@st.experimental_singleton()
def connect_to_gsheet():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector

    def get_data(gsheet_connector) -> pd.DataFrame:
        values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{GET_NAME}!A:C",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{POST_NAME}!A:G",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

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

    gsheet_connector = connect_to_gsheet()

    st.subheader("Bien joué mon reuf : tu es invité(e) à l'anniv de Chev")

    with st.expander("Informations"):
        st.write("Comme chaque années depuis 2015, pour célébrer mon anniversaire, j'organise un grand weekend festif. Au programme, BBQ, piscine, basket, pétanque et autres activités, mais surtout beaucoup d'alcool (même si c'est pas cool) et de rires.")
        st.write("J'avoue ça a l'air barbant comme ça, mais pour voir encore plus grand, je m'organise en avance pour nous permettre de mieux festoyer. Si t'es chaud, on se retrouve en région maconnaise pour fêter ça.")
        st.write("Le site va pas mal évoluer jusqu'à la date de la soirée donc hésite pas à revenir jetter un coup d'oeil.")
        st.write("Pour info, mon anniv c'est le 2 juin.")

    with st.expander("Participants"):
        st.dataframe(get_data(gsheet_connector))

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
            submitted = st.form_submit_button("Valider", use_container_width  = True)

    if submitted :
        st.success("Let's go ! Je te tiens au courant pour la suite")
        st.balloons()
        add_row_to_gsheet(gsheet_connector,[[idp, we1, we2, contact, info_contact, hype, ptheme]],)