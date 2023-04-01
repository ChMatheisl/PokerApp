import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
#import gspread
from google.oauth2 import service_account
from gsheetsdb import connect

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

sheet_url = st.secrets["private_gsheets_url"]

@st.cache_resource(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.set_page_config(    
    page_title="Alexa, spiel Snake Jazz",
    page_icon="🎰",
    layout="wide",)
choose = option_menu("Poker Tracking", ["Neues Spiel", "Scoreboard", "Visuals"],
                         icons=['house', 'camera fill', 'kanban'],
                         menu_icon="app-indicator", default_index=0,
                         orientation='horizontal')
st.write(rows)

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
    datetime.dateime.today())
    abgang = st.slider('Wie viel hast du am Ende mitgenommen?', 0, 50, 10)
    spieler_ergebnis = { 
        'Spieler': name,
        'Einzahlung': einzahlung,
        'Endstand': abgang,
        'Datum': datum
        }
   

    col1, col2, col3 = st.columns([1,1,1])

    if col1.button('Abschicken'):
        st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame.from_records([spieler_ergebnis])], ignore_index=True)

    if col3.button('Reset Daten'):
        st.session_state['df'] = pd.DataFrame()

    st.table(st.session_state['df'])

if choose == "Scoreboard":
    if "df" not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    # Spieergbenis
    name = st.text_input('Wer bist du?', 'Niko')
    einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 50, 10)
    abgang = st.slider('Wie viel hast du am Ende mitgenommen?', -50, 50, 10)
    spieler_ergebnis = { 
        'Spieler': name,
        'Einzahlung': einzahlung,
        'Endstand': abgang,
        'Datum': datetime.datetime.today()
        }

    col1, col2, col3 = st.columns([1,1,1])

    if col1.button('Abschicken'):
        st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame.from_records([spieler_ergebnis])], ignore_index=True)

    if col3.button('Reset Daten'):
        st.session_state['df'] = pd.DataFrame()

    st.table(st.session_state['df'])

if choose == "Visuals":
    if "df" not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    # Spieergbenis
    name = st.text_input('Wer bist du?', 'Niko')
    einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 50, 10)
    abgang = st.slider('Wie viel hast du am Ende mitgenommen?', -50, 50, 10)
    spieler_ergebnis = { 
        'Spieler': name,
        'Einzahlung': einzahlung,
        'Endstand': abgang,
        'Datum': datetime.datetime.today()
        }

    col1, col2, col3 = st.columns([1,1,1])

    if col1.button('Abschicken'):
        st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame.from_records([spieler_ergebnis])], ignore_index=True)

    if col3.button('Reset Daten'):
        st.session_state['df'] = pd.DataFrame()

    st.table(st.session_state['df'])