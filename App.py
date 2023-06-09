import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
#import gspread
from google.oauth2 import service_account
#from gsheetsdb import connect

from shillelagh.backends.apsw.db import connect
st.set_page_config(    
    page_title="Alexa, spiel Snake Jazz",
    page_icon="🎰",
    layout="wide",)

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
            ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            
    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("User", on_change=password_entered, key="username")
        st.text_input(
            "Passwort", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("User", on_change=password_entered, key="username")
        st.text_input(
            "Passwort", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User nicht bekannt oder Passwort falsch")
        return False
    else:
        # Password correct.
        return True

if check_password():
    choose = option_menu("Tracking", ["Neues Spiel", "Scoreboard", "Visuals"],
                            icons=['house', 'camera fill', 'kanban'],
                            menu_icon="app-indicator", default_index=0,
                            orientation='horizontal')

    adapter_kwargs={
                "gsheetsapi" : { 
                "service_account_info" : {
                    "type" : st.secrets["gcp_service_account"]["type"],
                    "project_id" : st.secrets["gcp_service_account"]["project_id"],
                    "private_key_id" : st.secrets["gcp_service_account"]["private_key_id"],
                    "private_key" : st.secrets["gcp_service_account"]["private_key"],
                    "client_email" : st.secrets["gcp_service_account"]["client_email"],
                    "client_id" : st.secrets["gcp_service_account"]["client_id"],
                    "auth_uri" : st.secrets["gcp_service_account"]["auth_uri"],
                    "token_uri" : st.secrets["gcp_service_account"]["token_uri"],
                    "auth_provider_x509_cert_url" : st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"]
                }}}

    conn = connect(":memory:", adapter_kwargs=adapter_kwargs)
    cursor = conn.cursor()
    sheet_url = st.secrets["private_gsheets_url"]

    # sheet_url = st.secrets["private_gsheets_url"]
    # @st.cache_resource(ttl=600)
    # def run_query(query):
    #     rows = conn.execute(query, headers=0)
    #     rows = rows.fetchall()
    #     return rows
    # rows = run_query(f'SELECT * FROM "{sheet_url}"')
    
    # conn.execute(f'INSERT INTO "{sheet_url}" Values Niko, 10, 23, Heute')
    # st.write(rows)

    # @st.cache_data(ttl=5)
    # def load_data(sheets_url):
    #     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    #     return pd.read_csv(csv_url, sep=',', on_bad_lines='skip')
    #gc = gspread.service_account()
    #sh = gc.open_by_url(st.secrets["public_gsheets_url"])
    #worksheet = sh.get_worksheet(0)
    #st.write(worksheet)
    #worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

    # if st.button('Neuer DF'):
    #     df = load_data(st.secrets["public_gsheets_url"])
    #     st.dataframe(df)

    if choose == "Neues Spiel":
        if "df" not in st.session_state:
            st.session_state['df'] = pd.DataFrame()

        # Spieergbenis
        name = st.text_input('Wer bist du?', 'Niko')
        einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 50, 10)
        datum = st.date_input(
        "Wann?",
        datetime.datetime.today())
        abgang = st.slider('Wie viel hast du am Ende mitgenommen?', 0, 50, 10)
        spieler_ergebnis = { 
            'Spieler': name,
            'Einzahlung': einzahlung,
            'Endstand': abgang,
            'Datum': datum
            }
        for value in spieler_ergebnis.values():
            pass

        col1, col2, col3 = st.columns([1,1,1])

        style = "<style>.row-widget.stButton {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        if col2.button('Abschicken'):
            query = f'INSERT INTO "{sheet_url}" VALUES (?, ?, ?, ?)'
            parameter = {'name': name, 'einzahlung': einzahlung, 'abgang': abgang, 'datum': datum}
            st.dataframe(parameter)
            cursor.execute(query, tuple(parameter.values()))

    if choose == "Scoreboard":
        hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        col4, col5, col6 = st.columns([1,1,1])
        query = f'SELECT * FROM "{sheet_url}"'
        full = cursor.execute(query)
        full = pd.DataFrame(full).rename(columns={0: 'Spieler', 1: 'Einzahlung', 2: 'Endstand', 3: 'Datum'})
        col5.table(full)

    if choose == "Visuals":
        query = f'SELECT * FROM "{sheet_url}"'
        full = cursor.execute(query)
        full = pd.DataFrame(full).rename(columns={0: 'Spieler', 1: 'Einzahlung', 2: 'Endstand', 3: 'Datum'})
        full['Δ'] = full['Einzahlung'] - full['Endstand']

        
        #1. Visual
        gruppiert = full.groupby('Datum')['Einzahlung'].sum().reset_index()
        st.subheader('Einzahlung je Datum')
        st.line_chart(gruppiert, x='Datum', y='Einzahlung')
        
        #2. Visual
        st.subheader('Einzahlung bestimmter Spieler')
        spieler = list(full['Spieler'].unique())
        aktuelle_auswahl = st.selectbox('Spieler', spieler)
        sub = full[full['Spieler']==aktuelle_auswahl]
        st.line_chart(sub, x='Datum', y='Einzahlung')

        #3. Visual
        st.bar_chart(sub, x='Datum', y='Δ')