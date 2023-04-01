import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
import datetime
#df = pd.read_excel('Test Tabelle.xlsx')
#col1, col2, col3 = st.columns([1,1,1])
#if col2.button('Click'):
#    st.table(df)
#if col3.button('Add Column'):
#    st.subheader('Wer bist du?') 
#    df['Neuer col'] = 'Test lul'
#    df.to_excel('Test Tabelle.xlsx')
#age = st.slider('How old are you?', 0, 130, 25)
#st.write("I'm ", age, 'years old')

@st.cache_data(ttl=5)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url, sep=',', on_bad_lines='skip')

if st.button('Neuer DF'):
    df = load_data(st.secrets["public_gsheets_url"])
    st.dataframe(df)

df = pd.DataFrame()
# Spieergbenis
name = st.text_input('Wer bist du?', 'Niko')
einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 50, 10)
abgang = st.slider('Wie viel hast du am Ende mitgenommen?', 0, 50, 10)
spieler_ergebnis = { 'Spieler': name, 'Einzahlung': einzahlung, 'Endstand': abgang, 'Datum': datetime.datetime.today()}

if st.button('Abschicken'):
    df = pd.concat([df, pd.DataFrame.from_records([spieler_ergebnis])])
    st.dataframe(df)