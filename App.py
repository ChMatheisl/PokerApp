import streamlit as st
import pandas as pd
st.header('Hello World Pokern')
df = pd.read_excel('Test Tabelle.xlsx')
if st.button('Click'):
    st.table(df)

