import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
df = pd.read_excel('Test Tabelle.xlsx')
col1, col2, col3 = st.columns([1,1,1])
if col2.button('Click'):
    st.table(df)
age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')