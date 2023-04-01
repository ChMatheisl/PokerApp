import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
import datetime
import SessionState

# @st.cache_data(ttl=5)
# def load_data(sheets_url):
#     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#     return pd.read_csv(csv_url, sep=',', on_bad_lines='skip')

# if st.button('Neuer DF'):
#     df = load_data(st.secrets["public_gsheets_url"])
#     st.dataframe(df)
data = pd.DataFrame()
session_state = SessionState.get(df=data)

if st.button('Aktueller Stand'):
    st.dataframe(session_state.df)

# Spieergbenis
name = st.text_input('Wer bist du?', 'Niko')
einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 50, 10)
abgang = st.slider('Wie viel hast du am Ende mitgenommen?', 0, 50, 10)
spieler_ergebnis = { 
    'Spieler': name,
    'Einzahlung': einzahlung,
    'Endstand': abgang,
    'Datum': datetime.datetime.today()
    }

if st.button('Abschicken'):
    session_state.df = pd.concat([session_state.df, pd.DataFrame.from_records([spieler_ergebnis])], ignore_index=True)