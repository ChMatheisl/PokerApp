import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
import datetime

df = pd.DataFrame()


@st.cache_data(ttl=5)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url, sep=',', on_bad_lines='skip')

if st.button('Neuer DF'):
    df = load_data(st.secrets["public_gsheets_url"])
    st.dataframe(df)

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
    df = pd.concat([df, pd.DataFrame.from_records([spieler_ergebnis])])
    st.dataframe(df)