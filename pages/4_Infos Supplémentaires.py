import streamlit as st

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
    with st.expander("Localisation"):
        st.write("2406 route de la Grisière, 71870, HURIGNY")
        st.write("Gares les plus proches : Mâcon Loché TGV ou Mâcon Ville")
        st.write("Afin de limiter l'impact environnemental de l'évènement, vous pouvez également faire du covoiturage avec les autres participants.")

    with st.expander("Principe du Weekend"):
        st.write("Durant l'ensemble du Weekend, il y aura différents évènements en équipe ou en solo, avec des goodies à la clé, plus d'infos bientôt.")
        st.write("Merci à toi de lire ces lignes, la curiosité et la réactivité vis à vis de ce site peuvent être utile pour prendre une longueur d'avance sur les autres.")