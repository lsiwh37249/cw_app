# streamlit_app.py
import streamlit as st
import pandas as pd

st.title("간단한 Streamlit 앱")
st.write("Hello, Streamlit!")

# 예시 데이터
df = pd.DataFrame({
    "이름": ["Alice", "Bob", "Charlie"],
    "점수": [90, 85, 95]
})
st.table(df)

