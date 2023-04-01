import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
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

st.subheader('Wer bist du?')
spieler = ['Chris', 'Niko', 'Steffen', 'Basti', 'Philip', 'Niko2']
cols = st.columns([1 for x in spieler])
for i, name in enumerate(spieler):
    cols[i].button(name)
einzahlung = st.slider('Wie viel hast du eingezahlt?', 0, 30, 10)