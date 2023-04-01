import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
df = pd.read_excel('Test Tabelle.xlsx')
col1, col2, col3 = st.columns([1,1,1])
if col2.button('Click'):
    st.table(df)